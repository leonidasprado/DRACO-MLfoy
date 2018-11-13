# global imports
import keras
import keras.models as models
import keras.layers as layer
import matplotlib
matplotlib.use('Agg')
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

import os

# Limit gpu usage
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from sklearn.metrics import roc_auc_score


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))

# local imports
import data_frame
from Network_architecture import architecture

class DNN():
    def __init__(self, in_path, save_path,
                event_classes, 
                event_category,
                train_variables, 
                prenet_targets,
                batch_size =500,
                train_epochs = 500,
                early_stopping = 5,
                optimizer = None,
                loss_function = "categorical_crossentropy",
                test_percentage = 0.2,
                eval_metrics = None):

        # save some information
        
        # path to input files
        self.in_path = in_path
        # output directory for results
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs( self.save_path )
        # list of classes
        self.event_classes = event_classes
        # name of event category (usually nJet/nTag category)
        self.event_category = event_category
        # target variables for pre-net
        self.prenet_targets = prenet_targets

        # list of input features
        self.train_variables = train_variables

        # batch size for training
        self.batch_size = batch_size
        # number of maximum training epochs
        self.train_epochs = train_epochs
        # number of early stopping epochs
        self.early_stopping = early_stopping
        # percentage of events saved for testing
        self.test_percentage = test_percentage        

        # loss function for training
        self.loss_function = loss_function
        # additional metrics for evaluation of training process
        self.eval_metrics = eval_metrics

        # load dataset
        self.data= self._load_datasets()

        # dict with aachen architectures for sl analysis
        architecture_1 = architecture()
        self.architecture_dic = architecture_1.get_architecture(self.event_category)

         # optimizer for training
        if not(optimizer):
            self.optimizer = self.architecture_dic["optimizer"]
        else:
            self.optimizer = optimizer


    def _load_datasets(self):
        ''' load dataset '''
        return data_frame.DataFrame(
            path_to_input_files = self.in_path,
            classes             = self.event_classes,
            event_category      = self.event_category,
            train_variables     = self.train_variables,
            prenet_targets      = self.prenet_targets,
            test_percentage     = self.test_percentage,
            norm_variables      = True)

    def build_default_model(self):
        ''' default Aachen-DNN model as used in the analysis '''

        number_of_input_neurons = self.data.n_input_neurons


        number_of_neurons_per_layer = self.architecture_dic["prenet_layer"]
        dropout                     = self.architecture_dic["Dropout"]
        activation_function         = self.architecture_dic["activation_function"]
        l2_regularization_beta      = self.architecture_dic["L2_Norm"]
    
        # prenet
        Inputs = keras.layers.Input( shape = (self.data.n_input_neurons,) )

        X = Inputs
        self.layer_list = [X]
        for i, nNeurons in enumerate(number_of_neurons_per_layer):
            Dense = keras.layers.Dense(nNeurons, activation = activation_function,
                                kernel_regularizer = keras.regularizers.l2(l2_regularization_beta),
                                name = "Dense_"+str(i))(X)

            self.layer_list.append( Dense )
            if dropout != 1: 
                X = keras.layers.Dropout( dropout )(Dense)
            else:
                X= Dense 
        
        X = keras.layers.Dense(self.data.n_prenet_output_neurons,
                activation = "softmax",
                kernel_regularizer = keras.regularizers.l2(l2_regularization_beta))(X)
        self.layer_list.append(X)

        pre_net = models.Model(inputs = [Inputs], outputs = [X])
        pre_net.summary()

        # compile and fit here?

        # Make Parameters of first model untrainable
        for layer in pre_net.layers:
            layer.trainable = False

        # ---------------
        # main net
        number_of_neurons_per_layer = self.architecture_dic["prenet_layer"]      

        # Create Input/conc layer for second NN
        conc_layer = keras.layers.concatenate(self.layer_list, axis = -1)

        Y = conc_layer

        for i, nNeurons in enumerate(number_of_neurons_per_layer):
            Y = keras.layers.Dense(nNeurons, activation = activation_function,
                            kernel_regularizer=keras.regularizers.l2(l2_regularization_beta),
                            name = "Dense_main_"+str(i))(Y)

            if dropout != 1:
                Y = keras.layers.Dropout(dropout)(Y)

        Y = keras.layers.Dense(self.data.n_output_neurons,
                activation = "softmax",
                kernel_regularizer=keras.regularizers.l2(l2_regularization_beta))(Y)


        main_net = models.Model(inputs = [Inputs], outputs = [Y])
        main_net.summary()

        return pre_net, main_net


    def build_model(self, pre_net = None, main_net = None):
        ''' build a DNN model
            if none is specified use default model '''

        if pre_net == None or main_net == None:
            print("loading default models")
            pre_net, main_net = self.build_default_model()

        for layer in pre_net.layers:
            layer.trainable = True
        # compile models
        pre_net.compile(
            loss = self.loss_function,
            optimizer = self.optimizer,
            metrics = self.eval_metrics)

        for layer in pre_net.layers:
            layer.trainable = False
        main_net.compile(
            loss = self.loss_function,
            optimizer = self.optimizer,
            metrics = self.eval_metrics)
            
        self.pre_net = pre_net
        self.main_net = main_net

        # model summaries
        self.pre_net.summary()
        self.main_net.summary()

        out_file = self.save_path+"/pre_net_summmary.yml"
        yml_pre_net = self.pre_net.to_yaml()
        with open(out_file, "w") as f:
            f.write(yml_pre_net)

        out_file = self.save_path+"/main_net_summmary.yml"
        yml_main_net = self.main_net.to_yaml()
        with open(out_file, "w") as f:
            f.write(yml_main_net)


    def train_models(self):
        ''' train prenet first then the main net '''
        callbacks = None
        if self.early_stopping:
            callbacks = [keras.callbacks.EarlyStopping(
                            monitor = "val_loss", 
                            patience = self.early_stopping)]

        self.pre_net.fit(
            x = self.data.get_train_data(as_matrix = True),
            y = self.data.get_prenet_train_labels(),
            batch_size = self.batch_size,
            epochs = self.train_epochs,
            shuffle = True,
            callbacks = callbacks,
            validation_split=0.2,
            )
        y_pred = self.pre_net.predict(self.data.get_train_data(as_matrix = True), verbose=1)

        score = roc_auc_score(self.data.get_prenet_train_labels(), y_pred)
        print('##############################################################################')
        print(score)
        print('##############################################################################')



        for layer in self.pre_net.layers:
            layer.trainable = False
        # save trained model
        '''
        out_file = self.save_path = "/trained_pre_net.h5py"
        self.pre_net.save(out_file)
        print("saved trained prenet model at "+str(out_file))

        prenet_config = self.pre_net.get_config()
        out_file = self.save_path +"/trained_pre_net_config"
        with open(out_file, "w") as f:
            f.write( str(prenet_config))
        print("saved prenet model config at "+str(out_file))

        out_file = self.save_path +"/trained_pre_net_weights.h5"
        self.pre_net.save_weights(out_file)
        print("wrote trained prenet weights to "+str(out_file))
        '''

        # train main net
        self.main_net.fit(
            x = self.data.get_train_data(as_matrix = True),
            y = self.data.get_train_labels(),
            batch_size = self.batch_size,
            epochs = self.train_epochs,
            shuffle = True,
            callbacks = callbacks,
            validation_split=0.2,
            )

        y_pred = self.main_net.predict(self.data.get_train_data(as_matrix = True), verbose=1)

        score = roc_auc_score(self.data.get_train_labels(), y_pred)
        print('##############################################################################')
        print(score)
        print('##############################################################################')
        '''
        # save trained model
        out_file = self.save_path = "/trained_main_net.h5py"
        self.main_net.save(out_file)
        print("saved trained model at "*str(out_file))

        mainnet_config = self.main_net.get_config()
        out_file = self.save_path +"/trained_main_net_config"
        with open(out_file, "w") as f:
            f.write( str(mainnet_config))
        print("saved model config at "+str(out_file))

        out_file = self.save_path +"/trained_main_net_weights.h5"
        self.main_net.save_weights(out_file)
        print("wrote trained weights to "+str(out_file))
        '''

    def eval_model(self):
        ''' evaluate trained model '''

        # prenet evaluation
        self.prenet_eval = self.pre_net.evaluate(
            self.data.get_test_data(as_matrix = True))
        print("prenet test loss: {}".format(self.prenet_eval[0]))
        for im, metric in enumerate(self.eval_metrics):
            print("prenet test {}: {}".format(metric, self.test_eval[im+1]))

        self.prenet_history = self.trained_pre_net.history

        self.prenet_predicted_vector = self.pre_net.predict( self.data.get_test_data(as_matrix = True) )


        # main net evaluation
        self.mainnet_eval = self.main_net.evaluate(
            x = self.data.get_test_data(as_matrix = True)
            )
        print("mainnet test loss: {}".format(self.mainnet_eval[0]))
        for im, metric in enumerate(self.eval_metrics):
            print("mainnet test {}: {}".format(metric, self. test_eval[im+1]))

        self.mainnet_history = self.trained_main_net.history

        self.mainnet_predicted_vector = self.main_net.predict() # TODO implement main net input

        self.predicted_classes = np.argmax( self.mainnet_predicted_vector, axis = 1)
    
        self.confusion_matrix = confusion_matrix(
            self.get_test_labels(), self.predicted_classes)

        

    # --------------------------------------------------------------------
    # result plotting functions
    # --------------------------------------------------------------------

    def plot_metrics(self):
        ''' plot history of loss function and evaluation metrics '''


        metrics = ["loss"]+self.eval_metrics

        for metric in metrics:
            # prenet plot
            plt.clf()
            train_history = self.prenet_history[metric]
            val_history = self.prenet_history["val_"+metric]

            n_epochs = len(train_history)
            epochs = np.arange(1,n_epochs+1,1)

            plt.plot(epochs, train_history, "b-", label = "train", lw = 2)
            plt.plot(epochs, val_history, "r-", label = "validation", lw = 2)
            plt.title("train and validation "+str(metric)+" of prenet")

            plt.grid()
            plt.xlabel("epoch")
            plt.ylabel(metric)

            plt.legend()

            out_path = self.save_path + "/prenet_history_"+str(metric)+".pdf"
            plt.savefig(out_path)
            print("saved plot of "+str(metric)+" at "+str(out_path))

            # main net
            plt.clf()
            train_history = self.mainnet_history[metric]
            val_history = self.mainnet_history["val_"+metric]

            n_epochs = len(train_history)
            epochs = np.arange(1,n_epochs+1,1)

            plt.plot(epochs, train_history, "b-", label = "train", lw = 2)
            plt.plot(epochs, val_history, "r-", label = "validation", lw = 2)
            plt.title("train and validation "+str(metric)+" of mainnet")

            plt.grid()
            plt.xlabel("epoch")
            plt.ylabel(metric)

            plt.legend()

            out_path = self.save_path + "/mainnet_history_"+str(metric)+".pdf"
            plt.savefig(out_path)
            print("saved plot of "+str(metric)+" at "+str(out_path))



















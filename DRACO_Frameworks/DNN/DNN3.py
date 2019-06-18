import os
import sys
import numpy as np
import json

# local imports
filedir  = os.path.dirname(os.path.realpath(__file__))
DRACOdir = os.path.dirname(filedir)
basedir  = os.path.dirname(DRACOdir)
sys.path.append(basedir)

# import with ROOT
from pyrootsOfTheCaribbean.evaluationScripts import plottingScripts2 as plottingScripts

# imports with keras
import utils.generateJTcut as JTcut
import architecture as arch
import data_frame

import keras
import keras.models as models
import keras.layers as layer
from keras import backend as K
import matplotlib.pyplot as plt
import pandas as pd

# Limit gpu usage
import tensorflow as tf

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
K.tensorflow_backend.set_session(tf.Session(config=config))




class DNN():

    def __init__(self, in_path, save_path,
                event_classes,
                event_category,
                train_variables,
                batch_size = 5000,
                train_epochs = 500,
                early_stopping = 10,
                optimizer = None,
                loss_function = "categorical_crossentropy",
                test_percentage = 0.2,
                eval_metrics = None,
                additional_cut = None):

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
        self.JTstring       = event_category
        self.event_category = JTcut.getJTstring(event_category)
        self.categoryLabel  = JTcut.getJTlabel(event_category)

        # list of input variables
        self.train_variables = train_variables

        # batch size for training
        self.batch_size = batch_size
        # number of training epochs
        self.train_epochs = train_epochs
        # number of early stopping epochs
        self.early_stopping = early_stopping
        # percentage of events saved for testing
        self.test_percentage = test_percentage

        # loss function for training
        self.loss_function = loss_function
        # additional metrics for evaluation of the training process
        #self.eval_metrics = eval_metrics
	self.eval_metrics = None

        # additional cuts to be applied after variable norm
        self.additional_cut = additional_cut

        # load data set
        self.data = self._load_datasets()
        self.cp_path = self.save_path+"/checkpoints/"
        if not os.path.exists(self.cp_path):
            os.makedirs(self.cp_path)
        out_file = self.cp_path + "/variable_norm.csv"
        self.data.norm_csv.to_csv(out_file)
        print("saved variabe norms at "+str(out_file))

        # make plotdir
        self.plot_path = self.save_path+"/plots/"
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

    def _load_datasets(self):
        ''' load data set '''

        return data_frame.DataFrame(
            path_to_input_files = self.in_path,
            classes             = self.event_classes,
            event_category      = self.event_category,
            train_variables     = self.train_variables,
            test_percentage     = self.test_percentage,
            norm_variables      = True,
            additional_cut      = self.additional_cut)

    def load_trained_model(self):
        ''' load an already trained model '''
        checkpoint_path = self.cp_path + "/trained_model.h5py"

        self.model = keras.models.load_model(checkpoint_path)

        #self.model_eval = self.model.evaluate(
        #    self.data.get_test_data(as_matrix = True),
        #    self.data.get_test_labels())

        self.model_prediction_vector = self.model.predict(
            self.data.get_test_data(as_matrix = True))

        self.predicted_classes = np.argmax( self.model_prediction_vector, axis = 1)
        #Some checks:
        print(self.model_prediction_vector)
        print(self.predicted_classes)
        print(self.event_classes)
        print(self.categoryLabel)
        print(self.data)
	for counter, value in enumerate(self.event_classes):
	  print(counter)
	  print(value)
	print("this thing ",value," is ",self.data.class_translation[value])
        print(self.data.class_translation)
        #print(self.data.get_full_df())
 
    def predict_event_query(self, query ):
        events = self.data.get_full_df().query( query )
        print(str(events.shape[0]) + " events matched the query '"+str(query)+"'.")

        for index, row in events.iterrows():
            print("========== DNN output ==========")
            print("Event: "+str(index))
            for var in row.values:
                print(var)
            print("-------------------->")
            output = self.model.predict( np.array([list(row.values)]) )[0]
            for i, node in enumerate(self.event_classes):
                print(str(node)+" node: "+str(output[i]))
            print("-------------------->")


    # --------------------------------------------------------------------
    # result plotting functions
    # --------------------------------------------------------------------


    def plot_discriminators(self, log = False):
        ''' plot all events classified as one category '''
        nbins = 18
        bin_range = [0.1, 1.0]

        plotDiscrs = plottingScripts.plotDiscriminators(
            data                = self.data,
            prediction_vector   = self.model_prediction_vector,
            event_classes       = self.event_classes,
            nbins               = nbins,
            bin_range           = bin_range,
            signal_class        = "ttHH4b",
            event_category      = self.categoryLabel,
            plotdir             = self.plot_path,
            logscale            = log)

        plotDiscrs.set_printROCScore(False)
        plotDiscrs.plot(ratio = False)

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
#fixing strange error:
sys.path.append("/afs/cern.ch/work/l/lprado/DRACO-MLfoy/pyrootsOfTheCaribbean/evaluationScripts")
import plottingScripts2 as plottingScripts
#from pyrootsOfTheCaribbean.evaluationScripts import plottingScripts2 as plottingScripts

# imports with keras
import utils.generateJTcut as JTcut
import architecture as arch
import data_frame2 as data_frame

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
                root_output,
                event_classes,
		event_classes_extra,
                event_category,
                train_variables,
                systematics,
                batch_size = 5000,
                train_epochs = 500,
                early_stopping = 100,
                optimizer = None,
                loss_function = "categorical_crossentropy",
                test_percentage = 0.2,
                eval_metrics = "acc",
                additional_cut = None):

        # save some information
        # path to input files
        self.in_path = in_path
        self.root_output = root_output
        # output directory for results
        self.save_path = save_path
        if not os.path.exists(self.save_path):
            os.makedirs( self.save_path )
        # list of classes
        self.event_classes = event_classes
        #classes for plotting
	self.event_classes_extra = event_classes_extra
        # name of event category (usually nJet/nTag category)
        self.JTstring       = event_category
        self.event_category = JTcut.getJTstring(event_category)
        self.categoryLabel  = JTcut.getJTlabel(event_category)

        #string for controlling systematic variation templates
        self.systematics = systematics

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
        print(self.data.norm_csv)
        print("saved variabe norms at "+str(out_file))

        # make plotdir
        self.plot_path = self.save_path+"/plots/"
        if not os.path.exists(self.plot_path):
            os.makedirs(self.plot_path)

        #self.bin_range=[[0.17,1.0],[0.17,0.84],[0.17,0.70],[0.17,0.58],[0.17,0.41],[0.17,0.64]]
	#ttHH4b steps of 0.0415
        self.bin_range=[np.array([0.17,0.253,0.2945,0.336,0.3775,0.419,0.4605,0.502,0.5435,0.585,0.6265,0.668,0.7095,0.751,0.7925,0.834,0.8755,0.917,0.9585,1.0],dtype='float64'),\
         np.array([0.17,0.26,0.305,0.35,0.395,0.44,0.485,0.53,0.575,0.62,0.665,0.71,0.84],dtype='float64'),\
         np.array([0.17,0.276,0.329,0.382,0.435,0.488,0.70],dtype='float64'),\
         np.array([0.17,0.244,0.281,0.318,0.355,0.392,0.429,0.58],dtype='float64'),\
         np.array([0.17,0.238,0.272,0.306,0.41],dtype='float64'),\
         np.array([0.17,0.263,0.294,0.325,0.356,0.387,0.418,0.449,0.48,0.511,0.542,0.64],dtype='float64')]
        #self.nbins=[len(self.bin_range[0])-1,len(self.bin_range[1])-1,len(self.bin_range[2])-1,len(self.bin_range[3])-1,len(self.bin_range[4])-1,len(self.bin_range[5])-1]
        #self.nbins=[20,15,10,11,7,15]
        self.nbins=[19,12,6,7,4,11]

    def _load_datasets(self):
        ''' load data set '''

        return data_frame.DataFrame(
            path_to_input_files = self.in_path,
            save_path           = self.save_path,
            classes             = self.event_classes_extra,
            node_classes        = self.event_classes,
            systematics         = self.systematics,
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
	print("prediction vector print: ",self.model_prediction_vector[0:10,:])
        print("predicted_classes is: ",self.predicted_classes)
        print("event_classes is: ",self.event_classes)
	print("event_classes_extra is:  ",self.event_classes_extra)
        print(self.categoryLabel)
        #print(self.data)
	for i, node_cls in enumerate(self.event_classes):
	  print(i)
	  print(node_cls)
	#print("this thing ",node_cls," is ",self.data.class_translation[node_cls])
        print(self.data.class_translation)
        #print(self.data.get_full_df())
	print("get test labels is:  ", self.data.get_test_labels(as_categorical=False))
 	#print("lumi weights:   ", self.data.get_lumi_weights())
	print("get test labels is:  ", self.data.get_test_labels(as_categorical=False)[0])
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
        nbins     = self.nbins
        bin_range = self.bin_range

        plotDiscrs = plottingScripts.plotDiscriminators(
            data                = self.data,
            prediction_vector   = self.model_prediction_vector,
            event_classes       = self.event_classes,
	    event_classes_extra  = self.event_classes_extra,
            systematics         = self.systematics,
            nbins               = nbins,
            bin_range           = bin_range,
            signal_class        = "ttHH4b",
	    data_class          = "data",
            event_category      = self.categoryLabel,
            plotdir             = self.plot_path,
            root_output         = self.root_output,
            logscale            = log)

        plotDiscrs.set_printROCScore(False)
        plotDiscrs.plot(ratio = False)

    def plot_discriminators_pretty(self, log = False):
        ''' plot all events classified as one category '''
        nbins     = self.nbins
        bin_range = self.bin_range

        plotDiscrs = plottingScripts.plotDiscriminatorsPretty(
            data                = self.data,
            prediction_vector   = self.model_prediction_vector,
            event_classes       = self.event_classes,
            event_classes_extra  = self.event_classes_extra,
            systematics         = self.systematics,
            nbins               = nbins,
            bin_range           = bin_range,
            signal_class        = "ttHH4b",
            data_class          = "data",
            event_category      = self.categoryLabel,
            plotdir             = self.plot_path,
            root_output         = self.root_output,
            logscale            = log)

        plotDiscrs.set_printROCScore(False)
        plotDiscrs.plot(ratio = False)


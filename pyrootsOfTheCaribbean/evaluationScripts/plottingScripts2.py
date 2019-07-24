import os
import sys
import numpy as np
import ROOT
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

# local imports
filedir  = os.path.dirname(os.path.realpath(__file__))
pyrootdir = os.path.dirname(filedir)
basedir  = os.path.dirname(pyrootdir)
sys.path.append(pyrootdir)
sys.path.append(basedir)

import plot_configs.setupPlots as setup


class plotDiscriminators:
    def __init__(self, data, prediction_vector, event_classes, event_classes_extra, nbins, bin_range, signal_class, data_class, event_category, plotdir, root_output, logscale = False):
        self.data              = data
        self.prediction_vector = prediction_vector
        self.predicted_classes = np.argmax( self.prediction_vector, axis = 1)

        self.event_classes     = event_classes
	self.event_classes_extra = event_classes_extra
        self.nbins             = nbins
        self.bin_range         = bin_range
        self.signal_class      = signal_class
	self.data_class        = data_class
        self.event_category    = event_category
        self.plotdir           = plotdir
        self.root_output       = root_output
        self.logscale          = logscale


        # default settings
        self.printROCScore = False

    def set_printROCScore(self, printROCScore):
        self.printROCScore = printROCScore

    def plot(self, ratio = False):
        f = ROOT.TFile(self.root_output,"RECREATE")
	subD1=f.mkdir("ttHH4b_node")
	subD2=f.mkdir("ttbb_node")
	subD3=f.mkdir("tt2b_node")
	subD4=f.mkdir("ttb_node")
	subD5=f.mkdir("ttcc_node")
	subD6=f.mkdir("ttlf_node")
        RDirectory = [subD1,subD2,subD3,subD4,subD5,subD6]
	node_bins=[[0.17,1.0],[0.17,0.84],[0.17,0.70],[0.17,0.58],[0.17,0.4],[0.17,0.64]]


        # generate one plot per output node
        for i, node_cls in enumerate(self.event_classes):
            nodeIndex = self.data.class_translation[node_cls]
            print("i is: ", i)
            print("nodeindex is ", nodeIndex)
	    print("node_cls is: ",node_cls)
            # get output values of this node
            out_values = self.prediction_vector[:,i]
            #print("The out_values are: ",out_values)
	    print("folder is:  ", RDirectory[i])
            if self.printROCScore:
                # calculate ROC value for specific node
                nodeROC = roc_auc_score(self.signalFlag, out_values)

            # fill lists according to class
            bkgHists  = []
            bkgLabels = []
            weightIntegral = 0
            
            nbins_node=int(50*(node_bins[nodeIndex][1]-node_bins[nodeIndex][0]))
            # loop over all classes to fill hists according to truth level class
            for j, truth_cls in enumerate(self.event_classes_extra):
                classIndex = self.data.class_translation[truth_cls]

                # filter values per event class
                filtered_values = [ out_values[k] for k in range(len(out_values)) \
                    if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                    and self.predicted_classes[k] == nodeIndex]

                filtered_weights = [ self.data.get_lumi_weights()[k] for k in range(len(out_values)) \
                    if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                    and self.predicted_classes[k] == nodeIndex]

                    
                histogram = setup.setupHistogram(
                        values    = filtered_values,
                        weights   = filtered_weights,
                        nbins     = nbins_node,#self.nbins,
                        bin_range = node_bins[nodeIndex],#self.bin_range,
                        color     = ROOT.kBlue,#setup.GetPlotColor(truth_cls),
                        xtitle    = str(truth_cls),
                        ytitle    = setup.GetyTitle(),
                        filled    = True)
                    
                RDirectory[i].cd()
                histogram.Write() 
		f.cd()
                bkgHists.append( histogram )
                bkgLabels.append( truth_cls )
		print("checking the Hists... :   ", bkgHists)
		print("checking the Labels... :   ", bkgLabels)




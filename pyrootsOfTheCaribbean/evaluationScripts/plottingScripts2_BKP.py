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
    def __init__(self, data, prediction_vector, event_classes, event_classes_extra, nbins, bin_range, signal_class, data_class, event_category, plotdir, logscale = False):
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
        self.logscale          = logscale

        self.signalIndex       = self.data.class_translation[self.signal_class]
        self.signalFlag        = self.data.get_class_flag(self.signal_class)

	self.dataIndex         = self.data.class_translation[self.data_class]
	self.dataFlag          = self.data.get_class_flag(self.data_class)

        # default settings
        self.printROCScore = False

    def set_printROCScore(self, printROCScore):
        self.printROCScore = printROCScore

    def plot(self, ratio = False):
        f = ROOT.TFile("ttHH_Test7_data_predict_"+"ge4j_ge3t"+".root","RECREATE")
	subD1=f.mkdir("ttHH4b_node")
	subD2=f.mkdir("ttbb_node")
	subD3=f.mkdir("tt2b_node")
	subD4=f.mkdir("ttb_node")
	subD5=f.mkdir("ttcc_node")
	subD6=f.mkdir("ttlf_node")
        RDirectory = [subD1,subD2,subD3,subD4,subD5,subD6]
	node_bins=[[0.17,1.0],[0.17,0.8],[0.17,0.65],[0.17,0.55],[0.17,0.4],[0.17,0.54]]
        # generate one plot per output node
        for i, node_cls in enumerate(self.event_classes):
            nodeIndex = self.data.class_translation[node_cls]
            print("i is: ", i)
            print("nodeindex is ", nodeIndex)
	    print("node_cls is: ",node_cls)
	    #print("signal flag is: ", self.signalFlag)
	    #print("data flag is: ", self.dataFlag)
            # get output values of this node
            out_values = self.prediction_vector[:,i]
            #print("The out_values are: ",out_values)
	    #print("signalIndex is:  ", self.signalIndex)
	    #print("dataIndex is:  ", self.dataIndex)
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

                if j == self.signalIndex:
                    # signal histogram
                    sig_values  = filtered_values
                    sig_label   = str(truth_cls)
                    sig_weights = filtered_weights
		elif j == self.dataIndex:
                    # data histogram
                    data_values  = filtered_values
                    data_label   = str(truth_cls)
                    data_weights = filtered_weights
                elif j < self.dataIndex:
                    # background histograms
                    weightIntegral += sum(filtered_weights)
                    
                    histogram = setup.setupHistogram(
                        values    = filtered_values,
                        weights   = filtered_weights,
                        nbins     = nbins_node,#self.nbins,
                        bin_range = node_bins[nodeIndex],#self.bin_range,
                        color     = setup.GetPlotColor(truth_cls),
                        xtitle    = str(truth_cls),
		    	#+" at "+str(node_cls)+" node",
                        ytitle    = setup.GetyTitle(),
                        filled    = True)
                    
                    RDirectory[i].cd()
                    histogram.Write() 
		    f.cd()
                    bkgHists.append( histogram )
                    bkgLabels.append( truth_cls )
		    print("checking the bkdHists... :   ", bkgHists)
		    print("checking the bkgLabels... :   ", bkgLabels)
                else:
		    #sys_histograms
                    sysHists = setup.setupHistogram(
                        values    = filtered_values,
                        weights   = filtered_weights,
                        nbins     = nbins_node,#self.nbins,
                        bin_range = node_bins[nodeIndex],#self.bin_range,
                        color     = ROOT.kBlue,#setup.GetPlotColor(truth_cls),
                        xtitle    = str(truth_cls),
                        #+" at "+str(node_cls)+" node",
                        ytitle    = setup.GetyTitle(),
                        filled    = False)

                    RDirectory[i].cd()
                    sysHists.Write()
                    f.cd()
                    print("checking the syst... value of j? :   ", j)
  
            # setup signal histogram
            sigHist = setup.setupHistogram(
                values    = sig_values,
                weights   = sig_weights,
                nbins     = nbins_node,#self.nbins,
                bin_range = node_bins[nodeIndex],#self.bin_range,
                color     = setup.GetPlotColor(sig_label),
                xtitle    = str(sig_label),
		#+" at "+str(node_cls)+" node",
                ytitle    = setup.GetyTitle(),
                filled    = False)

            RDirectory[i].cd()
            sigHist.Write()
            f.cd()

            # setup data histogram
            dataHist = setup.setupHistogram(
                values    = data_values,
                weights   = data_weights,
                nbins     = nbins_node,#self.nbins,
                bin_range = node_bins[nodeIndex],#self.bin_range,
                color     = setup.GetPlotColor(sig_label),
                xtitle    = "data_obs",
                ytitle    = setup.GetyTitle(),
                filled    = False)

	    RDirectory[i].cd()
            dataHist.Write()
	    f.cd()

            # set signal histogram linewidth
            sigHist.SetLineWidth(3)

            # set scalefactor
            scaleFactor = weightIntegral/(sum(sig_weights)+1e-9)
            sigHist.Scale(scaleFactor)

            plotOptions = {
                "ratio":      ratio,
                "ratioTitle": "#frac{scaled Signal}{Background}",
                "logscale":   self.logscale}
            canvas = setup.drawHistsOnCanvas(
                sigHist, bkgHists, plotOptions, 
                canvasName = node_cls+" final discriminator")

            # setup legend
            legend = setup.getLegend()

            # add signal entry
            legend.AddEntry(sigHist, sig_label+" x {:4.0f}".format(scaleFactor), "L")

            # add background entries
            for i, h in enumerate(bkgHists):
                legend.AddEntry(h, bkgLabels[i], "F")

            # draw legend
            legend.Draw("same")

            # add ROC score if activated
            if self.printROCScore:
                setup.printROCScore(canvas, nodeROC, plotOptions["ratio"])

            # add lumi and category to plot
            setup.printLumi(canvas, ratio = plotOptions["ratio"])
            setup.printCategoryLabel(canvas, self.event_category, ratio = plotOptions["ratio"])

            out_path = self.plotdir + "/finaldiscr_{}.pdf".format(node_cls)
            setup.saveCanvas(canvas, out_path)

        f.Close() 
        # add the histograms together
        workdir = os.path.dirname(self.plotdir[:-1])
        cmd = "pdfunite "+str(self.plotdir)+"/finaldiscr_*.pdf "+str(workdir)+"/discriminators.pdf"
        print(cmd)
        os.system(cmd)















class plotOutputNodes:
    def __init__(self, data, prediction_vector, event_classes, nbins, bin_range, signal_class, event_category, plotdir, logscale = False):
        self.data              = data
        self.prediction_vector = prediction_vector
        self.event_classes     = event_classes
        self.nbins             = nbins
        self.bin_range         = bin_range
        self.signal_class      = signal_class
        self.event_category    = event_category
        self.plotdir           = plotdir
        self.logscale          = logscale

        self.signalIndex       = self.data.class_translation[self.signal_class]
        self.signalFlag        = self.data.get_class_flag(self.signal_class)

        # default settings
        self.printROCScore = False
        self.cutVariable = False
        self.eventInCut = np.array([True for _ in range(len(self.prediction_vector))])

    def set_cutVariable(self, cutClass, cutValue):
        cutVariableIndex = self.data.class_translation[cutClass]
        predictions_cutVariable = self.prediction_vector[:, cutVariableIndex]
        self.eventInCut = [predictions_cutVariable[i] <= cutValue for i in len(self.prediction_vector)]

        self.cutVariable = True

    def set_printROCScore(self, printROCScore):
        self.printROCScore = printROCScore

    def plot(self, ratio = False):
        # generate one plot per output node
        for i, node_cls in enumerate(self.event_classes):
            # get output values of this node
            out_values = self.prediction_vector[:,i]

            if self.printROCScore:
                # calculate ROC value for specific node
                nodeROC = roc_auc_score(self.signalFlag, out_values)

            # fill lists according to class
            bkgHists  = []
            bkgLabels = []
            weightIntegral = 0

            # loop over all classes to fill hists according to truth level class
            for j, truth_cls in enumerate(self.event_classes):
                classIndex = self.data.class_translation[truth_cls]

                # filter values per event class
                filtered_values = [ out_values[k] for k in range(len(out_values)) \
                    if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                    and self.eventInCut[k]]

                filtered_weights = [ self.data.get_lumi_weights()[k] for k in range(len(out_values)) \
                    if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                    and self.eventInCut[k]]

                if j == self.signalIndex:
                    # signal histogram
                    sig_values  = filtered_values
                    sig_label   = str(truth_cls)
                    sig_weights = filtered_weights
                else:
                    # background histograms
                    weightIntegral += sum(filtered_weights)
                    
                    histogram = setup.setupHistogram(
                        values    = filtered_values,
                        weights   = filtered_weights,
                        nbins     = self.nbins,
                        bin_range = self.bin_range,
                        color     = setup.GetPlotColor(truth_cls),
                        xtitle    = str(truth_cls)+" at "+str(node_cls)+" node",
                        ytitle    = setup.GetyTitle(),
                        filled    = True)
                    
                    bkgHists.append( histogram )
                    bkgLabels.append( truth_cls )
            # setup signal histogram
            sigHist = setup.setupHistogram(
                values    = sig_values,
                weights   = sig_weights,
                nbins     = self.nbins,
                bin_range = self.bin_range,
                color     = setup.GetPlotColor(sig_label),
                xtitle    = str(sig_label)+" at "+str(node_cls)+" node",
                ytitle    = setup.GetyTitle(),
                filled    = False)
            # set signal histogram linewidth
            sigHist.SetLineWidth(3)

            # set scalefactor
            scaleFactor = weightIntegral/(sum(sig_weights)+1e-9)
            sigHist.Scale(scaleFactor)

            plotOptions = {
                "ratio":      ratio,
                "ratioTitle": "#frac{scaled Signal}{Background}",
                "logscale":   self.logscale}
            canvas = setup.drawHistsOnCanvas(
                sigHist, bkgHists, plotOptions, 
                canvasName = node_cls+" node")

            # setup legend
            legend = setup.getLegend()

            # add signal entry
            legend.AddEntry(sigHist, sig_label+" x {:4.0f}".format(scaleFactor), "L")

            # add background entries
            for i, h in enumerate(bkgHists):
                legend.AddEntry(h, bkgLabels[i], "F")

            ## scale signal Histogram
            #sigHist.Scale( scaleFactor )

            # draw legend
            legend.Draw("same")

            # add ROC score if activated
            if self.printROCScore:
                setup.printROCScore(canvas, nodeROC, plotOptions["ratio"])

            # add lumi and category to plot
            setup.printLumi(canvas, ratio = plotOptions["ratio"])
            setup.printCategoryLabel(canvas, self.event_category, ratio = plotOptions["ratio"])

            out_path = self.plotdir + "/outputNode_{}.pdf".format(node_cls)
            setup.saveCanvas(canvas, out_path)

        # add the histograms together
        workdir = os.path.dirname(self.plotdir[:-1])
        cmd = "pdfunite "+str(self.plotdir)+"/outputNode_*.pdf "+str(workdir)+"/outputNodes.pdf"
        print(cmd)
        os.system(cmd)









class plotConfusionMatrix:
    def __init__(self, data, prediction_vector, event_classes, event_category, plotdir):
        self.data              = data
        self.prediction_vector = prediction_vector
        self.predicted_classes = np.argmax(self.prediction_vector, axis = 1)

        self.event_classes     = event_classes
        self.n_classes         = len(self.event_classes)

        self.event_category    = event_category
        self.plotdir           = plotdir

        self.confusion_matrix = confusion_matrix(
            self.data.get_test_labels(as_categorical = False), self.predicted_classes)

        # default settings
        self.printROCScore = False
        self.ROCScore = None
    
    def set_printROCScore(self, printROCScore):
        self.printROCScore = printROCScore
        self.ROCScore = roc_auc_score(
            self.data.get_test_labels(), self.prediction_vector)

    def plot(self, norm_matrix = True):
        
        # norm confusion matrix if activated
        if norm_matrix:
            new_matrix = np.empty( (self.n_classes, self.n_classes), dtype = np.float64)
            for yit in range(self.n_classes):
                evt_sum = float(sum(self.confusion_matrix[yit,:]))
                for xit in range(self.n_classes):
                    new_matrix[yit,xit] = self.confusion_matrix[yit,xit]/(evt_sum+1e-9)

            self.confusion_matrix = new_matrix
        

        # initialize Histogram
        cm = setup.setup2DHistogram(
            matrix      = self.confusion_matrix.T,
            ncls        = self.n_classes,
            xtitle      = "predicted class",
            ytitle      = "true class",
            binlabel    = self.event_classes)

        canvas = setup.draw2DHistOnCanvas(cm, "confusion matrix", self.event_category, self.ROCScore)
        setup.saveCanvas(canvas, self.plotdir+"/confusionMatrix.pdf")
        










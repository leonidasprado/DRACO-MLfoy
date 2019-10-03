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

dict_syst={"Weight_CSVCErr1down":"CMS_btag_cferr1_2017Down","Weight_CSVCErr1up":"CMS_btag_cferr1_2017Up",\
"Weight_CSVCErr2down":"CMS_btag_cferr2_2017Down","Weight_CSVCErr2up":"CMS_btag_cferr2_2017Up",\
"Weight_CSVHFdown":"CMS_btag_hf_2017Down","Weight_CSVHFup":"CMS_btag_hf_2017Up",\
"Weight_CSVHFStats1down":"CMS_btag_hfstats1_2017Down","Weight_CSVHFStats1up":"CMS_btag_hfstats1_2017Up",\
"Weight_CSVHFStats2down":"CMS_btag_hfstats2_2017Down","Weight_CSVHFStats2up":"CMS_btag_hfstats2_2017Up",\
"Weight_CSVLFdown":"CMS_btag_lf_2017Down","Weight_CSVLFup":"CMS_btag_lf_2017Up",\
"Weight_CSVLFStats1down":"CMS_btag_lfstats1_2017Down","Weight_CSVLFStats1up":"CMS_btag_lfstats1_2017Up",\
"Weight_CSVLFStats2down":"CMS_btag_lfstats2_2017Down","Weight_CSVLFStats2up":"CMS_btag_lfstats2_2017Up",\
"Weight_pu69p2Down":"CMS_ttH_PUDown","Weight_pu69p2Up":"CMS_ttH_PUUp",\
"Weight_ElectronSFGFS_Down":"CMS_SFGFS_e_2017Down","Weight_ElectronSFGFS_Up":"CMS_SFGFS_e_2017Up",\
"Weight_ElectronSFID_Down":"CMS_SFID_e_2017Down","Weight_ElectronSFID_Up":"CMS_SFID_e_2017Up",\
"Weight_ElectronSFTrigger_Down":"CMS_SFTrigger_e_2017Down","Weight_ElectronSFTrigger_Up":"CMS_SFTrigger_e_2017Up",\
"Weight_MuonSFID_Down":"CMS_SFID_m_2017Down","Weight_MuonSFID_Up":"CMS_SFID_m_2017Up",\
"Weight_MuonSFIso_Up":"CMS_SFIso_m_2017Up","Weight_MuonSFIso_Down":"CMS_SFIso_m_2017Down",\
"Weight_MuonSFTrigger_Down":"CMS_SFTrigger_m_2017Down","Weight_MuonSFTrigger_Up":"CMS_SFTrigger_m_2017Up",\
"GenWeight_8":"CMS_ttH_ISR_ttbar_2017Down","GenWeight_6":"CMS_ttH_ISR_ttbar_2017Up",\
"GenWeight_9":"CMS_ttH_FSR_ttbar_2017Down","GenWeight_7":"CMS_ttH_FSR_ttbar_2017Up",\
"Weight_LHA_306000_up":"CMS_ttH_PDF_2017Up","Weight_LHA_306000_down":"CMS_ttH_PDF_2017Down",\
"Weight_scale_variation_muR_2p0_muF_1p0":"CMS_ttH_scaleMuRUp","Weight_scale_variation_muR_0p5_muF_1p0":"CMS_ttH_scaleMuRDown",\
"Weight_scale_variation_muR_1p0_muF_2p0":"CMS_ttH_scaleMuFUp","Weight_scale_variation_muR_1p0_muF_0p5":"CMS_ttH_scaleMuFDown"}

onlyttbarlist=("GenWeight_8","GenWeight_6","GenWeight_9","GenWeight_7","Weight_LHA_306000_up","Weight_LHA_306000_down","Weight_scale_variation_muR_2p0_muF_1p0","Weight_scale_variation_muR_0p5_muF_1p0","Weight_scale_variation_muR_1p0_muF_2p0","Weight_scale_variation_muR_1p0_muF_0p5")

class plotDiscriminators:
    def __init__(self, data, prediction_vector, event_classes, event_classes_extra, systematics, nbins, bin_range, signal_class, data_class, event_category, plotdir, root_output, logscale = False):
        self.data              = data
        self.prediction_vector = prediction_vector
        self.predicted_classes = np.argmax( self.prediction_vector, axis = 1)

        self.event_classes     = event_classes
	self.event_classes_extra = event_classes_extra
        self.systematics       = systematics
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
        RDirectory=[]
	for i, node in enumerate(self.event_classes):
          RDirectory.append(f.mkdir(str(node)+"_node"))

	node_bins=self.bin_range
        nbins_node=self.nbins
        #node_bins=[[0.17,1.0],[0.17,0.84],[0.17,0.70],[0.17,0.58],[0.17,0.4],[0.17,0.64]]
        print("nbins_node is: ",nbins_node)

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
            
            #nbins_node=int(50*(node_bins[nodeIndex][1]-node_bins[nodeIndex][0]))
            # loop over all classes to fill hists according to truth level class
            for j, truth_cls in enumerate(self.event_classes_extra):
                classIndex = self.data.class_translation[truth_cls]
                if "ttHH4b" in truth_cls and self.systematics in onlyttbarlist:
                  continue
                # filter values per event class
                filtered_values = [ out_values[k] for k in range(len(out_values)) \
                    if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                    and self.predicted_classes[k] == nodeIndex]

                if self.systematics == "1":
                    filtered_weights = [ self.data.get_lumi_weights()[k] for k in range(len(out_values)) \
                        if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                        and self.predicted_classes[k] == nodeIndex]
                    htitle = str(truth_cls)
                else:
                    filtered_weights = [ self.data.get_lumi_weights_syst()[k] for k in range(len(out_values)) \
                        if self.data.get_test_labels(as_categorical = False)[k] == classIndex \
                        and self.predicted_classes[k] == nodeIndex]
                    htitle = str(truth_cls) + "_" + dict_syst[self.systematics]

                histogram = setup.setupHistogram(
                        values    = filtered_values,
                        weights   = filtered_weights,
                        nbins     = nbins_node[nodeIndex],#self.nbins,
                        bin_range = node_bins[nodeIndex],#self.bin_range,
                        color     = ROOT.kBlue,#setup.GetPlotColor(truth_cls),
                        xtitle    = htitle, #str(truth_cls),
                        ytitle    = setup.GetyTitle(),
                        filled    = True)
                    
                RDirectory[i].cd()
                histogram.Write() 
		f.cd()
                bkgHists.append( histogram )
                bkgLabels.append( truth_cls )
		print("checking the Hists... :   ", bkgHists)
		print("checking the Labels... :   ", bkgLabels)




#Plotting discriminators on a canvas
class plotDiscriminatorsPretty:
    def __init__(self, data, prediction_vector, event_classes, event_classes_extra, systematics, nbins, bin_range, signal_class, data_class, event_category, plotdir, root_output, logscale = False):
        self.data              = data
        self.prediction_vector = prediction_vector
        self.predicted_classes = np.argmax( self.prediction_vector, axis = 1)

        self.event_classes     = event_classes
	self.event_classes_extra = event_classes_extra
        self.systematics       = systematics
        self.nbins             = nbins
        self.bin_range         = bin_range
        self.signal_class      = signal_class
	self.data_class        = data_class
        self.event_category    = event_category
        self.plotdir           = plotdir
        self.root_output       = root_output
        self.logscale          = logscale

        self.signalIndex       = self.data.class_translation[self.signal_class]
        self.signalFlag        = self.data.get_class_flag(self.signal_class)


        # default settings
        self.printROCScore = False

    def set_printROCScore(self, printROCScore):
        self.printROCScore = printROCScore

    def plot(self, ratio = False):
        f = ROOT.TFile(self.root_output,"RECREATE")
        RDirectory=[]
        for i, node in enumerate(self.event_classes):
          RDirectory.append(f.mkdir(str(node)+"_node"))

        node_bins=self.bin_range
        #node_bins=[[0.17,1.0],[0.17,0.84],[0.17,0.70],[0.17,0.58],[0.17,0.4],[0.17,0.64]]
        nbins_node=self.nbins
	
        print("pretty plot, coming down the street, pretty plot...")

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
            
            #nbins_node=int(50*(node_bins[nodeIndex][1]-node_bins[nodeIndex][0]))
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
                else:
                    # background histograms
                    weightIntegral += sum(filtered_weights)

                    histogram = setup.setupHistogram(
                        values    = filtered_values,
                        weights   = filtered_weights,
                        nbins     = nbins_node[nodeIndex],#self.nbins,
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


            # setup signal histogram
            sigHist = setup.setupHistogram(
                values    = sig_values,
                weights   = sig_weights,
                nbins     = nbins_node[nodeIndex],#self.nbins,
                bin_range = node_bins[nodeIndex],#self.bin_range,
                color     = setup.GetPlotColor(sig_label),
                xtitle    = str(sig_label),
                #+" at "+str(node_cls)+" node",
                ytitle    = setup.GetyTitle(),
                filled    = False)

            RDirectory[i].cd()
            sigHist.Write()
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


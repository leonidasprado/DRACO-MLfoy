import os
import sys
import pandas
import ROOT
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(os.path.dirname(filedir))
sys.path.append(basedir)

import utils.generateJTcut as JTcut
import plot_configs.variableConfig as binning
import plot_configs.setupPlots2 as setup

dict_variable={
    "N_BTagsT":"N_{b}(tight)",
    "N_BTagsL":"N_{b}(loose)",
    "N_BTagsM":"N_{b}(medium)",
    "Evt_Dr_MinDeltaRJets":"#DeltaR^{min}_{j,j}",
    "Evt_HT":"H_{T}",
    "Evt_HT_tagged":"H_{T}^{b}",
    "Evt_M_MinDeltaRJets":"m^{min#DeltaR}_{j,j}",
    "Evt_M2_TaggedJetsAverage":"(m^{2})^{avg}_{b}",
    "Evt_TaggedJet_MaxDeta_TaggedJets":"#Delta#eta^{max}_{b, b}",
    "Jet_CSV[0]":"d(jet 1)",
    "Jet_CSV[1]":"d(jet 2)",
    "Jet_CSV[2]":"d(jet 3)",
    "Jet_CSV[3]":"d(jet 4)",
    "Evt_Jet_MaxDeta_Jets":"#Delta#eta^{max}_{j, j}",
    "Evt_M_MinDeltaRLeptonTaggedJet":"m^{min#DeltaR}_{lep,b}",
    "Evt_JetPtOverJetE":"pt^{avg}_{j}/E^{avg}_{j}",
    "Evt_CSV_Dev":"#Sigma_{j}(d-d^{avg}_{j})^{2}",
    "LooseLepton_Eta[0]":"#eta(loose lepton, highest in pt)",
    "Evt_CSV_Dev_Tagged":"#Sigma_{b}(d-d^{avg}_{b})^{2}",
    "Evt_Dr_MinDeltaRTaggedJets":"#DeltaR^{min}_{b,b}",
    "BDT_common5_input_aplanarity":"aplanarity",
    "BDT_common5_input_sphericity_jets":"jet sphericity",
    "BDT_common5_input_sphericity_tags":"b-tagged jets sphericity",
    "BDT_common5_input_transverse_sphericity_jets":"transverse jet sphericity",
    "BDT_common5_input_transverse_sphericity_tags":"transverse tagged jet sphericity",
    "CSV[0]":"d_{1}",
    "CSV[1]":"d_{2}",
    "CSV[2]":"d_{3}",
    "CSV[3]":"d_{4}",
    "Evt_blr_ETH":"BLR",
    "Evt_Deta_JetsAverage":"#Delta#eta^{avg}_{j,j}",
    "Evt_Dr_MinDeltaRLeptonJet":"#DeltaR^{min}_{lep,j}",
    "Evt_TaggedJet_MaxDeta_Jets":"#Delta#eta^{max}_{j,b}",
    "Evt_M_TaggedJetsClosestTo125":"m^{closest to 125}_{b,b}",
    "LooseLepton_Pt[0]":"pt(loose lepton, highest in pt)",
    "Evt_Dr_JetsAverage":"#DeltaR^{avg}_{j,j}",
    "Evt_CSV_Average_Tagged":"d^{avg}_{b}",
    "Evt_CSV_Average":"d^{avg}_{j}",
    "Evt_Dr_MinDeltaRLeptonTaggedJet":"#DeltaR^{min}_{lep,b}",
    "Evt_Deta_TaggedJetsAverage":"#Delta#eta^{avg}_{b,b}",
    "Evt_blr_ETH_transformed":"BLR^{trans}",
    "Evt_CSV_Min_Tagged":"d^{min}_{b}",
    "Evt_M_JetsAverage":"m^{avg}_{j}",
    "Evt_CSV_Min":"d^{min}_{j}",
    "Evt_M_MinDeltaRTaggedJets":"m^{min#DeltaR}_{b,b}",
    "Evt_Dr_TaggedJetsAverage":"#DeltaR^{avg}_{b,b}",
    "Evt_M_TaggedJetsAverage":"m^{avg}_{b}",
    "BDT_common5_input_h1":"H_{1}",
    "BDT_common5_input_h0":"H_{0}",
    "BDT_common5_input_h3":"H_{3}",
    "BDT_common5_input_h2":"H_{2}",
    "Evt_M_MinDeltaRLeptonJet":"m^{min#DeltaR}_{lep, j}",
    "Jet_Eta[0]":"#eta(jet 1)",
    "Jet_Eta[1]":"#eta(jet 2)",
    "Jet_Eta[2]":"#eta(jet 3)",
    "Jet_Eta[3]":"#eta(jet 4)",
    "Jet_Pt[0]":"pt(jet 1)",
    "Jet_Pt[1]":"pt(jet 2)",
    "Jet_Pt[2]":"pt(jet 3)",
    "Jet_Pt[3]":"pt(jet 4)",
    "N_Jets":"N_{Jets}",
    "Weight_XS":"Weight_XS",
    "Weight_CSV":"Weight_CSV"
    }

class Sample:
    def __init__(self, sampleName, sampleNameColor, sampleFile, signalSample = False, dataSample = False, ttHSample = False):
        self.sampleName = sampleName
        self.sampleColor= sampleNameColor
        self.sampleFile = sampleFile
        self.isSignal   = signalSample
        self.isData     = dataSample
        self.isttH      = ttHSample
        
        self.load()
        self.cut_data   = {}

    def load(self):
        with pandas.HDFStore(self.sampleFile, mode = "r") as store:
            self.data = store.select("data")

    def cutData(self, cut, variables, lumi_scale):
        # cut events according to JT category
        category_cut = JTcut.getJTstring(cut)

        # only save variables that are needed
        if self.isSignal or self.isttH:
            self.cut_data[cut] = self.data.query(category_cut)[list(set(variables+["Weight_XS", "Weight_GEN_nom", "Weight_CSV","Weight_pu69p2","Weight_ElectronSFGFS","Weight_ElectronSFID","Weight_ElectronSFTrigger","Weight_MuonSFID","Weight_MuonSFIso","Weight_MuonSFTrigger"]))]
        elif self.isData:
            self.cut_data[cut] = self.data.query(category_cut)[list(set(variables+["Weight_XS","Weight_CSV"]))]
	else:
	    self.cut_data[cut] = self.data.query(category_cut)[list(set(variables+["Weight_XS", "Weight_GEN_nom", "Weight_CSV","Weight_pu69p2","Weight_ElectronSFGFS","Weight_ElectronSFID","Weight_ElectronSFTrigger","Weight_MuonSFID","Weight_MuonSFIso","Weight_MuonSFTrigger","Weight_LHA_306000_nominal"]))]

        # add weight entry for scaling
        if self.isSignal:
            self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_GEN_nom * x.Weight_CSV * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale*2)
            print("multiplies by 2")
        elif self.isttH:
            self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_GEN_nom * x.Weight_CSV * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale)
        elif self.isData:
            self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS*x.Weight_CSV)
	else:
	    self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi_scale)

        

class variablePlotter:
    def __init__(self, onlyrootfiles, root_output, output_dir, variable_set, add_vars, plotOptions = {}):
        self.output_dir     = output_dir
        self.variable_set   = variable_set
        self.add_vars       = list(add_vars)        
        self.root_output    = root_output
        self.onlyrootfiles  = onlyrootfiles

        self.samples        = {}
        self.categories     = []

        # handle options
        defaultOptions = {
            "ratio":        False,
            "ratioTitle":   None,
            "logscale":     False,
            "scaleSignal":  -1}
        for key in plotOptions:
            defaultOptions[key] = plotOptions[key]
        self.options = defaultOptions
        

    def addSample(self, **kwargs):
        print("adding sample: "+str(kwargs["sampleName"]))
        self.samples[kwargs["sampleName"]] = Sample(**kwargs)
        print("sample FILE is:   ", str(kwargs["sampleFile"]))

    def addCategory(self, category):
        print("adding category: {}".format(category))
        self.categories.append(category)


    def plot(self):
        # loop over categories and get list of variables
        for cat in self.categories:
            print("starting with category {}".format(cat))

            cat_dir = self.output_dir+"/"+cat+"/"
            if not os.path.exists(cat_dir):
                os.makedirs(cat_dir)

            # load list of variables from variable set
            variables = self.variable_set.variables[cat] + self.add_vars

            # filter events according to JT category
            for key in self.samples:
                self.samples[key].cutData(cat, variables, self.options["lumiScale"])

            #setup a root file
            f = ROOT.TFile(self.root_output,"RECREATE")
            RDirectory=[]

            # loop over all variables and perform plot
            for i,variable in enumerate(variables):
                print("plotting variable: {}".format(variable))

                # generate plot output name
                plot_name = cat_dir + "/{}.pdf".format(variable)
                plot_name = plot_name.replace("[","_").replace("]","")
               
                #adding folders in the root file 
                RDirectory.append(f.mkdir(str(variable)))
                    
                # generate plot
                self.histVariable(
                    f             = f,
                    RDirectory    = RDirectory,
                    i             = i,
                    variable      = variable,
                    plot_name     = plot_name,
                    cat           = cat)


    def histVariable(self, f, RDirectory, i, variable, plot_name, cat):
        # get number of bins and binrange from config filea
        bins = binning.getNbins(variable)
        bin_range = binning.getBinrange(variable)

        # check if bin_range was found
        if not bin_range:
            maxValue = -999
            minValue = 999
            for key in self.samples:
                maxValue = max(maxValue, max(self.samples[key].cut_data[cat][variable].values))
                minValue = min(minValue, min(self.samples[key].cut_data[cat][variable].values))
            config_string = "variables[\""+variable+"\"]\t\t\t= Variable(bin_range = [{},{}])\n".format(minValue, maxValue)
            with open("new_variable_configs.txt", "a") as f:
                f.write(config_string)
            bin_range = [minValue, maxValue]

        bkgHists = []
        bkgLabels = []
        weightIntegral = 0

        # loop over bachgrounds and fill hists
        for key in self.samples:
            sample = self.samples[key]
            if sample.isSignal: continue
            if sample.isData: continue

            # get weights
            weights = sample.cut_data[cat]["weight"].values
            weightIntegral += sum(weights)

            # setup histogram
            hist = setup.setupHistogram(
                values      = sample.cut_data[cat][variable].values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = setup.GetPlotColor(sample.sampleColor),
                xtitle      = sample.sampleName,
                ytitle      = setup.GetyTitle(),
                filled      = True)

            RDirectory[i].cd()
            hist.Write()
            f.cd()
            bkgHists.append(hist)
            bkgLabels.append(sample.sampleName)
            hist.SetDirectory(0)

        sigHists = []
        sigLabels = []
        sigScales = []
        
        # loop over signals and fill hists
        for key in self.samples:
            sample = self.samples[key]
            if not sample.isSignal: continue

            # get weights
            weights = sample.cut_data[cat]["weight"].values

            # determine scale factor
            if self.options["scaleSignal"] == -1:
                scaleFactor = weightIntegral/(sum(weights)+1e-9)
            else:
                scaleFactor = float(self.options["scaleSignal"])

            print("weight integral is: ", weightIntegral)
            print("ttHH integral is: ", sum(weights))
            # setup histogram
            hist = setup.setupHistogram(
                values      = sample.cut_data[cat][variable].values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = setup.GetPlotColor(sample.sampleColor),
                xtitle      = sample.sampleName,
                ytitle      = setup.GetyTitle(),
                filled      = False)

            RDirectory[i].cd()
            hist.Write()
            f.cd()
            hist.Scale(scaleFactor)
            sigHists.append(hist)
            sigLabels.append(sample.sampleName)
            sigScales.append(scaleFactor)

        datHists = []
        datLabels = []

        # loop over DATA and fill hists
        for key in self.samples:
            sample = self.samples[key]
            if not sample.isData: continue

            # get weights
            weights = sample.cut_data[cat]["weight"].values

            # setup histogram
            hist = setup.setupHistogram(
                values      = sample.cut_data[cat][variable].values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = ROOT.kBlue,
                xtitle      = sample.sampleName,
                ytitle      = setup.GetyTitle(),
                filled      = False)

            RDirectory[i].cd()
            hist.Write()
            f.cd()
            datHists.append(hist)
            datLabels.append(sample.sampleName)

        if not self.onlyrootfiles:
            # init canvas
            canvas = setup.drawHistsOnCanvas(
                sigHists, bkgHists, datHists, self.options,   
                canvasName = dict_variable[variable])
            print("variable IS LOOK======================================= ",dict_variable[variable])
            # setup legend
            legend = setup.getLegend()
            # add signal entries
            for iSig in range(len(sigHists)):
                legend.AddEntry(sigHists[iSig], sigLabels[iSig]+" x {:4.0f}".format(sigScales[iSig]), "L")
            # add background entries
            for iBkg in range(len(bkgHists)):
                legend.AddEntry(bkgHists[iBkg], bkgLabels[iBkg], "F")
            # add DATA entries
            for iDat in range(len(datHists)):
                legend.AddEntry(datHists[iDat], datLabels[iDat], "P")

            # draw legend
            legend.Draw("same")

            # add lumi and category to plot
            setup.printLumi(canvas, lumi = self.options["lumiScale"], ratio = self.options["ratio"])
            setup.printCategoryLabel(canvas, JTcut.getJTlabel(cat), ratio = self.options["ratio"])

            # save canvas
            setup.saveCanvas(canvas, plot_name)




                        


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
"Weight_scale_variation_muR_1p0_muF_2p0":"CMS_ttH_scaleMuFUp","Weight_scale_variation_muR_1p0_muF_0p5":"CMS_ttH_scaleMuFDown",\
"lumi_13TeVUp":"lumi_13TeVUp",\
"lumi_13TeVDown":"lumi_13TeVDown",\
"QCDscale_ttHHUp":"QCDscale_ttHHUp",\
"QCDscale_ttHHDown":"QCDscale_ttHHDown",\
"QCDscale_ttbarUp":"QCDscale_ttbarUp",\
"QCDscale_ttbarDown":"QCDscale_ttbarDown",\
"QCDscale_singletUp":"QCDscale_singletUp",\
"QCDscale_singletDown":"QCDscale_singletDown",\
"pdf_ggUp":"pdf_ggUp",\
"pdf_ggDown":"pdf_ggDown",\
"pdf_qgUp":"pdf_qgUp",\
"pdf_qgDown":"pdf_qgDown",\
"pdf_Higgs_ttHHUp":"pdf_Higgs_ttHHUp",\
"pdf_Higgs_ttHHDown":"pdf_Higgs_ttHHDown",\
"QCDscale_ttHbbUp":"QCDscale_ttHbbUp",\
"QCDscale_ttHbbDown":"QCDscale_ttHbbDown",\
"pdf_Higgs_ttHbbUp":"pdf_Higgs_ttHbbUp",\
"pdf_Higgs_ttHbbDown":"pdf_Higgs_ttHbbDown",\
"CMS_ttHbb_bgnorm_ttbarPlus2B_2017Up":"CMS_ttHbb_bgnorm_ttbarPlus2B_2017Up",\
"CMS_ttHbb_bgnorm_ttbarPlus2B_2017Down":"CMS_ttHbb_bgnorm_ttbarPlus2B_2017Down",\
"CMS_ttHbb_bgnorm_ttbarPlusBBbar_2017Up":"CMS_ttHbb_bgnorm_ttbarPlusBBbar_2017Up",\
"CMS_ttHbb_bgnorm_ttbarPlusBBbar_2017Down":"CMS_ttHbb_bgnorm_ttbarPlusBBbar_2017Down",\
"CMS_ttHbb_bgnorm_ttbarPlusB_2017Up":"CMS_ttHbb_bgnorm_ttbarPlusB_2017Up",\
"CMS_ttHbb_bgnorm_ttbarPlusB_2017Down":"CMS_ttHbb_bgnorm_ttbarPlusB_2017Down",\
"CMS_ttHbb_bgnorm_ttbarPlusCCbar_2017Up":"CMS_ttHbb_bgnorm_ttbarPlusCCbar_2017Up",\
"CMS_ttHbb_bgnorm_ttbarPlusCCbar_2017Down":"CMS_ttHbb_bgnorm_ttbarPlusCCbar_2017Down"\
}

onlyttbarlist=("GenWeight_8","GenWeight_6","GenWeight_9","GenWeight_7"\
                          ,"Weight_LHA_306000_up","Weight_LHA_306000_down"\
                          ,"Weight_scale_variation_muR_2p0_muF_1p0","Weight_scale_variation_muR_0p5_muF_1p0"\
                          ,"Weight_scale_variation_muR_1p0_muF_2p0","Weight_scale_variation_muR_1p0_muF_0p5"\
                          ) 
class Sample:
    def __init__(self, sampleName, sampleNameColor, sampleFile, inputsyst, signalSample = False, dataSample = False, ttHSample = False):
        self.sampleName = sampleName
        self.sampleColor= sampleNameColor
        self.sampleFile = sampleFile
        self.isSignal   = signalSample
        self.isData     = dataSample
        self.isttH      = ttHSample
        self.inputsyst  = inputsyst
        #print("lets see if it loaded correctly. The inputsyst is:    ", self.inputsyst)
        self.load()
        self.cut_data   = {}

    def load(self):
        with pandas.HDFStore(self.sampleFile, mode = "r") as store:
            self.data = store.select("data")

    def cutData(self, cut, variables, rate, rate_value, lumi_scale):
        # cut events according to JT category
        print("rate and rate_value is: ", rate , rate_value)
        print("value of input syst is: ", self.inputsyst)
        if rate: self.inputsyst = "1"
        category_cut = JTcut.getJTstring(cut)
        weight_set_ttH = ["Weight_XS", "Weight_GEN_nom", "Weight_CSV","Weight_pu69p2","Weight_ElectronSFGFS","Weight_ElectronSFID","Weight_ElectronSFTrigger","Weight_MuonSFID","Weight_MuonSFIso","Weight_MuonSFTrigger"]
        weight_set_ttbar = ["Weight_XS", "Weight_GEN_nom", "Weight_CSV","Weight_pu69p2","Weight_ElectronSFGFS","Weight_ElectronSFID","Weight_ElectronSFTrigger","Weight_MuonSFID","Weight_MuonSFIso","Weight_MuonSFTrigger","Weight_LHA_306000_nominal"]
        # only save variables that are needed
        if self.isSignal or self.isttH:
            if self.inputsyst not in "1" and self.inputsyst not in onlyttbarlist: weight_set_ttH += [self.inputsyst]
            self.cut_data[cut] = self.data.query(category_cut)[list(set(variables+weight_set_ttH))]
        elif self.isData:
            self.cut_data[cut] = self.data.query(category_cut)[list(set(variables+["Weight_XS","Weight_CSV"]))]
        else:
            if self.inputsyst not in "1": weight_set_ttbar += [self.inputsyst]
            self.cut_data[cut] = self.data.query(category_cut)[list(set(variables+weight_set_ttbar))]
        print("the value of inputsyst here is: ", self.inputsyst)
        if rate: self.inputsyst=rate_value
        print("see if input syst changed: ", self.inputsyst)
        extrafactor={True:2,False:1}
        # add weight entry for scaling
        if (self.isSignal or self.isttH) and self.inputsyst not in onlyttbarlist:
	    if "Weight_pu69p2" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale * extrafactor[self.isSignal])
            elif "Weight_ElectronSFGFS" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
	            * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale * extrafactor[self.isSignal])
            elif "Weight_ElectronSFID" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFTrigger\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale * extrafactor[self.isSignal])
            elif "Weight_ElectronSFTrigger" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale * extrafactor[self.isSignal])
            elif "Weight_MuonSFID" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * lumi_scale * extrafactor[self.isSignal])
            elif "Weight_MuonSFIso" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFTrigger * lumi_scale * extrafactor[self.isSignal])
            elif "Weight_MuonSFTrigger" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * lumi_scale * extrafactor[self.isSignal])
            else:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger\
                * lumi_scale * extrafactor[self.isSignal])
            #print("extra factor is", extrafactor[self.isSignal])
        elif self.isData:
            self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS*x.Weight_CSV)
        elif not self.isSignal and not self.isttH:
            if "Weight_pu69p2" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi_scale)
            elif "Weight_ElectronSFGFS" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFID * x.Weight_ElectronSFTrigger\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal *  lumi_scale)
            elif "Weight_ElectronSFID" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFTrigger\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi_scale)
            elif "Weight_ElectronSFTrigger" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger * x.Weight_LHA_306000_nominal * lumi_scale)
            elif "Weight_MuonSFID" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger\
                * x.Weight_LHA_306000_nominal * lumi_scale)
            elif "Weight_MuonSFIso" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFTrigger\
                * x.Weight_LHA_306000_nominal * lumi_scale)
            elif "Weight_MuonSFTrigger" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso\
                * x.Weight_LHA_306000_nominal * lumi_scale)
            elif "Weight_LHA_306000" in self.inputsyst:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * lumi_scale)
            else:
                self.cut_data[cut] = self.cut_data[cut].assign(weight = lambda x: x.Weight_XS * x.Weight_CSV * x.Weight_GEN_nom\
                * x.eval(self.inputsyst) * x.Weight_pu69p2 * x.Weight_ElectronSFGFS * x.Weight_ElectronSFID\
                * x.Weight_ElectronSFTrigger * x.Weight_MuonSFID * x.Weight_MuonSFIso * x.Weight_MuonSFTrigger\
                * x.Weight_LHA_306000_nominal * lumi_scale)


class variablePlotter:
    def __init__(self, rate, sampleFlag, rate_value, inputsyst, onlyrootfiles, root_output, output_dir, variable_set, add_vars, plotOptions = {}):
        self.output_dir     = output_dir
        self.variable_set   = variable_set
        self.add_vars       = list(add_vars)        
        self.root_output    = root_output
        self.onlyrootfiles  = onlyrootfiles
        self.inputsyst      = inputsyst
        self.rate           = rate
        self.sampleFlag     = sampleFlag
        self.rate_value     = rate_value
        #print(self.inputsyst)
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
        #print("sample FILE is:   ", str(kwargs["sampleFile"]))

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
                self.samples[key].cutData(cat, variables, self.rate, self.rate_value, self.options["lumiScale"])
                #print("sample is: ", key)

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
            if self.rate:
              if self.sampleFlag not in ("all","ttbar"):
                if (self.sampleFlag+"_"+self.inputsyst) != key: continue
              elif self.sampleFlag in "ttbar" and sample.isttH: continue
            if sample.isSignal: continue
            if sample.isData: continue
            if sample.isttH and self.inputsyst in onlyttbarlist: continue
            # get weights
            weights = sample.cut_data[cat]["weight"].values
            weightIntegral += sum(weights)
            #print("backgrounds are:   ",sample.sampleName)
            # setup histogram
            if self.inputsyst == "1":
                htitle = sample.sampleName
            else:
                htitle = sample.sampleColor + "_" + dict_syst[self.inputsyst]
            hist = setup.setupHistogram(
                values      = sample.cut_data[cat][variable].values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = setup.GetPlotColor(sample.sampleColor),
                xtitle      = htitle,
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
            if self.inputsyst in onlyttbarlist: continue
            if self.rate:
              if self.sampleFlag not in ("all"):
                if (self.sampleFlag+"_"+self.inputsyst) != key: continue

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
            if self.inputsyst == "1":
                htitle = sample.sampleName
            else:
                htitle = sample.sampleColor + "_" + dict_syst[self.inputsyst]
            hist = setup.setupHistogram(
                values      = sample.cut_data[cat][variable].values,
                weights     = weights,
                nbins       = bins,
                bin_range   = bin_range,
                color       = setup.GetPlotColor(sample.sampleColor),
                xtitle      = htitle,
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
                color       = ROOT.kBlack,
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




                        


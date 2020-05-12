import os
import sys
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(os.path.dirname(filedir))
sys.path.append(basedir)

import root2pandas
import variable_sets.ttHH_allVariables as variable_set



# define a base event selection which is applied for all Samples
base_selection = "\
( \
(N_Jets >= 4 and N_BTagsM >= 3 and Evt_Pt_MET > 20. and Weight_GEN_nom > 0.) \
and (\
(N_LooseMuons == 0 and N_TightElectrons == 1 and (Triggered_HLT_Ele35_WPTight_Gsf_vX == 1 or Triggered_HLT_Ele28_eta2p1_WPTight_Gsf_HT150_vX == 1)) \
or \
(N_LooseElectrons == 0 and N_TightMuons == 1 and Muon_Pt > 29. and (Triggered_HLT_IsoMu24_eta2p1_vX == 1 or Triggered_HLT_IsoMu27_vX == 1)) \
) \
)"

ttbar_selection = "(\
abs(Weight_scale_variation_muR_0p5_muF_0p5) <= 100 and \
abs(Weight_scale_variation_muR_0p5_muF_1p0) <= 100 and \
abs(Weight_scale_variation_muR_0p5_muF_2p0) <= 100 and \
abs(Weight_scale_variation_muR_1p0_muF_0p5) <= 100 and \
abs(Weight_scale_variation_muR_1p0_muF_1p0) <= 100 and \
abs(Weight_scale_variation_muR_1p0_muF_2p0) <= 100 and \
abs(Weight_scale_variation_muR_2p0_muF_0p5) <= 100 and \
abs(Weight_scale_variation_muR_2p0_muF_1p0) <= 100 and \
abs(Weight_scale_variation_muR_2p0_muF_2p0) <= 100 \
)"

#definitions
ttbarJERup_categories = root2pandas.EventCategories()
ttbarJERdown_categories = root2pandas.EventCategories()
ttbarJESup_categories = root2pandas.EventCategories()
ttbarJESdown_categories = root2pandas.EventCategories()
ttbarJESAbsoluteStatUp_categories = root2pandas.EventCategories()
ttbarJESAbsoluteStatDown_categories = root2pandas.EventCategories()
ttbarJESAbsoluteScaleUp_categories = root2pandas.EventCategories()
ttbarJESAbsoluteScaleDown_categories = root2pandas.EventCategories()
ttbarJESAbsoluteMPFBiasUp_categories = root2pandas.EventCategories()
ttbarJESAbsoluteMPFBiasDown_categories = root2pandas.EventCategories()
ttbarJESFragmentationUp_categories = root2pandas.EventCategories()
ttbarJESFragmentationDown_categories = root2pandas.EventCategories()
ttbarJESSinglePionECALUp_categories = root2pandas.EventCategories()
ttbarJESSinglePionECALDown_categories = root2pandas.EventCategories()
ttbarJESSinglePionHCALUp_categories = root2pandas.EventCategories()
ttbarJESSinglePionHCALDown_categories = root2pandas.EventCategories()
ttbarJESFlavorQCDUp_categories = root2pandas.EventCategories()
ttbarJESFlavorQCDDown_categories = root2pandas.EventCategories()
ttbarJESTimePtEtaUp_categories = root2pandas.EventCategories()
ttbarJESTimePtEtaDown_categories = root2pandas.EventCategories()
ttbarJESRelativeJEREC1Up_categories = root2pandas.EventCategories()
ttbarJESRelativeJEREC1Down_categories = root2pandas.EventCategories()
ttbarJESRelativePtBBUp_categories = root2pandas.EventCategories()
ttbarJESRelativePtBBDown_categories = root2pandas.EventCategories()
ttbarJESRelativePtEC1Up_categories = root2pandas.EventCategories()
ttbarJESRelativePtEC1Down_categories = root2pandas.EventCategories()
ttbarJESRelativeBalUp_categories = root2pandas.EventCategories()
ttbarJESRelativeBalDown_categories = root2pandas.EventCategories()
ttbarJESRelativeFSRUp_categories = root2pandas.EventCategories()
ttbarJESRelativeFSRDown_categories = root2pandas.EventCategories()
ttbarJESRelativeStatFSRUp_categories = root2pandas.EventCategories()
ttbarJESRelativeStatFSRDown_categories = root2pandas.EventCategories()
ttbarJESRelativeStatECUp_categories = root2pandas.EventCategories()
ttbarJESRelativeStatECDown_categories = root2pandas.EventCategories()
ttbarJESPileUpDataMCUp_categories = root2pandas.EventCategories()
ttbarJESPileUpDataMCDown_categories = root2pandas.EventCategories()
ttbarJESPileUpPtRefUp_categories = root2pandas.EventCategories()
ttbarJESPileUpPtRefDown_categories = root2pandas.EventCategories()
ttbarJESPileUpPtBBUp_categories = root2pandas.EventCategories()
ttbarJESPileUpPtBBDown_categories = root2pandas.EventCategories()
ttbarJESPileUpPtEC1Up_categories = root2pandas.EventCategories()
ttbarJESPileUpPtEC1Down_categories = root2pandas.EventCategories()

#dictionary
#systematics=["JESAbsoluteStatUp","JESAbsoluteStatDown","JESAbsoluteScaleUp","JESAbsoluteScaleDown","JESAbsoluteMPFBiasUp","JESAbsoluteMPFBiasDown","JESFragmentationUp","JESFragmentationDown","JESSinglePionECALUp","JESSinglePionECALDown","JESSinglePionHCALUp","JESSinglePionHCALDown","JESFlavorQCDUp","JESFlavorQCDDown","JESTimePtEtaUp","JESTimePtEtaDown","JESRelativePtBBUp","JESRelativePtBBDown","JESRelativePtEC1Up","JESRelativePtEC1Down","JESRelativeBalUp","JESRelativeBalDown","JESRelativeFSRUp","JESRelativeFSRDown","JESRelativeStatFSRUp","JESRelativeStatFSRDown","JESRelativeStatECUp","JESRelativeStatECDown","JESPileUpPtRefUp","JESPileUpPtRefDown","JESPileUpPtBBUp","JESPileUpPtBBDown","JESPileUpPtEC1Up","JESPileUpPtEC1Down"]
#systematics2=["JESAbsoluteStatup","JESAbsoluteStatdown","JESAbsoluteScaleup","JESAbsoluteScaledown","JESAbsoluteMPFBiasup","JESAbsoluteMPFBiasdown","JESFragmentationup","JESFragmentationdown","JESSinglePionECALup","JESSinglePionECALdown","JESSinglePionHCALup","JESSinglePionHCALdown","JESFlavorQCDup","JESFlavorQCDdown","JESTimePtEtaup","JESTimePtEtadown","JESRelativePtBBup","JESRelativePtBBdown","JESRelativePtEC1up","JESRelativePtEC1down","JESRelativeBalup","JESRelativeBaldown","JESRelativeFSRup","JESRelativeFSRdown","JESRelativeStatFSRup","JESRelativeStatFSRdown","JESRelativeStatECup","JESRelativeStatECdown","JESPileUpPtRefup","JESPileUpPtRefdown","JESPileUpPtBBup","JESPileUpPtBBdown","JESPileUpPtEC1up","JESPileUpPtEC1down"]
systematics=["JESUp","JESDown","JERUp","JERDown"]
systematics2=["JESup","JESdown","JERup","JERdown"]


#dict definition
dict_syst_ttbar={"JERUp": ttbarJERup_categories, "JERDown":ttbarJERdown_categories, "JESUp": ttbarJESup_categories, "JESDown":ttbarJESdown_categories,"JESAbsoluteStatUp":ttbarJESAbsoluteStatUp_categories,"JESAbsoluteStatDown":ttbarJESAbsoluteStatDown_categories,"JESAbsoluteScaleUp":ttbarJESAbsoluteScaleUp_categories,"JESAbsoluteScaleDown":ttbarJESAbsoluteScaleDown_categories,"JESAbsoluteMPFBiasUp":ttbarJESAbsoluteMPFBiasUp_categories,"JESAbsoluteMPFBiasDown":ttbarJESAbsoluteMPFBiasDown_categories,"JESFragmentationUp":ttbarJESFragmentationUp_categories,"JESFragmentationDown":ttbarJESFragmentationDown_categories,"JESSinglePionECALUp":ttbarJESSinglePionECALUp_categories,"JESSinglePionECALDown":ttbarJESSinglePionECALDown_categories,"JESSinglePionHCALUp":ttbarJESSinglePionHCALUp_categories,"JESSinglePionHCALDown":ttbarJESSinglePionHCALDown_categories,"JESFlavorQCDUp":ttbarJESFlavorQCDUp_categories,"JESFlavorQCDDown":ttbarJESFlavorQCDDown_categories,"JESTimePtEtaUp":ttbarJESTimePtEtaUp_categories,"JESTimePtEtaDown":ttbarJESTimePtEtaDown_categories,"JESRelativeJEREC1Up":ttbarJESRelativeJEREC1Up_categories,"JESRelativeJEREC1Down":ttbarJESRelativeJEREC1Down_categories,"JESRelativePtBBUp":ttbarJESRelativePtBBUp_categories,"JESRelativePtBBDown":ttbarJESRelativePtBBDown_categories,"JESRelativePtEC1Up":ttbarJESRelativePtEC1Up_categories,"JESRelativePtEC1Down":ttbarJESRelativePtEC1Down_categories,"JESRelativeBalUp":ttbarJESRelativeBalUp_categories,"JESRelativeBalDown":ttbarJESRelativeBalDown_categories,"JESRelativeFSRUp":ttbarJESRelativeFSRUp_categories,"JESRelativeFSRDown":ttbarJESRelativeFSRDown_categories,"JESRelativeStatFSRUp":ttbarJESRelativeStatFSRUp_categories,"JESRelativeStatFSRDown":ttbarJESRelativeStatFSRDown_categories,"JESRelativeStatECUp":ttbarJESRelativeStatECUp_categories,"JESRelativeStatECDown":ttbarJESRelativeStatECDown_categories,"JESPileUpDataMCUp":ttbarJESPileUpDataMCUp_categories,"JESPileUpDataMCDown":ttbarJESPileUpDataMCDown_categories,"JESPileUpPtRefUp":ttbarJESPileUpPtRefUp_categories,"JESPileUpPtRefDown":ttbarJESPileUpPtRefDown_categories,"JESPileUpPtBBUp":ttbarJESPileUpPtBBUp_categories,"JESPileUpPtBBDown":ttbarJESPileUpPtBBDown_categories,"JESPileUpPtEC1Up":ttbarJESPileUpPtEC1Up_categories,"JESPileUpPtEC1Down":ttbarJESPileUpPtEC1Down_categories} 

# define output classes
#for ttbar
#nominal:
ttbar_categories = root2pandas.EventCategories()
ttbar_categories.addCategory("ttbb", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("tt2b", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttb",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttlf", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttcc", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

#systematics:
for systs in systematics:
   dict_syst_ttbar[systs].addCategory("ttbb_"+systs, selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
   dict_syst_ttbar[systs].addCategory("tt2b_"+systs, selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
   dict_syst_ttbar[systs].addCategory("ttb_"+systs,  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
   dict_syst_ttbar[systs].addCategory("ttlf_"+systs, selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
   dict_syst_ttbar[systs].addCategory("ttcc_"+systs, selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

#some definitions
outdirttbar="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_ttbar_syst/"
outdir=outdirttbar
if not os.path.exists(outdir):
    os.makedirs(outdir)
# initialize dataset class
dataset = root2pandas.Dataset(
    outputdir   = outdir,
    naming      = "dnn",
    addCNNmap   = False,
    addMEM      = False)

# add base event selection
dataset.addBaseSelection(base_selection)

# add samples to dataset
for ii, systs in enumerate(systematics2):
  dataset.addSample(
      sampleName  = "TTToSL"+str(systs),
      ntuples     = "/eos/user/l/lprado/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/*"+str(systs)+"*.root",
      categories  = dict_syst_ttbar[str(systematics[ii])],
      selections  = None)

  dataset.addSample(
      sampleName  = "TTToHad"+str(systs),
      ntuples     = "/eos/user/l/lprado/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/*"+str(systs)+"*.root",
      categories  = dict_syst_ttbar[str(systematics[ii])],
      selections  = None)

  dataset.addSample(
      sampleName  = "TTToLep"+str(systs),
      ntuples     = "/eos/user/l/lprado/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/*"+str(systs)+"*.root",
      categories  = dict_syst_ttbar[str(systematics[ii])],
      selections  = None)
	  
# initialize variable list 
dataset.addVariables(variable_set.all_variables)

# define an additional variable list
additional_variables = [
    "N_Jets",
    "N_BTagsM",
    "N_BTagsL",
    "Weight_XS",
    "Weight_CSV",
    "Weight_GEN_nom",
    "Evt_ID", 
    "Evt_Run", 
    "Evt_Lumi",
#    "Weight_CSVCErr1down",
#    "Weight_CSVCErr1up",
#    "Weight_CSVCErr2down",
#    "Weight_CSVCErr2up",
#    "Weight_CSVHFdown",
#    "Weight_CSVHFup",
#    "Weight_CSVHFStats1down",
#    "Weight_CSVHFStats1up",
#    "Weight_CSVHFStats2down",
#    "Weight_CSVHFStats2up",
#    "Weight_CSVLFdown",
#    "Weight_CSVLFup",
#    "Weight_CSVLFStats1down",
#    "Weight_CSVLFStats1up",
#    "Weight_CSVLFStats2down",
#    "Weight_CSVLFStats2up",
    "Weight_pu69p2",
    "Weight_pu69p2Down",
    "Weight_pu69p2Up",
    "Weight_ElectronSFGFS",
    "Weight_ElectronSFGFS_Down",
    "Weight_ElectronSFGFS_Up",
    "Weight_ElectronSFID",
    "Weight_ElectronSFID_Down",
    "Weight_ElectronSFID_Up",
    "Weight_ElectronSFTrigger",
    "Weight_ElectronSFTrigger_Down",
    "Weight_ElectronSFTrigger_Up",
    "Weight_MuonSFID",
    "Weight_MuonSFID_Down",
    "Weight_MuonSFID_Up",
    "Weight_MuonSFIso",
    "Weight_MuonSFIso_Up",
    "Weight_MuonSFIso_Down",
    "Weight_MuonSFTrigger",
    "Weight_MuonSFTrigger_Down",
    "Weight_MuonSFTrigger_Up",
    "GenWeight_8",
    "GenWeight_6",
    "GenWeight_9",
    "GenWeight_7",
    "Weight_LHA_306000_nominal",
    "Weight_LHA_306000_up",
    "Weight_LHA_306000_down",
    "Weight_scale_variation_muR_2p0_muF_1p0",
    "Weight_scale_variation_muR_0p5_muF_1p0",
    "Weight_scale_variation_muR_1p0_muF_2p0",
    "Weight_scale_variation_muR_1p0_muF_0p5",
]

# add these variables to the variable list
dataset.addVariables(additional_variables)

# run the preprocessing
dataset.runPreprocessing()

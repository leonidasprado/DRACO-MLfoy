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

#definitions:
ttHbbJERup_categories = root2pandas.EventCategories()
ttHbbJERdown_categories = root2pandas.EventCategories()
ttHbbJESup_categories = root2pandas.EventCategories()
ttHbbJESdown_categories = root2pandas.EventCategories()
ttHbbJESAbsoluteStatUp_categories = root2pandas.EventCategories()
ttHbbJESAbsoluteStatDown_categories = root2pandas.EventCategories()
ttHbbJESAbsoluteScaleUp_categories = root2pandas.EventCategories()
ttHbbJESAbsoluteScaleDown_categories = root2pandas.EventCategories()
ttHbbJESAbsoluteMPFBiasUp_categories = root2pandas.EventCategories()
ttHbbJESAbsoluteMPFBiasDown_categories = root2pandas.EventCategories()
ttHbbJESFragmentationUp_categories = root2pandas.EventCategories()
ttHbbJESFragmentationDown_categories = root2pandas.EventCategories()
ttHbbJESSinglePionECALUp_categories = root2pandas.EventCategories()
ttHbbJESSinglePionECALDown_categories = root2pandas.EventCategories()
ttHbbJESSinglePionHCALUp_categories = root2pandas.EventCategories()
ttHbbJESSinglePionHCALDown_categories = root2pandas.EventCategories()
ttHbbJESFlavorQCDUp_categories = root2pandas.EventCategories()
ttHbbJESFlavorQCDDown_categories = root2pandas.EventCategories()
ttHbbJESTimePtEtaUp_categories = root2pandas.EventCategories()
ttHbbJESTimePtEtaDown_categories = root2pandas.EventCategories()
ttHbbJESRelativeJEREC1Up_categories = root2pandas.EventCategories()
ttHbbJESRelativeJEREC1Down_categories = root2pandas.EventCategories()
ttHbbJESRelativePtBBUp_categories = root2pandas.EventCategories()
ttHbbJESRelativePtBBDown_categories = root2pandas.EventCategories()
ttHbbJESRelativePtEC1Up_categories = root2pandas.EventCategories()
ttHbbJESRelativePtEC1Down_categories = root2pandas.EventCategories()
ttHbbJESRelativeBalUp_categories = root2pandas.EventCategories()
ttHbbJESRelativeBalDown_categories = root2pandas.EventCategories()
ttHbbJESRelativeFSRUp_categories = root2pandas.EventCategories()
ttHbbJESRelativeFSRDown_categories = root2pandas.EventCategories()
ttHbbJESRelativeStatFSRUp_categories = root2pandas.EventCategories()
ttHbbJESRelativeStatFSRDown_categories = root2pandas.EventCategories()
ttHbbJESRelativeStatECUp_categories = root2pandas.EventCategories()
ttHbbJESRelativeStatECDown_categories = root2pandas.EventCategories()
ttHbbJESPileUpDataMCUp_categories = root2pandas.EventCategories()
ttHbbJESPileUpDataMCDown_categories = root2pandas.EventCategories()
ttHbbJESPileUpPtRefUp_categories = root2pandas.EventCategories()
ttHbbJESPileUpPtRefDown_categories = root2pandas.EventCategories()
ttHbbJESPileUpPtBBUp_categories = root2pandas.EventCategories()
ttHbbJESPileUpPtBBDown_categories = root2pandas.EventCategories()
ttHbbJESPileUpPtEC1Up_categories = root2pandas.EventCategories()
ttHbbJESPileUpPtEC1Down_categories = root2pandas.EventCategories()

#dictionary
#systematics=["JERUp","JERDown","JESUp","JESDown","JESAbsoluteStatUp","JESAbsoluteStatDown","JESAbsoluteScaleUp","JESAbsoluteScaleDown","JESAbsoluteMPFBiasUp","JESAbsoluteMPFBiasDown","JESFragmentationUp","JESFragmentationDown","JESSinglePionECALUp","JESSinglePionECALDown","JESSinglePionHCALUp","JESSinglePionHCALDown","JESFlavorQCDUp","JESFlavorQCDDown","JESTimePtEtaUp","JESTimePtEtaDown","JESRelativeJEREC1Up","JESRelativeJEREC1Down","JESRelativePtBBUp","JESRelativePtBBDown","JESRelativePtEC1Up","JESRelativePtEC1Down","JESRelativeBalUp","JESRelativeBalDown","JESRelativeFSRUp","JESRelativeFSRDown","JESRelativeStatFSRUp","JESRelativeStatFSRDown","JESRelativeStatECUp","JESRelativeStatECDown","JESPileUpDataMCUp","JESPileUpDataMCDown","JESPileUpPtRefUp","JESPileUpPtRefDown","JESPileUpPtBBUp","JESPileUpPtBBDown","JESPileUpPtEC1Up","JESPileUpPtEC1Down"]
#systematics2=["JERup","JERdown","JESup","JESdown","JESAbsoluteStatup","JESAbsoluteStatdown","JESAbsoluteScaleup","JESAbsoluteScaledown","JESAbsoluteMPFBiasup","JESAbsoluteMPFBiasdown","JESFragmentationup","JESFragmentationdown","JESSinglePionECALup","JESSinglePionECALdown","JESSinglePionHCALup","JESSinglePionHCALdown","JESFlavorQCDup","JESFlavorQCDdown","JESTimePtEtaup","JESTimePtEtadown","JESRelativeJEREC1up","JESRelativeJEREC1down","JESRelativePtBBup","JESRelativePtBBdown","JESRelativePtEC1up","JESRelativePtEC1down","JESRelativeBalup","JESRelativeBaldown","JESRelativeFSRup","JESRelativeFSRdown","JESRelativeStatFSRup","JESRelativeStatFSRdown","JESRelativeStatECup","JESRelativeStatECdown","JESPileUpDataMCup","JESPileUpDataMCdown","JESPileUpPtRefup","JESPileUpPtRefdown","JESPileUpPtBBup","JESPileUpPtBBdown","JESPileUpPtEC1up","JESPileUpPtEC1down"]
systematics=["JESUp","JESDown","JERUp","JERDown"]
systematics2=["JESup","JESdown","JERup","JERdown"]

#dict definition
dict_syst_ttHbb={"JERUp": ttHbbJERup_categories, "JERDown":ttHbbJERdown_categories, "JESUp": ttHbbJESup_categories, "JESDown":ttHbbJESdown_categories,"JESAbsoluteStatUp":ttHbbJESAbsoluteStatUp_categories,"JESAbsoluteStatDown":ttHbbJESAbsoluteStatDown_categories,"JESAbsoluteScaleUp":ttHbbJESAbsoluteScaleUp_categories,"JESAbsoluteScaleDown":ttHbbJESAbsoluteScaleDown_categories,"JESAbsoluteMPFBiasUp":ttHbbJESAbsoluteMPFBiasUp_categories,"JESAbsoluteMPFBiasDown":ttHbbJESAbsoluteMPFBiasDown_categories,"JESFragmentationUp":ttHbbJESFragmentationUp_categories,"JESFragmentationDown":ttHbbJESFragmentationDown_categories,"JESSinglePionECALUp":ttHbbJESSinglePionECALUp_categories,"JESSinglePionECALDown":ttHbbJESSinglePionECALDown_categories,"JESSinglePionHCALUp":ttHbbJESSinglePionHCALUp_categories,"JESSinglePionHCALDown":ttHbbJESSinglePionHCALDown_categories,"JESFlavorQCDUp":ttHbbJESFlavorQCDUp_categories,"JESFlavorQCDDown":ttHbbJESFlavorQCDDown_categories,"JESTimePtEtaUp":ttHbbJESTimePtEtaUp_categories,"JESTimePtEtaDown":ttHbbJESTimePtEtaDown_categories,"JESRelativeJEREC1Up":ttHbbJESRelativeJEREC1Up_categories,"JESRelativeJEREC1Down":ttHbbJESRelativeJEREC1Down_categories,"JESRelativePtBBUp":ttHbbJESRelativePtBBUp_categories,"JESRelativePtBBDown":ttHbbJESRelativePtBBDown_categories,"JESRelativePtEC1Up":ttHbbJESRelativePtEC1Up_categories,"JESRelativePtEC1Down":ttHbbJESRelativePtEC1Down_categories,"JESRelativeBalUp":ttHbbJESRelativeBalUp_categories,"JESRelativeBalDown":ttHbbJESRelativeBalDown_categories,"JESRelativeFSRUp":ttHbbJESRelativeFSRUp_categories,"JESRelativeFSRDown":ttHbbJESRelativeFSRDown_categories,"JESRelativeStatFSRUp":ttHbbJESRelativeStatFSRUp_categories,"JESRelativeStatFSRDown":ttHbbJESRelativeStatFSRDown_categories,"JESRelativeStatECUp":ttHbbJESRelativeStatECUp_categories,"JESRelativeStatECDown":ttHbbJESRelativeStatECDown_categories,"JESPileUpDataMCUp":ttHbbJESPileUpDataMCUp_categories,"JESPileUpDataMCDown":ttHbbJESPileUpDataMCDown_categories,"JESPileUpPtRefUp":ttHbbJESPileUpPtRefUp_categories,"JESPileUpPtRefDown":ttHbbJESPileUpPtRefDown_categories,"JESPileUpPtBBUp":ttHbbJESPileUpPtBBUp_categories,"JESPileUpPtBBDown":ttHbbJESPileUpPtBBDown_categories,"JESPileUpPtEC1Up":ttHbbJESPileUpPtEC1Up_categories,"JESPileUpPtEC1Down":ttHbbJESPileUpPtEC1Down_categories}

# define output classes

#for ttH
#norminal
ttHbb_categories = root2pandas.EventCategories()
ttHbb_categories.addCategory("ttHbb", selection = None)
#systematics:
for systs in systematics:
  dict_syst_ttHbb[systs].addCategory("ttHbb"+"_"+systs, selection = None)

#some definitions
outdirttHbb="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_ttHbb_syst/"
outdir=outdirttHbb
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
      sampleName  = "ttHbb"+str(systs),
      ntuples     = "/eos/user/l/lprado/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/*"+str(systs)+"*.root",
      categories  = dict_syst_ttHbb[str(systematics[ii])],
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
    "Weight_MuonSFTrigger_Up"
]

# add these variables to the variable list
dataset.addVariables(additional_variables)

# run the preprocessing
dataset.runPreprocessing()

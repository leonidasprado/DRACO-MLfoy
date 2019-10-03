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
(N_LooseElectrons == 0 and N_TightMuons == 1 and Muon_Pt > 29. and Triggered_HLT_IsoMu27_vX == 1) \
) \
)"


# define other additional selections
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

ttHH_selection = "(Evt_Odd == 0)"
#definitions:
ttHHJERup_categories = root2pandas.EventCategories()
ttHHJERdown_categories = root2pandas.EventCategories()
ttHHJESup_categories = root2pandas.EventCategories()
ttHHJESdown_categories = root2pandas.EventCategories()
ttHHJESAbsoluteStatUp_categories = root2pandas.EventCategories()
ttHHJESAbsoluteStatDown_categories = root2pandas.EventCategories()
ttHHJESAbsoluteScaleUp_categories = root2pandas.EventCategories()
ttHHJESAbsoluteScaleDown_categories = root2pandas.EventCategories()
ttHHJESAbsoluteMPFBiasUp_categories = root2pandas.EventCategories()
ttHHJESAbsoluteMPFBiasDown_categories = root2pandas.EventCategories()
ttHHJESFragmentationUp_categories = root2pandas.EventCategories()
ttHHJESFragmentationDown_categories = root2pandas.EventCategories()
ttHHJESSinglePionECALUp_categories = root2pandas.EventCategories()
ttHHJESSinglePionECALDown_categories = root2pandas.EventCategories()
ttHHJESSinglePionHCALUp_categories = root2pandas.EventCategories()
ttHHJESSinglePionHCALDown_categories = root2pandas.EventCategories()
ttHHJESFlavorQCDUp_categories = root2pandas.EventCategories()
ttHHJESFlavorQCDDown_categories = root2pandas.EventCategories()
ttHHJESTimePtEtaUp_categories = root2pandas.EventCategories()
ttHHJESTimePtEtaDown_categories = root2pandas.EventCategories()
ttHHJESRelativeJEREC1Up_categories = root2pandas.EventCategories()
ttHHJESRelativeJEREC1Down_categories = root2pandas.EventCategories()
ttHHJESRelativePtBBUp_categories = root2pandas.EventCategories()
ttHHJESRelativePtBBDown_categories = root2pandas.EventCategories()
ttHHJESRelativePtEC1Up_categories = root2pandas.EventCategories()
ttHHJESRelativePtEC1Down_categories = root2pandas.EventCategories()
ttHHJESRelativeBalUp_categories = root2pandas.EventCategories()
ttHHJESRelativeBalDown_categories = root2pandas.EventCategories()
ttHHJESRelativeFSRUp_categories = root2pandas.EventCategories()
ttHHJESRelativeFSRDown_categories = root2pandas.EventCategories()
ttHHJESRelativeStatFSRUp_categories = root2pandas.EventCategories()
ttHHJESRelativeStatFSRDown_categories = root2pandas.EventCategories()
ttHHJESRelativeStatECUp_categories = root2pandas.EventCategories()
ttHHJESRelativeStatECDown_categories = root2pandas.EventCategories()
ttHHJESPileUpDataMCUp_categories = root2pandas.EventCategories()
ttHHJESPileUpDataMCDown_categories = root2pandas.EventCategories()
ttHHJESPileUpPtRefUp_categories = root2pandas.EventCategories()
ttHHJESPileUpPtRefDown_categories = root2pandas.EventCategories()
ttHHJESPileUpPtBBUp_categories = root2pandas.EventCategories()
ttHHJESPileUpPtBBDown_categories = root2pandas.EventCategories()
ttHHJESPileUpPtEC1Up_categories = root2pandas.EventCategories()
ttHHJESPileUpPtEC1Down_categories = root2pandas.EventCategories()

#dictionary
systematics=["JERUp","JERDown","JESUp","JESDown","JESAbsoluteStatUp","JESAbsoluteStatDown","JESAbsoluteScaleUp","JESAbsoluteScaleDown","JESAbsoluteMPFBiasUp","JESAbsoluteMPFBiasDown","JESFragmentationUp","JESFragmentationDown","JESSinglePionECALUp","JESSinglePionECALDown","JESSinglePionHCALUp","JESSinglePionHCALDown","JESFlavorQCDUp","JESFlavorQCDDown","JESTimePtEtaUp","JESTimePtEtaDown","JESRelativeJEREC1Up","JESRelativeJEREC1Down","JESRelativePtBBUp","JESRelativePtBBDown","JESRelativePtEC1Up","JESRelativePtEC1Down","JESRelativeBalUp","JESRelativeBalDown","JESRelativeFSRUp","JESRelativeFSRDown","JESRelativeStatFSRUp","JESRelativeStatFSRDown","JESRelativeStatECUp","JESRelativeStatECDown","JESPileUpDataMCUp","JESPileUpDataMCDown","JESPileUpPtRefUp","JESPileUpPtRefDown","JESPileUpPtBBUp","JESPileUpPtBBDown","JESPileUpPtEC1Up","JESPileUpPtEC1Down"]
systematics2=["JERup","JERdown","JESup","JESdown","JESAbsoluteStatup","JESAbsoluteStatdown","JESAbsoluteScaleup","JESAbsoluteScaledown","JESAbsoluteMPFBiasup","JESAbsoluteMPFBiasdown","JESFragmentationup","JESFragmentationdown","JESSinglePionECALup","JESSinglePionECALdown","JESSinglePionHCALup","JESSinglePionHCALdown","JESFlavorQCDup","JESFlavorQCDdown","JESTimePtEtaup","JESTimePtEtadown","JESRelativeJEREC1up","JESRelativeJEREC1down","JESRelativePtBBup","JESRelativePtBBdown","JESRelativePtEC1up","JESRelativePtEC1down","JESRelativeBalup","JESRelativeBaldown","JESRelativeFSRup","JESRelativeFSRdown","JESRelativeStatFSRup","JESRelativeStatFSRdown","JESRelativeStatECup","JESRelativeStatECdown","JESPileUpDataMCup","JESPileUpDataMCdown","JESPileUpPtRefup","JESPileUpPtRefdown","JESPileUpPtBBup","JESPileUpPtBBdown","JESPileUpPtEC1up","JESPileUpPtEC1down"]

#dict definition
dict_syst_ttHH={"JERUp": ttHHJERup_categories, "JERDown":ttHHJERdown_categories, "JESUp": ttHHJESup_categories, "JESDown":ttHHJESdown_categories,"JESAbsoluteStatUp":ttHHJESAbsoluteStatUp_categories,"JESAbsoluteStatDown":ttHHJESAbsoluteStatDown_categories,"JESAbsoluteScaleUp":ttHHJESAbsoluteScaleUp_categories,"JESAbsoluteScaleDown":ttHHJESAbsoluteScaleDown_categories,"JESAbsoluteMPFBiasUp":ttHHJESAbsoluteMPFBiasUp_categories,"JESAbsoluteMPFBiasDown":ttHHJESAbsoluteMPFBiasDown_categories,"JESFragmentationUp":ttHHJESFragmentationUp_categories,"JESFragmentationDown":ttHHJESFragmentationDown_categories,"JESSinglePionECALUp":ttHHJESSinglePionECALUp_categories,"JESSinglePionECALDown":ttHHJESSinglePionECALDown_categories,"JESSinglePionHCALUp":ttHHJESSinglePionHCALUp_categories,"JESSinglePionHCALDown":ttHHJESSinglePionHCALDown_categories,"JESFlavorQCDUp":ttHHJESFlavorQCDUp_categories,"JESFlavorQCDDown":ttHHJESFlavorQCDDown_categories,"JESTimePtEtaUp":ttHHJESTimePtEtaUp_categories,"JESTimePtEtaDown":ttHHJESTimePtEtaDown_categories,"JESRelativeJEREC1Up":ttHHJESRelativeJEREC1Up_categories,"JESRelativeJEREC1Down":ttHHJESRelativeJEREC1Down_categories,"JESRelativePtBBUp":ttHHJESRelativePtBBUp_categories,"JESRelativePtBBDown":ttHHJESRelativePtBBDown_categories,"JESRelativePtEC1Up":ttHHJESRelativePtEC1Up_categories,"JESRelativePtEC1Down":ttHHJESRelativePtEC1Down_categories,"JESRelativeBalUp":ttHHJESRelativeBalUp_categories,"JESRelativeBalDown":ttHHJESRelativeBalDown_categories,"JESRelativeFSRUp":ttHHJESRelativeFSRUp_categories,"JESRelativeFSRDown":ttHHJESRelativeFSRDown_categories,"JESRelativeStatFSRUp":ttHHJESRelativeStatFSRUp_categories,"JESRelativeStatFSRDown":ttHHJESRelativeStatFSRDown_categories,"JESRelativeStatECUp":ttHHJESRelativeStatECUp_categories,"JESRelativeStatECDown":ttHHJESRelativeStatECDown_categories,"JESPileUpDataMCUp":ttHHJESPileUpDataMCUp_categories,"JESPileUpDataMCDown":ttHHJESPileUpDataMCDown_categories,"JESPileUpPtRefUp":ttHHJESPileUpPtRefUp_categories,"JESPileUpPtRefDown":ttHHJESPileUpPtRefDown_categories,"JESPileUpPtBBUp":ttHHJESPileUpPtBBUp_categories,"JESPileUpPtBBDown":ttHHJESPileUpPtBBDown_categories,"JESPileUpPtEC1Up":ttHHJESPileUpPtEC1Up_categories,"JESPileUpPtEC1Down":ttHHJESPileUpPtEC1Down_categories}

#dict_syst_ttH={"JERUp": ttHJERup_categories, "JERDown":ttHJERdown_categories, "JESUp": ttHJESup_categories, "JESDown":ttHJESdown_categories} 

# define output classes
#for ttHH4b:
#nominal:
ttHH_categories = root2pandas.EventCategories()
ttHH_categories.addCategory("ttHH4b", selection = None)

#systematics:
for systs in systematics:
   dict_syst_ttHH[systs].addCategory("ttHH4b"+"_"+systs, selection = None)

#for ttH
#norminal
ttH_categories = root2pandas.EventCategories()
ttH_categories.addCategory("ttHbb", selection = None)
#systematics:
#for systs in systematics:
#  dict_syst_ttH[systs].addCategory("ttHbb"+"_"+systs, selection = None)


# initialize dataset class
dataset = root2pandas.Dataset(
    outputdir   = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_syst-allVar-systntuples2/",
    naming      = "dnn",
    addCNNmap   = False,
    addMEM      = False)

# add base event selection
dataset.addBaseSelection(base_selection)

for ii, systs in enumerate(systematics2):
  dataset.addSample(
      sampleName  = "ttHH4b"+str(systs),
      ntuples     = "/eos/user/l/lprado/ttHH_ntuples/TTHHTo4b_forDNN_2/*"+str(systs)+"*.root",
      categories  = dict_syst_ttHH[str(systematics[ii])],
      selections  = ttHH_selection)



#dataset.addSample(
#    sampleName  = "ttHbbJESup",
#    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/syst_ntuples/ttHTobb/*JESup*.root",
#    categories  = ttHJESup_categories,
#    selections  = ttHH_selection)

#dataset.addSample(
#    sampleName  = "ttHbbJESdown",
#    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/syst_ntuples/ttHTobb/*JESdown*.root",
#    categories  = ttHJESdown_categories,
#    selections  = ttHH_selection)

#dataset.addSample(
#    sampleName  = "ttHbbJERup",
#    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/syst_ntuples/ttHTobb/*JERup*.root",
#    categories  = ttHJERup_categories,
#    selections  = ttHH_selection)

#dataset.addSample(
#    sampleName  = "ttHbbJERdown",
#    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/syst_ntuples/ttHTobb/*JERdown*.root",
#    categories  = ttHJERdown_categories,
#    selections  = ttHH_selection)


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

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

# define output classes
ttHH_categories = root2pandas.EventCategories()
ttHH_categories.addCategory("ttHH4b", selection = None)

ttHHJESup_categories = root2pandas.EventCategories()
ttHHJESup_categories.addCategory("ttHH4b_JESUp", selection = None)

ttHHJESdown_categories = root2pandas.EventCategories()
ttHHJESdown_categories.addCategory("ttHH4b_JESDown", selection = None)

ttHHJERup_categories = root2pandas.EventCategories()
ttHHJERup_categories.addCategory("ttHH4b_JERUp", selection = None)

ttHHJERdown_categories = root2pandas.EventCategories()
ttHHJERdown_categories.addCategory("ttHH4b_JERDown", selection = None)



ttH_categories = root2pandas.EventCategories()
ttH_categories.addCategory("ttHbb", selection = None)

ttHJESup_categories = root2pandas.EventCategories()
ttHJESup_categories.addCategory("ttHbb_JESUp", selection = None)

ttHJESdown_categories = root2pandas.EventCategories()
ttHJESdown_categories.addCategory("ttHbb_JESDown", selection = None)

ttHJERup_categories = root2pandas.EventCategories()
ttHJERup_categories.addCategory("ttHbb_JERUp", selection = None)

ttHJERdown_categories = root2pandas.EventCategories()
ttHJERdown_categories.addCategory("ttHbb_JERDown", selection = None)



ttbar_categories = root2pandas.EventCategories()
ttbar_categories.addCategory("ttbb", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("tt2b", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttb",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttlf", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttcc", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

ttbarJESup_categories = root2pandas.EventCategories()
ttbarJESup_categories.addCategory("ttbb_JESUp", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbarJESup_categories.addCategory("tt2b_JESUp", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbarJESup_categories.addCategory("ttb_JESUp",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbarJESup_categories.addCategory("ttlf_JESUp", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbarJESup_categories.addCategory("ttcc_JESUp", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

ttbarJESdown_categories = root2pandas.EventCategories()
ttbarJESdown_categories.addCategory("ttbb_JESDown", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbarJESdown_categories.addCategory("tt2b_JESDown", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbarJESdown_categories.addCategory("ttb_JESDown",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbarJESdown_categories.addCategory("ttlf_JESDown", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbarJESdown_categories.addCategory("ttcc_JESDown", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

ttbarJERup_categories = root2pandas.EventCategories()
ttbarJERup_categories.addCategory("ttbb_JERUp", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbarJERup_categories.addCategory("tt2b_JERUp", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbarJERup_categories.addCategory("ttb_JERUp",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbarJERup_categories.addCategory("ttlf_JERUp", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbarJERup_categories.addCategory("ttcc_JERUp", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

ttbarJERdown_categories = root2pandas.EventCategories()
ttbarJERdown_categories.addCategory("ttbb_JERDown", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbarJERdown_categories.addCategory("tt2b_JERDown", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbarJERdown_categories.addCategory("ttb_JERDown",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbarJERdown_categories.addCategory("ttlf_JERDown", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbarJERdown_categories.addCategory("ttcc_JERDown", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")




# initialize dataset class
dataset = root2pandas.Dataset(
    outputdir   = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_syst-allVar/",
    naming      = "dnn",
    addCNNmap   = False,
    addMEM      = False)

# add base event selection
dataset.addBaseSelection(base_selection)


# add samples to dataset
dataset.addSample(
    sampleName  = "ttHH4b",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/syst_ntuples/TTHHTo4b_forDNN/*nominal*.root",
    categories  = ttHH_categories,
    selections  = ttHH_selection)


dataset.addSample(
    sampleName  = "ttHbb",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/syst_ntuples/ttHTobb/*nominal*.root",
    categories  = ttH_categories,
    selections  = ttHH_selection)


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
    "Weight_CSVCErr1down",
    "Weight_CSVCErr1up",
    "Weight_CSVCErr2down",
    "Weight_CSVCErr2up",
    "Weight_CSVHFdown",
    "Weight_CSVHFup",
    "Weight_CSVHFStats1down",
    "Weight_CSVHFStats1up",
    "Weight_CSVHFStats2down",
    "Weight_CSVHFStats2up",
    "Weight_CSVLFdown",
    "Weight_CSVLFup",
    "Weight_CSVLFStats1down",
    "Weight_CSVLFStats1up",
    "Weight_CSVLFStats2down",
    "Weight_CSVLFStats2up",
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

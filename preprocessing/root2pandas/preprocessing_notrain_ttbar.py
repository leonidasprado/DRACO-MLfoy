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

# define output classes
ttbar_categories = root2pandas.EventCategories()
ttbar_categories.addCategory("ttbb", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("tt2b", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttb",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttlf", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttcc", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

#some definitions
outdirttbar="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_ttlep/"
#outdirttbar="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_ttbar/"
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
#dataset.addSample(
#    sampleName  = "TTToSL",
#    ntuples     = "/eos/user/l/lprado/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/*nominal*.root",
#    categories  = ttbar_categories,
#    selections  = None)

#dataset.addSample(
#    sampleName  = "TTToHad",
#    ntuples     = "/eos/user/l/lprado/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/*nominal*.root",
#    categories  = ttbar_categories,
#    selections  = None)

dataset.addSample(
    sampleName  = "TTToLep",
    ntuples     = "/eos/user/l/lprado/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/*nominal*.root",
    categories  = ttbar_categories,
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
    "Weight_MuonSFTrigger_Up",
#
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

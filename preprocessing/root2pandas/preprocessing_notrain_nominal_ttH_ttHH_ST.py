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

ttHH_selection = "(Evt_Odd == 1)"
#ttHH_selection = "(Evt_Odd == 0)"

# define output classes
ttHH_categories = root2pandas.EventCategories()
ttHH_categories.addCategory("ttHH4b", selection = None)

ttH_categories = root2pandas.EventCategories()
ttH_categories.addCategory("ttHbb", selection = None)

SingleTop_categories = root2pandas.EventCategories()
SingleTop_categories.addCategory("SingleTop", selection = None)

# some definitions
outdirttHH="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_ttHH_odd/"
#outdirttHH="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_ttH_ttHH/"
outdir=outdirttHH
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
dataset.addSample(
    sampleName  = "ttHH4b",
    ntuples     = "/eos/user/l/lprado/TTHHTo4b_5f_LO_TuneCP5_13TeV_madgraph_pythia8/*nominal*.root",
    categories  = ttHH_categories,
    selections  = ttHH_selection)


#dataset.addSample(
#    sampleName  = "ttHbb",
#    ntuples     = "/eos/user/l/lprado/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/*nominal*.root",
#    categories  = ttH_categories,
#    selections  = None)

#dataset.addSample(
#    sampleName  = "STsch",
#    ntuples     = "/eos/user/l/lprado/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/*nominal*.root",
#    categories  = SingleTop_categories,
#    selections  = None)

#dataset.addSample(
#    sampleName  = "STtchAntitop",
#    ntuples     = "/eos/user/l/lprado/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/*nominal*.root",
#    categories  = SingleTop_categories,
#    selections  = None)

#dataset.addSample(
#    sampleName  = "STtchTop",
#    ntuples     = "/eos/user/l/lprado/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/*nominal*.root",
#    categories  = SingleTop_categories,
#    selections  = None)

#dataset.addSample(
#    sampleName  = "STtwchAntitop",
#    ntuples     = "/eos/user/l/lprado/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/*nominal*.root",
#    categories  = SingleTop_categories,
#    selections  = None)

#dataset.addSample(
#    sampleName  = "STtwchTop",
#    ntuples     = "/eos/user/l/lprado/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/*nominal*.root",
#    categories  = SingleTop_categories,
#    selections  = None)

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
]

# add these variables to the variable list
dataset.addVariables(additional_variables)

# run the preprocessing
dataset.runPreprocessing()

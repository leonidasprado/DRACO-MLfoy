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
(N_Jets >= 4 and N_BTagsM >= 3 and Evt_Pt_MET > 20.) \
and (\
(N_LooseMuons == 0 and N_TightElectrons == 1 and (Triggered_HLT_Ele35_WPTight_Gsf_vX == 1 or Triggered_HLT_Ele28_eta2p1_WPTight_Gsf_HT150_vX == 1)) \
or \
(N_LooseElectrons == 0 and N_TightMuons == 1 and Muon_Pt > 29. and (Triggered_HLT_IsoMu24_eta2p1_vX == 1 or Triggered_HLT_IsoMu27_vX == 1)) \
) \
)"

base_selectionMuEF = "\
( \
(N_Jets >= 4 and N_BTagsM >= 2 and Evt_Pt_MET > 20.) \
and (\
(N_LooseMuons == 0 and N_TightElectrons == 1 and (Triggered_HLT_Ele35_WPTight_Gsf_vX == 1 or Triggered_HLT_Ele28_eta2p1_WPTight_Gsf_HT150_vX == 1)) \
or \
(N_LooseElectrons == 0 and N_TightMuons == 1 and Muon_Pt > 29. and Triggered_HLT_IsoMu27_vX == 1) \
) \
)"


# define other additional selections

# define output classes
data_categories = root2pandas.EventCategories()
data_categories.addCategory("data_obs", selection = None)

outdirdata="/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11_data/"
outdir=outdirdata
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

dataset.addSample(
    sampleName  = "dataEB",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleElectronB/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataEC",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleElectronC/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataED",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleElectronD/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataEE",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleElectronE/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataEF",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleElectronF/*nominal*.root",
    categories  = data_categories,
    selections  = None)

dataset.addSample(
    sampleName  = "dataMB",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleMuonB/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataMC",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleMuonC/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataMD",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleMuonD/*nominal*.root",
    categories  = data_categories,
    selections  = None)
dataset.addSample(
    sampleName  = "dataME",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleMuonE/*nominal*.root",
    categories  = data_categories,
    selections  = base_selectionMuEF)
dataset.addSample(
    sampleName  = "dataMF",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/data/SingleMuonF/*nominal*.root",
    categories  = data_categories,
    selections  = base_selectionMuEF)


# initialize variable list 
dataset.addVariables(variable_set.all_variables)

# define an additional variable list
additional_variables = [
    "N_Jets",
    "N_BTagsM",
    "N_BTagsL",
    "Weight_XS",
    "Weight_CSV",
#    "Weight_GEN_nom",
    "Evt_ID", 
    "Evt_Run", 
    "Evt_Lumi"]

# add these variables to the variable list
dataset.addVariables(additional_variables)

# run the preprocessing
dataset.runPreprocessing()

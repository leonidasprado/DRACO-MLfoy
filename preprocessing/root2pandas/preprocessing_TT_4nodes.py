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

ttHH_selection = "(Evt_Odd == 1)"

# define output classes
ttHH_categories = root2pandas.EventCategories()
ttHH_categories.addCategory("ttHH4b", selection = None)

ttbar_categories = root2pandas.EventCategories()
ttbar_categories.addCategory("tthf", selection = "(GenEvt_I_TTPlusBB >= 1 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttlf", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
ttbar_categories.addCategory("ttcc", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")

#ttbar_categories.addCategory("ttbb", selection = "(GenEvt_I_TTPlusBB == 3 and GenEvt_I_TTPlusCC == 0)")
#ttbar_categories.addCategory("tt2b", selection = "(GenEvt_I_TTPlusBB == 2 and GenEvt_I_TTPlusCC == 0)")
#ttbar_categories.addCategory("ttb",  selection = "(GenEvt_I_TTPlusBB == 1 and GenEvt_I_TTPlusCC == 0)")
#ttbar_categories.addCategory("ttlf", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 0)")
#ttbar_categories.addCategory("ttcc", selection = "(GenEvt_I_TTPlusBB == 0 and GenEvt_I_TTPlusCC == 1)")


# initialize dataset class
dataset = root2pandas.Dataset(
    outputdir   = "/afs/cern.ch/user/l/lprado/work/DNNInputFiles/DNN_ttHH_4nodes_allVar/",
    naming      = "dnn",
    addCNNmap   = False,
    addMEM      = False)

# add base event selection
dataset.addBaseSelection(base_selection)






# add samples to dataset

dataset.addSample(
    sampleName  = "TTToSL",
    ntuples     = "/eos/user/l/lprado/ttHH_ntuples/TTToSemiLeptonic_forDNN/*nominal*.root",
    categories  = ttbar_categories,
    selections  = None)#ttbar_selection)

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
    "Evt_Lumi"]

# add these variables to the variable list
dataset.addVariables(additional_variables)

# run the preprocessing
dataset.runPreprocessing()

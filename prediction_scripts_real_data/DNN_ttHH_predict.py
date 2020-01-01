# global imports
import os
import sys
import ROOT
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

# import class for DNN training
import DRACO_Frameworks.DNN.DNN3 as DNN
# specify which variable set to use
import variable_sets.ttHH_topVariables as variable_set

# when executing the script give the jet-tag category as a first argument
# (ge)[nJets]j_(ge)[nTags]t
#JTcategory      = sys.argv[1]
JTcategory      = "ge4j_ge3t"

# the input variables are loaded from the variable_set file
variables       = variable_set.variables[JTcategory]

# specify all the event classes, e.g. ["ttH", "ttbb", "tt2b", ...]
#event_classes also correspond to the nodes in the DNN
event_classes = ["ttHH4b", "ttbb", "tt2b","ttb","ttcc","ttlf"]

#below are the datasets to be loaded. Chose it as a terminal argument
event_nominal=["ttHH4b", "ttbb", "tt2b","ttb","ttcc","ttlf"]
#thi nominal_extra is mainly used for testing
event_nominal_extra=["ttbb"]
#event_nominal_extra=["ttHbb"]
event_data=["data_obs"]

#event_syst will have as input an Up or Down variation, here treated the same
#TO DO:
#add ttH when it is time to implement it
event_syst=["ttHH4b_"+str(sys.argv[1]),"ttbb_"+str(sys.argv[1]),"tt2b_"+str(sys.argv[1]),"ttb_"+str(sys.argv[1]),"ttcc_"+str(sys.argv[1]),"ttlf_"+str(sys.argv[1])]

#dictionary of classes
dict_event={"nominal":event_nominal, "nominal_extra": event_nominal_extra, "data":event_data}

#this is the constructed event class that will be passed on
if str(sys.argv[1]) in ("nominal","nominal_extra","data"):
  event_classes_extra = dict_event[str(sys.argv[1])]
else:
  event_classes_extra = event_syst

inputsyst="1"
if len(sys.argv)>2:
  inputsyst=str(sys.argv[2])
  root_output = "ttHH_predict_"+str(sys.argv[2])+"_"+JTcategory+".root"
else:
  #output root file for storing histograms:
  root_output = "ttHH_predict_"+str(sys.argv[1])+"_"+JTcategory+".root"

# absolute path to folder with input dataframes
inPath   = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_syst-allVar"
#inPath   = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_syst-topVar"
#inPath   = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_ttH_TT_2017_v1-topVar"
#inPath   = "/afs/cern.ch/user/l/lprado/work/DNNInputFiles/DNN_ttHH_2017_v2-topVar"


# path to output directory (adjust NAMING)
savepath = basedir+"/workdir/"+"ttHH_2017_predict_"+str(JTcategory)

# initializing DNN training class
#not all is needed for the prediction
dnn = DNN.DNN(
    in_path         = inPath,
    save_path       = savepath,
    root_output     = root_output,
    event_classes   = event_classes,
    event_classes_extra = event_classes_extra,
    event_category  = JTcategory,
    train_variables = variables,
    systematics     = inputsyst,
    # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
    #if set to 1, use all the events. This script is based on training script.
    test_percentage = 1.0)

#Model already exists, defined with training script
dnn.load_trained_model()
# plotting 
# plot the output discriminators
#Root file created in plotting script
if len(sys.argv)<=2 and str(sys.argv[1])=="nominal":
  dnn.plot_discriminators_pretty()
else:
  dnn.plot_discriminators()

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
event_classes = ["ttHH4b", "ttbb", "tt2b","ttb","ttcc","ttlf"]
event_classes3 = ["ttHH4b", "ttHbb", "ttbb", "tt2b","ttb","ttcc","ttlf"]
event_classes2 = ["ttHH4b"]

# absolute path to folder with input dataframes
inPath   = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_ttH_TT_2017_v1-topVar"
#inPath   = "/afs/cern.ch/user/l/lprado/work/DNNInputFiles/DNN_ttHH_2017_v2-topVar"


# path to output directory (adjust NAMING)
savepath = basedir+"/workdir/"+"ttHH_2017_predict_"+str(JTcategory)

# initializing DNN training class
#not all is needed for the prediction
dnn = DNN.DNN(
    in_path         = inPath,
    save_path       = savepath,
    event_classes   = event_classes,
    event_category  = JTcategory,
    train_variables = variables,
    # number of epochs
    train_epochs    = 500,
    # number of epochs without decrease in loss before stopping
    early_stopping  = 100,
    # metrics for evaluation (c.f. KERAS metrics)
    eval_metrics    = ["acc"],
    # percentage of train set to be used for testing (i.e. evaluating/plotting after training)
    test_percentage = 0.2)

# build default model
#dnn.build_model()
# perform the training
#dnn.train_model()
# evalute the trained model
#dnn.eval_model()
#If model already exists, use only commands below
dnn.load_trained_model()
# plotting 
# plot the evaluation metrics
#dnn.plot_metrics()
# plot the confusion matrix
#dnn.plot_confusionMatrix(norm_matrix = True)
# plot the output discriminators
#------TEST-------#
f = ROOT.TFile("ttHH_Test1_predict_"+str(JTcategory)+".root","RECREATE")
#Modified the plot.discriminatiors() function for this. Need to create a root file first
#dnn.plot_discriminators()
f.Close()

#some tests
#dnn.predict_event_query("Evt_ID == 5929612")
#dnn.get_input_weights()

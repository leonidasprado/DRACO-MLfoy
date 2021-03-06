# global imports
import os
import sys

# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

# import class for DNN training
import DRACO_Frameworks.DNN.DNN as DNN
# specify which variable set to use
import variable_sets.ttHH_topVariables as variable_set

# when executing the script give the jet-tag category as a first argument
# (ge)[nJets]j_(ge)[nTags]t
JTcategory      = sys.argv[1]

# the input variables are loaded from the variable_set file
variables       = variable_set.variables[JTcategory]

# specify all the event classes, e.g. ["ttH", "ttbb", "tt2b", ...]
#event_classes = ["ttHH4b", "ttbar"]
#event_classes = ["ttHH4b", "tthf","ttcc","ttlf"]
event_classes = ["ttHH4b", "ttbb", "tt2b","ttb","ttcc","ttlf"]

# absolute path to folder with input dataframes
#inPath   = "/afs/cern.ch/user/l/lprado/work/DNNInputFiles/DNN_ttHH_4nodes_allVar"
#inPath   = "/afs/cern.ch/user/l/lprado/work/DNNInputFiles/DNN_ttHH_TTalternative-allVar"
inPath   = "/afs/cern.ch/user/l/lprado/work/DNNInputFiles/ttHH_May11"

# path to output directory (adjust NAMING)
savepath = basedir+"/workdir/"+"ttHH_May11_topVar_"+str(JTcategory)

# initializing DNN training class
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
dnn.build_model()
# perform the training
dnn.train_model()
# evalute the trained model
dnn.eval_model()
#If model already exists, use only commands below
#dnn.load_trained_model()
# get variable ranking
dnn.get_input_weights()

# plotting 
# plot the evaluation metrics
dnn.plot_metrics()
# plot the confusion matrix
dnn.plot_confusionMatrix(norm_matrix = True)
# plot the output discriminators
dnn.plot_discriminators()

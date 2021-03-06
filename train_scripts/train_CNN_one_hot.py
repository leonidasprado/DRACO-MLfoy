# global imports
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)
import DRACO_Frameworks.CNN.CNN_one_hot as CNN


inPath = "/storage/c/vanderlinden/DRACO-MLfoy/workdir/train_samples/base_train_set"

cnn = CNN.CNN(
    in_path         = inPath,
    save_path       = basedir+"/workdir/basic_cnn_one_hot",
    class_label     = "nJets",
    batch_size      = 256,
    train_epochs    = 10,
    optimizer       = "adam",
    loss_function   = "categorical_crossentropy",
    eval_metrics    = ["mean_squared_error", "acc"] )

cnn.load_datasets()
cnn.build_model()
cnn.train_model()
cnn.eval_model()

# evaluate stuff
cnn.print_classification_examples()
cnn.print_classification_report()
cnn.plot_metrics()
cnn.plot_discriminators()
cnn.plot_confusion_matrix()








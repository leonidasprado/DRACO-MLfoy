import os
import sys
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

import variable_sets.ttHH_allVariables as variable_set
from evaluationScripts.plotVariables2 import variablePlotter

# location of input dataframes
#data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_2tags_test_NEWTRIG_2"
data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_May11"
#data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_2tags_test_NEWTRIG_newttbar_nTuple"
#data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_2tags_test_ttbar_NEWTRIG_NEWnTUPLE_Had_Lep_SemiLep"
#data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_2tags_test_OLD_TRIG"
#data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH_syst-allVar-ttHbb-systntuples"

# output location of plots
plot_dir = "/afs/cern.ch/user/l/lprado/work/Plots_Input_var_ttHH_May11"
#plot_dir = "/afs/cern.ch/user/l/lprado/work/Plots_Input_var_ttHH_2017-allVar-ttH_2TAG_TEST_NEWTRIG_newttbar_nTuple_Had_Lep_SemiLep"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# plotting options
plotOptions = {
    "ratio":        True,
    "logscale":     False,
    "scaleSignal":  -1,
    "lumiScale":    41.5,
    "ratioTitle":   ""
    }
#   scaleSignal:
#   -1:     scale to background Integral
#   float:  scale with float value
#   False:  dont scale

# additional variables to plot
additional_variables = [
    'N_Jets',
    'N_BTagsM',
    'N_BTagsL',
    'Weight_XS',
    'Weight_CSV',
 ]


# initialize plotter
plotter = variablePlotter(
    output_dir      = plot_dir,
    variable_set    = variable_set,
    add_vars        = additional_variables,
    plotOptions     = plotOptions
    )

# add samples
plotter.addSample(
    sampleName      = "ttHH",
    sampleFile      = data_dir+"/ttHH4b_dnn.h5",
    signalSample    = True)
plotter.addSample(
    sampleName      = "ttbb",
    sampleFile      = data_dir+"/ttbb_dnn.h5")

plotter.addSample(
    sampleName      = "tt2b",
    sampleFile      = data_dir+"/tt2b_dnn.h5")

plotter.addSample(
    sampleName      = "ttb",
    sampleFile      = data_dir+"/ttb_dnn.h5")

plotter.addSample(
    sampleName      = "ttcc",
    sampleFile      = data_dir+"/ttcc_dnn.h5")

plotter.addSample(
    sampleName      = "ttlf",
    sampleFile      = data_dir+"/ttlf_dnn.h5")

plotter.addSample(
    sampleName      = "ttHbb",
    sampleFile      = data_dir+"/ttHbb_dnn.h5",
    ttHSample       = True)

plotter.addSample(
    sampleName      = "SingleTop",
    sampleFile      = data_dir+"/SingleTop_dnn.h5",
    ttHSample       = True)

plotter.addSample(
    sampleName      = "data",
    sampleFile      = data_dir+"/data_obs_dnn.h5",
    dataSample      = True)


# add JT categories
#plotter.addCategory("4j_ge3t")
#plotter.addCategory("5j_ge3t")
#plotter.addCategory("ge6j_ge3t")
#plotter.addCategory("le5j_ge3t")
plotter.addCategory("ge4j_ge3t")
#plotter.addCategory("ge4j_ge2t")
#plotter.addCategory("6j_4t")
#plotter.addCategory("6j_ge3t")
#plotter.addCategory("ge7j_ge3t")


# perform plotting routine
plotter.plot()

import os
import sys
# local imports
filedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(filedir)
sys.path.append(basedir)

import variable_sets.ttHH_allVariables as variable_set
from evaluationScripts.plotVariables import variablePlotter

# location of input dataframes
data_dir = "/afs/cern.ch/user/l/lprado/work/InputFiles/ttHH-allVar-ttbbOpenLoops-tt4bStudy"

# output location of plots
plot_dir = "/afs/cern.ch/user/l/lprado/work/SomePlots_ttHH_tt4b_OpenLoops"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# plotting options
plotOptions = {
    "ratio":        False,
    "logscale":     False,
    "scaleSignal":  -1,
    "lumiScale":    1
    }
#   scaleSignal:
#   -1:     scale to background Integral
#   float:  scale with float value
#   False:  dont scale

# additional variables to plot
additional_variables = [
    'N_Jets',
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
    sampleName      = "ttbbb",
    sampleFile      = data_dir+"/ttbbb_dnn.h5")

plotter.addSample(
    sampleName      = "tt4b",
    sampleFile      = data_dir+"/tt4b_dnn.h5",
    signalSample = True)



# add JT categories
#plotter.addCategory("4j_ge3t")
#plotter.addCategory("5j_ge3t")
#plotter.addCategory("ge6j_ge3t")
#plotter.addCategory("le5j_ge3t")
plotter.addCategory("ge4j_ge3t")
#plotter.addCategory("6j_ge3t")
#plotter.addCategory("ge7j_ge3t")


# perform plotting routine
plotter.plot()

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
#    'N_BTagsM',
#    'N_BTagsL',
#    'Weight_XS',
#    'Weight_CSV',
 ]
onlyrootfiles=True
syst=""
systFile=""
inputsyst="1"
#Construct systematics or not
if str(sys.argv[1]) in ("nominal"):
  onlyrootfiles = False
  if len(sys.argv)>2:
      onlyrootfiles = True
      inputsyst=str(sys.argv[2]) #inputsyst uses ntuple naming convention
      syst = "_"+inputsyst
else:
  syst= "_"+str(sys.argv[1])
  systFile=syst

#root file naming uses ntuple naming
if len(sys.argv)>2:
  root_output = "ttHH_InputVar_"+str(sys.argv[2])+".root"
else:
  root_output = "ttHH_InputVar_"+str(sys.argv[1])+".root"

rate=False
sampleFlag=""
rate_value=""
#if "len(sys.argv)>3", it means it is a rate syst:
# python  plotInputVariables.py nominal ratesystUp/Down sampleName NumericalValue
if len(sys.argv)>3:
    rate = True
    sampleFlag = str(sys.argv[3])
    rate_value = str(sys.argv[4])

# initialize plotter
plotter = variablePlotter(
    rate            = rate,
    sampleFlag      = sampleFlag,
    rate_value      = rate_value,
    inputsyst       = inputsyst,
    onlyrootfiles   = onlyrootfiles,
    root_output     = root_output,
    output_dir      = plot_dir,
    variable_set    = variable_set,
    add_vars        = additional_variables,
    plotOptions     = plotOptions
    )

# add samples
plotter.addSample(
    sampleName      = "ttHH4b"+syst,
    sampleNameColor = "ttHH4b",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/ttHH4b"+systFile+"_dnn.h5",
    signalSample    = True)
plotter.addSample(
    sampleName      = "ttbb"+syst,
    sampleNameColor = "ttbb",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/ttbb"+systFile+"_dnn.h5")

plotter.addSample(
    sampleName      = "tt2b"+syst,
    sampleNameColor = "tt2b",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/tt2b"+systFile+"_dnn.h5")

plotter.addSample(
    sampleName      = "ttb"+syst,
    sampleNameColor = "ttb",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/ttb"+systFile+"_dnn.h5")

plotter.addSample(
    sampleName      = "ttcc"+syst,
    sampleNameColor = "ttcc",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/ttcc"+systFile+"_dnn.h5")

plotter.addSample(
    sampleName      = "ttlf"+syst,
    sampleNameColor = "ttlf",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/ttlf"+systFile+"_dnn.h5")

plotter.addSample(
    sampleName      = "ttHbb"+syst,
    sampleNameColor = "ttHbb",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/ttHbb"+systFile+"_dnn.h5",
    ttHSample       = True)

plotter.addSample(
    sampleName      = "SingleTop"+syst,
    sampleNameColor = "SingleTop",
    inputsyst       = inputsyst,
    sampleFile      = data_dir+"/SingleTop"+systFile+"_dnn.h5",
    ttHSample       = True)

if not onlyrootfiles:
      plotter.addSample(
          sampleName      = "data_obs",
          sampleNameColor = "data",
          inputsyst       = inputsyst,
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

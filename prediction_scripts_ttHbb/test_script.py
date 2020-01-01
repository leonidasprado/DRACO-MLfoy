import ROOT
from ROOT import TFile, TTree, TH1F, gDirectory
import sys

filename = sys.argv[1]
proc_num = sys.argv[2]
f=ROOT.TFile(filename)
subD1="ttHH4b_node"
subD2="ttbb_node"
subD3="tt2b_node"
subD4="ttb_node"
subD5="ttcc_node"
subD6="ttlf_node"
subD=[subD1,subD2,subD3,subD4,subD5,subD5,subD6]
processes=["ttHH4b","ttbb","tt2b", "ttb", "ttcc", "ttlf","ttHbb", "data_obs"]
for i, item in enumerate(subD):
    print("-"*50)
    print("directory number ", i)
    print("directory is: ", item)
    for j, process in enumerate(processes):
      print("j is: ", j, "is it less than ", proc_num, " ?")
      if j < int(proc_num):
        print("process is ",process+":")
        histo=f.Get(item+"/"+ process)
        print("number of events is: ", histo.GetEntries())
        print("Integral is: ",histo.Integral())


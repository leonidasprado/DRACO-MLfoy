import ROOT
from ROOT import TFile, TTree, TH1F, gDirectory
import sys

#choose the nominal histograms to create the fake data one
filename = sys.argv[1]

#The new root file
fnew = ROOT.TFile("ttHH_predict_asimov_ge4j_ge3t.root","RECREATE")
subD1=fnew.mkdir("ttHH4b_node")
subD2=fnew.mkdir("ttbb_node")
subD3=fnew.mkdir("tt2b_node")
subD4=fnew.mkdir("ttb_node")
subD5=fnew.mkdir("ttcc_node")
subD6=fnew.mkdir("ttlf_node")
RDirectory = [subD1,subD2,subD3,subD4,subD5,subD6]

#The root file being open
f=ROOT.TFile(filename)
subD=["ttHH4b_node","ttbb_node","tt2b_node","ttb_node","ttcc_node","ttlf_node"]
processes=["ttHH4b","ttbb","tt2b", "ttb", "ttcc", "ttlf"]#,"ttHbb", "data_obs"]
number_data=0
for i, item in enumerate(subD):
    print("-"*50)
    print("directory number ", i)
    print("directory is: ", item)
    for j, process in enumerate(processes):
        print("process is ",process+":")
        histo=f.Get(item+"/"+ process)
        print("value of j is: ", j)
        if j==0: histo2 = histo
        if j>0: histo2 = histo2 + histo
        print("number of events is: ", histo.GetEntries())
        print("Integral is: ",histo.Integral())
    print("before reseting, histo2 has some bla: ", histo2.Integral())
    number_data+=histo2.Integral()
    fnew.cd()
    RDirectory[i].cd()
    histo2.SetName("data_obs")
    histo2.SetXTitle("data_obs")
    histo2.Write()
    f.cd()
print("total number of asimov = ", number_data)

import ROOT
from ROOT import TFile, TTree, TH1F, gDirectory
import sys

filename = "ttHH_predict_nominal_ge4j_ge3t.root"
ROOT.gROOT.SetBatch(1)
#The root file being open
f=ROOT.TFile(filename)
subD=["ttHH4b_node","ttbb_node","tt2b_node","ttb_node","ttcc_node","ttlf_node"]
nominal_processes=["ttHH4b","ttbb","tt2b", "ttb", "ttcc", "ttlf"]
number_data=0
for node in subD:
        c1= ROOT.TCanvas()
        c1.cd()
        histo_nominal_1 = f.Get(node+"/"+"ttHH4b")
        #histo_nominal_1.SetXTitle(node)
        histo_nominal_2=f.Get(node+"/"+"ttbbb")
        histo_nominal_2.SetXTitle(node)
        histo_nominal_3=f.Get(node+"/"+"tt4b")
        print(str(histo_nominal_2.Integral()))
        norm=int(float(histo_nominal_2.Integral())/float(histo_nominal_1.Integral()))
        histo_nominal_1.Scale(norm)
        histo_nominal_2.SetLineColor(ROOT.kRed)
        histo_nominal_3.SetLineColor(ROOT.kGreen)
        histo_nominal_2.Draw()
        histo_nominal_1.Draw("same")
        histo_nominal_3.Draw("same")
        leg = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
        leg.SetHeader("processes")
        leg.AddEntry(histo_nominal_1, "ttHH4b x "+str(norm), "lep")
        leg.AddEntry(histo_nominal_2, "ttbbb", "lep")
        leg.AddEntry(histo_nominal_3, "tt4b", "lep")
        leg.Draw()
        c1.SaveAs("tt4b_plots/"+node+".png")

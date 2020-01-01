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
        histo_nominal_3=f.Get(node+"/"+"tt4b")
        histo_nominal_4=f.Get(node+"/"+"ttbb")
        integral1=float(histo_nominal_1.Integral())
        integral2=float(histo_nominal_2.Integral())
        integral3=float(histo_nominal_3.Integral())
        integral4=float(histo_nominal_4.Integral())
        print integral4
        scale1 = 1.0/(integral1)
        scale2 = 1.0/(integral2)
        scale3 = 1.0/(integral3)
        scale4 = 1.0/(integral4)
        print scale4
        histo_nominal_1.Scale(scale1)
        histo_nominal_2.Scale(scale2)
        histo_nominal_3.Scale(scale3)
        histo_nominal_4.Scale(scale4)
        histo_nominal_2.SetLineColor(ROOT.kRed)
        histo_nominal_3.SetLineColor(ROOT.kGreen)
        histo_nominal_4.SetLineColor(ROOT.kMagenta)
        histo_nominal_1.SetXTitle(node)
        histo_nominal_1.Draw()
        histo_nominal_2.Draw("same")
        histo_nominal_3.Draw("same")
        histo_nominal_4.Draw("same")
        if "ttHH4b" in node:
            leg = ROOT.TLegend(0.1, 0.8, 0.3, 0.9)
        else:
            leg = ROOT.TLegend(0.7, 0.8, 0.9, 0.9)        
        leg.SetNColumns(2)
        #leg.SetHeader("processes (normalized to 1)")
        leg.AddEntry(histo_nominal_1, "ttHH4b", "lep")
        leg.AddEntry(histo_nominal_2, "ttbbb", "lep")
        leg.AddEntry(histo_nominal_3, "tt4b", "lep")
        leg.AddEntry(histo_nominal_4, "ttbb", "lep")
        leg.Draw()
        c1.SaveAs("tt4b_plots_OpenLoops_v2/"+node+".png")
        c1.SaveAs("tt4b_plots_OpenLoops_v2/"+node+".pdf")

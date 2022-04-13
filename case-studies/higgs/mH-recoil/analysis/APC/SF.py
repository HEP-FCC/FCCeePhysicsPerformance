#!/usr/bin/env python
import sys, os
import os.path
import ntpath
import importlib
import ROOT
import copy
import re
from ROOT import *
import argparse
import math

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
if __name__ == "__main__":
  #fileDir = '/afs/cern.ch/work/l/lia/private/FCC/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/outputs/FCCee/higgs/mH-recoil/mumu'
  fileDir = '/eos/home-l/lia/FCCee/mumu'
  #sel = 'Gen_mass_220'
  sel = 'sel0'
  #var = 'Gen_pt_mumu_025'
  #var = 'Gen_pt_mumu'
  var = 'leptonic_recoil_m'
  f_kkmcp8 = ROOT.TFile(os.path.join(fileDir,"_".join(["kkmcp8_ee_mumu_noFSR_ecm240",sel,"histo.root"])))
  f_wzp6 = ROOT.TFile(os.path.join(fileDir,"_".join(["wzp6_ee_mumu_noFSR_ecm240",sel,"histo.root"])))
  print(os.path.join(fileDir,"_".join(["kkmcp8_ee_mumu_noFSR_ecm240",sel,"histo.root"])))

  h_pt_kkmcp8 = f_kkmcp8.Get(var)
  h_pt_wzp6 = f_wzp6.Get(var)
  h_pt_kkmcp8.SetName("h_"+var+"_kkmcp8") 
  h_pt_wzp6.SetName("h_"+var+"_wzp6")
  
  h_pt_kkmcp8.Scale(1.0/h_pt_kkmcp8.Integral())
  h_pt_wzp6.Scale(1.0/h_pt_wzp6.Integral())
  
  h_SF_pt = h_pt_kkmcp8.Clone("pT_mumu_SF_kkmc8_over_wzp6")

  h_SF_pt.Divide(h_pt_wzp6)
 
  if not os.path.exists(os.path.join(fileDir,"plots_SF")):
    os.system('mkdir ' + os.path.join(fileDir,"plots_SF"))

  c_SF_pt = ROOT.TCanvas('SF_ptmumu_kkmcp8_over_wzp6','SF_ptmumu_kkmcp8_over_wzp6',1200,1600)
  padFrac=0.45
  uppPad=TPad("uppPad","",0,padFrac,1,1)
  lowPad=TPad("lowPad","",0,0,1,padFrac)
  uppPad.SetBottomMargin(0.01)
  lowPad.SetTopMargin(0.01)
  lowPad.SetBottomMargin(0.3)
  uppPad.Draw()
  lowPad.SetFillColor(0)
  lowPad.Draw()

  uppPad.cd()
  uppPad.SetLogy()
  h_pt_kkmcp8.SetLineColor(kBlue)
  h_pt_wzp6.SetLineColor(kRed)
  h_pt_kkmcp8.SetStats(0)
  h_pt_wzp6.SetStats(0)
  h_pt_kkmcp8.GetYaxis().SetTitle("1.0/bin width")
  legend = ROOT.TLegend(0.6,0.7,0.9,0.9)
  legend.AddEntry(h_pt_kkmcp8,"kkmcp8")
  legend.AddEntry(h_pt_wzp6,"wzp6")
  h_pt_kkmcp8.Draw()
  h_pt_wzp6.Draw("same")
  legend.Draw()
  lowPad.cd()
  h_SF_pt.GetYaxis().SetTitle('SF kkmcp8/wzp6')
  h_SF_pt.SetStats(0)
  h_SF_pt.GetYaxis().SetRangeUser(0.8,1.1)
  h_SF_pt.Draw()
  c_SF_pt.SaveAs(os.path.join(fileDir,"plots_SF","_".join(["SF",var,sel])+".pdf"))

  f_save = ROOT.TFile(os.path.join(fileDir,"kkmcp8_wzp6_ecm240_scale.root"),'RECREATE')
  h_pt_kkmcp8.Write()
  h_pt_wzp6.Write()
  h_SF_pt.Write()
  f_save.Write()
  f_save.Close()

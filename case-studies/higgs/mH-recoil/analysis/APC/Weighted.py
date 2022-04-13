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
  
  #f = ["events_075322554_Delphes_headon","events_075322554_FullSim_headon"]
  #sel = 'sel0'
  #var = 'leptonic_recoil_m_zoom2'
  #leg = ['mumuH FullSili. Delphes','mumuH FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'Delphes_FullSim'
  
  #f = ["events_045918595_Delphes_AllMuons","events_045918595_FullSim_AllMuons"]
  #sel = 'sel0'
  #var = 'muon_pt_zoom1'
  #leg = ['ZZ AllMuons FullSili. Delphes','ZZ AllMuons FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'AllMuons_Delphes_FullSim'
 
  #f = ["events_045918595_Delphes_IsoMuons","events_045918595_FullSim_IsoMuons"]
  #sel = 'sel0'
  #var = 'muon_pt_zoom1'
  #leg = ['ZZ IsoMuons FullSili. Delphes','ZZ IsoMuons FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'IsoMuons_Delphes_FullSim'

  #f = ["events_045918595_Delphes_AllMuons","events_045918595_FullSim_AllMuons"]
  #sel = 'sel27'
  #var = 'leptonic_recoil_m_zoom16'
  #leg = ['ZZ AllMuons FullSili. Delphes','ZZ AllMuons FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'AllMuons_Delphes_FullSim'

  #f = ["events_045918595_Delphes_IsoMuons","events_045918595_FullSim_IsoMuons"]
  #sel = 'sel27'
  #var = 'leptonic_recoil_m_zoom16'
  #leg = ['ZZ IsoMuons FullSili. Delphes','ZZ IsoMuons FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'IsoMuons_Delphes_FullSim'
 
  #f = ["events_045918595_Delphes_AllMuons","events_045918595_Delphes_IsoMuons"]
  #sel = 'sel0'
  #var = 'muon_pt_zoom1'
  #leg = ['ZZ AllMuons FullSili. Delphes','ZZ IsoMuons FullSili. Delphes']
  #r = 'AllMuons/IsoMuons'
  #suffix = 'Delphes_AllMuons_IsoMuons'
 
  #f = ["events_045918595_FullSim_AllMuons","events_045918595_FullSim_IsoMuons"]
  #sel = 'sel0'
  #var = 'muon_pt_zoom1'
  #leg = ['ZZ AllMuons FullSili. FullSim.','ZZ IsoMuons FullSili. FullSim.']
  #r = 'AllMuons/IsoMuons'
  #suffix = 'FullSim_AllMuons_IsoMuons'

  #f = ["events_045918595_Delphes_AllMuons","events_045918595_Delphes_IsoMuons"]
  #sel = 'sel27'
  #var = 'leptonic_recoil_m_zoom16'
  #leg = ['ZZ AllMuons FullSili. Delphes','ZZ IsoMuons FullSili. Delphes']
  #r = 'AllMuons/IsoMuons'
  #suffix = 'Delphes_AllMuons_IsoMuons'
 
  #f = ["events_045918595_FullSim_AllMuons","events_045918595_FullSim_IsoMuons"]
  #sel = 'sel27'
  #var = 'leptonic_recoil_m_zoom16'
  #leg = ['ZZ AllMuons FullSili. FullSim.','ZZ IsoMuons FullSili. FullSim.']
  #r = 'AllMuons/IsoMuons'
  #suffix = 'FullSim_AllMuons_IsoMuons'
 
  #f = ["events_075322554_Delphes_headon","events_075322554_FullSim_xing"]
  #sel = 'sel23'
  #var = 'leptonic_recoil_m_zoom2'
  #leg = ['mumuH FullSili. Delphes headon','mumuH FullSili. FullSim. boosted-back']
  #r = 'headon/xing boosted-back'
  #suffix = 'Delphes_headon_FullSim_boosted_back'
 
  #f = ["events_075322554_FullSim_headon","events_075322554_FullSim_xing"]
  #sel = 'sel23'
  #var = 'leptonic_recoil_m_zoom2'
  #leg = ['mumuH FullSili. FullSim. headon','mumuH FullSili. FullSim. boosted-back']
  #r = 'headon/xing boosted-back'
  #suffix = 'FullSim_headon_boosted_back'
 
  #f = ["events_075322554_Delphes_headon","events_075322554_FullSim_xing"]
  #sel = 'sel23'
  #var = 'leptonic_recoil_pt'
  #leg = ['mumuH FullSili. Delphes headon','mumuH FullSili. FullSim. boosted-back']
  #r = 'headon/xing boosted-back'
  #suffix = 'Delphes_headon_FullSim_boosted_back'
 
#  f = ["events_075322554_FullSim_headon","events_075322554_FullSim_xing"]
#  sel = 'sel23'
#  var = 'leptonic_recoil_pt'
#  leg = ['mumuH FullSili. FullSim. headon','mumuH FullSili. FullSim. boosted-back']
#  r = 'headon/xing boosted-back'
#  suffix = 'FullSim_headon_boosted_back'

  #f = ["events_075322554_FullSim_xing","events_075322554_FullSim_xing_1up"]
  #sel = 'sel23'
  #var = 'leptonic_recoil_m_zoom2'
  #leg = ['mumuH FullSili. FullSim. xing boosted-back 15mrad','mumuH FullSili. FullSim. xing boosted-back 1 percent up']
  #r = '15mrad/15.15mrad'
  #suffix = 'FullSim_headon_boosted_back_1up'
 
  #f = ["events_075322554_FullSim_xing","events_075322554_FullSim_xing_1down"]
  #sel = 'sel23'
  #var = 'leptonic_recoil_m_zoom2'
  #leg = ['mumuH FullSili. FullSim. xing boosted-back 15mrad','mumuH FullSili. FullSim. xing boosted-back 1 percent down']
  #r = '15mrad/14.85mrad'
  #suffix = 'FullSim_headon_boosted_back_1down'
 
  #f = ["events_075322554_Delphes_headon","events_075322554_FullSim_headon"]
  #sel = 'sel23'
  #var = 'leptonic_recoil_m_zoom2'
  #leg = ['mumuH FullSili. Delphes','mumuH FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'Delphes_FullSim'
 
  #f = ["events_075322554_Delphes_headon","events_075322554_FullSim_headon"]
  #sel = 'sel28'
  #var = 'mz_zoom8'
  #leg = ['mumuH FullSili. Delphes','mumuH FullSili. FullSim.']
  #r = 'Delphes/FullSim.'
  #suffix = 'Delphes_FullSim'

  ''' 
  f = ["events_075322554_Delphes_headon","events_075322554_FullSim_headon"]
  sel = 'sel0'
  #sel = 'sel23'
  #var = 'z_pt'
  #var = 'mz_zoom6'
  var = 'z_e'
  leg = ['mumuH FullSili. Delphes','mumuH FullSili. FullSim.']
  r = 'Delphes/FullSim.'
  suffix = 'Delphes_FullSim'
  '''

  f = ["events_075322554_FullSim_headon","events_075322554_FullSim_xing","events_075322554_FullSim_xing_noboost"]
  sel = 'sel23'
  var = 'leptonic_recoil_m_zoom2'
  leg = ['mumuH FullSili. FullSim. headon','mumuH FullSili. FullSim. boosted-back','mumuH FullSili. FullSim. no boosted-back']
  r = 'headon/xing boosted-back'
  suffix = 'FullSim_headon_boosted_back_noboost'

 
  f_weighted = ROOT.TFile(os.path.join(fileDir,"_".join([f[0],sel,"histo.root"])))
  f_unweighted = ROOT.TFile(os.path.join(fileDir,"_".join([f[1],sel,"histo.root"])))
  f3 = ROOT.TFile(os.path.join(fileDir,"_".join([f[2],sel,"histo.root"])))
  h_weighted = f_weighted.Get(var)
  h_unweighted = f_unweighted.Get(var)
  h3 = f3.Get(var)
  h_weighted.SetName("h_"+var+"_weighted") 
  h_unweighted.SetName("h_"+var+"_unweighted")
  h3.SetName("h_"+var+"_"+f[2])
  #h_weighted.Scale(1.0/h_weighted.Integral())
  #h_unweighted.Scale(1.0/h_unweighted.Integral())
  
  h_ratio = h_weighted.Clone("weighted_over_unweighted")

  h_ratio.Divide(h_unweighted)
 
  if not os.path.exists(os.path.join(fileDir,"plots_ratio")):
    os.system('mkdir ' + os.path.join(fileDir,"plots_ratio"))

  c_ratio = ROOT.TCanvas('weighted_unweighted_ratio','weighted_unweighted_ratio',1200,1600)
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
  #uppPad.SetLogy()
  h_weighted.SetLineColor(kBlue)
  h_unweighted.SetLineColor(kRed)
  h3.SetLineColor(kOrange)
  h_weighted.SetStats(0)
  h_unweighted.SetStats(0)
  #h_weighted.GetYaxis().SetTitle("1.0/bin width")
  h_weighted.GetYaxis().SetTitle("Events")
  legend = ROOT.TLegend(0.6,0.7,0.9,0.9)
  #legend.AddEntry(h_weighted,"AllMuons_IDEA_FullSili._Delphes")
  #legend.AddEntry(h_unweighted,"IsoMuons_IDEA_FullSili._Delphes")
  #legend.AddEntry(h_weighted,"IDEA_FullSili._FullSim_headon")
  #legend.AddEntry(h_unweighted,"IDEA_FullSili._FullSim_xing_boostedback")
  legend.AddEntry(h_weighted,leg[0])
  legend.AddEntry(h_unweighted,leg[1])
  legend.AddEntry(h3,leg[2])
  #legend.AddEntry(h_weighted,"mumuH weighted")
  #legend.AddEntry(h_unweighted,"mumuH unweighted")
  h_weighted.Draw('hist')
  h_unweighted.Draw("same")
  h3.Draw("same")
  #h_unweighted.Draw('same')
  legend.Draw()
  lowPad.cd()
  #h_ratio.GetYaxis().SetTitle('ratio weighted/unweighted')
  #h_ratio.GetYaxis().SetTitle('ratio')
  #h_ratio.GetYaxis().SetTitle('FullSim. headon/xing_boostedback')
  h_ratio.GetYaxis().SetTitle(r)
  h_ratio.SetStats(0)
  #h_ratio.GetYaxis().SetRangeUser(0.8,1.2)
  h_ratio.GetYaxis().SetRangeUser(0.,2.)
  h_ratio.SetLineColor(kBlack)
  h_ratio.GetXaxis().SetTitleOffset(1.40)
  h_ratio.Draw()
  #flat = ROOT.TF1("flat","1",0,200)
  #flat.SetLineColor(kRed)
  #flat.Draw('same')
  #h_ratio.Draw('same')
  c_ratio.SaveAs(os.path.join(fileDir,"plots_ratio","_".join(["ratio",var,sel,suffix])+".pdf"))

  f_save = ROOT.TFile(os.path.join(fileDir,"wzp6_ee_mumuH_ecm240_weighted_ratio.root"),'RECREATE')
  h_weighted.Write()
  h_unweighted.Write()
  h_ratio.Write()
  f_save.Write()
  f_save.Close()

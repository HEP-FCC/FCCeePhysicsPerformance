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
def removekey(d, key):
  r = dict(d)
  del r[key]
  return r
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def runFit():
  global model
  global hist  
  global x
  if(fitMode == 0):
    fitresult = model.fitTo(hist,ROOT.RooFit.Save(),ROOT.RooFit.NumCPU(8,0),ROOT.RooFit.Extended(True),ROOT.RooFit.Optimize(False),ROOT.RooFit.Offset(True),ROOT.RooFit.Minimizer("Minuit2","migrad"),ROOT.RooFit.Strategy(2))
  elif(fitMode == 1):
    x.setRange("CR",double(fitRange[0]),double(fitRange[1]))
    fitresult = model.fitTo(hist, ROOT.RooFit.Save(),ROOT.RooFit.NumCPU(8,0),ROOT.RooFit.Range('CR'),ROOT.RooFit.Extended(True),ROOT.RooFit.Optimize(False),ROOT.RooFit.Offset(True),ROOT.RooFit.Minimizer("Minuit2","migrad"),ROOT.RooFit.Strategy(2))
  elif(fitMode == 2):
    x.setRange("SBL",double(sidebandRange[0]),double(sidebandRange[1]))
    x.setRange("SBH",double(sidebandRange[2]),double(sidebandRange[3]))
    fitresult = model.fitTo(hist, ROOT.RooFit.Save(),ROOT.RooFit.NumCPU(8,0),ROOT.RooFit.Range('SBL,SBH'),ROOT.RooFit.Extended(True),ROOT.RooFit.Optimize(False),ROOT.RooFit.Offset(True),ROOT.RooFit.Minimizer("Minuit2","migrad"),ROOT.RooFit.Strategy(2))  
  return fitresult
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def WorkMode():
  w = 999
  if (SBMode):
    return w
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def mapHistos(var, sel):
  inputDir = param.inputDir
  print("--->Accessing the input directory " + inputDir)
  print("------>Loading ")
  print('------>run fit for var:{}     selection:{}'.format(var,sel))

  SgnHistos = {}
  BkgHistos = {}
  #SumHistos = []
  
  print("--------->Signals")
  for sgnKey in sgnProcesses:
    SgnHistos[sgnKey]=[]
    for f in sgnProcesses[sgnKey]:
      fin=os.path.join(param.inputDir,f+'_'+sel+'_histo.root')
      if not os.path.isfile(fin):
        print ('------------>file {} does not exist, skip'.format(fin))
      else:
        print ('------------>Loading {}'.format(fin))
        tf=ROOT.TFile(fin)
        h=tf.Get(var)
        hh = copy.deepcopy(h)
        hh.Scale(param.intLumi)
        if len(SgnHistos[sgnKey])==0:
          SgnHistos[sgnKey].append(hh)
        else:
          hh.Add(SgnHistos[sgnKey][0])
          SgnHistos[sgnKey][0]=hh
  
  if(SBMode):
    print("--------->Backgrounds")
    for bkgKey in bkgProcesses:
      BkgHistos[bkgKey]=[]
      for f in bkgProcesses[bkgKey]:
        fin=os.path.join(param.inputDir,f+'_'+sel+'_histo.root')
        if not os.path.isfile(fin):
          print ('file {} does not exist, skip'.format(fin))
        else:
          print ('------------>Loading {}'.format(fin))
          tf=ROOT.TFile(fin)
          h=tf.Get(var)
          hh = copy.deepcopy(h)
          hh.Scale(param.intLumi)
          if len(BkgHistos[bkgKey])==0:
            BkgHistos[bkgKey].append(hh)
          else:
            hh.Add(BkgHistos[bkgKey][0])
            BkgHistos[bkgKey][0]=hh

  
  for sgnKey in SgnHistos:
    if len(SgnHistos[sgnKey])==0:
      SgnHistos=removekey(SgnHistos,sgnKey)

  if(SBMode):
    for bkgKey in BkgHistos:
      if len(BkgHistos[bkgKey])==0:
        BkgHistos=removekey(BkgHistos,bkgKey)

  SumHistos_tmp = []
  for sgnKey in SgnHistos:
    h_tmp = copy.deepcopy(SgnHistos[sgnKey][0])
    if len(SumHistos_tmp)==0:
      SumHistos_tmp.append(h_tmp)
    else:
      SumHistos_tmp[0].Add(h_tmp)


  if NewModelledSignalMode:
    SumHistos_tmp[0]=copy.deepcopy(ModelNewSignal(SgnHistos))
  
  if(SBMode):
    for bkgKey in BkgHistos:
      h_tmp = copy.deepcopy(BkgHistos[bkgKey][0])
      SumHistos_tmp[0].Add(h_tmp)
   
  SumHistos = SumHistos_tmp[0]

  
  return SgnHistos, BkgHistos, SumHistos
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----



# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def readData():
  inputDir = param.inputDir
  print("--->Accessing the input directory " + inputDir)
  print("------>Loading ")
  
  print("--------->Signal")

  global sgnHistos
  global bkgHistos
  global sumHistos

  for sgnKey in sgnProcesses:
    sgnHistos[sgnKey] = []
    #fin = os.path.join(inputDir, "wzp6_ee_" + sgnKey + "_ecm" + str(int(param.energy)) + "_v2"+ "_" + sel + "_histo.root")
    #fin = os.path.join(inputDir, "p8_noBES_ee_" + sgnKey + "_ecm" + str(int(param.energy)) + "_" + sel + "_histo.root")
    #fin = os.path.join(inputDir, "p8_ee_" + sgnKey + "_ecm" + str(int(param.energy)) + "_" + sel + "_histo.root")
    fin = os.path.join(inputDir, sgnKey + "_" + sel + "_histo.root")
    if not os.path.isfile(fin):
      print ('------------>file {} does not exist, skip'.format(fin))
    else:  
      tf=ROOT.TFile(fin)
      h=tf.Get(param.histoName)
      hh = copy.deepcopy(h)
      hh.Scale(param.intLumi)
      sgnHistos[sgnKey] = hh
    print("------------>"+sgnKey + "_" + sel + "_histo.root")
  print(sgnHistos)

  if (NewModelledSignalMode):
    sumHistos = ModelNewSignal().Clone()
  else:
    sumHistos = copy.deepcopy(sgnHistos[list(sgnHistos.keys())[0]])
    print(sumHistos)
    for sgnKey in sgnHistos:
      if (sgnKey != list(sgnHistos.keys())[0]): 
        sumHistos.Add(sgnHistos[sgnKey])

  if (SBMode):  
    print("--------->Background")
    for bkgKey in bkgProcesses:  
      bkgHistos[bkgKey] = []
      #fin = os.path.join(inputDir, "p8_noBES_ee_" + bkgKey + "_ecm" + str(int(param.energy)) + "_" + sel + "_histo.root")
      fin = os.path.join(inputDir, bkgKey + "_" + sel + "_histo.root")
      if not os.path.isfile(fin):
        print ('------------>file {} does not exist, skip'.format(fin))
      else:
        tf=ROOT.TFile(fin)
        h=tf.Get(param.histoName)
        hh = copy.deepcopy(h)
        hh.Scale(param.intLumi)
        bkgHistos[bkgKey] = hh
      print("------------>" + bkgKey + "_" + sel + "_histo.root")
    for bkgKey in bkgHistos:
      sumHistos.Add(bkgHistos[bkgKey])

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def ModelNewSignal(SgnHistos):
  
  SumSgnHistos_tmp = []
  for sgnKey in SgnHistos:
    h_tmp = copy.deepcopy(SgnHistos[sgnKey][0])
    if len(SumSgnHistos_tmp)==0:
      SumSgnHistos_tmp.append(h_tmp)
    else:
      SumSgnHistos_tmp[0].Add(h_tmp)

  sumSgnHistos = SumSgnHistos_tmp[0]
  x_NMS = ROOT.RooRealVar("m_recoil", "m_recoil", sumSgnHistos.GetXaxis().GetXmin(), sumSgnHistos.GetXaxis().GetXmax())
  #mean_NMS = ROOT.RooRealVar("mean", "mean", peak, peak - 2.0, peak + 2.0)
  #sigma_NMS = ROOT.RooRealVar("sigma", "width", 0.3, 0.2, 0.4)
  sigma_NMS = ROOT.RooRealVar("sigma", "width", 0.3, 0.2, 0.4)
  #alpha_L_NMS = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.0, 0.8, 5.0)
  alpha_L_NMS = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.0, 0.7, 5.0)
  n_L_NMS = ROOT.RooRealVar("nL", "n of Crystal Ball", 5.0, 0.0, 200.0)
  #alpha_H_NMS = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 1.0, 0.8, 5.0)
  alpha_H_NMS = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 1.0, 0.7, 5.0)
  n_H_NMS = ROOT.RooRealVar("nH", "n of Crystal Ball", 5.0, 0.0, 200.0)
  
  #nsig_init_NMS = 0.0
  
  #sumSgnHistos = copy.deepcopy(sgnHistos[list(sgnHistos.keys())[0]])
  #for sgnKey in sgnHistos:
  #  if (sgnKey != list(sgnHistos.keys())[0]):
  #    sumSgnHistos.Add(sgnHistos[sgnKey])

  peak_NMS = sumSgnHistos.GetXaxis().GetBinCenter(sumSgnHistos.GetMaximumBin())
  mean_NMS = ROOT.RooRealVar("mean", "mean", peak_NMS, peak_NMS - 2.0, peak_NMS + 2.0)

  nsig_init_NMS = sumSgnHistos.Integral()  
  
  nsig_NMS = ROOT.RooRealVar("nsig", "number of signal events", nsig_init_NMS, 0.2*nsig_init_NMS, 1.5*nsig_init_NMS)

  if (modelFunction == 'DCB'):
    signal_NMS = ROOT.RooCrystalBall("DCB", "DCB", x_NMS, mean_NMS, sigma_NMS, alpha_L_NMS, n_L_NMS, alpha_H_NMS, n_H_NMS)
  else:
    print('fit function ' + modelFunction + ' for New Modelled Signal is not supported. Please implment it!')
  
  model_NMS = ROOT.RooAddPdf("Signal_Modelled","Signal_Modelled",ROOT.RooArgList(signal_NMS),ROOT.RooArgList(nsig_NMS))

  hist = ROOT.RooDataHist("signalHsitos", "signalHistos", ROOT.RooArgList(x_NMS), sumSgnHistos)
  fit_result = model_NMS.fitTo(hist,ROOT.RooFit.Save(),ROOT.RooFit.NumCPU(8,0),ROOT.RooFit.Extended(True),ROOT.RooFit.Optimize(False),ROOT.RooFit.Offset(True),ROOT.RooFit.Minimizer("Minuit2","migrad"),ROOT.RooFit.Strategy(2))
  print("--->Saving WorkSpace")
  w = ROOT.RooWorkspace("modelWS","modelWS")
  getattr(w, 'import')(model_NMS)
  w.Print()


  #sgnChannels = sgnProcesses[0]
  #for sgn in sgnProcesses:
  #  if (sgn!=sgnProcesses[0]):
  #    sgnChannels += "_"
  #    sgnChannels += sgn

  sgnchannels = '_'.join(SgnHistos)
  
  xframe = x_NMS.frame(ROOT.RooFit.Title(modelFunction + " pdf with data"))  # RooPlot
  hist.plotOn(xframe, ROOT.RooFit.Name("Data_temp"), ROOT.RooFit.DrawOption("Z"), ROOT.RooFit.MarkerSize(0.2))
  model_NMS.plotOn(xframe, ROOT.RooFit.Name("SB"), ROOT.RooFit.LineColor(ROOT.kOrange))
  hist.plotOn(xframe, ROOT.RooFit.Name("Data"), ROOT.RooFit.DrawOption("Z"), ROOT.RooFit.MarkerSize(0.2))
  ndf =  fit_result.floatParsFinal().getSize()
  chi2 = xframe.chiSquare("SB", "Data", ndf)
  #ras_sig = ROOT.RooArgSet(signal_NMS)
  #model_NMS.plotOn(xframe, ROOT.RooFit.Name("S"), ROOT.RooFit.Components(ras_sig), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
  c1 = TCanvas('c1','',800,800)
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
  model_NMS.paramOn(xframe, ROOT.RooFit.Layout(0.60), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)))
  xframe.SetYTitle('Events / (' + str(sumSgnHistos.GetBinWidth(1)) + ' GeV)')
  xframe.GetYaxis().SetTitleFont(43)
  xframe.GetYaxis().SetTitleSize(26)
  xframe.Draw()
  t = TLatex()
  t.SetNDC()
  t.SetTextFont(42)
  t.SetTextSize(0.035)
  t.DrawLatex(0.15,0.60, ('#chi^{{2}}/NDF: {0:0.2f}'.format(chi2)) )
  
  t.DrawLatex(0.15,0.80, sgnchannels )
  t.DrawLatex(0.15,0.70, 'L = 5 ab^{-1}' )
  leg = ROOT.TLegend(0.10,0.35,0.25,0.55,inputDir.split('/')[-1])
  leg.AddEntry("Data","Data")

  
  leg.AddEntry("SB","Sig. Only Fit")
  leg.Draw()
  lowPad.cd()
  xframe2 = x_NMS.frame()
  hpull = xframe.pullHist("Data", "SB")
  hpull.SetMarkerSize(0.5)
  xframe2.addPlotable(hpull, 'Z p')

  xframe2.SetTitle('')
  xframe2.GetYaxis().SetRangeUser(-10,10)
  xframe2.GetXaxis().SetTitleOffset(3.0)
  xframe2.GetYaxis().SetTitleFont(43)
  xframe2.GetYaxis().SetTitleSize(26)
  xframe2.GetXaxis().SetTitleFont(43)
  xframe2.GetXaxis().SetTitleSize(26)
  
  if 'recoil' in histoName:
    xframe2.SetXTitle('M_{recoil} [GeV]')
  elif 'mz' in histoName:
    xframe2.SetXTitle('M_{Z} [GeV]')
  else:
    xframe2.SetXTitle(sumSgnHistos.GetXaxis().GetTitle())
  xframe2.SetYTitle('#frac{Data-Fit}{Error}')
  xframe2.Draw()
  flat = ROOT.TF1("flat","0",0,200)
  flat.SetLineColor(kRed)
  flat.Draw('same')
  xframe2.Draw("same")

  
  
  if not os.path.exists(os.path.join(inputDir,"workspaces")):
    os.system('mkdir ' + os.path.join(inputDir,"workspaces"))
  print(os.path.join(inputDir,"workspaces",inputDir.split('/')[-1] + "_" + sgnchannels + "_" + histoName + "_" + sgnFunction + "_workspace.root"))
  w.writeToFile(os.path.join(inputDir,"workspaces",inputDir.split('/')[-1] + "_" + sgnchannels + "_" + histoName + "_" + sgnFunction + "_workspace.root"))
  c1.SaveAs(os.path.join(inputDir,"workspaces",inputDir.split('/')[-1] + "_" + sgnchannels + "_" + histoName + "_" + str(int(sumSgnHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumSgnHistos.GetXaxis().GetXmax())) + "_" +modelFunction + "_fit_result.pdf"))
  f = ROOT.TFile.Open(os.path.join(inputDir,"workspaces",inputDir.split('/')[-1] + "_" + sgnchannels + "_" + histoName + "_" + sgnFunction + "_workspace.root"))
  print("--->Signal fit saved: " + os.path.join(inputDir,"workspaces",inputDir.split('/')[-1] + "_" + sgnchannels + "_" + histoName + "_" + str(int(sumSgnHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumSgnHistos.GetXaxis().GetXmax())) + "_" +modelFunction + "_fit_result.pdf"))
  WS = f.Get("modelWS")
  sgnX = WS.var('m_recoil')
  sgnPDF = WS.pdf('DCB')
  sgnData = sgnPDF.generate(ROOT.RooArgSet(sgnX), int(sumSgnHistos.GetEntries()))
  print("sumSgnHistos.GetNbinsX() " + str(sumSgnHistos.GetNbinsX()))
  sgnHist = sgnData.createHistogram("h_sgn",sgnX,ROOT.RooFit.Binning(sumSgnHistos.GetNbinsX()))
  print ("sumSgnHistos.Integral() = " + str(sumSgnHistos.Integral()))
  sgnHist.Scale(sumSgnHistos.Integral()/sgnHist.Integral())
  print ("Scaled sgnHist Integral = " + str(sgnHist.Integral()))
  h = copy.deepcopy(sgnHist)
  return h
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def buildModel():
  global x
  global mean
  global sigma
  global alpha_L
  global alpha_H
  global n_L
  global n_H
  global p0
  global p1
  global p2
  global sig_p0
  global sig_p1
  global sig_p2
  global sigfrac
  global signal
  sigFunc = param.sgnFunction
  if (sigFunc == 'CBR'):
    signal = ROOT.RooCBShape("Crystal Ball", "Crystal Ball PDF", x, mean, sigma, alphaR, n)
  elif (sigFunc == 'CBL'):
    signal = ROOT.RooCBShape("Crystal Ball", "Crystal Ball PDF", x, mean, sigma, alphaL, n)
  elif (sigFunc == 'BW'):
    signal = ROOT.RooBreitWigner("BreitWigner", "RooBreitWigner PDF", x, mean, sigma)
  elif (sigFunc == 'landau'):
    signal = ROOT.RooLandau("Landau", "Landau PDF", x, mean, sigma)
  elif (sigFunc == 'Gaussian'):
    signal = ROOT.RooGaussian("Gaussian", "Gaussian PDF", x, mean, sigma)
  elif (sigFunc == 'DCB'):
    signal = ROOT.RooCrystalBall("Double Crystal Ball", "Double Crystal Ball PDF", x, mean, sigma, alpha_L, n_L,alpha_H, n_H)
  elif (sigFunc == "Novosibirsk"):
    signal = ROOT.RooNovosibirsk("Novosibirsk", "Novosibirsk", x, mean, sigma, tail)
  elif (sigFunc == "Bukin"):
    signal = ROOT.RooBukinPdf("Bukin", "Bukin", x, mean, sigma, xi, rho_H, rho_L)
  elif (sigFunc == "Voigtian"):
    signal = ROOT.RooVoigtian("Voigtian", "Voigtian", x, mean, sigma, sigma2)
  elif (sigFunc == "GExp"):
    signal = ROOT.RooGExpModel("GExp", "GExp", x, tau, SF)
  elif (sigFunc == 'Exp'):
    signal  = ROOT.RooExponential("Exponential", "Exponential", x, c)
  elif (sigFunc == 'Pol1'):
    signal = ROOT.RooPolynomial("Pol1", "Pol1", x, ROOT.RooArgList(sig_p0, sig_p1))
  elif (sigFunc == 'Pol2'):
    signal = ROOT.RooPolynomial("Pol2", "Pol2", x, ROOT.RooArgList(sig_p0, sig_p1, sig_p2))
  elif (sigFunc == 'Pol3'):
    signal = ROOT.RooPolynomial("Pol3", "Pol3", x, ROOT.RooArgList(sig_p0, sig_p1, sig_p2, sig_p3))
  elif (sigFunc == 'Pol4'):
    signal = ROOT.RooPolynomial("Pol4", "Pol4", x, ROOT.RooArgList(sig_p0, sig_p1, sig_p2, sig_p3, sig_p4))
  elif (sigFunc == "Pow"):
    plIndex = ROOT.RooRealVar("plIndex", "Power Law Spectral Index", -2, -100000, -0.01)
    #signal = ROOT.RooGenericPdf("spec", "pow((@4/abs(@3))-abs(@3)-(@0-@1)/@2,@4)", RooArgList(x, mean, sigma, alphaL, plIndex))
    signal = ROOT.RooGenericPdf("spec", "pow(@0,@1)", RooArgList(x, plIndex))
  else:
    print('fit function ' + sigFunc + ' is not supported. Please implment it!')
    exit(1)

  if (SBMode):
    global background
    bkgFunc = param.bkgFunction
    if (bkgFunc == 'Exp'):
      background = ROOT.RooExponential("Exponential", "Exponential", x, c)
    elif (bkgFunc == 'Pol1'):
      background = ROOT.RooPolynomial("Pol1", "Pol1", x, ROOT.RooArgList(p0, p1))
    elif (bkgFunc == 'Pol2'):
      background = ROOT.RooPolynomial("Pol2", "Pol2", x, ROOT.RooArgList(p0, p1, p2))
    elif (bkgFunc == 'Pol3'):
      background = ROOT.RooPolynomial("Pol3", "Pol3", x, ROOT.RooArgList(p0, p1, p2, p3))
    elif (bkgFunc == 'Pol4'):
      background = ROOT.RooPolynomial("Pol4", "Pol4", x, ROOT.RooArgList(p0, p1, p2, p3, p4))
    elif (bkgFunc == 'Chebychev1'):
      background = ROOT.RooChebychev("Chebychev1", "Chebychev1", x, ROOT.RooArgList(p0, p1))
    elif (bkgFunc == 'Chebychev2'):
      background = ROOT.RooChebychev("Chebychev2", "Chebychev2", x, ROOT.RooArgList(p0, p1, p2))
    elif (bkgFunc == 'Chebychev3'):
      background = ROOT.RooChebychev("Chebychev3", "Chebychev3", x, ROOT.RooArgList(p0, p1, p2, p3))
    elif (bkgFunc == 'Chebychev4'):
      background = ROOT.RooChebychev("Chebychev4", "Chebychev4", x, ROOT.RooArgList(p0, p1, p2, p3, p4))
    else:
      print('fit function ' + bkgFunc + ' is not supported. Please implment it!')
      exit(2)

  if(SBMode):
    model = ROOT.RooAddPdf("total_pdf","total_pdf",ROOT.RooArgList(signal,background),ROOT.RooArgList(nsig, nbkg))
  else:
    model = ROOT.RooAddPdf("total_pdf","total_pdf",ROOT.RooArgList(signal),ROOT.RooArgList(nsig))
  model.Print()  
  return model
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
def plot():
  if (SBMode):
    func = sgnFunction + '_' + bkgFunction
  else:
    func = sgnFunction
  #for sgn in sgnFunction:
  #  if(len(func)==0):
  #    func = sgn
  #  else:
  #    func+= "_"+sgn
  #if(SBMode):
  #  for bkg in bkgFunction:
  #    func += "_"+bkg

  xframe = x.frame(ROOT.RooFit.Title(func + " pdf with data"))  # RooPlot
  hist.plotOn(xframe, ROOT.RooFit.Name("Data_temp"), ROOT.RooFit.DrawOption("Z"), ROOT.RooFit.MarkerSize(0.2))
  model.plotOn(xframe, ROOT.RooFit.Name("SB"), ROOT.RooFit.LineColor(ROOT.kOrange))
  hist.plotOn(xframe, ROOT.RooFit.Name("Data"), ROOT.RooFit.DrawOption("Z"), ROOT.RooFit.MarkerSize(0.2))
  ndf =  fitResult.floatParsFinal().getSize()
  chi2 = xframe.chiSquare("SB", "Data", ndf)
  if (SBMode):
    ras_bkg = ROOT.RooArgSet(background)
    ras_sig = ROOT.RooArgSet(signal)
    model.plotOn(xframe, ROOT.RooFit.Name("S"), ROOT.RooFit.Components(ras_sig), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
    model.plotOn(xframe, ROOT.RooFit.Name("B"), ROOT.RooFit.Components(ras_bkg), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kGreen))
  #else:
  #  ras_sig = ROOT.RooArgSet(signal)
  #  model.plotOn(xframe, ROOT.RooFit.Name("S"), ROOT.RooFit.Components(ras_sig), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kGreen))
  
  
  
  c1 = TCanvas('c1','',800,800)
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
  model.paramOn(xframe, ROOT.RooFit.Layout(0.60), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)))
  #if not SBMode:
    #if 'ZZ' in sgnProcesses or 'WW' in sgnProcesses:
  #xframe.GetYaxis().SetRangeUser(0,600)
  xframe.SetYTitle('Events / (' + str(sumHistos.GetBinWidth(1)) + ' GeV)')
  xframe.GetYaxis().SetTitleFont(43)
  xframe.GetYaxis().SetTitleSize(26)
  xframe.Draw()
  t = TLatex()
  t.SetNDC()
  t.SetTextFont(42)
  t.SetTextSize(0.035)
  t.DrawLatex(0.15,0.60, ('#chi^{{2}}/NDF: {0:0.2f}'.format(chi2)) )
  sgnchannels = '_'.join(sgnHistos)
  #for sgn in sgnHistos:
  #  if (sgn!=sgnHistos[0]): 
  #    channels += "_"
  #    channels += sgn
  if (SBMode):
    bkgchannels = '_'.join(bkgHistos)
    #for bkg in bkgProcesses:
    #  channels += '_'+bkg
  if (SBMode):
    channels = '_'.join([sgnchannels,bkgchannels])
  else:
    channels = sgnchannels
  t.DrawLatex(0.15,0.80, "Sgn.: "+sgnchannels )
  if SBMode:
    t.DrawLatex(0.15,0.75, "Bkg.: "+bkgchannels )
  t.DrawLatex(0.15,0.70, 'L = 5 ab^{-1}' )
  t.DrawLatex(0.15,0.65, 'Selection: '+sel)
  leg = ROOT.TLegend(0.10,0.35,0.25,0.55,inputDir.split('/')[-1])
  leg.AddEntry("Data","Data")
  if(SBMode):
    leg.AddEntry("SB","S + B Fit")
    leg.AddEntry("S","Sig. Fit")
    leg.AddEntry("B","Bkg. Fit")
  else:
    leg.AddEntry("SB","Sig. Only Fit")
  leg.Draw()
  lowPad.cd()
  xframe2 = x.frame() 
  if(fitMode == 0 or fitMode == 1):
    hpull = xframe.pullHist("Data", "SB")
    hpull.SetMarkerSize(0.5)
    xframe2.addPlotable(hpull, 'Z p')
  elif(fitMode == 2):
    dataHist  = xframe.getHist("Data_temp")
    curve1 = xframe.getObject(1)
    curve2 = xframe.getObject(2)
    hresid1 =  dataHist.makePullHist(curve1,True);
    hresid2 =  dataHist.makePullHist(curve2,True);
    hresid1.SetMarkerSize(0.5)
    hresid2.SetMarkerSize(0.5)
    xframe2.addPlotable(hresid1,"Z P")
    xframe2.addPlotable(hresid2,"Z P")
  xframe2.SetTitle('')
  xframe2.GetYaxis().SetRangeUser(-10,10)
  xframe2.GetXaxis().SetTitleOffset(3.0)
  xframe2.GetYaxis().SetTitleFont(43)
  xframe2.GetYaxis().SetTitleSize(26)
  xframe2.GetXaxis().SetTitleFont(43)
  xframe2.GetXaxis().SetTitleSize(26)
  
  mean.Print()
  sigma.Print()
  alpha_L.Print()
  alpha_H.Print()
  n_L.Print()
  n_H.Print()
  nsig.Print()
  if(SBMode):
    nbkg.Print()
    p0.Print()
    p1.Print()
    p2.Print()

  if 'recoil' in histoName:
    xframe2.SetXTitle('M_{recoil} [GeV]')
  elif 'mz' in histoName:
    xframe2.SetXTitle('M_{Z} [GeV]')
  else:
    xframe2.SetXTitle(sumHistos.GetXaxis().GetTitle())
  xframe2.SetYTitle('#frac{Data-Fit}{Error}')
  xframe2.Draw()
  flat = ROOT.TF1("flat","0",0,200)
  flat.SetLineColor(kRed)
  flat.Draw('same')
  xframe2.Draw("same")
  if not os.path.exists(outDir):
    os.system('mkdir ' + outDir)
  if (fitMode == 0):
    if(NewModelledSignalMode):
      fileName = os.path.join(outDir,inputDir.split('/')[-1] + "_" + channels + "_" + histoName + "_" + str(int(sumHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumHistos.GetXaxis().GetXmax())) + "_" + func + "_fullRange_NewModelledSignal_fit_result.pdf")
    else:
      fileName = os.path.join(outDir,inputDir.split('/')[-1] + "_" + channels + "_" + histoName + "_" + str(int(sumHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumHistos.GetXaxis().GetXmax())) + "_" + func + "_fullRange_fit_result.pdf")
  elif (fitMode ==1 ):
    if(NewModelledSignalMode):
      fileName = os.path.join(outDir,inputDir.split('/')[-1] + "_" + channels + "_" + histoName + "_" + str(int(sumHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumHistos.GetXaxis().GetXmax())) + "_" + func + "_fitRange_"+fitRange[0]+"_"+fitRange[1]+"_NewModelledSignal_fit_result.pdf")
    else:
      fileName = os.path.join(outDir,inputDir.split('/')[-1] + "_" + channels + "_" + histoName + "_" + str(int(sumHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumHistos.GetXaxis().GetXmax())) + "_" + func + "_fitRange_"+fitRange[0]+"_"+fitRange[1]+"_fit_result.pdf")
  elif (fitMode == 2):
    if(NewModelledSignalMode):
      fileName = os.path.join(outDir,inputDir.split('/')[-1] + "_" + channels + "_" + histoName + "_" + str(int(sumHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumHistos.GetXaxis().GetXmax())) + "_" + func + "_sidebandRange_"+sidebandRange[0]+"_"+sidebandRange[1]+"_"+sidebandRange[2]+"_"+sidebandRange[3]+"_NewModelledSignal_fit_result.pdf") 
    else:
      fileName = os.path.join(outDir,inputDir.split('/')[-1] + "_" + channels + "_" + histoName + "_" + str(int(sumHistos.GetXaxis().GetXmin())) + "_" +  str(int(sumHistos.GetXaxis().GetXmax())) + "_" + func + "_sidebandRange_"+sidebandRange[0]+"_"+sidebandRange[1]+"_"+sidebandRange[2]+"_"+sidebandRange[3]+"_fit_result.pdf")
  c1.SaveAs(fileName)
  print("--->Fit result saved: " + fileName)
  print("--->Adjust the parameters if needed")
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
if __name__ == "__main__":
  ROOT.gROOT.SetBatch(True)
  ROOT.gErrorIgnoreLevel = ROOT.kWarning
  paramFile = sys.argv[1]
   
  module_path = os.path.abspath(paramFile)
  module_dir = os.path.dirname(module_path)
  base_name = os.path.splitext(ntpath.basename(paramFile))[0]
  
  print(paramFile)
  print(module_path)
  print(module_dir)
  print(base_name)

  sys.path.insert(0, module_dir)
  param = importlib.import_module(base_name)

  SBMode = param.SBMode
  NewModelledSignalMode = param.NewModelledSignalMode
  modelFunction = param.modelFunction
  sgnProcesses = param.sgnProcesses
  bkgProcesses = param.bkgProcesses
  sgnFunction = param.sgnFunction
  bkgFunction = param.bkgFunction
  outDir = param.outDir
  inputDir = param.inputDir
  sel = param.sel
  fitMode = param.fitMode
  histoName = param.histoName
  fitRange = param.fitRange
  sidebandRange = param.sidebandRange

  if (param.SBMode):
    print("--->Signal + Background fit\n")
    print("------>Working on signal processes:")
    for Sgn in sgnProcesses:
      print(" " + Sgn)
    print("\n")
    print("------>Working on background processes:")
    for Bkg in bkgProcesses:
      print(" " + Bkg)
    print("\n")
    print("------>Will apply fit function ")
    print(" " + sgnFunction)
    print(" +")
    print(" " + bkgFunction)
    print("\n")
  else:
    print("--->Signal Only fit")
    print("------>Working on signal processes:")
    for Sgn in sgnProcesses:
      print(" " + Sgn)
    print("\n")
    print("------>Will apply fit function ")
    print(" " + sgnFunction)
    print("\n")

  sgnHistos,bkgHistos,sumHistos = mapHistos(histoName, sel)
 
  #sgnHistos = ModelNewSignal(sgnHistos)
  for sgnKey in sgnHistos:
    print(sgnKey)
    print(sgnHistos[sgnKey][0].Integral())
  for bkgKey in bkgHistos:
    print(bkgKey)
    print(bkgHistos[bkgKey][0].Integral())
  print('sum')
  print(sumHistos.Integral())

  x = ROOT.RooRealVar("m leptonic recoil", "m leptonic recoil", sumHistos.GetXaxis().GetXmin(), sumHistos.GetXaxis().GetXmax())
  
  #default parameters' settings
  peak = sumHistos.GetXaxis().GetBinCenter(sumHistos.GetMaximumBin())
  mean = ROOT.RooRealVar("mean", "mean", peak, peak - 1.0, peak + 1.0)
  sigma = ROOT.RooRealVar("sigma", "width", 0.25, 0.2, 0.4)
  #sigma = ROOT.RooRealVar("sigma", "width", 0.25, 0.2, 3.0)
  alphaR = ROOT.RooRealVar("alphaiR", "alpha of Crystal Ball", -1.0, -5.0, -0.5)
  alphaL = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.0, 0.3, 5.0)
  n = ROOT.RooRealVar("n", "n of Crystal Ball", 5.0, 0.0, 200.0)
  mean2 = ROOT.RooRealVar("mean2", "mean of gaussian", peak, peak -5.0, peak + 5.0)
  sigma2 = ROOT.RooRealVar("sigma2", "width of gaussian", -5, -1.0, 0.0)

  #higgs region
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.0, 0.8, 5.0)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 5.0, 0.0, 200.0)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 1.0, 0.8, 5.0)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 5.0, 0.0, 200.0)

  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.653, 1.653, 1.653)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 3.28, 3.28, 3.28)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 1.040, 1.040, 1.040)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 0.973, 0.973, 0.973)

  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.610, 1.610, 1.610)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 3.32, 3.32, 3.32)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.936, 0.936, 0.936)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.098, 1.098, 1.098)

  #Z region
  alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.0, 0.7, 10.0)
  n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 5.0, 0.0, 200.0) 
  alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 1.0, 0.7, 10.0)
  n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 5.0, 0.0, 200.0) 
  
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.200, 1.200, 1.200)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 2.298, 2.298, 2.298) 
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.743, 0.743, 0.743)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.290, 1.290, 1.290)

  #IDEAtrkCovBES
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.333, 1.333, 1.333)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 36, 36, 36) 
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.834, 0.834, 0.834)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 0.930, 0.930, 0.930)

  #CLDtrkCov
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.519, 1.519, 1.519)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 4.18, 4.18, 4.18) 
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.959, 0.959, 0.959)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.171, 1.171, 1.171)
  
  #CLDtrkCovBES
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.0, 0.7, 20.0)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 5.0, 0.0, 200.0)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 1.0, 0.7, 20.0)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 5.0, 0.0, 200.0)
  
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.622, 1.622, 1.622)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 4.08, 4.08, 4.08)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.706, 0.706, 0.706)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.104, 1.104, 1.104)

  #IDEA 2021spring
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 2.102, 2.102, 2.102)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 2.14, 2.14, 2.14)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.727, 0.727, 0.727)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.007, 1.007, 1.007)

  #IDEA 2021spring noBES
  #alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.637, 1.637, 1.637)
  #n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 3.32, 3.32, 3.32)
  #alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.925, 0.925, 0.925)
  #n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.111, 1.111, 1.111)
 
  c = ROOT.RooRealVar("c", "constant of Exponential", -0.3, -0.4, 0.0)
  sig_p0 = ROOT.RooRealVar("sig_p0", "p0 of polynomial", -5.0, 5.0)
  sig_p1 = ROOT.RooRealVar("sig_p1", "p1 of polynomial", -2.0, 2.0)
  sig_p2 = ROOT.RooRealVar("sig_p2", "p2 of polynomial", -3.0, 3.0)
  sig_p3 = ROOT.RooRealVar("sig_p3", "p3 of polynomial", -3.0, 3.0)
  sig_p4 = ROOT.RooRealVar("sig_p4", "p4 of polynomial", -3.0, 3.0)
  
  
  p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -5.0, 5.0)
  p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -2.0, 2.0)
  p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -3.0, 3.0)
  p3 = ROOT.RooRealVar("p3", "p3 of polynomial", -3.0, 3.0)
  p4 = ROOT.RooRealVar("p4", "p4 of polynomial", -3.0, 3.0)
  
  sigfrac = ROOT.RooRealVar("sigfrac","fraction of component 1 in signal",0.5,0.,1.)
  #passing parameters from configuration code
  if hasattr(param, 'mean'):
    mean = param.mean
  if hasattr(param, 'sigma'):
    sigma = param.sigma
  if hasattr(param, 'alpha_L'):
    alpha_L = param.alpha_L
  if hasattr(param, 'n_L'):
    n_L = param.n_L
  if hasattr(param, 'alpha_H'):
    alpha_H = param.alpha_H
  if hasattr(param, 'n_H'):
    n_H = param.n_H
  if hasattr(param, 'p0'):
    p0 = param.p0
  if hasattr(param, 'p1'):
    p1 = param.p1
  if hasattr(param, 'p2'):
    p2 = param.p2
  if hasattr(param, 'p3'):
    p3 = param.p3
  if hasattr(param, 'p4'):
    p4 = param.p4
  if hasattr(param, 'sig_p0'):
    sig_p0 = param.sig_p0
  if hasattr(param, 'sig_p1'):
    sig_p1 = param.sig_p1
  if hasattr(param, 'sig_p2'):
    sig_p2 = param.sig_p2
  if hasattr(param, 'sig_p3'):
    sig_p3 = param.sig_p3
  if hasattr(param, 'sig_p4'):
    sig_p4 = param.sig_p4

  
  nsig_init = 0.0
  nmax = 0.0
  for keySgn in sgnHistos:
    nsig_init += sgnHistos[keySgn][0].Integral()
    nmax += sgnHistos[keySgn][0].Integral()
  nsig  = ROOT.RooRealVar("nsig", "number of signal events", nsig_init, 0.2*nsig_init, 1.5*nmax)
  if(SBMode):
    nbkg_init = 0.0
    for keyBkg in bkgHistos:
      nbkg_init += bkgHistos[keyBkg][0].Integral()
      nmax += bkgHistos[keyBkg][0].Integral()
    nbkg  = ROOT.RooRealVar("nbkg", "number of background events", nbkg_init, 0.2*nbkg_init, 1.5*nmax)
  
  #c = ROOT.RooRealVar("c", "constant of Exponential", -0.3, -0.4, 0.0)
  #sig_p0 = ROOT.RooRealVar("sig_p0", "p0 of polynomial", -5.0, 5.0)
  #sig_p1 = ROOT.RooRealVar("sig_p1", "p1 of polynomial", -2.0, 2.0)
  #sig_p2 = ROOT.RooRealVar("sig_p2", "p2 of polynomial", -3.0, 3.0)
  #sig_p3 = ROOT.RooRealVar("sig_p3", "p3 of polynomial", -3.0, 3.0)
  #sig_p4 = ROOT.RooRealVar("sig_p4", "p4 of polynomial", -3.0, 3.0)


  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -5.0, 5.0)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -2.0, 2.0)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -3.0, 3.0)
  #p3 = ROOT.RooRealVar("p3", "p3 of polynomial", -3.0, 3.0)
  #p4 = ROOT.RooRealVar("p4", "p4 of polynomial", -3.0, 3.0)

  
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00029, -0.00029)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000449, -0.0000449)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", 0.000000017, 0.000000017)
  
  #IDEA
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", 0.0052, 0.0052)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000118, -0.0000118)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.000000446, -0.000000446)

  #IDEABES  
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00129, -0.00129)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000351, -0.0000351)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", 0.000000005, 0.000000005)

  #IDEABES ZZ+WW
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", 0.031, 0.031)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", 0.000049, 0.000049)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.000001843, -0.000001843)

  #CLD
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00292, -0.00292)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.00005568, -0.00005568)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", 0.000000215, 0.000000215)

  #CLD BES
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", 0.0031, 0.0031)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000282, -0.0000282)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.000000248, -0.000000248)

  #IDEA 2021spring ZZ
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", 0.0240, 0.0240)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0002000, -0.0002000)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.000000021, -0.000000021)

  #IDEA 2021spring WW
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -2.879, -2.879)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", 0.0484, 0.0484)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.0001944, -0.0001944)

  #IDEA 2021spring ZZ
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00118, -0.00118)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000183, -0.0000183)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.000000018, -0.000000018)
  #p3 = ROOT.RooRealVar("p3", "p3 of polynomial", -0.000000000674, -0.000000000674)

  #IDEA 2021spring WW
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -1.751, -1.751)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", 0.0090, 0.0090)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", 0.000297, 0.000297)
  #p3 = ROOT.RooRealVar("p3", "p3 of polynomial", -0.000001834, -0.000001834)

  #IDEA 2021spring ZZ noBES
  #p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00387, -0.00387)
  #p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000158, -0.0000158)
  #p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.0000000123, -0.0000000123)

  #signal = []
  #background = []

  model = buildModel()
  #signal.Print()
  #background.Print()
  signal.Print()
  model.Print()
  hist = ROOT.RooDataHist("data", "data", ROOT.RooArgList(x), sumHistos)  
  #fitresult = model.fitTo(hist,ROOT.RooFit.Save(),ROOT.RooFit.NumCPU(8,0),ROOT.RooFit.Extended(True),ROOT.RooFit.Optimize(False),ROOT.RooFit.Offset(True),ROOT.RooFit.Minimizer("Minuit2","migrad"),ROOT.RooFit.Strategy(2))
  fitResult = runFit()
  plot()

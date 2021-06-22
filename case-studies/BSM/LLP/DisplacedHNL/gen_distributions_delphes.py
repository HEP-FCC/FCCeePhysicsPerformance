# Author: Suchita Kulkarni
# Email: suchita.kulkarni@gmail.com
import numpy as np
import sys, os
import ROOT
import argparse, glob, random
from ROOT import TFile, TH1F
import math
#from helpers import *
#t = lxy*m/pt
M_PI = 3.14

elementary_PID = [11, 13, 14, 16, 18, 22]
#os.system('')
ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

speed_of_light = 3E8 #m/s
outdir = './output'
if not os.path.exists(outdir):os.mkdir(outdir)

chain = ROOT.TChain("Delphes")
#inputfile = '/home/kulkarni_suchita/physics_codes/MG5_setup/MG5_setup/MG5_aMC_v2_8_2/sig_schannel/Events/run_01/unweighted_events.root'
inputfile = '../test_sample/HNL_50cm_electron/HNL_50cm_electron_0.root'
chain.Add(inputfile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchJet = treeReader.UseBranch("GenJet")
branchElectron = treeReader.UseBranch("Electron")
branchGenPtcl = treeReader.UseBranch("Particle")

outFileName = outdir+'/validation_from_hepmc.root'
outHistFile = ROOT.TFile.Open( outFileName ,"RECREATE")
# Histograms
hjetpT = ROOT.TH1D("pTj1","p_{T}(j_1)" ,50, 0 ,50)
hsubjetpT = ROOT.TH1D("pTj2","p_{T}(j_2)" ,70, 0, 35)
hinvmass = ROOT.TH1D("invmass","M_{j1, j2, e}" ,70 ,0 ,105)
helectronpT = ROOT.TH1D("pTelectron", "p_{T}(electron)", 50, 0, 50)
hLxy = ROOT.TH1D("transDispHNL", "Transverse displacement of the HNL", 70, 0, 2000)
ht = ROOT.TH1D("tDistribution", "Time distribution of the HNL", 50, 0, 0.000000016)
hpid = ROOT.TH1D("PIDs", "PIDs of HNL daughters", 150, 0, 15)
hinvmassmc = ROOT.TH1D("invmassMC","MC invariant mass" ,80, 0, 100)
hnjets = ROOT.TH1D("njets", "Number of jets", 14, 0, 14)
hnelectrons = ROOT.TH1D("nelectrons", "Number of electrons", 4, 0, 4 )
hHNLmass = ROOT.TH1D("HNLmass", "HNL mass", 150, 0, 60000)
hminDeltaR = ROOT.TH1D("DeltaR", "DeltaR", 50, 0, 5)
hePsudorapidity = ROOT.TH1D("lepton_pseudorapidity", "lepton pseudorapidity", 50, -5, 5)
hjetPsudorapidity = ROOT.TH1D("jet_pseudorapidity", "jet pseudorapidity", 50, -5, 5)
hHNLpT = ROOT.TH1D("HNLpT", "HNL pT", 80, 0, 40)
obj = ROOT.TObject()
particle = ROOT.GenParticle()

# Start of counters
total = 0
count = 0
totalJet0Counter = 0
totalJet2Counter = 0
totalJet1Counter = 0
totalJetsMoreThan1Counter = 0


# Loop over all events
for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)
  # genptclarray is apparently NOT an array, it only saves the number of particles 
  genptclarray = branchGenPtcl.GetEntries()
  # Iterate over that number of particles
  for i in range(genptclarray):
      # get the particle id
      ptclpid = branchGenPtcl.At(i).PID
      # get the status of particle
      ptclstatus = branchGenPtcl.At(i).Status
      # check if particle has PID of Heavy Neutral Lepton
      if abs(ptclpid) == 9900012:
          # pT of the HNL
          hHNLpT.Fill(branchGenPtcl.At(i).PT) 
          #print ('The mass of the HNL: ', branchGenPtcl.At(i).Mass)
          # get the position of first dark quarks in array of genptclarray to which zprime decays
          # finding the position of the first daughter of the HNL
          daut1 = branchGenPtcl.At(i).D1
          #print ('daut1: ', daut1)
          # get the position of first dark quarks in array of genptclarray to which zprime decays
          # finding the position of the third daughter of the HNL
          daut2 = branchGenPtcl.At(i).D2
          #print ('daut2: ', daut2)
          # finding the position of the second daughter of the HNL
          daut3 = daut1 + 1
          #print ('daut3: ', daut3)
          # checking the PID of the daughters
          daut1pid = abs(branchGenPtcl.At(daut1).PID)
          #print ('The PID of the first daughter is: ', daut1pid)
          daut2pid = abs(branchGenPtcl.At(daut2).PID)
          #print ('The PID of the third daughter is: ', daut2pid)
          daut3pid = abs(branchGenPtcl.At(daut3).PID)
          #print ('The PID of the second daughter is: ', daut3pid)
          # compute the invarint mass of the HNL from the three daughter particles
          mcinvmass = (branchGenPtcl.At(daut1).P4() + branchGenPtcl.At(daut2).P4() + branchGenPtcl.At(daut3).P4()).M()
          #print ('The mcinvmass is: ', mcinvmass)
          # Histogram for HNL invariant mass
          hinvmassmc.Fill(mcinvmass)
          #Calculating the transverse displacement of the HNL (Lxy)
          Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
          # Histogram for HNL Lxy
          hLxy.Fill(Lxy)
          # Calculating the time distribution of the HNL
          # NOTE: Account for the mass being in MeV
          t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 1000 * 3E8)
          # Histogram for HNL time distribution
          ht.Fill(t)
          # Histogram for pT of electron coming from HNL
          helectronpT.Fill(branchGenPtcl.At(daut1).PT)
          # Taking care of the misidentification of electrons to jets in the program by using the DeltaR function
          # Counting the total number of electrons per event among the daughters of the HNL and calculating the distance between the e and jets
          eCounter = 0
          for i in range (daut1, daut2+1):
              if abs (branchGenPtcl.At(i).PID) == 11:       
                  eCounter = eCounter + 1
                  # pT cut for the electron at 5 GeV
                  if branchGenPtcl.At(i).PT > 5:
                      branchjetEntries = branchJet.GetEntries()
                      drmin = 10000
                      jetCounter = 0
                      # looping over all jets present in branchJet
                      for j in range (branchjetEntries):
                          # pT cut for the jet at 5 GeV
                          if branchJet.At(j).PT > 5:
                              # calculate deltaR between the e and the jet from branchJet
                              # for that first creating the vectors required
                              velectron = ROOT.TVector3()
                              vjet = ROOT.TVector3()
                              velectron.SetPtEtaPhi(branchGenPtcl.At(i).PT , branchGenPtcl.At(i).Eta , branchGenPtcl.At(i).Phi)
                              vjet.SetPtEtaPhi(branchJet.At(j).PT , branchJet.At(j).Eta , branchJet.At(j).Phi)
                              deltaR = velectron.DeltaR(vjet)
                              # also finding the pseudorapidity usin these vectors
                              ePsudorapidity = velectron.Eta()
                              jetPsudorapidity = vjet.Eta()
                              # to calculate the minimum distance between the electron and the closest jet
                              # uncomment the following three lines and comment hminDeltaR.Fill(deltaR)
                              #if deltaR < drmin:
                                  #drmin = deltaR
                      #hminDeltaR.Fill(drmin)
                             #calculating the no. of jets when deltaR > 0.1 
                              if deltaR > 0.1:
                                  jetCounter = jetCounter + 1
                      hnjets.Fill(jetCounter)
                      if jetCounter == 0:
                          totalJet0Counter = totalJet0Counter + 1
                      if jetCounter == 2:
                          totalJet2Counter = totalJet2Counter + 1
                      if jetCounter == 1:
                          totalJet1Counter = totalJet1Counter + 1
                      if jetCounter > 1:
                          totalJetsMoreThan1Counter = totalJetsMoreThan1Counter + 1 
                      hminDeltaR.Fill(deltaR)
                      # Histogram for pseudorapidity
                      hePsudorapidity.Fill(ePsudorapidity)
                      hjetPsudorapidity.Fill(jetPsudorapidity)
          # Histogram for the electron counter
          hnelectrons.Fill(eCounter)
          #if eCounter == 1:
          #Counting the total number of electrons for all events
          total = total + eCounter
          #Checking for how many events the HNL branches to e and W--> e, v          
          if abs (branchGenPtcl.At(daut1).PID) is not 11:
              count = count + 1 
          #print ('Total number of electrons: ', total)

  # check if the events contain at least one jet
  if branchJet.GetEntries() > 0:
     #print (branchJet.GetEntries())
     jet = branchJet.At(0)
     #hnjets.Fill(branchJet.GetEntries())
  # If event contains at least 1 jet
  #print ('number of jets: ' , branchJet.GetEntries())
  if branchJet.GetEntries() >= 2:
      # Take first jet
      jet = branchJet.At(0)
      # Histogram for jet1 pT 
      hjetpT.Fill(jet.PT)
      jet1 = branchJet.At(1)
      # Histogram for jet2 pT
      hsubjetpT.Fill(jet1.PT)
      # Calculating the invariant mass from the jets and the lepton
      hinvmass.Fill(((jet.P4()) + (jet1.P4()) + (branchGenPtcl.At(daut1).P4())).M())
      jet = branchJet.At(0);
      #helectronpT.Fill(branchGenPtcl.At(daut1).PT)


outHistFile.Write()
outHistFile.Close()

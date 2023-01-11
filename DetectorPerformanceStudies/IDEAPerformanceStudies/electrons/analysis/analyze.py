#
# author: Lia Lavezzi - University of Torino & INFN - lia.lavezzi@to.infn.it                                                                                                                              
#

from EventStore import EventStore
import ROOT
import numpy as np
import math
import pandas as pd
import os
import re
from array import array

###################################################
#               SETTINGS 
basepath = os.environ['SIM_OUTPUT_DIR']+"/conv/"
pdg='e'
l_theta = [10, 30, 50, 70, 89]
l_ptot  = [0.5, 1, 2, 5, 10] 

###################################################
# DO NOT TOUCH FROM HERE ON ...it should work as it is!

# list of output graphs
l_graph = []

# output file 
output=ROOT.TFile("output.root", "RECREATE")

magfield=2 # T CHECK it must not be hardcoded
print("ciao") 

# loop over theta
for th in enumerate(l_theta) :
  
    # need array of double for the TGraph 
    a_ptot = array("d")
    a_resolution = array("d")

    # loop on total momentum ptot
    for pp in enumerate(l_ptot) :

        theta=th[1]
        ptot=pp[1]
        print("---------------_> theta",theta, "momentum",ptot)
        suffix= str(pdg)+"_"+str(theta)+"_"+str(ptot)

        # get mc file and tree ----------------------------------
        mpath=basepath+"mctrack/"
        mname="MCData00001_"+suffix
        print("reading MC file:",mpath+mname+".root")
        mtreename = "S_MCParticlePrimTracks"
        try :
            mstore = EventStore(mpath+mname+".root")
        except :
            print("file",mpath+mname+".root","not found!")
            continue

        # get reco file and tree --------------------------------
        rpath=basepath+"track/"
        rname="EDMTracks_"+suffix
        print("reading RECO file:",rpath+rname+".root") 
        rtreename = "recoTracks"
        rstore = EventStore(rpath+rname+".root")
        
        # mc lists ------------------------------------------
        l_m_pt = []
        
        # reco lists ----------------------------------------
        l_r_eventID = []
        l_r_d0 = []
        l_r_phi   = []
        l_r_omega  = []
        l_r_z0 = []
        l_r_tanlam = []
        l_r_pt = []
        l_resid = []
        
        # mc loop on events ---------------------------------
        for i, event in enumerate(mstore):
            mctrack = event.get(mtreename)
            #  print("event no.",i,"has",len(mctrack),"MC tracks")
            for m in mctrack :
                mcpt = np.sqrt(m.getMomentum().x * m.getMomentum().x + m.getMomentum().y * m.getMomentum().y) # [MeV]
                mcpt=mcpt*1.e-3 # [GeV]
                l_m_pt.append(mcpt)
                
        print("mc done")
                
        # reco loop on events -------------------------------
        for j, event in enumerate(rstore):
            
            track = event.get(rtreename)
            # print("event no.",j,"has",len(track),"tracks")
            
            for t in track :

                chi2 = t.getChi2()
                dedx = t.getDEdx()
                dedx_err = t.getDEdxError()
                ndf = t.getNdf()
                objectID = t.getObjectID()
                rad_inner = t.getRadiusOfInnermostHit()
                subdet_hitno = t.getSubDetectorHitNumbers()
                state = t.getTrackStates()
                hits = t.getTrackerHits()
                tr = t.getTracks()
                ty = t.getType()
                
                # edm4hep::TrackState --> state                                                                                                                                                                
                # AtCalorimeter, AtFirstHit, AtIP, AtLastHit, AtOther, AtVertex
                # D0, phi, omega, Z0, tanLambda
                st = state.at(0)
                d0=st.D0
                phi=st.phi
                omega=st.omega # signed curvature [1./mm]
                z0=st.Z0
                tanlam=st.tanLambda

                R = 1e-3/omega # [m]
                pt = 0.3*R*magfield

                l_r_d0.append(d0)
                l_r_phi.append(phi)
                l_r_omega.append(omega)
                l_r_z0.append(z0)
                l_r_tanlam.append(tanlam)

                # transverse momentum: pt
                l_r_pt.append(pt)
                # reco - MC transverse momentum divided by MC pt squared --> resolution for comparison with CLD 
                l_resid.append((pt-mcpt)/(mcpt*mcpt))

        print("reco done")
        print("montecarlo ",len(l_m_pt),"reconstruction",len(l_r_pt))

        # ROOT ---------------------------------------------------
        # three steps to have the right range for fitting:
        # 1 - first histo very large, to see mean/RMS
        #
        # set histo limits
        x1= -5
        x2=  5
        nbin = 100
        h_pt0=ROOT.TH1F("h_pt0_"+suffix.replace(".","_"),"reconstructed pt0,"+pdg+", theta="+str(theta)+"deg, ptot="+str(ptot)+"GeV/c",nbin,x1,x2)
        for k in range(0,len(l_resid)) :
            h_pt0.Fill(l_resid[k])
        hmean = h_pt0.GetMean()
        hsigma = h_pt0.GetRMS()
        h_pt0.Delete() # Write()

        # 2 - second histo is large 3 (or 5, depending on mcpt) sigma:
        nsigma = 3
        # for low mcpt we use 5 sigma as distros are larger
        if(mcpt<0.9) :
            nsigma = 5
        #
        # set histo limits    
        x1= hmean-nsigma*hsigma
        x2= hmean+nsigma*hsigma
        nbin = 100
        # pre fill to set histo/fit limits
        h_pt1=ROOT.TH1F("h_pt1_"+suffix.replace(".","_"),"reconstructed pt1,"+pdg+", theta="+str(theta)+"deg, ptot="+str(ptot)+"GeV/c",nbin,x1,x2)
        for k in range(0,len(l_resid)) :
            h_pt1.Fill(l_resid[k])
        hmean  = h_pt1.GetMean()
        hsigma = h_pt1.GetRMS()
        hmax = h_pt1.GetMaximum()
        bin1 = h_pt1.FindFirstBinAbove(hmax*0.5)-1;
        bin2 = h_pt1.FindLastBinAbove(hmax*0.5)+1;
        fwhm = h_pt1.GetBinCenter(bin2) - h_pt1.GetBinCenter(bin1);
        h_pt1.Delete() # Write()

        # 3 - final range for the histo: peak large enough, symmetrical w.r.t. 0 
        #
        # I want at least 30 bins in the peak to fit it
        bin_width = fwhm/30
        x1= hmean-bin_width*60;
        x2= hmean+bin_width*60;
        # low momentum distributions are larger
        if(mcpt<0.9) :
            bin_width = fwhm/20
            x1= hmean-bin_width*80;
            x2= hmean+bin_width*80;
        #
        # make the histo symmetrical w.r.t. 0    
        if(ROOT.TMath.Abs(x1) > ROOT.TMath.Abs(x2)) :
            x2 = -x1
        else : 
            x1 = -x2
        #
        # set number of bins without changing the bin_width
        nbin = (int) ((x2-x1)/bin_width)
        #
        # final histo
        h_pt=ROOT.TH1F("h_pt_"+suffix.replace(".","_"),"reconstructed p_{T}-p_{T,MC}/p_{T,MC}^{2},"+pdg+", theta="+str(theta)+"deg, ptot="+str(ptot)+"GeV/c",nbin,x1,x2)
        for k in range(0,len(l_resid)) :
            h_pt.Fill(l_resid[k])
        hmean = h_pt.GetMean();
        hsigma = h_pt.GetRMS()

        # ---------------------------------------------------------------- FIT
        # set limits for the fitting functions
        x1 = hmean-3*hsigma
        x2 = hmean+3*hsigma
        # fitting function
        func=ROOT.TF1("func","gaus",x1,x2)
        h_pt.Fit(func,"RQ")
        param=func.GetParameters()
        h_pt.Write()

        # sigma = resolution
        a_resolution.append(param[2])
        a_ptot.append(ptot)
        print("->->-> theta",theta,"ptot",ptot,"resolution",param[2])
    
    # resolution vs ptot
    g1 = ROOT.TGraph(len(l_ptot),a_ptot,a_resolution)
    g1.SetName("g_"+str(theta))
    g1.Write()   
    l_graph.append(g1)

# ------------------------------------------------------ PLOT the multigraph
color = [4, 2, 6, 3, 1]
m_style = [26, 25, 27, 28, 24]
x0_leg = 0.6
y0_leg = 0.8
xwidth_leg = 0.2
ywidth_leg = 0.1
leg = ROOT.TLegend(x0_leg, y0_leg, x0_leg + xwidth_leg, y0_leg + ywidth_leg)

mg = ROOT.TMultiGraph()
for i in range(0, len(l_graph)) :
    l_graph[i].SetMarkerStyle(m_style[i])
    l_graph[i].SetMarkerColor(color[i])
    l_graph[i].SetLineColor(color[i])
    l_graph[i].SetMarkerSize(1.4)
    l_graph[i].SetLineWidth(2)
    l_graph[i].SetName("g_"+str(l_theta[i]))
    leg.AddEntry(l_graph[i],"#theta = "+str(l_theta[i])+" deg")
    mg.Add(l_graph[i],"cp");

c1=ROOT.TCanvas()
c1.SetName("c1")
c1.SetGridx()
c1.SetGridy()
c1.SetLogx()
c1.SetLogy()
mg.GetXaxis().SetRangeUser(0.4,100)
mg.GetYaxis().SetRangeUser(1e-5,1)

mg.Draw("APL")
leg.Draw("same")
c1.Print("./g1.png") 
print("end")

output.Write()
output.Close()

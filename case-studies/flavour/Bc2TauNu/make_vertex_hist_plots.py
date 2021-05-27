import sys, os, argparse
import json
import numpy as np
from uncertainties import *
import matplotlib.pyplot as plt
from ROOT import TFile

#Local code
from userConfig import loc, train_vars, train_vars_vtx
import plotting
import utils as ut
import matplotlib.ticker as plticker

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Load ROOT file containing hists
file = TFile.Open(f"{loc.EOS}/vertex_hists.root")

hists = {"h_reco": {"hist": file.Get("h_reco"),"xname": "Number of vertices", "yname": "Density", "xrange": [0,12.1],"yrange": [0,0.4]},
         "h_mc": {"hist": file.Get("h_mc"),"xname": "Number of vertices", "yname": "Density", "xrange": [0,12.1],"yrange": [0,0.4]},
         "h_recoeff_SV_3trk": {"hist": file.Get("h_recoeff_SV_3trk"), "xname": "Number of MC tracks", "yname": "Fraction reco. as three-track vertex", "xrange": [0,7.1], "yrange": [0.,1.]}
         }

for h in hists:
    hists[h]["bins"] = hists[h]["hist"].GetNbinsX()
    hists[h]["contents"] = []
    hists[h]["edges"] = []
    for i in range(0,hists[h]["bins"]):
        w = hists[h]["hist"].GetBinWidth(i)
        hists[h]["contents"].append(hists[h]["hist"].GetBinContent(i))
        hists[h]["edges"].append(hists[h]["hist"].GetBinCenter(i) - 0.5*w)
    #Final upper bin edge
    hists[h]["edges"].append(hists[h]["hist"].GetBinCenter(hists[h]["bins"]) + 0.5*w)

#Plot reco MC comparison
fig, ax = plt.subplots(figsize=(8,8))
reco = plt.stairs(hists["h_reco"]["contents"], hists["h_reco"]["edges"], color="crimson", linewidth=2, label="Reco. vertices")
mc = plt.stairs(hists["h_mc"]["contents"], hists["h_mc"]["edges"], color="dodgerblue", linewidth=2, label="MC vertices ($N_{\\mathrm{charged}} > 1$)")
plt.xlim(hists["h_reco"]["xrange"])
plt.ylim(hists["h_reco"]["yrange"])
ax.tick_params(axis='both', which='major', labelsize=25)
plt.xlabel(hists["h_reco"]["xname"],fontsize=30)
plt.ylabel(hists["h_reco"]["yname"],fontsize=30)
l = plticker.MultipleLocator(base=2.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(l)
plt.legend(fontsize=25)
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/mc_vs_reco_vertices.pdf")

#Plot the efficiency
fig, ax = plt.subplots(figsize=(8,8))
eff = plt.stairs(hists["h_recoeff_SV_3trk"]["contents"], hists["h_recoeff_SV_3trk"]["edges"], color="k", linewidth=2)
plt.xlim(hists["h_recoeff_SV_3trk"]["xrange"])
plt.ylim(hists["h_recoeff_SV_3trk"]["yrange"])
ax.tick_params(axis='both', which='major', labelsize=25)
plt.xlabel(hists["h_recoeff_SV_3trk"]["xname"],fontsize=30)
plt.ylabel(hists["h_recoeff_SV_3trk"]["yname"],fontsize=30)
l = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
ax.xaxis.set_major_locator(l)
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/three_track_vertex_eff.pdf")

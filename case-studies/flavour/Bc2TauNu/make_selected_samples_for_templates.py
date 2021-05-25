import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
from decay_mode_xs import modes as bkg_modes

#Local code
from userConfig import loc, mode, train_vars, train_vars_vtx, Ediff_cut
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Loaction of files used for final analysis on EOS
path = loc.ANALYSIS

modes = OrderedDict()

file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
#Signal and B+ modes
modes["Bc2TauNu"] = f"{file_prefix}_Bc2TauNuTAUHADNU"
modes["Bu2TauNu"] = f"{file_prefix}_Bu2TauNuTAUHADNU"
modes["Zbb"] = "p8_ee_Zbb_ecm91"
#Background decays
for b in bkg_modes:
    for d in bkg_modes[b]:
        modes[f"{b}_{d}"] = f"{file_prefix}_{b}2{d}"

tree = {}
events = {}
df = {}

#Cuts
BDT2_cut = 0.99 #Looser than optimal to have enough stats in each sample to plot
BDT1_cut = 0.99 #Looser than optimal to have enough stats in each sample to plot

cut = f"EVT_ThrustDiff_E > {Ediff_cut} and EVT_MVA1 > {BDT1_cut} and EVT_MVA2 > {BDT2_cut}"

for m in modes:
    print(m)
    tree[m] = uproot.open(f"{path}/{modes[m]}_sel2.root")["events"]
    df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*"])
    #Apply Ediff cut, BDT1 cut, and BDT2 cut
    df[m] = df[m].query(cut)
    print("Number of events: %s" % len(df[m]))
    #Write the dataframe to a pickle file, can be loaded in the fitting script
    df[m].to_pickle(f"{loc.PKL}/{m}_selected_for_fit.pkl")

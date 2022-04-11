import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
import pickle
from decay_mode_xs import modes as bkg_modes
from scipy import interpolate

#Local code
from userConfig import loc, train_vars, train_vars_vtx, Ediff_cut, NBin_MVA_fit
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

path = loc.ANALYSIS

modes = OrderedDict()

file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
cat = 'bu'
MVA2_name = 'EVT_MVA2_bu'
if cat == 'bc':
  MVA2_name = 'EVT_MVA2_bc'

#Background decays
for b in bkg_modes:
    for d in bkg_modes[b]:
        modes[f"{b}_{d}"] = {"name": f"{file_prefix}_{b}2{d}"}

#Cuts
bdt = {"MVA1": 0.90,
       "MVA2": 0.80
       }

cut = f"EVT_ThrustDiff_E > {Ediff_cut} and EVT_MVA1Bis > {bdt['MVA1']} and {MVA2_name} > {bdt['MVA2']}"

#Load dataframes for each mode
tree = {}
df = {}

#Make a summed sample of all modes to compare to
df_all = pd.DataFrame()

for m in modes:
    #Load samples with MVA1 > 0.9 or MVA2 > 0.8 cuts applied
    tree[m] = uproot.open(f"{path}/{modes[m]['name']}_selBase.root")["events"]
    df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*"])
    df[m] = df[m].query(cut)
    print(f"Decay mode {m} stats: {len(df[m])}")

    #log transform the BDT
    df[m]["log_EVT_MVA1"] = -np.log(1. - df[m]["EVT_MVA1Bis"])
    df[m]["log_EVT_MVA2"] = -np.log(1. - df[m][MVA2_name])

    df_all = df_all.append(df[m])


#Fit the -log(1 - MVA) distributions MVA1 > 0.90, MVA2 > 0.80, to use in efficiency evaluation above a certain cut
for x in bdt:
    bins = NBin_MVA_fit

    fig,ax = plt.subplots(figsize=(8,8))
    if(x=="MVA1"):
        xmax = 9
    else:
        xmax = 6.
    xmin = -np.log(1. - bdt[x])

    counts, bin_edges = np.histogram(df_all[f"log_EVT_{x}"], bins, range=(xmin, xmax))
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    err = np.sqrt(counts)
    print ("count in each bin.")
    print (counts)
    #Normalise
    err = err / np.sum(counts)
    counts = counts / np.sum(counts)
    plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color='k', markersize=2)

#    weights = np.divide(np.ones(err.shape), err, out=np.zeros(err.shape), where=err!=0) # gives 0 if err is 0
    weights = 1. / err
    print ("weight in each bin.")
    print (weights)

    #Cubic spline of the MVA distribution
    spline = interpolate.splrep(bin_centres, counts, w=weights)

    xvals = np.linspace(xmin, xmax, 1000)
    spline_vals = interpolate.splev(xvals, spline)

    #Save the spline to pickle for use in background efficiency determination
    with open(f'{loc.PKL}/{x}_{cat}_spline.pkl', 'wb') as f:
        pickle.dump(spline, f)

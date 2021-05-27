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
from userConfig import loc, train_vars, train_vars_vtx, Ediff_cut
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Fetch optimal cuts for NZ = 5e12 to show on plot
with open(f'{loc.JSON}/optimal_yields_5.json') as f:
  yields = json.load(f)

path = loc.ANALYSIS

modes = OrderedDict()

file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
#Background decays
for b in bkg_modes:
    for d in bkg_modes[b]:
        modes[f"{b}_{d}"] = {"name": f"{file_prefix}_{b}2{d}"}

#Cuts
bdt = {"MVA1": 0.95,
       "MVA2": 0.95
       }

cut = f"EVT_ThrustDiff_E {Ediff_cut} and EVT_MVA1 > {bdt['MVA1']} and EVT_MVA2 > {bdt['MVA2']}"

#Load dataframes for each mode
tree = {}
df = {}

#Make a summed sample of all modes to compare to
df_all = pd.DataFrame()

for m in modes:
    #Load samples with MVA > 0.95 cuts applied
    tree[m] = uproot.open(f"{path}/{modes[m]['name']}_sel2.root")["events"]
    df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*"])
    #Apply Ediff cut, BDT1 cut, and BDT2 cut
    df[m] = df[m].query(cut)
    print(f"Decay mode {m} stats: {len(df[m])}")

    #log transform the BDT
    df[m]["log_EVT_MVA1"] = -np.log(1. - df[m]["EVT_MVA1"])
    df[m]["log_EVT_MVA2"] = -np.log(1. - df[m]["EVT_MVA2"])

    df_all = df_all.append(df[m])


#Fit the -log(1 - MVA) distributions above 0.95, to use in efficiency evaluation above a certain cut
for x in bdt:
    bins = 100

    fig,ax = plt.subplots(figsize=(8,8))
    if(x=="MVA1"):
        xmax = 10.7
    else:
        xmax = 7.
    xmin = -np.log(1. - bdt[x])

    counts, bin_edges = np.histogram(df_all[f"log_EVT_{x}"], bins, range=(xmin, xmax))
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    err = np.sqrt(counts)
    #Normalise
    err = err / np.sum(counts)
    counts = counts / np.sum(counts)
    plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color='k', markersize=2)

    weights = 1./err

    #Cubic spline of the MVA distribution
    spline = interpolate.splrep(bin_centres, counts, w=weights)

    xvals = np.linspace(xmin, xmax, 1000)
    spline_vals = interpolate.splev(xvals, spline)

    plt.plot(xvals, spline_vals, color="red")

    name = x.replace("MVA", "BDT")
    plt.xlabel(f"-log(1 - {x})",fontsize=30)
    plt.xlim(xmin, xmax)
    ax.tick_params(axis='both', which='major', labelsize=25)

    cut_99_val = 0.99
    cut_99 = -np.log(1. - cut_99_val)
    plt.axvline(x=cut_99,color="dodgerblue",linestyle="--",label=f"BDT $>{cut_99_val}$")

    cut_best_val = yields[x]
    cut_best = -np.log(1. - cut_best_val)

    plt.axvline(x=cut_best,color="orange",linestyle="--",label="Optimal BDT $>%.5f$" % cut_best_val)

    x_vals_above_cut = np.linspace(cut_best,xmax,int(1000*((cut_best - xmin)/(xmax-xmin))))
    spline_vals_above_cut = interpolate.splev(x_vals_above_cut, spline)
    plt.fill_between(x_vals_above_cut,spline_vals_above_cut,color="crimson",alpha=0.2)

    #ax.get_yaxis().set_visible(False)
    plt.yscale('log')
    ymin, ymax = plt.ylim()
    plt.ylim(ymin,2*ymax)
    plt.legend(fontsize=25,loc="lower left")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{x}_spline.pdf")

    #Save the spline to pickle for use in background efficiency determination
    with open(f'{loc.PKL}/{x}_spline.pkl', 'wb') as f:
        pickle.dump(spline, f)

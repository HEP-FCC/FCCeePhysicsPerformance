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
from userConfig import loc, mode, train_vars, train_vars_vtx
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

path = loc.ANALYSIS

modes = OrderedDict()

file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
#Signal and B+ modes
modes["Bc2TauNu"] = f"{file_prefix}_Bc2TauNuTAUHADNU"
modes["Zbb"] = "p8_ee_Zbb_ecm91"

tree = {}
events = {}
df = {}

for m in modes:
    print(m)
    tree[m] = uproot.open(f"{path}/{modes[m]}_sel2.root")["events"]
    df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*"])
    #Ratio of charged to neutral energy
    df[m]["EVT_ThrustEmax_R_Echarged_Enuetral"] = df[m]["EVT_ThrustEmax_Echarged"] / df[m]["EVT_ThrustEmax_Eneutral"]
    print(f"Number of events {len(df[m])}")

vars = {"EVT_ThrustEmax_Echarged": {"name": "Maximum hemisphere charged E", "range": [0.,50.], "unit": "[GeV/$c^2$]"},
        "EVT_ThrustEmax_Eneutral": {"name": "Maximum hemisphere neutral E", "range": [0.,50.], "unit": "[GeV/$c^2$]"},
        "EVT_ThrustEmax_E": {"name": "Maximum hemisphere E", "range": [0.,50.], "unit": "[GeV/$c^2$]"},
        }


bins = 30

xvar = "EVT_ThrustEmax_Echarged"
yvar = "EVT_ThrustEmax_Eneutral"

for m in modes:

    fig, ax = plt.subplots(figsize=(8,8))

    plt.hist2d(df[m][xvar], df[m][yvar], bins=bins, range = [vars[xvar]["range"], vars[yvar]["range"]], density=True)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(vars[xvar]["range"][0], vars[xvar]["range"][1])
    plt.ylim(vars[yvar]["range"][0], vars[yvar]["range"][1])
    plt.xlabel(vars[xvar]["name"]+" "+vars[xvar]["unit"],fontsize=30)
    plt.ylabel(vars[yvar]["name"]+" "+vars[yvar]["unit"],fontsize=30)
    plt.tight_layout()

    fig.savefig(f"{loc.PLOTS}/{m}_{xvar}_vs_{yvar}.pdf")

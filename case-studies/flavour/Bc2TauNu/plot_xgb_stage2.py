import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import joblib
import uproot
#from root_pandas import read_root, to_root

#Local code
from userConfig import loc, mode, train_vars, train_vars_vtx, train_vars_2
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

vars_list = train_vars_2.copy()

# Load trained model
bdt = joblib.load(f"{loc.BDT}/xgb_bdt_stage2.joblib")

MVA1_cut = 0.6

#Load samples

#Bc -> tau nu signal
path = f"{loc.TRAIN2}"
all_vars = vars_list.copy()
all_vars.append("CUT_CandTruth")
all_vars.append("CUT_CandRho")
all_vars.append("CUT_CandVtxThrustEmin")
all_vars.append("EVT_CandMass")
tree_sig = uproot.open(f"{path}/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU.root")["events"]
df_sig = tree_sig.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = 500000)
df_sig = df_sig.query(f"EVT_MVA1Bis > {MVA1_cut} and CUT_CandTruth==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
df_sig = df_sig[vars_list]
df_sig["BDT"] = bdt.predict_proba(df_sig).tolist()
df_sig["BDT"] = df_sig["BDT"].apply(lambda x: x[1])

#Bu -> tau nu signal
path = f"{loc.TRAIN2}"
tree_Bu = uproot.open(f"{path}/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.root")["events"]
df_Bu = tree_Bu.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = 500000)
df_Bu = df_Bu.query(f"EVT_MVA1Bis > {MVA1_cut} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
df_Bu = df_Bu[vars_list]
df_Bu["BDT"] = bdt.predict_proba(df_Bu).tolist()
df_Bu["BDT"] = df_Bu["BDT"].apply(lambda x: x[1])

#Z -> qq inclusive
tree_bkg = {}
df_bkg = {}
x_bkg = {}
y_bkg = {}
bkgs = {"uds": ["#d1e5f0","q\\bar{q}"],
        "cc": ["#92c5de","c\\bar{c}"],
        "bb": ["#2166ac","b\\bar{b}"]
        }
for q in bkgs:
    tree_bkg[q] = uproot.open(f"{path}/p8_ee_Z{q}_ecm91.root")["events"]
    df_bkg[q] = tree_bkg[q].arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = 500000)
    df_bkg[q] = df_bkg[q].query(f"EVT_MVA1Bis > {MVA1_cut} and CUT_CandTruth==0 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
    df_bkg[q] = df_bkg[q][vars_list]
    df_bkg[q]["BDT"] = bdt.predict_proba(df_bkg[q]).tolist()
    df_bkg[q]["BDT"] = df_bkg[q]["BDT"].apply(lambda x: x[1])

fig, ax = plt.subplots(figsize=(12,8))
xmin = 0
xmax = 1
bins_bkg = int(np.sqrt(len(df_bkg["cc"])))
bins_sig = int(np.sqrt(len(df_sig)))
plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='step',linewidth=1.5)
plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='stepfilled',alpha=0.3,linewidth=1.5,label="$B_c^+ \\to \\tau^+ \\nu_\\tau$")
plt.hist(df_Bu["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="k",histtype='step',linewidth=1.5,label="$B^+ \\to \\tau^+ \\nu_\\tau$")
for q in bkgs:
    plt.hist(df_bkg[q]["BDT"],bins=bins_bkg,range=(xmin,xmax),density=True,color=bkgs[q][0],histtype='step',linewidth=1.5,label="Inc. $Z^0 \\to %s$" % bkgs[q][1])
ax.tick_params(axis='both', which='major', labelsize=25)
plt.xlim(xmin,xmax)
plt.xlabel("BDT2 score",fontsize=30)
plt.ylabel("Normalised counts",fontsize=30)
plt.yscale('log')
ymin,ymax = plt.ylim()
plt.ylim(ymin,50*ymax)
plt.legend(fontsize=25, loc="upper left")
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/Bc2TauNu_vs_inclusive_Z_uds_cc_bb_BDT_stage2.pdf")

#Plot efficiency as a function of BDT cut in each sample
BDT_cuts = np.linspace(0,999,999)
N_sig = len(df_sig)
N_Bu = len(df_Bu)
N_Zuds = len(df_bkg["uds"])
N_Zcc = len(df_bkg["cc"])
N_Zbb = len(df_bkg["bb"])
eff_sig = []
eff_Bu = []
eff_bkg = {}
N_bkg = {}
for q in bkgs:
    eff_bkg[q] = []
    N_bkg[q] = len(df_bkg[q])
cut_vals = []
for x in BDT_cuts:
    cut_val = float(x)/100
    cut_vals.append(cut_val)
    eff_sig.append(float(len(df_sig.query("BDT > %s" % cut_val))) / N_sig)
    eff_Bu.append(float(len(df_Bu.query("BDT > %s" % cut_val))) / N_Bu)
    for q in bkgs:
        eff_bkg[q].append(float(len(df_bkg[q].query("BDT > %s" % cut_val))) / N_bkg[q])

fig, ax = plt.subplots(figsize=(12,8))

plt.plot(cut_vals, eff_sig, color="#b2182b",label="$B_c^+ \\to \\tau^+ \\nu_\\tau$")
plt.plot(cut_vals, eff_Bu, color="k",label="$B^+ \\to \\tau^+ \\nu_\\tau$")
for q in bkgs:
    plt.plot(cut_vals, eff_bkg[q], color=bkgs[q][0],label="Inc. $Z^0 \\to %s$" % bkgs[q][1])

ax.tick_params(axis='both', which='major', labelsize=25)
plt.xlim(xmin,xmax)
plt.xlabel("BDT2 score",fontsize=30)
plt.ylabel("Efficiency",fontsize=30)
plt.yscale('log')
ymin,ymax = plt.ylim()
plt.ylim(ymin,2)
plt.legend(fontsize=25, loc="lower left")
plt.grid(alpha=0.4,which="both")
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/Bc2TauNu_vs_inclusive_Z_uds_cc_bb_BDT_eff_stage2.pdf")

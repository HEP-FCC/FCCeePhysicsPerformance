import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import joblib

#Local code
from userConfig import loc, train_vars, train_vars_vtx, FCC_label
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)


def run(vars, sig):
    # Load trained model
    bdt = joblib.load(f"{loc.BDT}/xgb_bdt_{sig}_{vars}.joblib")

    #Bc -> tau nu signal
    if(vars=="normal"):
        vars_list = train_vars
    elif(vars=="vtx"):
        vars_list = train_vars_vtx

    #Load samples

    #Bc -> tau nu signal
    path = f"{loc.PKL}"
    df_Bc = pd.read_pickle(f"{path}/Bc2TauNu.pkl")
    df_Bc = df_Bc[vars_list]
    df_Bc["BDT"] = bdt.predict_proba(df_Bc).tolist()
    df_Bc["BDT"] = df_Bc["BDT"].apply(lambda x: x[1])

    #Bu -> tau nu signal
    df_Bu = pd.read_pickle(f"{path}/Bu2TauNu.pkl")
    df_Bu = df_Bu[vars_list]
    df_Bu["BDT"] = bdt.predict_proba(df_Bu).tolist()
    df_Bu["BDT"] = df_Bu["BDT"].apply(lambda x: x[1])

    df_sig = df_Bc
    df_other = df_Bu
    sig_label = '$B_c^+ \\to \\tau^+ \\nu_\\tau$'
    other_label = '$B^+ \\to \\tau^+ \\nu_\\tau$'
    if sig == 'Bu2TauNu' or sig == 'BuBc':
      df_sig = df_Bu
      df_other = df_Bc
      sig_label = '$B^+ \\to \\tau^+ \\nu_\\tau$'
      other_label = '$B_c^+ \\to \\tau^+ \\nu_\\tau$'

    #Z -> qq inclusive
    df_bkg = {}
    x_bkg = {}
    y_bkg = {}
    bkgs = {"uds": ["#d1e5f0","q\\bar{q}"],
            "cc": ["#92c5de","c\\bar{c}"],
            "bb": ["#2166ac","b\\bar{b}"]
            }
    for q in bkgs:
        df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")
        df_bkg[q] = df_bkg[q].sample(n=200000,random_state=100)
        df_bkg[q] = df_bkg[q][vars_list]
        df_bkg[q]["BDT"] = bdt.predict_proba(df_bkg[q]).tolist()
        df_bkg[q]["BDT"] = df_bkg[q]["BDT"].apply(lambda x: x[1])

    fig, ax = plt.subplots(figsize=(12,8))
    xmin = 0
    xmax = 1
    bins_bkg = int(np.sqrt(len(df_bkg["cc"])))
    bins_sig = int(np.sqrt(len(df_sig)))
    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='step',linewidth=1.5, label=sig_label)
#    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='stepfilled',alpha=0.3,linewidth=1.5,label=sig_label)
    plt.hist(df_other["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#508273",histtype='step',linewidth=1.5,label=other_label)
    for q in bkgs:
        plt.hist(df_bkg[q]["BDT"],bins=bins_bkg,range=(xmin,xmax),density=True,color=bkgs[q][0],histtype='step',linewidth=1.5,label="Inc. $Z^0 \\to %s$" % bkgs[q][1])
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.set_title( FCC_label, loc='right', fontsize=20)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Normalised counts",fontsize=30)
    plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,50*ymax)
    plt.legend(fontsize=25, loc="upper left")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{sig}_vs_inclusive_Z_uds_cc_bb_BDT_{vars}.pdf")

    #Plot efficiency as a function of BDT cut in each sample
    BDT_cuts = np.linspace(0,999,999)
    N_sig = len(df_sig)
    N_other = len(df_other)
    N_Zuds = len(df_bkg["uds"])
    N_Zcc = len(df_bkg["cc"])
    N_Zbb = len(df_bkg["bb"])
    eff_sig = []
    eff_other = []
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
        eff_other.append(float(len(df_other.query("BDT > %s" % cut_val))) / N_other)
        for q in bkgs:
            eff_bkg[q].append(float(len(df_bkg[q].query("BDT > %s" % cut_val))) / N_bkg[q])

    fig, ax = plt.subplots(figsize=(12,8))

    plt.plot(cut_vals, eff_sig, color="#b2182b",label=sig_label)
    plt.plot(cut_vals, eff_other, color="#508273",label=other_label)
    for q in bkgs:
        plt.plot(cut_vals, eff_bkg[q], color=bkgs[q][0],label="Inc. $Z^0 \\to %s$" % bkgs[q][1])

    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.set_title( FCC_label, loc='right', fontsize=20)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Efficiency",fontsize=30)
    plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,2)
    plt.legend(fontsize=25, loc="lower left")
    plt.grid(alpha=0.4,which="both")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{sig}_vs_inclusive_Z_uds_cc_bb_BDT_eff_{vars}.pdf")


def main():
    parser = argparse.ArgumentParser(description='Plot xgb model for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    parser.add_argument("--SigName", choices=["Bc2TauNu","Bu2TauNu", "BuBc"],required=False,help="Name of signal sample used in the training",default="BuBc")
    args = parser.parse_args()

    run(args.Vars, args.SigName)

if __name__ == '__main__':
    main()

import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot
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
    processes = {"Bu":  ["Bu2TauNu", "p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU", "#b2182b", '$B^+ \\to \\tau^+ \\nu_\\tau$'],
                 "Bc":  ["Bc2TauNu", "p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU", "#508273", '$B_c^+ \\to \\tau^+ \\nu_\\tau$'],
                 "uds": ["uds", "p8_ee_Zuds_ecm91", "#d1e5f0","$Z^0 \\to q\\bar{q}$"],
                 "cc":  ["cc",  "p8_ee_Zcc_ecm91",  "#92c5de","$Z^0 \\to c\\bar{c}$"],
                 "bb":  ["bb",  "p8_ee_Zbb_ecm91",  "#2166ac","$Z^0 \\to b\\bar{b}$"]}
    df_train = {}
    df_test = {}
    N_train = {}
    N_test  = {}
 
    path_train = f"{loc.PKL}"
#    path_train = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/training_stage1"
#    path_test  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/analysis_stage1"
    for proc in processes:
      # If using pkl from process_sig_bkg_samples_for_xgb.py
      df_train[proc] = pd.read_pickle(f"{path_train}/{processes[proc][0]}.pkl") 
      df_train[proc] = df_train[proc].sample(n=500000,random_state=100)
      df_train[proc] = df_train[proc][vars_list]
      df_train[proc]["BDT"] = bdt.predict_proba(df_train[proc]).tolist()
      df_train[proc]["BDT"] = df_train[proc]["BDT"].apply(lambda x: x[1])
      N_train [proc] = len(df_train[proc])

      df_test[proc] = pd.read_pickle(f"{path_train}/{processes[proc][0]}_testing.pkl") 
      print (f'{proc}, {len(df_test[proc])}')
      df_test[proc] = df_test[proc].sample(n=500000,random_state=100)
      df_test[proc] = df_test[proc][vars_list]
      df_test[proc]["BDT"] = bdt.predict_proba(df_test[proc]).tolist()
      df_test[proc]["BDT"] = df_test[proc]["BDT"].apply(lambda x: x[1])
      N_test [proc] = len(df_test[proc])

#      # With root files directly from batch production
#      if proc == 'Bu' or proc == 'Bc':
#        N_train [proc] = uproot.open(f"{path_train}/{processes[proc][1]}/chunk0.root")["eventsProcessed"].value
#        tree_temp = uproot.open(f"{path_train}/{processes[proc][1]}/chunk0.root")["events"]
#        df_train[proc] = tree_temp.arrays(library="pd", how="zip", filter_name=["EVT_*"])
#        for f in range(1,5):
#          N_train [proc] += uproot.open(f"{path_train}/{processes[proc][1]}/chunk{f}.root")["eventsProcessed"].value
#          tree_temp = uproot.open(f"{path_train}/{processes[proc][1]}/chunk{f}.root")["events"]
#          df_temp = tree_temp.arrays(library="pd", how="zip", filter_name=["EVT_*"])
#          df_train[proc] = pd.concat([df_train[proc], df_temp])
#      else:
#        N_train [proc] = uproot.open(f"{path_train}/{processes[proc][1]}/chunk0.root")["eventsProcessed"].value
#        tree_temp = uproot.open(f"{path_train}/{processes[proc][1]}/chunk0.root")["events"]
#        df_train[proc] = tree_temp.arrays(library="pd", how="zip", filter_name=["EVT_*"])
#      df_train[proc] = df_train[proc][vars_list]
#      df_train[proc]["BDT"] = bdt.predict_proba(df_train[proc]).tolist()
#      df_train[proc]["BDT"] = df_train[proc]["BDT"].apply(lambda x: x[1])
#
#
#      N_test [proc] = uproot.open(f"{path_test}/{processes[proc][1]}/chunk0.root")["eventsProcessed"].value
#      tree_temp = uproot.open(f"{path_test}/{processes[proc][1]}/chunk0.root")["events"]
#      df_test[proc] = tree_temp.arrays(library="pd", how="zip", filter_name=["EVT_*"])
#      df_test[proc] = df_test[proc][vars_list]
#      df_test[proc]["BDT"] = bdt.predict_proba(df_test[proc]).tolist()
#      df_test[proc]["BDT"] = df_test[proc]["BDT"].apply(lambda x: x[1])
 
      print (f'{proc}:  train: {N_train[proc]},  test: {N_test[proc]} to {len(df_test[proc])}')




#    fig, ax = plt.subplots(figsize=(12,8))
#    xmin = 0
#    xmax = 1
#    bins_bkg = int(np.sqrt(len(df_bkg["cc"])))
#    bins_sig = int(np.sqrt(len(df_sig)))
#    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='step',linewidth=1.5)
#    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='stepfilled',alpha=0.3,linewidth=1.5,label=sig_label)
#    plt.hist(df_other["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="k",histtype='step',linewidth=1.5,label=other_label)
#    for q in bkgs:
#        plt.hist(df_bkg[q]["BDT"],bins=bins_bkg,range=(xmin,xmax),density=True,color=bkgs[q][0],histtype='step',linewidth=1.5,label="Inc. $Z^0 \\to %s$" % bkgs[q][1])
#    ax.tick_params(axis='both', which='major', labelsize=25)
#    ax.set_title( FCC_label, loc='right', fontsize=20)
#    plt.xlim(xmin,xmax)
#    plt.xlabel("BDT1 score",fontsize=30)
#    plt.ylabel("Normalised counts",fontsize=30)
#    plt.yscale('log')
#    ymin,ymax = plt.ylim()
#    plt.ylim(ymin,50*ymax)
#    plt.legend(fontsize=25, loc="upper left")
#    plt.tight_layout()
#    fig.savefig(f"{loc.PLOTS}/{sig}_vs_inclusive_Z_uds_cc_bb_BDT_{vars}.pdf")










    #Plot efficiency as a function of BDT cut in each sample
    eff_train = {}
    eff_test  = {}
    BDT_cuts = np.linspace(0.05,5.05,500)
    cut_vals = []
    for proc in processes:
      eff_train[proc] = []
      eff_test [proc] = []
    for x in BDT_cuts:
      cut_val = float(x)
      cut_vals.append(cut_val)
      cut_val = 1 - pow(10, -cut_val)
      for proc in processes:
        eff_train[proc].append( max( 1e-3, float(len(df_train[proc].query("BDT > %s" % cut_val)))) / N_train[proc] )
        eff_test [proc].append( max( 1e-3, float(len(df_test [proc].query("BDT > %s" % cut_val)))) / N_test [proc] )


    fig, ax = plt.subplots(figsize=(12,8))

    for proc in processes:
      plt.plot(cut_vals, eff_train[proc], color=processes[proc][2], label=f'Train {processes[proc][3]}')
    for proc in processes:
      plt.plot(cut_vals, eff_test [proc], color=processes[proc][2], label=f'Test {processes[proc][3]}', linestyle='dashed')

    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.set_title( FCC_label, loc='right', fontsize=20)
    plt.xlim(0,4.1)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Efficiency",fontsize=30)
    plt.xticks([0, 1, 2, 3, 4], ["$1-10^0$", "$1-10^{-1}$", "$1-10^{-2}$", "$1-10^{-3}$", "$1-10^{-4}$"])
    plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(10e-6,2)
    plt.legend(fontsize=18, loc="lower left", ncol=2)
    plt.grid(alpha=0.4,which="both")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/BDT1_{vars}_overtrain_eff.pdf")


def main():
    parser = argparse.ArgumentParser(description='Plot xgb model for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    parser.add_argument("--SigName", choices=["Bc2TauNu","Bu2TauNu", "BuBc"],required=False,help="Name of signal sample used in the training",default="BuBc")
    args = parser.parse_args()

    run(args.Vars, args.SigName)

if __name__ == '__main__':
    main()

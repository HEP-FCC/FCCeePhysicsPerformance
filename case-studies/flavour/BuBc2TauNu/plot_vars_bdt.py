import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import uproot
import joblib

#Local code
from userConfig import loc, train_vars, train_vars_vtx, train_vars_2
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def run(stage):
    # Load trained model
    bdt = joblib.load(f"{loc.BDT}/xgb_bdt_BuBc_vtx.joblib")
    vars_list = train_vars_vtx
    if stage == 'stage2':
#      bdt = joblib.load(f"{loc.BDT}/xgb_bdt_stage2_Bu_vs_Bc_vs_qq_multi.joblib")
      vars_list = train_vars_2
      vars_list.append("EVT_ThrustEmin_E")
      vars_list.append("EVT_ThrustEmax_E")
      vars_list.append("EVT_DVmass_min")
      vars_list.append("EVT_DVmass_max")
      vars_list.append("EVT_DVmass_ave")
      vars_list.append("EVT_DVmass_Dmeson")

    #Load samples
    entry_plot = 200000
    MVA1_cut = "EVT_MVA1Bis > 0.6"
    if stage == 'stage1':
#      path = f"{loc.TRAIN}"
      path = "/afs/cern.ch/work/x/xzuo/public/FCC_files/Bc2TauNu/data/pkl"
      df_Bc = pd.read_pickle(f"{path}/Bc2TauNu.pkl")
      df_Bc = df_Bc.sample(n=entry_plot,random_state=100)
      df_Bc = df_Bc[vars_list]
      df_Bc["BDT"] = bdt.predict_proba(df_Bc).tolist()
      df_Bc["BDT"] = df_Bc["BDT"].apply(lambda x: x[1])
  
      #Bu -> tau nu signal
      df_Bu = pd.read_pickle(f"{path}/Bu2TauNu.pkl")
      df_Bu = df_Bu.sample(n=entry_plot,random_state=100)
      df_Bu = df_Bu[vars_list]
      df_Bu["BDT"] = bdt.predict_proba(df_Bu).tolist()
      df_Bu["BDT"] = df_Bu["BDT"].apply(lambda x: x[1])

      df_Zbb = pd.read_pickle(f"{path}/bb.pkl")
      df_Zbb = df_Zbb.sample(n=2*entry_plot,random_state=100)
      df_Zbb = df_Zbb[vars_list]
      df_Zbb["BDT"] = bdt.predict_proba(df_Zbb).tolist()
      df_Zbb["BDT"] = df_Zbb["BDT"].apply(lambda x: x[1])

      df_Zcc = pd.read_pickle(f"{path}/cc.pkl")
      df_Zcc = df_Zcc.sample(n=2*entry_plot,random_state=100)
      df_Zcc = df_Zcc[vars_list]
      df_Zcc["BDT"] = bdt.predict_proba(df_Zcc).tolist()
      df_Zcc["BDT"] = df_Zcc["BDT"].apply(lambda x: x[1])

    else:
      path = f"{loc.TRAIN2}"
      #Load samples
      tree_Bc = uproot.open(f"{path}/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU.root")["events"]
      df_Bc = tree_Bc.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = entry_plot)
      df_Bc = df_Bc.query(f"{MVA1_cut} and CUT_CandTruth==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
      
      #Bc -> tau nu signal
      tree_Bu = uproot.open(f"{path}/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU.root")["events"]
      df_Bu = tree_Bu.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = entry_plot)
      df_Bu = df_Bu.query(f"{MVA1_cut} and CUT_CandTruth2==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
  
      tree_Zbb = uproot.open(f"{path}/p8_ee_Zbb_ecm91.root")["events"]
      df_Zbb = tree_Zbb.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = 4 * entry_plot)
      df_Zbb = df_Zbb.query(f"{MVA1_cut} and CUT_CandTruth==0 and CUT_CandTruth2==0 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")

      tree_Zcc = uproot.open(f"{path}/p8_ee_Zcc_ecm91.root")["events"]
      df_Zcc = tree_Zcc.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = 4 * entry_plot)
      df_Zcc = df_Zcc.query(f"{MVA1_cut} and CUT_CandTruth==0 and CUT_CandTruth2==0 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")

    Bc_label = '$B_c^+ \\to \\tau^+ \\nu_\\tau$'
    Bu_label = '$B^+ \\to \\tau^+ \\nu_\\tau$'
    Zbb_label = '$Z^0 \\to b\\bar{b}$'
    Zcc_label = '$Z^0 \\to c\\bar{c}$'

    cuts = {"precut": "BDT>0",
            "MVA1_0p9": "BDT>0.9"}
    if stage == "stage2":
      cuts = {"precut": "EVT_MVA2_bu>0",
              "MVA2Bu_0p8": "EVT_MVA2_bu>0.8",
              "MVA2Bc_0p8": "EVT_MVA2_bc>0.8"}
    for cut in cuts:
      print (f"selecting {cut}")
      df_Bc_plot = df_Bc.query(cuts[cut])
      df_Bu_plot = df_Bu.query(cuts[cut])
      df_Zbb_plot = df_Zbb.query(cuts[cut]) 
      df_Zcc_plot = df_Zcc.query(cuts[cut])
      df_tot = df_Bc_plot.append(df_Bu_plot).append(df_Zbb_plot).append(df_Zcc_plot)
      for var in vars_list:
        print (f"plotting {var}")
        fig, ax = plt.subplots(figsize=(12,8))
        xmin = df_tot[var].quantile(0.01)
        xmax = df_tot[var].quantile(0.99) # some very high outliers 
        if 'DVz0' in var or 'DVd0' in var:
          xmin = 0
          xmax = 5
        if 'DVmass' in var:
          xmin = 0 
          xmax = 3
        bins_bkg = 100 #min(100, int(np.sqrt(len(df_Zbb_plot))) )
        bins_cc  = 100 #min(100, int(np.sqrt(len(df_Zcc_plot))) )
        bins_sig = 100 #min(100, int(np.sqrt(len(df_Bc_plot)))  )
        if 'N' in var:
          bins_bkg = 40
          bins_cc = 40
          bins_sig = 40
        print (f"{xmin}  {xmax}")
        print (f"{bins_bkg} {bins_cc} {bins_sig}")
        plt.hist(df_Bc_plot[var], bins=bins_sig,range=(xmin,xmax),density=True,color="g",histtype='step',linewidth=1.5,label=Bc_label)
        plt.hist(df_Bu_plot[var], bins=bins_sig,range=(xmin,xmax),density=True,color="r",histtype='step',linewidth=1.5,label=Bu_label)
        plt.hist(df_Zbb_plot[var],bins=bins_bkg,range=(xmin,xmax),density=True,color="b",histtype='step',linewidth=1.5,label=Zbb_label)
        plt.hist(df_Zcc_plot[var],bins=bins_bkg,range=(xmin,xmax),density=True,color="k",histtype='step',linewidth=1.5,label=Zcc_label)
        ax.tick_params(axis='both', which='major', labelsize=25)
        plt.xlim(xmin,xmax)
        plt.xlabel(var.replace('_', '\_'),fontsize=30)
        if 'dPV2DV' in var or 'DVz0' in var or 'DVd0' in var:
          plt.xscale('log')
          plt.xlim(left=0.01)
        plt.ylabel("Normalised counts",fontsize=30)
        plt.yscale('linear')
        ymin,ymax = plt.ylim()
        plt.ylim(ymin,1.5*ymax)
        plt.legend(fontsize=25, loc="upper left")
        plt.tight_layout()
        fig.savefig(f"{loc.PLOTS}/{stage}_vars/{stage}_{var}_{cut}.png")


def main():
    parser = argparse.ArgumentParser(description='Plot xgb model for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--BDTstage", choices=["stage1", "stage2"], required=False, default="stage2")
    args = parser.parse_args()

    run(args.BDTstage)

if __name__ == '__main__':
    main()

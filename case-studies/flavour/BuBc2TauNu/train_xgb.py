import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
#from root_pandas import read_root
import uproot
import ROOT
import joblib
import glob

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut

def run(vars, sig):

    #Both Bu and Bc -> tau nu signal
    if(vars=="normal"):
        vars_list = train_vars
    elif(vars=="vtx"):
        vars_list = train_vars_vtx
    print("TRAINING VARS")
    print(vars_list)
    path = f"{loc.PKL}"
#    path = "/afs/cern.ch/work/x/xzuo/public/FCC_files/Bc2TauNu/data/pkl"
    df_bc = pd.read_pickle(f"{path}/Bc2TauNu.pkl")
    df_bc = df_bc[vars_list]
    df_bu = pd.read_pickle(f"{path}/Bu2TauNu.pkl")
    df_bu = df_bu[vars_list]
    print(f"Number of Bc events: {len(df_bc)}")
    print(f"Number of Bu events: {len(df_bu)}")
    df_sig = df_bc
    if sig == 'Bu2TauNu':
      df_sig = df_bu
    elif sig == 'BuBc':
      print("Sampling the same number of events from each")
      if len(df_bu) > len(df_bc):
        df_bu = df_bu.sample(n=len(df_bc),random_state=10)
      else:
        df_bc = df_bc.sample(n=len(df_bu),random_state=10)
      df_sig = df_bc.append(df_bu)
    print(f"Number of signal events: {len(df_sig)}")

    #Z -> qq inclusive
    n_tot_bkg = 2e6
    BF = {}
    BF["bb"] = 0.1512
    BF["cc"] = 0.1203
    BF["uds"] = 0.6991 - BF["bb"] - BF["cc"]

    #Efficiency of the pre-selection equirements on each bkg
    eff = {}
    #Number of generated events for each background type
    N = {}

    bkgs = ["uds","cc","bb"]

    #Loop over all background files and calculate total number of generated events
    for q in bkgs:
        path_gen = f"{loc.TRAIN}/{mode_names[q]}"

        #List of all sub-files in the path
        files = glob.glob(f"{path_gen}/*.root")

        N[q] = 0
        for f in files:
            N_this = uproot.open(f)["eventsProcessed"].value
            N[q] = N[q] + N_this

    df_bkg = {}
    for q in bkgs:
        df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")#,usecols=vars_list)
        df_bkg[q] = df_bkg[q][vars_list]
        print(f"Total size of {q} sample: {len(df_bkg[q])}")
        eff[q] = float(len(df_bkg[q]))/N[q]
        print(f"Efficiency of pre-selection on {q} sample: {eff[q]}")
    BF_tot = eff["uds"]*BF["uds"] + eff["cc"]*BF["cc"] + eff["bb"]*BF["bb"]
    for q in bkgs:
      if n_tot_bkg > len(df_bkg[q]) / (eff[q]*BF[q]/BF_tot):
        n_tot_bkg = 0.99 * len(df_bkg[q]) / (eff[q]*BF[q]/BF_tot)
        # make sure training selection does not exceed sample size
        # 0.99 to make sure there is no rounding effect
    print (f"Select total {n_tot_bkg} events")
    for q in bkgs:
        df_bkg[q] = df_bkg[q].sample(n=int(n_tot_bkg*(eff[q]*BF[q]/BF_tot)),random_state=10)
        print(f"Size of {q} in combined sample: {len(df_bkg[q])}")

    #Make a combined background sample according to BFs
    df_bkg_tot = df_bkg["uds"].append(df_bkg["cc"])
    df_bkg_tot = df_bkg_tot.append(df_bkg["bb"])
    #Shuffle the background so it is an even mixture of the modes
    df_bkg_tot = df_bkg_tot.sample(frac=1)

    #Signal and background labels
    df_sig["label"] = 1
    df_bkg_tot["label"] = 0

    #Combine the datasets
    df_tot = df_sig.append(df_bkg_tot)

    #Split into class label (y) and training vars (x)
    y = df_tot["label"]
    x = df_tot[vars_list]

    y = y.to_numpy()
    x = x.to_numpy()

    #Sample weights to balance the classes
    weights = compute_sample_weight(class_weight='balanced', y=y)

    #BDT
    config_dict = {
            "n_estimators": 1000,
            "learning_rate": 0.3,
            "max_depth": 5,
            }

    bdt = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                            max_depth=config_dict["max_depth"],
                            learning_rate=config_dict["learning_rate"],
                            )

    #Fit the model
    print("Training model")
    bdt.fit(x, y, sample_weight=weights)

    feature_importances = pd.DataFrame(bdt.feature_importances_,
                                     index = vars_list,
                                     columns=['importance']).sort_values('importance',ascending=False)

    print("Feature importances")
    print(feature_importances)

    #Create ROC curves
    decisions = bdt.predict_proba(x)[:,1]

    # Compute ROC curves and area under the curve
    fpr, tpr, thresholds = roc_curve(y, decisions)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(8,8))
    plt.plot(tpr, 1-fpr, lw=1.5, color="k", label='ROC (area = %0.3f)'%(roc_auc))
    plt.plot([0.45, 1.], [0.45, 1.], linestyle="--", color="k", label='50/50')
    plt.xlim(0.45,1.)
    plt.ylim(0.45,1.)
    plt.ylabel('Background rejection',fontsize=30)
    plt.xlabel('Signal efficiency',fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.legend(loc="upper left",fontsize=20)
    plt.grid()
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{sig}_vs_inclusive_Z_uds_cc_bb_ROC_{vars}.pdf")

    #Write the model to a ROOT file on EOS, for application elsewhere in FCCAnalyses
    out = f"{loc.BDT}"
    print("Writing xgboost model to ROOT file")
    ROOT.TMVA.Experimental.SaveXGBoost(bdt, f"{sig}_BDT", f"{out}/xgb_bdt_{sig}_{vars}.root", num_inputs=len(vars_list))

    #Write model to joblib file
    joblib.dump(bdt, f"{out}/xgb_bdt_{sig}_{vars}.joblib")

def main():
    parser = argparse.ArgumentParser(description='Train xgb model for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    parser.add_argument("--SigName", choices=["Bc2TauNu","Bu2TauNu", "BuBc"],required=False,help="Whether to use Bc2TauNu or Bu2TauNu as the signal",default="BuBc")
    args = parser.parse_args()

    run(args.Vars, args.SigName)

if __name__ == '__main__':
    main()

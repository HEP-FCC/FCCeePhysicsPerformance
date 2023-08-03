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
 
    path_train = f"{loc.PKL}_2022Oct"
    for proc in processes:
      # If using pkl from process_sig_bkg_samples_for_xgb.py
      df_train[proc] = pd.read_pickle(f"{path_train}/{processes[proc][0]}.pkl") 
      df_train[proc] = df_train[proc].sample(n=500000,random_state=100)
      df_train[proc] = df_train[proc][vars_list]
      N_train [proc] = len(df_train[proc])

      df_test[proc] = pd.read_pickle(f"{path_train}/{processes[proc][0]}_testing.pkl") 
      print (f'{proc}, {len(df_test[proc])}')
      df_test[proc] = df_test[proc].sample(n=500000,random_state=100)
      df_test[proc] = df_test[proc][vars_list]
      N_test [proc] = len(df_test[proc])


      print (f'{proc}:  train: {N_train[proc]},  test: {N_test[proc]} to {len(df_test[proc])}')


    binning = { "EVT_NTau23Pi"   : ["Num. of 3$\\pi$ vertices",     5,  0,  5],
                "EVT_NVertex"    : ["Num. of reco. vertices",   10,  0, 10],
                "EVT_NtracksPV"  : ["Num. of tracks from PV",   30,  0, 30],
                "EVT_ThrustEmax_E"        : ["Max hem. tot Energy (GeV)",      40, 20, 60],
                "EVT_ThrustEmax_Echarged" : ["Max hem. charged Energy (GeV)",      50, 0, 50],
                "EVT_ThrustEmax_Eneutral" : ["Max hem. neutral Energy (GeV)",      50, 0, 50],
                "EVT_ThrustEmax_NDV"      : ["Num. of secondary vertices in max hem.",       5, 0,  5],
                "EVT_ThrustEmax_Ncharged" : ["Charged multiplicity in max hem.",            25, 0, 25],
                "EVT_ThrustEmax_Nneutral" : ["Neutral multiplicity in max hem.",            25, 0, 25],
                "EVT_ThrustEmin_E"        : ["Min hem. tot Energy (GeV)",          50, 0, 50],
                "EVT_ThrustEmin_Echarged" : ["Min hem. charged Energy (GeV)",      50, 0, 50],
                "EVT_ThrustEmin_Eneutral" : ["Min hem. neutral Energy (GeV)",      50, 0, 50],
                "EVT_ThrustEmin_NDV"      : ["Num. of secondary vertices in min hem.",       5, 0,  5],
                "EVT_ThrustEmin_Ncharged" : ["Charged multiplicity in min hem.",            25, 0, 25],
                "EVT_ThrustEmin_Nneutral" : ["Neutral multiplicity in min hem.",            25, 0, 25],
                "EVT_dPV2DVave"           : ["Mean distance between SVs to PV (mm)",        50, 0, 50],
                "EVT_dPV2DVmax"           : ["Max distance between SVs to PV (mm)",         50, 0, 50],
                "EVT_dPV2DVmin"           : ["Min distance between SVs to PV (mm)",         50, 0, 25],
              }


    for var in vars_list:
        fig, ax = plt.subplots(figsize=(12,8))
        xmin = min( df_train['Bu'][var].quantile(0.01), df_train['Bc'][var].quantile(0.01), df_train['bb'][var].quantile(0.01) )
        xmax = max( df_train['Bu'][var].quantile(0.99), df_train['Bc'][var].quantile(0.99), df_train['bb'][var].quantile(0.99) ) 

        for proc in processes:
            plt.hist(df_train[proc][var], bins=binning[var][1],range=(binning[var][2], binning[var][3]),density=True,color=processes[proc][2],histtype='step',linewidth=1.5,label=f'Train {processes[proc][3]}', fill=(proc == 'Bu' or proc == 'Bc'),  alpha=0.3 if (proc=='Bu' or proc=='Bc') else 1.0)
        for proc in processes:
            plt.hist(df_test[proc][var],  bins=binning[var][1],range=(binning[var][2], binning[var][3]),density=True,color=processes[proc][2],histtype='step',linewidth=2.5,label=f'Test {processes[proc][3]}', linestyle='dashed')

        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.set_title( FCC_label, loc='right', fontsize=20)

        plt.xlabel(binning[var][0],fontsize=30)
        plt.ylabel("Normalised yield (a.u.)",fontsize=30)
        plt.xlim(binning[var][2], binning[var][3])
        ymin,ymax = plt.ylim()
        plt.ylim(ymin,1.5*ymax)
        plt.legend(fontsize=18, loc="upper right", ncol=2)
        plt.tight_layout()
        fig.savefig(f"{loc.PLOTS}/BDT1_vars/{var}.png")
        fig.savefig(f"{loc.PLOTS}/BDT1_vars/{var}.pdf")
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Plot xgb model for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    parser.add_argument("--SigName", choices=["Bc2TauNu","Bu2TauNu", "BuBc"],required=False,help="Name of signal sample used in the training",default="BuBc")
    args = parser.parse_args()

    run(args.Vars, args.SigName)

if __name__ == '__main__':
    main()

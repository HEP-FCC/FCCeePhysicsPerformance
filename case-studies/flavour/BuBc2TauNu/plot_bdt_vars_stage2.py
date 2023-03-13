import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xgboost as xgb
import joblib
import uproot
from sklearn.metrics import roc_curve, auc
#from root_pandas import read_root, to_root

#Local code
from userConfig import loc, train_vars, train_vars_vtx, train_vars_2, train_vars_2_Dvtx, train_vars_2_Dvtx_trim1, FCC_label
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

vars_list = train_vars_2_Dvtx.copy()
#vars_list = train_vars_2.copy()

#use Bc or Bu as sig


MVA1_cut_train = "EVT_MVA1Bis > 0.6"
MVA1_cut_test = "EVT_MVA1 > 0.6"
MVA2_cut = "EVT_MVA2 > 0.0"

entry_plot = 500000


processes = {"Bu":  ["Bu2TauNu", "p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU", "#b2182b", '$B^+ \\to \\tau^+ \\nu_\\tau$'],
             "Bc":  ["Bc2TauNu", "p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU", "#508273", '$B_c^+ \\to \\tau^+ \\nu_\\tau$'],
             "uds": ["uds", "p8_ee_Zuds_ecm91", "#d1e5f0","$Z^0 \\to q\\bar{q}$"],
             "cc":  ["cc",  "p8_ee_Zcc_ecm91",  "#92c5de","$Z^0 \\to c\\bar{c}$"],
             "bb":  ["bb",  "p8_ee_Zbb_ecm91",  "#2166ac","$Z^0 \\to b\\bar{b}$"]}
df_train = {}
df_test = {}
N_train = {}
N_test  = {}




path_train = f"{loc.TRAIN2}"
path_test  = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu/flatNtuples/spring2021/prod_04/testing_stage2"

for proc in processes:
  if   proc == 'Bc': truth = 'CUT_CandTruth==1'
  elif proc == 'Bu': truth = 'CUT_CandTruth2==1'
  else:              truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'

  entry_this = entry_plot
  if proc == 'uds': entry_this = 20000
  if proc == 'cc' : entry_this = 200000
 
  tree_temp = uproot.open(f"{path_train}/{processes[proc][1]}.root")["events"]
  df_train[proc] = tree_temp.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = entry_this)
  df_train[proc] = df_train[proc].query(f"{MVA1_cut_train} and {truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
  df_train[proc] = df_train[proc][vars_list]
  N_train [proc] = len(df_train[proc])

  tree_temp = uproot.open(f"{path_test}/{processes[proc][1]}.root")["events"]
  df_test[proc] = tree_temp.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = entry_this)
  df_test[proc] = df_test[proc].query(f"{MVA1_cut_test} and {truth}  and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
  df_test[proc] = df_test[proc][vars_list]
  N_test [proc] = len(df_test[proc])

  print (f'{proc}    train: {N_train[proc]},       test: {N_test[proc]}')



#for cat in ['BDT_Bu', 'BDT_Bc', 'BDT_bkg']:
#    BDT_label = cat.replace('BDT_', 'BDT2 ') + ' score'
#    eff_train = {}
#    eff_test  = {}
#    cut_vals = []
#    cut_name = cat
#    if cat == 'BDT_bkg': cut_name = "(BDT_Bu + BDT_Bc)"
#    for proc in processes:
#      eff_train[proc] = []
#      eff_test [proc] = []
#    for x in BDT_cuts:
#      cut_val = float(x)
#      cut_vals.append(cut_val)
#      cut_val = 1 - pow(10, -cut_val)
#      for proc in processes:
#        eff_train[proc].append( max( 1e-3, float(len(df_train[proc].query(cut_name + "> %s" % cut_val)))) / N_train[proc] )
#        eff_test [proc].append( max( 1e-3, float(len(df_test [proc].query(cut_name + "> %s" % cut_val)))) / N_test [proc] )
#
#
#    fig, ax = plt.subplots(figsize=(12,8))
#
#    for proc in processes:
#      plt.plot(cut_vals, eff_train[proc], color=processes[proc][2], label=f'Train {processes[proc][3]}')
#    for proc in processes:
#      plt.plot(cut_vals, eff_test [proc], color=processes[proc][2], label=f'Test {processes[proc][3]}', linestyle='dashed')
#
#    ax.tick_params(axis='both', which='major', labelsize=20)
#    ax.set_title( FCC_label, loc='right', fontsize=20)
#    plt.xlim(0,3.6)
#    plt.xlabel(BDT_label,fontsize=30)
#    if cat != 'BDT_bkg':
#      plt.xlabel('1 - ' + BDT_label, fontsize=30)
#    plt.ylabel("Efficiency",fontsize=30)
#    plt.xticks([0, 1, 2, 3], ["$10^0$", "$10^{-1}$", "$10^{-2}$", "$10^{-3}$"])
#    if cat == 'BDT_bkg': plt.xticks([0, 1, 2, 3], ["$10^0$", "$10^{-1}$", "$10^{-2}$", "$10^{-3}$"])
#    plt.yscale('log')
#    ymin,ymax = plt.ylim()
#    plt.ylim(1e-5,2)
#    plt.legend(fontsize=18, loc="upper right", ncol=2)
#    if cat == 'BDT_bkg': plt.legend(fontsize=18, loc="lower left", ncol=2)
#    plt.grid(alpha=0.4,which="both")
#    plt.tight_layout()



binning = { "EVT_Nominal_B_E"         : ["Nominal energy of B system (GeV)",    50,    0,  75],
            "EVT_PVmass"              : ["$m$(PV) (GeV)",                       40,    0,  40],
            "EVT_CandN"               : ["Num. of 3$\\pi$ candidates",           4,    0,   4],
            "EVT_CandAngleThrust"     : ["3$\\pi$ angle to thrust axis (rad)",  50,    0,   1],
            "EVT_CandMass"            : ["$m$(3$\\pi$) (GeV)",                  50,  0.5,   2],
            "EVT_CandRho1Mass"        : ["$m(3\\pi^+\\pi^-)_1$ (GeV)",          50,  0.2, 1.2],
            "EVT_CandRho2Mass"        : ["$m(3\\pi^+\\pi^-)_2$ (GeV)",          50,  0.2, 1.2],
            "EVT_CandP"               : ["$p$(3$\\pi$) (GeV)",                  40,    0,  40],
            "EVT_CandPx"              : ["$p_x$(3$\\pi$) (GeV)",                50,  -25,  25],
            "EVT_CandPy"              : ["$p_y$(3$\\pi$) (GeV)",                50,  -25,  25],            
            "EVT_CandPz"              : ["$p_z$(3$\\pi$) (GeV)",                50,  -25,  25],
            "EVT_CandVtxChi2"         : ["$\\chi^2$(3$\\pi$)",                  50,    0,   5],
            "EVT_CandVtxFD"           : ["Distance of 3$\\pi$ cand. from PV (mm)",   50,    0,  15],
            "EVT_CandD0"              : ["$d_0$(3$\\pi$) (mm)",                 50, -1.5, 1.5],
            "EVT_CandZ0"              : ["$z_0$(3$\\pi$) (mm)",                 50, -2.5, 2.5],     
            "EVT_DVd0_ave"            : ["Mean $d_0$ of other SVs (mm)",        50,-0.75,0.75],
            "EVT_DVd0_max"            : ["Max $d_0$ of other SVs (mm)",         50,-0.75,0.75],
            "EVT_DVd0_min"            : ["Min $d_0$ of other SVs (mm)",         50,-0.75,0.75],
            "EVT_DVz0_ave"            : ["Mean $z_0$ of other SVs (mm)",        50,  -2,   2],
            "EVT_DVz0_max"            : ["Max $z_0$ of other SVs (mm)",         50,  -2,   2],
            "EVT_DVz0_min"            : ["Min $z_0$ of other SVs (mm)",         50,  -2,   2],
            "EVT_DVmass_Dmeson_Emin"  : ["Closest $m_{SV}$ to D meson in sig. hem. (GeV)",  50,  1, 2.5],
            "EVT_d2PVd0_Dmeson_Emin"  : ["$xy$ distance to PV of SV closest to $m_D$ (mm)", 50,  0,   2],
            "EVT_d2PVz_Dmeson_Emin"   : ["$z$ distance to PV of SV closest to $m_D$ (mm)",  50, -2,   2],
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
    if var == 'EVT_d2PVd0_Dmeson_Emin': 
        plt.ylim(ymin,1.1*ymax)
    plt.legend(fontsize=18, loc="upper right", ncol=2)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/BDT2_vars/{var}.png")
    fig.savefig(f"{loc.PLOTS}/BDT2_vars/{var}.pdf")
    plt.close(fig)





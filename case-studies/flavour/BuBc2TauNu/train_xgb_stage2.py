import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot
#from root_pandas import read_root, to_root
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
import ROOT
import joblib
import glob

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
from userConfig import loc, mode_names, train_vars, train_vars_vtx, train_vars_2, train_vars_2_Dvtx, train_vars_2_Dvtx_trim1
import plotting
import utils as ut

train_with_Dvtx = True
vars_list = train_vars_2.copy()
if train_with_Dvtx:
  vars_list = train_vars_2_Dvtx.copy()

#Cut on MVA1 before training to focus it
MVA1_cut = "EVT_MVA1Bis > 0.6"
MVA2_cut = "EVT_MVA2 > 0.0"


#use Bc or Bu as sig
suffix = 'Bu_vs_Bc_vs_qq_multi'
if train_with_Dvtx:
  suffix = suffix + '_Dvtx_morelayer_d3n1000'
path = f"{loc.TRAIN2}"

tree_sig = uproot.open(path+f"/{mode_names['Bu2TauNu']}.root")["events"]
df_sig = tree_sig.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = 6e5)
print("TRAINING VARS")
print(vars_list)
print("Number of training vars: %s" % len(vars_list))

print(f"Number of signal events: {len(df_sig)}")
#Apply truth-matching, require rho window, require 3π candidate to be in min energy hemisphere, and reqire m_3pi < m_tau
df_sig = df_sig.query(f"{MVA1_cut} and CUT_CandTruth2==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
print(f"Number of signal events after truth matching, MVA1, rho cut and hemisphere cut: {len(df_sig)}")
df_sig = df_sig[vars_list]


tree_bc = uproot.open(path+f"/{mode_names['Bc2TauNu']}.root")["events"]
df_bc = tree_bc.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"])
print("Number of training vars: %s" % len(vars_list))

print(f"Number of Bc events: {len(df_bc)}")
#Apply truth-matching, require rho window, require 3?~@ candidate to be in min energy hemisphere, and reqire m_3pi < m_tau
df_bc = df_bc.query(f"{MVA1_cut} and CUT_CandTruth==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
print(f"Number of Bc events after truth matching, MVA1, rho cut and hemisphere cut: {len(df_bc)}")
df_bc = df_bc[vars_list]


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

tree_bkg = {}
df_bkg = {}
events_bkg = {}
for q in bkgs:
    tree_bkg[q] = uproot.open(path+f"/{mode_names[q]}.root")["events"]
    df_bkg[q] = tree_bkg[q].arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"])
    df_bkg[q] = df_bkg[q].query(f"{MVA1_cut} and CUT_CandTruth==0 and CUT_CandTruth2==0 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
    print(f"Total size of {q} sample: {len(df_bkg[q])}")
    eff[q] = float(len(df_bkg[q]))/N[q]
    print(f"Efficiency of pre-selection on {q} sample: {eff[q]}")
    df_bkg[q] = df_bkg[q][vars_list]

BF_tot = eff["uds"]*BF["uds"] + eff["cc"]*BF["cc"] + eff["bb"]*BF["bb"]
for q in bkgs:
    if n_tot_bkg > len(df_bkg[q]) / (eff[q]*BF[q]/BF_tot): 
      n_tot_bkg = 0.99 * len(df_bkg[q]) / (eff[q]*BF[q]/BF_tot) 
      # make sure training selection does not exceed sample size
      # 0.99 to make sure there is no rounding effect
print (f"Select total {n_tot_bkg} events")
for q in bkgs:
    n_required = int(n_tot_bkg*(eff[q]*BF[q]/BF_tot))
    print(f"Number of {q} required: {n_required}")
    #if(q!="uds"):
    df_bkg[q] = df_bkg[q].sample(n=n_required,random_state=10)
    print(f"Size of {q} in combined sample: {len(df_bkg[q])}")

#Make a combined background sample according to BFs
df_bkg_tot = df_bkg["uds"].append(df_bkg["cc"])
df_bkg_tot = df_bkg_tot.append(df_bkg["bb"])
#Shuffle the background so it is an even mixture of the modes
df_bkg_tot = df_bkg_tot.sample(frac=1)


#Signal and background labels
df_sig["label"] = 1
df_bc["label"] = 2
df_bkg_tot["label"] = 0

print ("sample size each")
print (len(df_sig))
print (len(df_bc))
print (len(df_bkg_tot))

#Combine the datasets
df_tot = df_sig.append(df_bc).append(df_bkg_tot)

print ("sample size tot")
print (len(df_tot))

#Split into class label (y) and training vars (x)
y = df_tot["label"]
x = df_tot[vars_list]

y = y.to_numpy()
x = x.to_numpy()

#Sample weights to balance the classes
weights = compute_sample_weight(class_weight='balanced', y=y)

#BDT
config_dict = {
            "n_estimators": 1000, #1000,
            "learning_rate": 0.3,
            "max_depth": 3, #5,
            }

bdt = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                        max_depth=config_dict["max_depth"],
                        learning_rate=config_dict["learning_rate"],
                        objective='multi:softprob'
                        )

#Fit the model
print("Training model")
bdt.fit(x, y, sample_weight=weights)

feature_importances = pd.DataFrame(bdt.feature_importances_,
                                   index = vars_list,
                                   columns=['importance']).sort_values('importance',ascending=False)

print("Feature importances")
print(feature_importances)


#Write the model to a ROOT file for application elsewhere in FCCAnalyses
out = f"{loc.BDT}"

#Write model to joblib file
joblib.dump(bdt, f"{out}/xgb_bdt_stage2_{suffix}.joblib")

#Also dump as json for ROOT interpretation
#bdt.dump_model(f"{out}/xgb_bdt_stage2_{suffix}.json", dump_format='json')

# comment TMVA form output. TMVA Experimental only supports binary at the moment.
print("Writing xgboost model to ROOT file")
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "BuBc_BDT2", f"{out}/xgb_bdt_stage2_{suffix}.root", num_inputs=len(vars_list))


# ROC curve plotting accomplished in the plotting script and not here.

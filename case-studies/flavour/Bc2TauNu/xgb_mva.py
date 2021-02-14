import sys,os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from root_pandas import read_root, to_root
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.utils.class_weight import compute_sample_weight
from scipy.stats import ks_2samp

#Local code
from userConfig import loc, mode
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Variables to use in the MVA
training_vars = ["EVT_thrutshemis_e_min",
                 "EVT_thrutshemis_e_max",
                 "echarged_min",
                 "echarged_max",
                 "eneutral_min",
                 "eneutral_max",
                 "ncharged_min",
                 "ncharged_max",
                 "nneutral_min",
                 "nneutral_max"
                ]

#Bc -> tau nu signal
path = f"{loc.CSV}"
df_sig = pd.read_csv(f"{path}/Bc2TauNu.csv",usecols=training_vars)

#Z -> qq inclusive
n_tot_bkg = 1e6
BF = {}
BF["bb"] = 0.1512
BF["cc"] = 0.1203
BF["uds"] = 0.6991 - BF["bb"] - BF["cc"]
BF_tot = BF["uds"] + BF["cc"] + BF["bb"]
df_bkg = {}
for q in ["uds","cc","bb"]:
    df_bkg[q] = pd.read_csv(f"{path}/inclusive_Z{q}.csv",usecols=training_vars)
    print(f"Total size of {q} sample: {len(df_bkg[q])}")
    df_bkg[q] = df_bkg[q].sample(n=int(n_tot_bkg*(BF[q]/BF_tot)),random_state=10)
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
x = df_tot[training_vars]

#Split into samples to be used in the two BDTs, which will be used to make predictions for each other
x_A, x_B, y_A, y_B = train_test_split(x, y, test_size=0.5, random_state=100)

#Sample weights to balance the classes
weights_A = compute_sample_weight(class_weight='balanced', y=y_A)
weights_B = compute_sample_weight(class_weight='balanced', y=y_B)

#BDTs for each sample, which we will apply to the other sample (cross BDT)
config_dict = {
        "n_estimators": 400,
        "learning_rate": 0.3,
        "max_depth": 3,
        }

bdt_A = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                                   max_depth=config_dict["max_depth"],
                                   learning_rate=config_dict["learning_rate"],
                                  )

bdt_B = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                                   max_depth=config_dict["max_depth"],
                                   learning_rate=config_dict["learning_rate"],
                                  )

#Fit the models
bdt_A.fit(x_A, y_A, sample_weight=weights_A)
bdt_B.fit(x_B, y_B, sample_weight=weights_B)

#Get the feature importances
feature_importances_A = pd.DataFrame(bdt_A.feature_importances_,
                                     index = training_vars,
                                     columns=['importance']).sort_values('importance',ascending=False)

print("Feature importances for BDT A")
print(feature_importances_A)

feature_importances_B = pd.DataFrame(bdt_B.feature_importances_,
                                     index = training_vars,
                                     columns=['importance']).sort_values('importance',ascending=False)

print("Feature importances for BDT B")
print(feature_importances_B)

#Create ROC curves
decisions_B = bdt_A.predict_proba(x_B)[:,1]
decisions_A = bdt_B.predict_proba(x_A)[:,1]

# Compute ROC curves and area under the curve
fpr_A, tpr_A, thresholds_A = roc_curve(y_A, decisions_A)
roc_auc_A = auc(fpr_A, tpr_A)

fpr_B, tpr_B, thresholds_B = roc_curve(y_B, decisions_B)
roc_auc_B = auc(fpr_B, tpr_B)


fig, ax = plt.subplots(figsize=(8,8))
plt.plot(tpr_A, 1-fpr_A, lw=1.5, color="#7fcdbb", label='ROC A (area = %0.3f)'%(roc_auc_A))
plt.plot(tpr_B, 1-fpr_B, lw=1.5, color="#2c7fb8", label='ROC B (area = %0.3f)'%(roc_auc_B))

plt.plot([0.45, 1.], [0.45, 1.], linestyle="--", color="k", label='50/50')
plt.xlim(0.45,1.)
plt.ylim(0.45,1.)
plt.ylabel('Background rejection',fontsize=30)
plt.xlabel('Signal efficiency',fontsize=30)
ax.tick_params(axis='both', which='major', labelsize=25)
plt.legend(loc="upper left",fontsize=20)
plt.grid()
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/Bc2TauNu_vs_inclusive_Z_uds_cc_bb_ROC.pdf")

#Get BDT scores
sig_A, sig_B = train_test_split(df_sig, test_size=0.5, random_state=100)
bkg_A, bkg_B = train_test_split(df_bkg_tot, test_size=0.5, random_state=100)
sig_A_train_vars = sig_A[training_vars]
sig_B_train_vars = sig_B[training_vars]
bkg_A_train_vars = bkg_A[training_vars]
bkg_B_train_vars = bkg_B[training_vars]

sig_A["BDT_all"] = bdt_B.predict_proba(sig_A_train_vars).tolist()
sig_B["BDT_all"] = bdt_A.predict_proba(sig_B_train_vars).tolist()
bkg_A["BDT_all"] = bdt_B.predict_proba(bkg_A_train_vars).tolist()
bkg_B["BDT_all"] = bdt_A.predict_proba(bkg_B_train_vars).tolist()
sig_A['BDT_all'] = sig_A['BDT_all'].apply(lambda x: x[1])
sig_B['BDT_all'] = sig_B['BDT_all'].apply(lambda x: x[1])
bkg_A['BDT_all'] = bkg_A['BDT_all'].apply(lambda x: x[1])
bkg_B['BDT_all'] = bkg_B['BDT_all'].apply(lambda x: x[1])

#Combine the samples and plot signal and background BDTs
sig_tot = sig_A.append(sig_B)
bkg_tot = bkg_A.append(bkg_B)

#Find cut which keeps 1 background event i.e. 1e-6 eff
eff_bkg = 1
BDT_cut = 0.
n_bkg_tot = len(bkg_tot)
df_bkg_cut = bkg_tot.copy()
for i in range(0,10000):
    cut = float(i)/10000.
    df_bkg_cut = df_bkg_cut.query(f"BDT_all > {cut}")
    n_bkg_cut = float(len(df_bkg_cut))
    if(n_bkg_cut == 1):
        BDT_cut = cut
        break
print("BDT cut that keeps 10^-6 bkg = %s" % BDT_cut)

#Signal efficiency at this BDT cut
n_sig_pass = float(len(sig_tot.query(f"BDT_all > {BDT_cut}")))
eff_sig_pass = n_sig_pass / len(sig_tot)
print("Signal eff. for this cut = %s" % eff_sig_pass)

#KS tests for signal and background
ks_sig = ks_2samp(sig_A["BDT_all"],sig_B["BDT_all"])

ks_bkg = ks_2samp(bkg_A["BDT_all"],bkg_B["BDT_all"])

print(f"KS score for signal A vs. B: {ks_sig[0]}")
print(f"KS score for background A vs. B: {ks_bkg[0]}")


fig, ax = plt.subplots(figsize=(12,8))
xmin = 0
xmax = 1
bins_bkg = int(np.sqrt(len(bkg_A)))
bins_sig = int(np.sqrt(len(sig_A)))
plt.hist(sig_A["BDT_all"],bins=bins_sig,range=(xmin,xmax),density=True,color="crimson",histtype='step',linewidth=2,label="$B_c^+ \\to \\tau^+ \\nu_\\tau$ (BDT A)")
plt.hist(sig_B["BDT_all"],bins=bins_sig,range=(xmin,xmax),density=True,color="crimson",histtype='stepfilled',alpha=0.5,linewidth=2,label="$B_c^+ \\to \\tau^+ \\nu_\\tau$ (BDT B)")
plt.hist(bkg_tot["BDT_all"],bins=bins_bkg,range=(xmin,xmax),density=True,color="k",histtype='step',linewidth=2,label="Inclusive $Z^0 \\to q\\bar{q},c\\bar{c},b\\bar{b}$ (BDT A)")
plt.hist(bkg_B["BDT_all"],bins=bins_bkg,range=(xmin,xmax),density=True,color="k",histtype='stepfilled',alpha=0.5,linewidth=2,label="Inclusive $Z^0 \\to q\\bar{q},c\\bar{c},b\\bar{b}$ (BDT B)")
ax.tick_params(axis='both', which='major', labelsize=25)
plt.xlim(xmin,xmax)
plt.xlabel("BDT score ($q\\bar{q},c\\bar{c},b\\bar{b}$)",fontsize=30)
plt.ylabel("Normalised counts",fontsize=30)
plt.yscale('log')
ymin,ymax = plt.ylim()
plt.ylim(ymin,50*ymax)
plt.legend(fontsize=18, loc="upper left")
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/Bc2TauNu_vs_inclusive_Z_uds_cc_bb_BDT.pdf")

#Save signal sample to ROOT file
for B in ["Bu","Bc"]:
    df_sig_out = pd.read_csv(f"{path}/{B}2TauNu.csv")
    df_sig_out_train = df_sig_out[training_vars]
    df_sig_out["BDT_A"] = bdt_A.predict_proba(df_sig_out_train).tolist()
    df_sig_out["BDT_A"] = df_sig_out["BDT_A"].apply(lambda x: x[1])
    df_sig_out["BDT_B"] = bdt_B.predict_proba(df_sig_out_train).tolist()
    df_sig_out["BDT_B"] = df_sig_out["BDT_B"].apply(lambda x: x[1])
    df_sig_out["BDT_all"] = 0.5*(df_sig_out["BDT_A"] + df_sig_out["BDT_B"])
    df_sig_out = df_sig_out.drop("BDT_A",1)
    df_sig_out = df_sig_out.drop("BDT_B",1)

    file_name = f"{path}/{B}2TauNu_BDT.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
    df_sig_out.to_csv(file_name)

#Also apply MVA to the Z -> qq background samples
for qq in ["uds","cc","bb"]:
    df_bkg_out = pd.read_csv(f"{path}/inclusive_Z{qq}.csv",usecols=training_vars)
    df_bkg_out["BDT_A"] = bdt_A.predict_proba(df_bkg_out).tolist()
    df_bkg_out["BDT_A"] = df_bkg_out["BDT_A"].apply(lambda x: x[1])
    df_bkg_out["BDT_B"] = bdt_B.predict_proba(df_bkg_out[training_vars]).tolist()
    df_bkg_out["BDT_B"] = df_bkg_out["BDT_B"].apply(lambda x: x[1])
    df_bkg_out["BDT_all"] = 0.5*(df_bkg_out["BDT_A"] + df_bkg_out["BDT_B"])
    df_bkg_out = df_bkg_out.drop("BDT_A",1)
    df_bkg_out = df_bkg_out.drop("BDT_B",1)

    file_name = f"{path}/inclusive_Z{qq}_BDT.csv"
    if os.path.exists(file_name):
        os.remove(file_name)
    df_bkg_out.to_csv(file_name)

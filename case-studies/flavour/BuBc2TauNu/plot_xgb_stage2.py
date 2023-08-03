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


#use Bc or Bu as sig

bu = 'Bu2TauNu'
bc = 'Bc2TauNu'

suffix = 'Bu_vs_Bc_vs_qq_multi_final'
#BDT_Name = 'xgb_bdt_stage2_Bu_vs_Bc_only'

bdt = joblib.load(f"{loc.BDT}/xgb_bdt_stage2_{suffix}.joblib")

MVA1_cut = "EVT_MVA1Bis > 0.6"
MVA2_cut = "EVT_MVA2 > 0.0"

entry_plot = 300000

path = f"{loc.TRAIN2}"
#Load samples
tree_sig = uproot.open(f"{path}/p8_ee_Zbb_ecm91_EvtGen_{bu}TAUHADNU.root")["events"]
df_sig = tree_sig.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = entry_plot)
df_sig = df_sig.query(f"{MVA1_cut} and CUT_CandTruth2==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
print (f"Number of Bu selected: {len(df_sig)}")
df_sig = df_sig[vars_list]

#Bc -> tau nu signal
tree_other = uproot.open(f"{path}/p8_ee_Zbb_ecm91_EvtGen_{bc}TAUHADNU.root")["events"]
df_other = tree_other.arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = entry_plot)
df_other = df_other.query(f"{MVA1_cut} and CUT_CandTruth==1 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
print (f"Number of Bc selected: {len(df_other)}")
df_other = df_other[vars_list]


#Z -> qq inclusive
tree_bkg = {}
df_bkg = {}
bkgs = {"uds": ["#d1e5f0","q\\bar{q}"],
        "cc": ["#92c5de","c\\bar{c}"],
        "bb": ["#2166ac","b\\bar{b}"]
        }

BF = {}
BF["bb"] = 0.1512
BF["cc"] = 0.1203
BF["uds"] = 0.6991 - BF["bb"] - BF["cc"]

# eff numbers from training script output
eff = {}
eff['uds'] = 2.0176e-05 
eff['cc'] = 0.000814455 
eff['bb'] = 0.0050582

n_read = {}
n_read['uds'] = 100000
n_read['cc'] = 200000
n_read['bb'] = 500000

BF_tot = eff["uds"]*BF["uds"] + eff["cc"]*BF["cc"] + eff["bb"]*BF["bb"]

entry_tot = entry_plot / BF_tot

for q in bkgs:
    tree_bkg[q] = uproot.open(f"{path}/p8_ee_Z{q}_ecm91.root")["events"]
    df_bkg[q] = tree_bkg[q].arrays(library="pd", how="zip", filter_name=["EVT_*","CUT_*"], entry_stop = n_read[q])
    df_bkg[q] = df_bkg[q].query(f"{MVA1_cut} and CUT_CandTruth==0 and CUT_CandTruth2==0 and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8")
    print (f"Number of {q} selected: {len(df_bkg[q])}")
    print(f"getting {int(entry_tot * BF[q] * eff[q])} events for {q}")
    df_bkg[q] = df_bkg[q].sample(n=int(entry_tot * BF[q] * eff[q]),random_state=10)
    df_bkg[q] = df_bkg[q][vars_list]



sig_label = '$B^+ \\to \\tau^+ \\nu_\\tau$'
other_label = '$B_c^+ \\to \\tau^+ \\nu_\\tau$'
bkg_label = 'Inc. $Z^0 \\to$ hadrons'

df_sig['label'] = 1
df_other['label'] = 2
for q in bkgs:
    df_bkg[q]['label'] = 0

df_bkg_tot = df_bkg['uds'].append(df_bkg['cc']).append(df_bkg['bb'])
df_tot = df_sig.append(df_other).append(df_bkg_tot)

y = df_tot['label'].to_numpy()

bdt_out = {}
# each of them is an n * 3 array
bdt_out['bu'] = bdt.predict_proba(df_sig[vars_list])
bdt_out['bc'] = bdt.predict_proba(df_other[vars_list])
bdt_out['uds'] = bdt.predict_proba(df_bkg['uds'][vars_list])
bdt_out['cc'] = bdt.predict_proba(df_bkg['cc'][vars_list])
bdt_out['bb'] = bdt.predict_proba(df_bkg['bb'][vars_list])
bdt_out['bkg'] = bdt.predict_proba(df_bkg_tot[vars_list])
bdt_out['tot'] = bdt.predict_proba(df_tot[vars_list])

df_sig['BDT_bu'] = bdt_out['bu'][:,1]
df_sig['BDT_bc'] = bdt_out['bu'][:,2]
df_other['BDT_bu'] = bdt_out['bc'][:,1]
df_other['BDT_bc'] = bdt_out['bc'][:,2]
for q in bkgs:
    df_bkg[q]['BDT_bu'] = bdt_out[q][:,1]
    df_bkg[q]['BDT_bc'] = bdt_out[q][:,2]
df_bkg_tot['BDT_bu'] = bdt_out['bkg'][:,1]
df_bkg_tot['BDT_bc'] = bdt_out['bkg'][:,2]
df_sig['color'] = 'r'
df_other['color'] = 'g'
df_bkg_tot['color'] = 'b'

# make roc curve
fpr1, tpr1, thresholds = roc_curve(y, bdt_out['tot'][:,1], pos_label=1)
roc_auc1 = auc(fpr1, tpr1)
fpr2, tpr2, thresholds = roc_curve(y, bdt_out['tot'][:,2], pos_label=2)
roc_auc2 = auc(fpr2, tpr2)

fig, ax = plt.subplots(figsize=(8,8))
ax.set_title( FCC_label, loc='right', fontsize=20)
plt.plot(tpr1, 1-fpr1, lw=1.5, color="k", label='Bu ROC (area = %0.3f)'%(roc_auc1))
plt.plot(tpr2, 1-fpr2, lw=1.5, color="r", label='Bc ROC (area = %0.3f)'%(roc_auc2))
plt.plot([0.45, 1.], [0.45, 1.], linestyle="--", color="k", label='50/50')
plt.xlim(0.45,1.)
plt.ylim(0.45,1.)
plt.ylabel('Background rejection',fontsize=30)
plt.xlabel('Signal efficiency',fontsize=30)
ax.tick_params(axis='both', which='major', labelsize=25)
plt.legend(loc="lower left",fontsize=20)
plt.grid()
plt.tight_layout()
fig.savefig(f"{loc.PLOTS}/{suffix}_ROC_stage2.pdf")

# make scatter plot
df_scatter = df_sig.append(df_other).append(df_bkg_tot)
df_scatter = df_scatter[['BDT_bu', 'BDT_bc', 'color']]
df_scatter = df_scatter.sample(frac=1,random_state=10)
fig_scatter, ax_scatter = plt.subplots(figsize=(8,8))
plt.scatter(df_scatter['BDT_bu'], df_scatter['BDT_bc'], 0.01, c=df_scatter['color'], alpha=0.5)
#plt.scatter(bdt_out['bkg'][:,1], bdt_out['bkg'][:,2], 0.02, c='b', alpha=0.5)
#plt.scatter(bdt_out['bu'][:,1],  bdt_out['bu'][:,2],  0.02, c='r', alpha=0.5)
#plt.scatter(bdt_out['bc'][:,1],  bdt_out['bc'][:,2],  0.02, c='g', alpha=0.5)
plt.xlim(0.,1.)
plt.ylim(0.,1.)
plt.ylabel('BDT Bc score',fontsize=30)
plt.xlabel('BDT Bu score',fontsize=30)
ax_scatter.tick_params(axis='both', which='major', labelsize=25)
ax_scatter.set_title( FCC_label, loc='right', fontsize=20)
leg = [mpl.lines.Line2D([0],[0], marker='o', markersize=10, color='w', markerfacecolor='b', label=bkg_label),
       mpl.lines.Line2D([0],[0], marker='o', markersize=10, color='w', markerfacecolor='r', label=sig_label),
       mpl.lines.Line2D([0],[0], marker='o', markersize=10, color='w', markerfacecolor='g', label=other_label)]
plt.legend(handles=leg, loc="upper right",fontsize=20)

fig_scatter.savefig(f"{loc.PLOTS}/{suffix}_stage2_BDT_out_scatter.pdf")
fig_scatter.savefig(f"{loc.PLOTS}/{suffix}_stage2_BDT_out_scatter.png")

# fill BDT scores into histos, first arg is row and will be the y value, second is column and will be the x value
hist1, xedge1, yedge1 = np.histogram2d(bdt_out['bu'][:,2],  bdt_out['bu'][:,1],  bins =250, range=[[0., 1.], [0., 1.]])
hist2, xedge2, yedge2 = np.histogram2d(bdt_out['bc'][:,2],  bdt_out['bc'][:,1],  bins =250, range=[[0., 1.], [0., 1.]])
hist3, xedge3, yegde3 = np.histogram2d(bdt_out['bkg'][:,2], bdt_out['bkg'][:,1], bins =250, range=[[0., 1.], [0., 1.]])
extent = [xedge1[0], xedge1[-1], yedge1[0], yedge1[-1]]
h1max = np.max(hist1)
h2max = np.max(hist2)
h3max = np.max(hist3)
# convert log yield to RGB values between 0. and 1.
hist1 = 1. * np.log10( hist1 + 1) / np.log10(h1max + 1) 
hist2 = 1. * np.log10( hist2 + 1) / np.log10(h2max + 1) 
hist3 = 1. * np.log10( hist3 + 1) / np.log10(h3max + 1) 

hist0 = np.full(hist1.shape, 0)
histRGB = np.dstack((hist1, hist2, hist3))
hist1 = np.dstack((hist1, hist0, hist0))
hist2 = np.dstack((hist0, hist2, hist0))
hist3 = np.dstack((hist0, hist0, hist3))

fig_score, axs = plt.subplots(2,2, figsize=(12,8))

axs[0,0].imshow(histRGB, extent=extent, origin='lower')
axs[0,1].imshow(hist1, extent=extent, origin='lower')
axs[1,0].imshow(hist2, extent=extent, origin='lower')
axs[1,1].imshow(hist3, extent=extent, origin='lower')

axs[0,0].annotate("All events", xy=(0.3,0.8),xycoords='axes fraction', fontsize=15, color='white')
axs[0,1].annotate(sig_label, xy=(0.3,0.8),xycoords='axes fraction', fontsize=15, color='r')
axs[1,0].annotate(other_label, xy=(0.3,0.8),xycoords='axes fraction', fontsize=15, color='g')
axs[1,1].annotate(bkg_label, xy=(0.3,0.8),xycoords='axes fraction', fontsize=15, color='b')

axs[0,0].set_ylabel('Bc score',fontsize=15)
axs[0,1].set_ylabel('Bc score',fontsize=15)
axs[1,0].set_ylabel('Bc score',fontsize=15)
axs[1,1].set_ylabel('Bc score',fontsize=15)
axs[0,0].set_xlabel('Bu score',fontsize=15)
axs[0,1].set_xlabel('Bu score',fontsize=15)
axs[1,0].set_xlabel('Bu score',fontsize=15)
axs[1,1].set_xlabel('Bu score',fontsize=15)

normR = mpl.colors.LogNorm(vmin = 0.1, vmax=h1max)
normG = mpl.colors.LogNorm(vmin = 0.1, vmax=h2max)
normB = mpl.colors.LogNorm(vmin = 0.1, vmax=h3max)
mapR = mpl.colors.LinearSegmentedColormap('justRed'  ,{'red':[(0.,0.,0.), (1.,1.,0.)], 'green':[(0.,0.,0.), (1.,0.,0.)], 'blue':[(0.,0.,0.), (1.,0.,0.)] })
mapG = mpl.colors.LinearSegmentedColormap('justGreen',{'red':[(0.,0.,0.), (1.,0.,0.)], 'green':[(0.,0.,0.), (1.,1.,0.)], 'blue':[(0.,0.,0.), (1.,0.,0.)] })
mapB = mpl.colors.LinearSegmentedColormap('justBlue' ,{'red':[(0.,0.,0.), (1.,0.,0.)], 'green':[(0.,0.,0.), (1.,0.,0.)], 'blue':[(0.,0.,0.), (1.,1.,0.)] })
rbar = fig_score.colorbar(mpl.cm.ScalarMappable(norm=normR, cmap=mapR), ax=axs, fraction=0.05, aspect=40)
gbar = fig_score.colorbar(mpl.cm.ScalarMappable(norm=normG, cmap=mapG), ax=axs, fraction=0.05, aspect=40)
bbar = fig_score.colorbar(mpl.cm.ScalarMappable(norm=normB, cmap=mapB), ax=axs, fraction=0.05, aspect=40)
rbar.set_label('Normalized Bu counts', size=15)
gbar.set_label('Normalized Bc counts', size=15)
bbar.set_label('Normalized bkg counts', size=15)

fig_score.savefig(f"{loc.PLOTS}/{suffix}_stage2_BDT_out_RGB.pdf")
fig_score.savefig(f"{loc.PLOTS}/{suffix}_stage2_BDT_out_RGB.png")


#Plot efficiency as a function of BDT cut in each sample
BDT_cuts = np.linspace(0,999,999)
N_sig = len(df_sig)
N_other = len(df_other)
N_Zuds = len(df_bkg["uds"])
N_Zcc = len(df_bkg["cc"])
N_Zbb = len(df_bkg["bb"])
effbu_sig = []
effbu_other = []
effbu_bkg = {}
effbc_sig = []
effbc_other = []
effbc_bkg = {}
N_bkg = {}
for q in bkgs:
    effbu_bkg[q] = []
    effbc_bkg[q] = []
    N_bkg[q] = len(df_bkg[q])
cut_vals = []
for x in BDT_cuts:
    cut_val = float(x)/100
    cut_vals.append(cut_val)
    effbu_sig.append(float(len(df_sig.query("BDT_bu > %s" % cut_val))) / N_sig)
    effbc_sig.append(float(len(df_sig.query("BDT_bc > %s" % cut_val))) / N_sig)
    effbu_other.append(float(len(df_other.query("BDT_bu > %s" % cut_val))) / N_other)
    effbc_other.append(float(len(df_other.query("BDT_bc > %s" % cut_val))) / N_other)
    for q in bkgs:
        effbu_bkg[q].append(float(len(df_bkg[q].query("BDT_bu > %s" % cut_val))) / N_bkg[q])
        effbc_bkg[q].append(float(len(df_bkg[q].query("BDT_bc > %s" % cut_val))) / N_bkg[q])

fig_eff, ax = plt.subplots(figsize=(12,8))

plt.plot(cut_vals, effbu_sig, color="#b2182b",label=sig_label)
plt.plot(cut_vals, effbu_other, color="k",label=other_label)
for q in bkgs:
    plt.plot(cut_vals, effbu_bkg[q], color=bkgs[q][0],label="Inc. $Z^0 \\to %s$" % bkgs[q][1])

ax.tick_params(axis='both', which='major', labelsize=25)
ax.set_title( FCC_label, loc='right', fontsize=20)
plt.xlim(0.,1.)
plt.xlabel("BDT2 Bu score",fontsize=30)
plt.ylabel("Efficiency",fontsize=30)
plt.yscale('log')
ymin,ymax = plt.ylim()
plt.ylim(max(ymin,1e-4),2)
plt.legend(fontsize=25, loc="lower left")
plt.grid(alpha=0.4,which="both")
plt.tight_layout()
fig_eff.savefig(f"{loc.PLOTS}/{suffix}_stage2_BDT_Bu_eff.pdf")


fig_eff, ax = plt.subplots(figsize=(12,8))

plt.plot(cut_vals, effbc_other, color="#b2182b",label=other_label)
plt.plot(cut_vals, effbc_sig, color="k",label=sig_label)
for q in bkgs:
    plt.plot(cut_vals, effbc_bkg[q], color=bkgs[q][0],label="Inc. $Z^0 \\to %s$" % bkgs[q][1])

ax.tick_params(axis='both', which='major', labelsize=25)
ax.set_title( FCC_label, loc='right', fontsize=20)
plt.xlim(0.,1.)
plt.xlabel("BDT2 Bc score",fontsize=30)
plt.ylabel("Efficiency",fontsize=30)
plt.yscale('log')
ymin,ymax = plt.ylim()
plt.ylim(max(ymin,1e-4),2)
plt.legend(fontsize=25, loc="lower left")
plt.grid(alpha=0.4,which="both")
plt.tight_layout()
fig_eff.savefig(f"{loc.PLOTS}/{suffix}_stage2_BDT_Bc_eff.pdf")


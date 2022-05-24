from operator import index
import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.metrics import roc_curve, auc
from tqdm import tqdm

#Local code
from userConfig import loc, train_vars, train_vars_vtx
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

intLumi        = 5.0e+06 #in pb-1
def run(vars):
    # Load trained model
    bdt = joblib.load(f"{loc.BDT}/xgb_bdt_{vars}.joblib")
    
    #Bc -> tau nu signal
    if(vars=="normal"):
        vars_list = train_vars
    elif(vars=="vtx"):
        vars_list = train_vars_vtx

    #Load samples
    #from https://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php
    N={}
    Sigma={}
    N_sig=1000000
    N["WWmumu"]=10000000
    N["ZZ"]=59800000
    N["Zll"]=49400000
    N["eeZ"]=5000000*2
    Sigma_sig=0.0067643
    Sigma["WWmumu"]=0.25792
    Sigma["ZZ"]=1.35899
    Sigma["Zll"]=5.288
    Sigma["eeZ"]=0.10368*2


    #Bc -> tau nu signal
    path = f"{loc.PKL}"
    df_sig = pd.read_pickle(f"{path}/mumuH.pkl")
    df_sig = df_sig[vars_list]
    df_sig["BDT"] = bdt.predict_proba(df_sig).tolist()
    df_sig["BDT"] = df_sig["BDT"].apply(lambda x: x[1])
    df_sig["weight"] = (Sigma_sig /N_sig) * intLumi
    #Z -> qq inclusive
    df_bkg = {}
    x_bkg = {}
    y_bkg = {}
    bkgs = {"WWmumu": ["#d1e5f0","W^{+}(\\mu^{+}\\nu_{\\mu})W^{-}(\\mu^{-}\\bar{nu_{\\mu}})"],
            "ZZ": ["#92c5de","ZZ"],
            "Zll": ["#2166ac","Z/\\gamma\\to\\mu^{+}\\mu^{-}"],
            "eeZ": ["#ff00ff", "eeZ"]
            }
    for q in tqdm(bkgs):
        df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")
        N_tmp = len(df_bkg[q])
        N_input = 200000
        #df_bkg[q] = df_bkg[q].sample(n=N_input,random_state=100)
        df_bkg[q] = df_bkg[q].sample(frac=1,random_state=100) 
        df_bkg[q] = df_bkg[q][vars_list]
        df_bkg[q]["BDT"] = bdt.predict_proba(df_bkg[q]).tolist()
        df_bkg[q]["BDT"] = df_bkg[q]["BDT"].apply(lambda x: x[1])
        #df_bkg[q]["weight"] = (Sigma[q] *N_tmp*intLumi)/(N[q]*N_input)
        df_bkg[q]["weight"] = (Sigma[q] *intLumi)/(N[q]) 

    #df_bkg_tot = df_bkg["ZZ"].append(df_bkg["WWmumu"])
    #df_bkg_tot = df_bkg_tot.append(df_bkg["Zll"])
    #df_bkg_tot = df_bkg_tot.append(df_bkg["eeZ"])
    #Shuffle the background so it is an even mixture of the modes
    #df_bkg_tot = df_bkg_tot.sample(frac=1)
    #Signal and background labels
    #df_sig = df_sig[vars_list]
    #df_bkg_tot = df_bkg_tot[vars_list]
    #df_sig["label"] = 1
    #df_bkg_tot["label"] = 0
    #df_tot = df_sig.append(df_bkg_tot)
    #plot ROC curve
    #Create ROC curves
    #x = df_tot[vars_list]
    #y = df_tot["label"]
    #x = x.to_numpy()
    #y = y.to_numpy()
    #df_tot["BDT"] = bdt.predict_proba(df_tot[vars_list]).tolist()
    #df_tot["BDT"] = df_tot["BDT"].apply(lambda x: x[1])
    
    # Compute ROC curves and area under the curve
    #fpr, tpr, thresholds = roc_curve(y, df_tot["BDT"])
    #roc_auc = auc(fpr, tpr)

    #fig, ax = plt.subplots(figsize=(8,8))
    #plt.plot(fpr, tpr, lw=1.5, color="k", label='ROC (area = %0.3f)'%(roc_auc))
    #plt.plot([0., 1.], [0., 1.], linestyle="--", color="k", label='50/50')
    #plt.xlim(0.,1.)
    #plt.ylim(0.,1.)
    #plt.ylabel('Signal efficiency',fontsize=30)
    #plt.xlabel('Background efficiency',fontsize=30)
    #ax.tick_params(axis='both', which='major', labelsize=25)
    #plt.legend(loc="lower right",fontsize=20)
    #plt.grid()
    #plt.tight_layout()
    #fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_ROC_{vars}.pdf")
    
    #compute the significance
    df_bkg_tot = pd.concat((df_bkg[q] for q in bkgs), ignore_index=True)
    df_Z = ut.Significance(df_sig, df_bkg_tot,nbins=100)
    max_index=df_Z["Z"].idxmax()
    print('max-Z: {:.2f}'.format(df_Z.loc[max_index,"Z"]), 'cut threshold: [', max_index, ']')
    fig, ax = plt.subplots(figsize=(12,8))
    plt.scatter(df_Z.index, df_Z["Z"])
    ax.scatter(x=max_index, y=df_Z.loc[max_index,"Z"], c='r', marker="*")
    plt.xlabel("BDT Score ")
    plt.ylabel("Significance")
    txt1 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    txt2 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0) 
    plt.legend([txt1, txt2], ('max-Z: {:.2f} cut threshold: [{:.2f}]'.format(df_Z.loc[max_index,"Z"],max_index), "$Z = \\sqrt{2*((S+B)*log(1+S/B)-S)}$"))
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_Significance_Z0_{vars}.pdf") 

    #compute the significance
    df_bkg_tot = pd.concat((df_bkg[q] for q in bkgs), ignore_index=True)
    df_Z = ut.Significance(df_sig, df_bkg_tot,func=ut.Z, nbins=100)
    max_index=df_Z["Z"].idxmax()
    print('max-Z: {:.2f}'.format(df_Z.loc[max_index,"Z"]), 'cut threshold: [', max_index, ']')
    fig, ax = plt.subplots(figsize=(12,8))
    plt.scatter(df_Z.index, df_Z["Z"])
    ax.scatter(x=max_index, y=df_Z.loc[max_index,"Z"], c='r', marker="*")
    plt.xlabel("BDT Score ")
    plt.ylabel("Significance")
    txt1 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    txt2 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0) 
    plt.legend([txt1, txt2], ('max-Z: {:.2f} cut threshold: [{:.2f}]'.format(df_Z.loc[max_index,"Z"],max_index), "$Z = S/\\sqrt{S+B}$"))
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_Significance_Z_{vars}.pdf") 

    #df_bkg_tot['isSignal'] = 0
    #sys.exit() 
    #plot BDT normalizaed counts as function of BDT
    fig, ax = plt.subplots(figsize=(12,8))
    xmin = 0
    xmax = 1
    bins_bkg = int(np.sqrt(len(df_bkg["ZZ"])))
    bins_sig = int(np.sqrt(len(df_sig)))
    bins_bkg = 100
    bins_sig = 100
    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='step',linewidth=1.5)
    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='stepfilled',alpha=0.3,linewidth=1.5,label="$e^{+}e^{-}\\rightarrow Z(\\mu^{+}\\mu^{-})H$")
    for q in bkgs:
        plt.hist(df_bkg[q]["BDT"],bins=bins_bkg,range=(xmin,xmax),density=True,color=bkgs[q][0],histtype='step',linewidth=1.5,label="$e^{+}e^{-} \\to %s$" % bkgs[q][1])
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Normalised counts",fontsize=30)
    plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,50*ymax)
    plt.legend(fontsize=25, loc="upper left")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_BDT_{vars}.pdf")

    #Plot efficiency as a function of BDT cut in each sample
    BDT_cuts = np.linspace(0,99,99)
    N_sig = len(df_sig)
    N_WWmumu = len(df_bkg["WWmumu"])
    N_ZZ = len(df_bkg["ZZ"])
    N_Zll = len(df_bkg["Zll"])
    eff_sig = []
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
        for q in bkgs:
            eff_bkg[q].append(float(len(df_bkg[q].query("BDT > %s" % cut_val))) / N_bkg[q])

    fig, ax = plt.subplots(figsize=(12,8))

    plt.plot(cut_vals, eff_sig, color="#b2182b",label="$e^{+}e^{-}\\rightarrow Z(\\mu^{+}\\mu^{-})H$")
    for q in bkgs:
        plt.plot(cut_vals, eff_bkg[q], color=bkgs[q][0],label="$e^{+}e^{-} \\to %s$" % bkgs[q][1])

    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Efficiency",fontsize=30)
    #plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,1.3)
    plt.legend(fontsize=20, loc="best")
    plt.grid(alpha=0.4,which="both")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_BDT_eff_nolog_{vars}.pdf")

    #Plot significance as a function of BDT cut in each sample
    BDT_cuts = np.linspace(0,999,999)
    N_sig_tot = len(df_sig)
    N_WWmumu_tot = len(df_bkg["WWmumu"])
    N_ZZ_tot = len(df_bkg["ZZ"])
    N_Zll_tot = len(df_bkg["Zll"])
    
    Significance = []
    cut_vals = []
    for x in BDT_cuts:
        cut_val = float(x)/100
        cut_vals.append(cut_val)
        N_sig=float(len(df_sig.query("BDT > %s" % cut_val)))
        N_bkg = 0
        for q in bkgs:
            N_bkg = N_bkg + float(len(df_bkg[q].query("BDT > %s" % cut_val)))
        if (N_bkg+N_sig)==0:
          Significance.append(0)
        else:
          Significance.append(N_sig/np.sqrt(N_sig+N_bkg))
        #print (N_sig)
        #print (N_bkg)
    #print(Significance)
    fig, ax = plt.subplots(figsize=(12,8))

    plt.plot(cut_vals, Significance, color="#b2182b",label="$S/\\sqrt{S+B}, S: mumuH, B: ZZ, WWmumu, Zll$")
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Significnace",fontsize=30)
    plt.yscale('log')
    #ymin,ymax = plt.ylim()
    #plt.ylim(ymin,2)
    plt.legend(fontsize=25, loc="lower left")
    plt.grid(alpha=0.4,which="both")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_BDT_Sig_{vars}.pdf")


def main():
    parser = argparse.ArgumentParser(description='Plot xgb model for ZH Recoil')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    args = parser.parse_args()

    run(args.Vars)

if __name__ == '__main__':
    main()

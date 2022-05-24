import numbers
from re import I
import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score
#from root_pandas import read_root
import uproot
import ROOT
import joblib
import glob
import seaborn as sns

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
#from userConfig import loc, mode, train_vars, train_vars_vtx, mode_names
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut

def run(vars):

    #Bc -> tau nu signal
    if(vars=="normal"):
        vars_list = train_vars
    elif(vars=="vtx"):
        vars_list = train_vars_vtx
    print("TRAINING VARS")
    print(vars_list)
    path = f"{loc.PKL}"
    df_sig = pd.read_pickle(f"{path}/mumuH.pkl")
    df_sig = df_sig[vars_list]
    print(f"Number of signal events: {len(df_sig)}")

    path_gen_sig = f"{loc.TRAIN}/{mode_names['mumuH']}"
    files_sig = glob.glob(f"{path_gen_sig}/*.root")
    
    N_sig = int(0)
    for f_sig in files_sig:
        NT_TParam = uproot.open(f_sig)["eventsProcessed"]
        #df_gen_sig = tree.arrays(library="pd")
        #N_sig = N_sig + df_gen_sig.iloc[0]["eventsProcessed"]
        N_sig = N_sig + NT_TParam.value
    eff_sig = float(len(df_sig))/N_sig
    
    #xsec, from http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php
    xsec = {}
    xsec["mumuH"] = 0.0067643
    xsec["WWmumu"] = 0.25792
    xsec["ZZ"] = 1.35899
    xsec["Zll"] = 5.288
    xsec["eeZ"] = 0.20736
    #Efficiency of the pre-selection equirements on each bkg
    eff = {}
    #Number of generated events for each background type
    N = {}

    bkgs = ["ZZ","WWmumu","Zll","eeZ"]

    #Loop over all background files and calculate total number of generated events
    for q in bkgs:
        if (q=="eeZ"):
            path_egamma = f"{loc.TRAIN}/{mode_names['egamma']}"
            path_gammae = f"{loc.TRAIN}/{mode_names['gammae']}"
            files = glob.glob(f"{path_egamma}/*.root") + glob.glob(f"{path_gammae}/*.root")
        else:
            #Location of MC files
            path_gen = f"{loc.TRAIN}/{mode_names[q]}"
            #List of all sub-files in the path
            files = glob.glob(f"{path_gen}/*.root")
          

        N[q] = 0
        for f in files:
            NT_Param = uproot.open(f)["eventsProcessed"]
            #df_gen = tree.arrays(library="pd")
            #df_gen = read_root(f,"metadata")
            #N[q] = N[q] + df_gen.iloc[0]["eventsProcessed"]
            N[q] = N[q] + NT_Param.value 
    df_bkg = {}
    for q in bkgs:
        df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")#,usecols=vars_list)
        df_bkg[q] = df_bkg[q][vars_list]
        print(f"Total size of {q} sample: {len(df_bkg[q])}")
        eff[q] = float(len(df_bkg[q]))/N[q]
        print(f"Efficiency of pre-selection on {q} sample: {eff[q]}")
    
    xsec_tot_bkg = eff["ZZ"]*xsec["ZZ"] + eff["WWmumu"]*xsec["WWmumu"] + eff["Zll"]*xsec["Zll"] + eff["eeZ"]*xsec["eeZ"]
   
    
    for q in bkgs:
        df_bkg[q] = df_bkg[q].sample(n=int(N_sig*((eff[q]*xsec[q])/xsec_tot_bkg)),random_state=10)
        print(f"Size of {q} in combined sample: {len(df_bkg[q])}")

    #Make a combined background sample according to BFs
    df_bkg_tot = pd.concat((df_bkg[q] for q in bkgs), ignore_index=True)
    #Shuffle the background so it is an even mixture of the modes
    df_bkg_tot = df_bkg_tot.sample(frac=1)
    
    #Signal and background labels
    df_sig['isSignal'] = 1
    df_bkg_tot['isSignal'] = 0
    #Combine the datasets
    # final DF
    df_tot = pd.concat((df_sig,df_bkg_tot),ignore_index=True)
    #df_tot = df_sig.append(df_bkg_tot) 
    df_tot = df_tot.sample(frac=1)

    #split into data train and data test
    df_train, df_test = train_test_split(df_tot, test_size=0.33, random_state=7) 
    df_tot.loc[df_train.index, "test"] = False
    df_tot.loc[df_test.index, "test"] = True
    X_train = df_train[vars_list]
    y_train = df_train['isSignal']
    X_test  = df_test[vars_list]
    y_test  = df_test['isSignal']

    X_train =  X_train.to_numpy()   
    y_train =  y_train.to_numpy() 
    X_test  =  X_test.to_numpy() 
    y_test  =  y_test.to_numpy() 
    #BDT
    config_dict = {
            "n_estimators"      : 1000,
            "learning_rate"     : 0.15,
            "max_depth"         : 10,
            'subsample'         : 0.5,
            'gamma'             : 3,
            'min_child_weight'  : 10,
            'max_delta_step'    : 0,
            'colsample_bytree'  : 0.5,
            }
    early_stopping_round = 100
    # Training
    bdt = xgb.XGBClassifier(n_estimators    =config_dict["n_estimators"],
                            max_depth       =config_dict["max_depth"],
                            learning_rate   =config_dict["learning_rate"],
                            subsample       =config_dict["subsample"],
                            gamma           =config_dict["gamma"],
                            min_child_weight=config_dict["min_child_weight"], 
                            max_delta_step  =config_dict["max_delta_step"],
                            colsample_bytree=config_dict["colsample_bytree"],
                            #feature_names=vars_list,
                            )
    eval_set = [(X_train, y_train), (X_test, y_test)]
    ##Fit the model
    print("Training model")
    bdt.fit(X_train, y_train, eval_metric=["error", "logloss", "auc"], eval_set=eval_set, early_stopping_rounds=early_stopping_round, verbose=True)
    best_iteration = bdt.best_iteration + 1 
    #if best_iteration < config_dict["n_estimators"]:
    if True:
              print("early stopping after {0} boosting rounds".format(best_iteration))
              print("")
    feature_importances = pd.DataFrame(bdt.feature_importances_,
                                        index = vars_list,
                                       columns=['importance']).sort_values('importance',ascending=False)

    #Write the model to a ROOT file on EOS, for application elsewhere in FCCAnalyses
    out = f"{loc.BDT}"
    print("Writing xgboost model to ROOT file")
    ROOT.TMVA.Experimental.SaveXGBoost(bdt, "ZH_Recoil_BDT", f"{out}/xgb_bdt_{vars}.root", num_inputs=len(vars_list))
    #Write model to joblib file
    joblib.dump(bdt, f"{out}/xgb_bdt_{vars}.joblib")

    # Add new column for the BDT output
    df_tot.loc[df_train.index, "score"] = bdt.predict_proba(X_train)[:,1]
    df_tot.loc[df_test.index, "score"] = bdt.predict_proba(X_test)[:,1]
    
    print("Feature importances")
    print(feature_importances)
    
    # make predictions for test data
    y_pred = bdt.predict(X_test)
    predictions = [round(value) for value in y_pred]
    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    
    # retrieve performance metrics
    results = bdt.evals_result()
    epochs = len(results['validation_0']['error'])
    x_axis = range(0, epochs)
    
    # plot log loss
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['logloss'], label='Train')
    ax.plot(x_axis, results['validation_1']['logloss'], label='Test')
    plt.axvline(best_iteration, color="gray", label="Optimal tree number")
    ax.legend()
    plt.xlabel("Number of trees")
    plt.ylabel('Log Loss')
    plt.title('XGBoost Log Loss')
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_logloss_{vars}.pdf")
    
    # plot classification error
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['error'], label='Train')
    ax.plot(x_axis, results['validation_1']['error'], label='Test')
    plt.axvline(best_iteration, color="gray", label="Optimal tree number")
    ax.legend()
    plt.xlabel("Number of trees")
    plt.ylabel('Classification Error')
    plt.title('XGBoost Classification Error')
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_error_{vars}.pdf")

    # plot classification error
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['auc'], label='Train')
    ax.plot(x_axis, results['validation_1']['auc'], label='Test')
    plt.axvline(best_iteration, color="gray", label="Optimal tree number")
    ax.legend()
    plt.xlabel("Number of trees")
    plt.ylabel('auc')
    plt.title('XGBoost auc')
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_auc_{vars}.pdf")

    # plot ROC 1
    fig, axes = plt.subplots(1, 1, figsize=(5,5))
    df_train = df_tot.query('test==False')
    df_valid =  df_tot.query("test==True")
    eps=0.
    ax=axes
    ax.set_xlabel("$\epsilon_B$")
    ax.set_ylabel("$\epsilon_S$")
    ut.plot_roc_curve(df_valid, "score", ax=ax, label="valid sample", tpr_threshold=eps)
    ut.plot_roc_curve(df_train, "score", ax=ax, color="#ff7f02", tpr_threshold=eps,linestyle='--', label="train sample")
    plt.plot([eps, 1], [eps, 1], color='navy', lw=2, linestyle='--')
    ax.set_title('ROC')
    ax.legend()
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_ROC1_{vars}.pdf")

    #plot score with trained, test, signal, backgrounds
    fig, axes = plt.subplots(1, 1, figsize=(5,5))
    Bins = 20
    htype="step"
    #plt.figure()
    tag=['signal_train', 'signal_valid', 'bkg_train', 'bkg_valid']
    line=['solid', 'dashed', 'solid', 'dashed']
    color=['red', 'red', 'blue', 'blue']
    cut=['test==False & isSignal==1', 'test==True & isSignal==1', 'test==False & isSignal!=1', 'test==True & isSignal!=1']
    for (x,y,z,w) in zip(tag, line, color, cut):
        df_instance = df_tot.query(w)
        print(x, len(df_instance), "Ratio: %.2f%%" % ((len(df_instance)/float(len(df_tot)))* 100.0))
        # better to recover the negative weights when evaluating the performance
        #print(df_instance['score'])
        #print(df_instance.index) 
        plt.hist(df_instance['score'], density=True, bins=Bins, histtype=htype, label=x, linestyle=y, color=z)
    ax = axes
    plt.yscale('log')
    ax.legend(loc=2, ncol=2)
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_SB_{vars}.pdf")
    
    #Create ROC curves
    decisions_train = bdt.predict_proba(X_train)[:,1]
    decisions_test = bdt.predict_proba(X_test)[:,1]
    # Compute ROC curves and area under the curve
    fpr_train, tpr_train, thresholds_train = roc_curve(y_train, decisions_train)
    fpr_test, tpr_test, thresholds_test = roc_curve(y_test, decisions_test)
    roc_auc_train = auc(fpr_train, tpr_train)
    roc_auc_test = auc(fpr_test, tpr_test)
    
    fig, ax = plt.subplots(figsize=(8,8))
    plt.plot(tpr_train, fpr_train, lw=1.5, color="k", label='train ROC (area = %0.3f)'%(roc_auc_train))
    plt.plot(tpr_test, fpr_test, lw=1.5, color="#ff7f02", label='test ROC_test (area = %0.3f)'%(roc_auc_test))
    plt.xlim(0.,1.)
    plt.ylabel('Background rejection',fontsize=30)
    plt.xlabel('Signal efficiency',fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.legend(loc="upper right",fontsize=20)
    plt.grid()
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_ROC_{vars}.pdf")
    
    ## visualize the three
    #plt.figure(figsize = (50,200))
    #ax = plt.subplot(111) 
    #xgb.plot_tree(bdt,num_trees=1,ax=ax,rankdir='LR')
    #plt.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_Tree_{vars}.pdf")

    # plot importance
    #plt.figure(figsize = (30,30))
    #ax = plt.subplot(111)
    fig, ax = plt.subplots(figsize=(12, 6))
    xgb.plot_importance(bdt,ax=ax)
    #xgb.plot_importance(bdt).set_yticklabels(vars_list)
    plt.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_Importance_{vars}.pdf")

    fig, ax = plt.subplots(figsize=(12, 6))
    df_Z = ut.thres_opt(df_tot)
    max_col=df_Z.max().idxmax()
    max_index=df_Z[max_col].idxmax()
    print('max-Z: {:.2f}'.format(df_Z.loc[max_index,max_col]), 'cut threshold: [', max_col, max_index, ']')
    plt.title('Z-scan plot')
    ax = sns.heatmap(df_Z, vmin=0.0, cmap="Blues", cbar_kws={'label':'Significance'})
    ax.set(xlabel='low thres', ylabel='high thres')
    ax.scatter(x=np.where(df_Z.columns==max_col), y=np.where(df_Z.columns==max_index), c='r', marker="*")
    plt.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_Z_scan_{vars}.pdf") 

    fig, ax = plt.subplots(figsize=(12, 6))
    df_Z = ut.thres_opt(df_tot, func=ut.Zmu)
    max_col=df_Z.max().idxmax()
    max_index=df_Z[max_col].idxmax()
    print('max-Z: {:.2f}'.format(df_Z.loc[max_index,max_col]), 'cut threshold: [', max_col, max_index, ']')
    plt.title('Z-scan plot')
    ax = sns.heatmap(df_Z, vmin=0.0, cmap="Blues", cbar_kws={'label':'Significance'})
    ax.set(xlabel='low thres', ylabel='high thres')
    ax.scatter(x=np.where(df_Z.columns==max_col), y=np.where(df_Z.columns==max_index), c='r', marker="*")
    plt.savefig(f"{loc.PLOTS}/mumuH_vs_ZZ_WWmumu_Zll_eeZ_Zmu_scan_{vars}.pdf") 
   
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def main():
    parser = argparse.ArgumentParser(description='Train xgb model for ZH recoil study')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    args = parser.parse_args()

    run(args.Vars)

if __name__ == '__main__':
    main()

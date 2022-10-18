import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot
import joblib
import glob
from scipy import interpolate
import pickle
import argparse
from collections import OrderedDict

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
from userConfig import loc, mode_names, train_vars, train_vars_vtx, train_vars_2, Ediff_cut, Nsig_min, MVA_cuts, FCC_label
import plotting
import utils as ut
from decay_mode_xs import modes as bkg_modes
from decay_mode_xs import prod


def run(Sig):

    #BDT variables to optimise, and the hemisphere energy difference which we cut on > 10 GeV
    var_list = ["EVT_MVA1Bis", "EVT_MVA2_bc", "EVT_MVA2_bu", "EVT_ThrustEmax_E", "EVT_ThrustEmin_E"]
    path = loc.ANALYSIS 
 
    EVT_MVA2 = 'EVT_MVA2_bc'
    if Sig == 'bu':
      EVT_MVA2 = 'EVT_MVA2_bu'

    Cut_truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'
    Cut_sel = f'{Cut_truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
    cut = f"EVT_MVA1Bis > 0.6 and {EVT_MVA2} > 0.6 and {Cut_sel}"

    MVA_values = {"EVT_MVA1Bis": {0.6:  "#37006E", 
                                  0.8:  "#5300C7", 
                                  0.9:  "#9945ED", 
                                  0.95: "#8660AC", 
                                  0.98: "#B381E6"},
 
                  "EVT_MVA2_bc": {0.6:  "#825D14", 
                                  0.7:  "#B5821B", 
                                  0.8:  "#E0A021", 
                                  0.9:  "#DBC08A", 
                                  0.95: "#F5DCA9"}, 

                  "EVT_MVA2_bu": {0.6:  "#825D14", 
                                  0.7:  "#B5821B", 
                                  0.8:  "#E0A021", 
                                  0.9:  "#DBC08A", 
                                  0.95: "#F5DCA9"}
                 }

    plot_vars = {
                "EVT_ThrustEmax_E": {"name": "Maximum hemisphere E", "low": 22., "high": 52., "unit": "GeV/$c^2$"},
                "EVT_ThrustEmin_E": {"name": "Minimum hemisphere E", "low": 2.,  "high": 42., "unit": "GeV/$c^2$"},
               }

    # consider Zbb and Zcc bkg processes
    N_gen_bb = uproot.open(f"{path}/p8_ee_Zbb_ecm91.root")["eventsProcessed"].value
    print(f"Number generated for bb: {N_gen_bb}")
    tree_bb = uproot.open(f"{path}/p8_ee_Zbb_ecm91.root")["events"]
    df_bb = tree_bb.arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
    df_bb = df_bb.query(cut)
    df_bb = df_bb[var_list]
    print (f"bb : {len(df_bb)}")

    N_gen_cc = uproot.open(f"{path}/p8_ee_Zcc_ecm91.root")["eventsProcessed"].value
    print(f"Number generated for cc: {N_gen_cc}")
    tree_cc = uproot.open(f"{path}/p8_ee_Zcc_ecm91.root")["events"]
    df_cc = tree_cc.arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
    df_cc = df_cc.query(cut)
    df_cc = df_cc[var_list]
    print (f"cc : {len(df_cc)}")

    #Number of Z's expected
    N_Z = 5.0 * 1e12
    #PDG BF(Z -> bb)
    BF_Zbb = 0.1512
    BF_Zcc = 0.1203
    #different from the N_bb in estimate_purity.py
    N_bb = N_Z * BF_Zbb 
    N_cc = N_Z * BF_Zcc


    hists = {}
    N_evt = {}
    for stage in ["EVT_MVA1Bis", EVT_MVA2]:
      other_cut = "EVT_MVA1Bis > 0.9"
      if stage   == "EVT_MVA1Bis": other_cut = EVT_MVA2 + "> 0.8"

      for var in plot_vars:
        hists[stage+var] = {}
        N_evt[stage+var] = {}
        fig, ax = plt.subplots(figsize=(12,8))
        print (f"\n\nscan cuts for {stage}:")
        for MVA_cut in MVA_values[stage]:
          cut_MVA = f"{stage} > {MVA_cut} and {other_cut}"
          temp_bb = df_bb.query(cut_MVA)
          temp_cc = df_cc.query(cut_MVA)
          temp_tot = temp_bb.append(temp_cc)
          print (f"{cut_MVA} :    {len(temp_bb)} bb events, {len(temp_cc)} cc events")
          plt.hist(temp_tot[var], bins=40, range=(plot_vars[var]["low"], plot_vars[var]["high"]),density=True,color=MVA_values[stage][MVA_cut],histtype='step',linewidth=1.5,label=cut_MVA.replace("EVT_","").replace("Bis","").replace(">","$>$"))

        ax.tick_params(axis='both', which='major', labelsize=25)
        ax.set_title( FCC_label, loc='right', fontsize=20)
        plt.xlim(plot_vars[var]["low"], plot_vars[var]["high"])
        plt.xlabel(var.replace('_', '\_') + " (GeV)",fontsize=30)
        plt.ylabel("Normalised distribution (a.u.)",fontsize=30)
        plt.yscale('linear')
        ymin,ymax = plt.ylim()
        plt.ylim(ymin,1.5*ymax)
        plt.legend(fontsize=20, loc="upper left")
        plt.tight_layout()
        fig.savefig(f"{loc.PLOTS}/cat_{Sig}_shape_{var}_scan_{stage}.png")



def main():
    parser = argparse.ArgumentParser(description='Estimate optimal cuts and associated yields')
    parser.add_argument("--Sig", choices=['bu','bc'],required=False,default='bc')
    args = parser.parse_args()

    run(args.Sig)

if __name__ == '__main__':
    main()

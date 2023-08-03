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
from decay_mode_xs import prod, b_hadrons, c_hadrons


def run(Sig):

    #BDT variables to optimise, and the hemisphere energy difference which we cut on > 10 GeV
    var_list = ["EVT_MVA1Bis", "EVT_MVA2_bc", "EVT_MVA2_bu", "EVT_MVA2_bkg", "EVT_ThrustEmax_E", "EVT_ThrustEmin_E"]
    path = loc.ANALYSIS 
 
    EVT_MVA2 = 'EVT_MVA2_bc'
    if Sig == 'bu':
      EVT_MVA2 = 'EVT_MVA2_bu'

    Cut_truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'
    Cut_sel = f'{Cut_truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
    cut = f"EVT_MVA1Bis > {MVA_cuts['base']['MVA1']} and 1 - EVT_MVA2_bkg > {MVA_cuts['base']['MVA2_bkg']} and {EVT_MVA2} > {MVA_cuts['base']['MVA2_sig']} and {Cut_sel}"

    modes = OrderedDict()
    modes['bb'] = OrderedDict()
    modes['cc'] = OrderedDict()
    bb_prefix = "p8_ee_Zbb_ecm91_EvtGen"
    cc_prefix = "p8_ee_Zcc_ecm91_EvtGen"
    #Background decays
    for b in b_hadrons:
        for d in bkg_modes[b]:
            modes['bb'][f"{b}_{d}"] = [f"{bb_prefix}_{b}2{d}", prod[b], bkg_modes[b][d]]

    for c in c_hadrons:
        for d in bkg_modes[c]:
            modes['cc'][f"{c}_{d}"] = [f"{cc_prefix}_{c}2{d}", prod[c], bkg_modes[c][d]]



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


    tree  = {}
    N_gen = {}
    df = {}
    for m in modes["bb"]:
        N_gen[m] = uproot.open(f"{path}/{modes['bb'][m][0]}.root")["eventsProcessed"].value
        tree[m]  = uproot.open(f"{path}/{modes['bb'][m][0]}.root")["events"]
        df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
        df[m] = df[m].query(cut)
        df[m] = df[m][var_list]
        print (f"{m} : {len(df[m])}")
    for m in modes["cc"]:
        N_gen[m] = uproot.open(f"{path}/{modes['cc'][m][0]}.root")["eventsProcessed"].value
        tree[m]  = uproot.open(f"{path}/{modes['cc'][m][0]}.root")["events"]
        df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
        df[m] = df[m].query(cut)
        df[m] = df[m][var_list]
        print (f"{m} : {len(df[m])}")


    other_values = [0.9, 0.95, 0.98, 0.99]
    MVA_values = [0.95, 0.98, 0.987, 0.99, 0.995, 0.999, 0.9995, 0.9999]
    
    for stage in ["EVT_MVA1Bis", "EVT_MVA2_bkg"]:
      other = "EVT_MVA2_bkg"
      if stage == "EVT_MVA2_bkg": other = "EVT_MVA1Bis"

      print (f"\n\nscan cuts for {stage}:")
      base = {}
      base['bb'] = len(df_bb)
      base['cc'] = len(df_cc)
      eff_scan = {}
      eff_scan['bb'] = {}
      eff_scan['cc'] = {}
      eff_scan['bb_comb'] = {}
      eff_scan['cc_comb'] = {}
      for m in df:
          base[m] = len(df[m])
          eff_scan[m] = {}
      for other_cut in other_values: 
        for MVA_cut in MVA_values:
          cut_MVA = f"{stage} > {MVA_cut} and 1 - {other} > {other_cut} "
          if stage == "EVT_MVA2_bkg": cut_MVA = f"1 - {stage} > {MVA_cut} and {other} > {other_cut}"

          temp_bb = df_bb.query(cut_MVA)
          temp_cc = df_cc.query(cut_MVA)
          eff_scan['bb'][MVA_cut] = len(temp_bb) / base['bb']
          eff_scan['cc'][MVA_cut] = len(temp_cc) / base['cc']
          base['bb_comb'] = 0
          base['cc_comb'] = 0
          eff_scan['bb_comb'][MVA_cut] = 0
          eff_scan['cc_comb'][MVA_cut] = 0
          #for m in df:
          for m in modes["bb"]:
            temp_df = df[m].query(cut_MVA)
            eff_scan[m][MVA_cut] = len(temp_df) / base[m]
            base["bb_comb"] += base[m] / N_gen[m] * modes['bb'][m][1] * modes['bb'][m][2]
            eff_scan['bb_comb'][MVA_cut] += len(temp_df) / N_gen[m] * modes['bb'][m][1] * modes['bb'][m][2]
          eff_scan['bb_comb'][MVA_cut] = eff_scan['bb_comb'][MVA_cut] / base["bb_comb"]
          for m in modes["cc"]:
            temp_df = df[m].query(cut_MVA)
            eff_scan[m][MVA_cut] = len(temp_df) / base[m]
            base["cc_comb"] += base[m] / N_gen[m] * modes['cc'][m][1] * modes['cc'][m][2]
            eff_scan['cc_comb'][MVA_cut] += len(temp_df) / N_gen[m] * modes['cc'][m][1] * modes['cc'][m][2]
          eff_scan['cc_comb'][MVA_cut] = eff_scan['cc_comb'][MVA_cut] / base["cc_comb"]

        out_name = f'{loc.TEXT}/bkg_eff_comparison_cat_{Sig}_keep_{other}_{other_cut}_scan_MVA_{stage}.txt' 
        out_f = open(out_name, 'w')
        title = "mode".ljust(20) + "BR".ljust(15) + "base events".ljust(15)
        for MVA_cut in MVA_values:
            title = title + (stage + " > " + f"{MVA_cut}").ljust(20)
        out_f.write (title + '\n')
        bb_line = 'Zbb'.ljust(20) + "-".ljust(15) + f"{base['bb']}".ljust(15)
        for MVA_cut in MVA_values:
            bb_line = bb_line + ("%.3E"%eff_scan['bb'][MVA_cut]).ljust(20)
        out_f.write (bb_line + '\n')
        bb_comb_line = 'Zbb_exc_comb'.ljust(20) + "-".ljust(15) + "-".ljust(15)
        for MVA_cut in MVA_values:
            bb_comb_line = bb_comb_line + ("%.3E"%eff_scan['bb_comb'][MVA_cut]).ljust(20)
        out_f.write (bb_comb_line + '\n')
        for m in modes['bb']:
          exc_line = m.ljust(20) + f"{modes['bb'][m][2]}".ljust(15) + f"{base[m]}".ljust(15)
          for MVA_cut in MVA_values:
            exc_line = exc_line + ("%.3E"%eff_scan[m][MVA_cut]).ljust(20)
          out_f.write (exc_line + '\n')

        out_f.write ('\n')
        cc_line = 'Zcc'.ljust(20) + "-".ljust(15) + f"{base['cc']}".ljust(15)
        for MVA_cut in MVA_values:
            cc_line = cc_line + ("%.3E"%eff_scan['cc'][MVA_cut]).ljust(20)
        out_f.write (cc_line + '\n')
        cc_comb_line = 'Zcc_exc_comb'.ljust(20) + "-".ljust(15) + "-".ljust(15)
        for MVA_cut in MVA_values:
            cc_comb_line = cc_comb_line + ("%.3E"%eff_scan['cc_comb'][MVA_cut]).ljust(20)
        out_f.write (cc_comb_line + '\n')
        for m in modes['cc']:
          exc_line = m.ljust(20) + f"{modes['cc'][m][2]}".ljust(15) + f"{base[m]}".ljust(15)
          for MVA_cut in MVA_values:
            exc_line = exc_line + ("%.3E"%eff_scan[m][MVA_cut]).ljust(20)
          out_f.write (exc_line + '\n')

def main():
    parser = argparse.ArgumentParser(description='Estimate optimal cuts and associated yields')
    parser.add_argument("--Sig", choices=['bu','bc'],required=False,default='bu')
    args = parser.parse_args()

    run(args.Sig)

if __name__ == '__main__':
    main()

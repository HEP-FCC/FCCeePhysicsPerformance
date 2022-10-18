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
    var_list = ["EVT_MVA1Bis", "EVT_MVA2_bc", "EVT_MVA2_bu", "EVT_ThrustEmax_E", "EVT_ThrustEmin_E"]
    path = loc.ANALYSIS 
 
    EVT_MVA2 = 'EVT_MVA2_bc'
    if Sig == 'bu':
      EVT_MVA2 = 'EVT_MVA2_bu'

    Cut_truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'
    Cut_sel = f'{Cut_truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
    cut = f"EVT_MVA1Bis > {MVA_cuts['base']['MVA1']} and {EVT_MVA2} > {MVA_cuts['base']['MVA2']} and {Cut_sel}"

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


    cut_MVA = f"EVT_MVA1Bis > {MVA_cuts['tight']['MVA1']} and {EVT_MVA2} > {MVA_cuts['tight']['MVA2']}"
    base = {}
    count = {}
    eff_scan = {}
    for m in df:
        base[m] = len(df[m])
        eff_scan[m] = {}

    base['bb_comb'] = 0
    base['cc_comb'] = 0
    count['bb_comb'] = 0
    count['cc_comb'] = 0
    eff_scan['bb_comb'] = 0
    eff_scan['cc_comb'] = 0
    #for m in df:
    for m in modes["bb"]:
      temp_df = df[m].query(cut_MVA)
      count[m] = len(temp_df)
      eff_scan[m] = count[m] / base[m]
      count['bb_comb'] += count[m]
      base['bb_comb'] += base[m] / N_gen[m] * modes['bb'][m][1] * modes['bb'][m][2]
      eff_scan['bb_comb'] += len(temp_df) / N_gen[m] * modes['bb'][m][1] * modes['bb'][m][2]
    eff_scan['bb_comb'] = eff_scan['bb_comb'] / base["bb_comb"]
    for m in modes["cc"]:
      temp_df = df[m].query(cut_MVA)
      count[m] = len(temp_df)
      eff_scan[m] = count[m] / base[m]
      count['cc_comb'] += count[m]
      base["cc_comb"] += base[m] / N_gen[m] * modes['cc'][m][1] * modes['cc'][m][2]
      eff_scan['cc_comb'] += len(temp_df) / N_gen[m] * modes['cc'][m][1] * modes['cc'][m][2]
    eff_scan['cc_comb'] = eff_scan['cc_comb'] / base["cc_comb"]


    print (f'In {Sig} cat:')
    print (cut_MVA)
    title = "mode".ljust(20) + "BR".ljust(15) + "event count".ljust(15) + "tight eff regarding baseline".ljust(30)
    print (title)
    bb_line = 'Zbb_exc_comb'.ljust(20) + "-".ljust(15) + f"{count['bb_comb']}".ljust(15) + ("%.3E"%eff_scan['bb_comb']).ljust(30)
    print (bb_line)
    for m in modes['bb']:
      exc_line = m.ljust(20) + f"{modes['bb'][m][2]}".ljust(15) + f"{count[m]}".ljust(15) + ("%.3E"%eff_scan[m]).ljust(30)
      print (exc_line)
    print ('\n')
    cc_line = 'Zcc_exc_comb'.ljust(20) + "-".ljust(15) + f"{count['cc_comb']}".ljust(15) + ("%.3E"%eff_scan['cc_comb']).ljust(30)
    print (cc_line)
    for m in modes['cc']:
      exc_line = m.ljust(20) + f"{modes['cc'][m][2]}".ljust(15) + f"{count[m]}".ljust(15) + ("%.3E"%eff_scan[m]).ljust(30)
      print (exc_line)



def main():
    parser = argparse.ArgumentParser(description='Estimate optimal cuts and associated yields')
    parser.add_argument("--Sig", choices=['bu','bc'],required=False,default='bc')
    args = parser.parse_args()

    run(args.Sig)

if __name__ == '__main__':
    main()

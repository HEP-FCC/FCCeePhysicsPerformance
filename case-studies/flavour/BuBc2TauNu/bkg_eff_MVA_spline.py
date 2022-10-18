import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
import pickle
from decay_mode_xs import modes as bkg_modes
from decay_mode_xs import prod, b_hadrons, c_hadrons
from scipy import interpolate
import time

#Local code
from userConfig import loc, train_vars, train_vars_vtx, Ediff_cut, NBin_MVA_fit, MVA_cuts
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)



def run(cat):

    #BDT variables to optimise, and the hemisphere energy difference which we cut on > 10 GeV
    var_list = ["EVT_MVA1Bis", "EVT_MVA2_bc", "EVT_MVA2_bu", "EVT_MVA2_bkg", "EVT_ThrustEmax_E", "EVT_ThrustEmin_E"]
    path = loc.ANALYSIS

    EVT_MVA2 = 'EVT_MVA2_bc'
    if cat == 'bu':
      EVT_MVA2 = 'EVT_MVA2_bu'

    Cut_truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'
    Cut_sel = f'{Cut_truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
    cut = f"EVT_MVA1Bis > {MVA_cuts['tight']['MVA1']} and {EVT_MVA2} > {MVA_cuts['tight']['MVA2']} and {Cut_sel}"

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
        df[m]["log_EVT_MVA1"] = -np.log(1. - df[m]["EVT_MVA1Bis"])
        df[m]["log_EVT_MVA2_bkg"] = -np.log(df[m]["EVT_MVA2_bkg"])
        df[m]["log_EVT_MVA2_sig"] = -np.log(1. - df[m][EVT_MVA2])
        print (f"{m} : {len(df[m])}")
    for m in modes["cc"]:
        N_gen[m] = uproot.open(f"{path}/{modes['cc'][m][0]}.root")["eventsProcessed"].value
        tree[m]  = uproot.open(f"{path}/{modes['cc'][m][0]}.root")["events"]
        df[m] = tree[m].arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
        df[m] = df[m].query(cut)
        df[m] = df[m][var_list]
        df[m]["log_EVT_MVA1"] = -np.log(1. - df[m]["EVT_MVA1Bis"])
        df[m]["log_EVT_MVA2_bkg"] = -np.log(df[m]["EVT_MVA2_bkg"])
        df[m]["log_EVT_MVA2_sig"] = -np.log(1. - df[m][EVT_MVA2])
        print (f"{m} : {len(df[m])}")



    # Make spline for MVA1
    print ('\ngetting MVA1 spline\n-------------------')
    time_start = time.time()
    xmin = MVA_cuts["spline"][f'MVA1_in_{cat}']['xmin']
    xmax = MVA_cuts["spline"][f'MVA1_in_{cat}']['xmax']

    base = {}
    count = {}
    weight = {}
    eff_scan = {}
    spline = {}

    for m in df:
        base[m] = len(df[m])
    for flav in ['bb', 'cc']:
      base[flav] = 0
      eff_scan[flav] = 0
      weight[flav] = 0
      bin_edges = 0 

      for m in modes[flav]:
        count[m], bin_edges = np.histogram(df[m]["log_EVT_MVA1"], NBin_MVA_fit['MVA1'], range=(xmin, xmax))
        count[m] = np.flip(count[m])
        count[m] = count[m].cumsum()
        count[m] = np.flip(count[m])
        weight[m] = np.sqrt(count[m])
        base[flav]     += base[m]   / N_gen[m] * modes[flav][m][1] * modes[flav][m][2]
        eff_scan[flav] += count[m]  / N_gen[m] * modes[flav][m][1] * modes[flav][m][2]
        weight[flav]   += weight[m]
      eff_scan[flav] = eff_scan[flav] / base[flav]
      cut_bound = bin_edges[:-1]
      spline[flav] = interpolate.splrep(cut_bound, eff_scan[flav], w=weight[flav])

      print (eff_scan[flav])
      print (weight[flav])
  
      with open(f'{loc.PKL}/spline/{cat}_MVA1_scan_{flav}_spline.pkl', 'wb') as f:
          pickle.dump(spline[flav], f)
    time_stop = time.time()
    print (f'Time for forming MVA1 spline: {time_stop - time_start}')

    # Make grid spline for MVA2
    print ('\ngetting MVA2 spline\n-------------------')
    time_start = time.time()
    sig_min = MVA_cuts["spline"][f'MVA2_sig_in_{cat}']['xmin']
    sig_max = MVA_cuts["spline"][f'MVA2_sig_in_{cat}']['xmax']
    bkg_min = MVA_cuts["spline"][f'MVA2_bkg_in_{cat}']['xmin']
    bkg_max = MVA_cuts["spline"][f'MVA2_bkg_in_{cat}']['xmax']

    for flav in ['bb', 'cc']:
      base[flav] = 0
      eff_scan[flav] = 0
      weight[flav] = 0
      xedges, yedges = 0, 0

      for m in modes[flav]:
        count[m], xedges, yedges = np.histogram2d(df[m]["log_EVT_MVA2_sig"], df[m]["log_EVT_MVA2_bkg"], bins=[NBin_MVA_fit['MVA2_sig'], NBin_MVA_fit['MVA2_bkg']], range=[[sig_min, sig_max],[bkg_min, bkg_max]])
        count[m] = np.flip(count[m])
        count[m] = count[m].cumsum(axis=0)
        count[m] = count[m].cumsum(axis=1)
        count[m] = np.flip(count[m])

        weight[m] = np.sqrt(count[m])
        base[flav]     += base[m]   / N_gen[m] * modes[flav][m][1] * modes[flav][m][2]
        eff_scan[flav] += count[m]  / N_gen[m] * modes[flav][m][1] * modes[flav][m][2]
        weight[flav]   += weight[m]
      eff_scan[flav] = eff_scan[flav] / base[flav]
      cut_bound_x = xedges[:-1]
      cut_bound_y = yedges[:-1]
      spline[flav] = interpolate.RectBivariateSpline(cut_bound_x, cut_bound_y, eff_scan[flav])  # RectBivariateSpline does not take weight

      print (eff_scan[flav])
      print (weight[flav])
      with open(f'{loc.PKL}/spline/{cat}_MVA2_2d_scan_{flav}_spline.pkl', 'wb') as f:
          pickle.dump(spline[flav], f)
    time_stop = time.time()
    print (f'Time for forming MVA2 spline: {time_stop - time_start}') 



    # Make 1D spline for MVA2_bkg, as a cross check
#    print ('\ngetting MVA2 spline\n-------------------')
#    time_start = time.time()
#    bkg_min = MVA_cuts["spline"][f'MVA2_bkg_in_{cat}']['xmin']
#    bkg_max = MVA_cuts["spline"][f'MVA2_bkg_in_{cat}']['xmax']
#
#    for flav in ['bb', 'cc']:
#      base[flav] = 0
#      eff_scan[flav] = 0
#      weight[flav] = 0
#      bin_edges = 0
#
#      for m in modes[flav]:
#        count[m], bin_edges = np.histogram(df[m]["log_EVT_MVA2_bkg"], NBin_MVA_fit['MVA1'], range=(bkg_min, bkg_max))
#        count[m] = np.flip(count[m])
#        count[m] = count[m].cumsum()
#        count[m] = np.flip(count[m])
#        weight[m] = np.sqrt(count[m])
#        base[flav]     += base[m]   / N_gen[m] * modes[flav][m][1] * modes[flav][m][2]
#        eff_scan[flav] += count[m]  / N_gen[m] * modes[flav][m][1] * modes[flav][m][2]
#        weight[flav]   += weight[m]
#      eff_scan[flav] = eff_scan[flav] / base[flav]
#      cut_bound = bin_edges[:-1]
#      spline[flav] = interpolate.splrep(cut_bound, eff_scan[flav], w=weight[flav])
#
#      print (eff_scan[flav])
#      print (weight[flav])
#      with open(f'{loc.PKL}/spline/{cat}_MVA2_1d_bkg_scan_{flav}_spline.pkl', 'wb') as f:
#          pickle.dump(spline[flav], f)
#    time_stop = time.time()
#    print (f'Time for forming MVA2 spline: {time_stop - time_start}')




def main():
    parser = argparse.ArgumentParser(description='Estimate optimal cuts and associated yields')
    parser.add_argument("--cat", choices=['bu','bc'],required=False,default='bc')
    args = parser.parse_args()

    run(args.cat)

if __name__ == '__main__':
    main()


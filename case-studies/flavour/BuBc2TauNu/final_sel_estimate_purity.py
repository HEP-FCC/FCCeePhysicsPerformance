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
from userConfig import loc, train_vars, train_vars_vtx, Ediff_cut, NBin_MVA_fit, MVA_cuts, Eff, Nsig_min
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)


def run(NZ,cat):

    #BDT variables to optimise, and the hemisphere energy difference which we cut on > 10 GeV
    var_list = ["EVT_MVA1Bis", "EVT_MVA2_bc", "EVT_MVA2_bu", "EVT_MVA2_bkg", "EVT_ThrustEmax_E", "EVT_ThrustEmin_E"]
    path = loc.ANALYSIS

    other = 'bu'
    name_sig   = 'Bc2TauNu'
    name_other = 'Bu2TauNu'
    if cat == 'bu':
      other = 'bc'
      name_sig   = 'Bu2TauNu'
      name_other = 'Bc2TauNu'


    file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
    N_gen_sig = uproot.open(f"{path}/{file_prefix}_{name_sig}TAUHADNU.root")["eventsProcessed"].value
    print(f"Number generated for {cat}: {N_gen_sig}")
    df_sig = pd.read_pickle(f"{loc.PKL}/final/{cat.replace('b','B')}_evt_in_{cat}_cat_for_final_sel.pkl")
    df_sig["log_EVT_MVA2_sig"] = df_sig[f"log_EVT_MVA2_{cat}"]
    print (f"process {cat} : {len(df_sig)}")

    N_gen_other = uproot.open(f"{path}/{file_prefix}_{name_other}TAUHADNU.root")["eventsProcessed"].value
    print(f"Number generated for {other}: {N_gen_other}")
    df_other = pd.read_pickle(f"{loc.PKL}/final/{other.replace('b','B')}_evt_in_{cat}_cat_for_final_sel.pkl")
    df_other["log_EVT_MVA2_sig"] = df_other[f"log_EVT_MVA2_{cat}"]
    print (f"process {other} : {len(df_other)}")


    #Number of Z's expected
    N_Z = float(NZ) * 1e12
    #PDG BF(Z -> bb)
    BF_Zbb = 0.1512
    BF_Zcc = 0.1203
    N_bb = N_Z * BF_Zbb
    N_cc = N_Z * BF_Zcc

    # Do not consider factor of 2 for inclusive events
    # (To estimate yields of exclusive samples one should multiply by 2, but we only use exclusive samples for relative efficiencies and not yields.)
    N_tight = {}
    N_tight['bb'] = N_bb * Eff['base'][cat]['Zbb'] * Eff['tight'][cat]['Zbb'] 
    N_tight['cc'] = N_cc * Eff['base'][cat]['Zcc'] * Eff['tight'][cat]['Zcc']
    print (f"Zbb after tight sel in {cat}: {N_tight['bb'] :.3}")
    print (f"Zcc after tight sel in {cat}: {N_tight['cc'] :.3}")

    #Olcyr calculation of BF(Bc -> tau nu)
    BF_Bc2TauNu = 1.94e-2
    #PDG values
    BF_Bu2TauNu = 1.09e-4
    BF_Tau23Pi = 0.0931

    #Pythia Bc production fraction
    Bu_prod_frac = 0.43
    Bc_prod_frac = 0.0004

    # 2 b quarks in every Zbb event
    N_Bc2TauNu = 2 * N_bb * Bc_prod_frac * BF_Bc2TauNu * BF_Tau23Pi
    print("N(Bc -> tau nu): %.0f" % N_Bc2TauNu)
    N_Bu2TauNu = 2 * N_bb * Bu_prod_frac * BF_Bu2TauNu * BF_Tau23Pi
    print("N(Bu -> tau nu): %.0f" % N_Bu2TauNu)

    N_sig2TauNu = N_Bc2TauNu
    N_other2TauNu = N_Bu2TauNu
    if cat == 'bu':
      N_sig2TauNu = N_Bu2TauNu
      N_other2TauNu = N_Bc2TauNu


    spline = {'MVA1': {}, 'MVA2': {}}
    for flav in ['bb', 'cc']:
      with open(f'{loc.PKL}/spline/{cat}_MVA1_scan_{flav}_spline.pkl', 'rb') as f:
        spline['MVA1'][flav] = pickle.load(f)
      with open(f'{loc.PKL}/spline/{cat}_MVA2_2d_scan_{flav}_spline.pkl', 'rb') as f:
#      with open(f'{loc.PKL}/spline/{cat}_MVA2_1d_bkg_scan_{flav}_spline.pkl', 'rb') as f: #for validating bkg scan only
        spline['MVA2'][flav] = pickle.load(f)


    # find final optimal selection
    time_start = time.time()

    eff1 = {}
    eff2 = {}
    n_bkg = {}
    best = {'purity': 0, 'MVA1': 0, 'MVA2_sig': 0, 'MVA2_bkg': 0,
            'n_sig': 0, 'n_other': 0, 'bkg_bb': 0, 'bkg_cc': 0}

    # scan range should be within spline range
    # from BDT eff, best S/B for MVA2_bc is around 0.92, best S/B for MVA2_bu is around 0.995
    # Bc keep high eff for extreme MVA2_bkg, Bu drops fast at extreme MVA2_bkg
#    if cat == 'bc': 
#      # Optimal sel is loose MVA2_bc + tight MVA2_bkg
#      MVA1_min     = MVA_cuts['spline'][f"MVA1_in_{cat}"]["xmin"] + 0.1
#      MVA1_max     = MVA_cuts['spline'][f"MVA1_in_{cat}"]["xmax"] - 0.1
#      MVA2_sig_min = MVA_cuts['spline'][f"MVA2_sig_in_{cat}"]["xmin"] + 1e-4 # 0.90
#      MVA2_sig_max = MVA_cuts['spline'][f"MVA2_sig_in_{cat}"]["xmax"] - 3    # 0.995
#      MVA2_bkg_min = MVA_cuts['spline'][f"MVA2_bkg_in_{cat}"]["xmin"] + 0.5  # 0.03
#      MVA2_bkg_max = MVA_cuts['spline'][f"MVA2_bkg_in_{cat}"]["xmax"] - 0.1  # 0.00037
#    if cat == 'bu': 
#      # Optimal sel is tight MVA2_bu + loose MVA2_bkg
#      MVA1_min     = MVA_cuts['spline'][f"MVA1_in_{cat}"]["xmin"] + 0.01
#      MVA1_max     = MVA_cuts['spline'][f"MVA1_in_{cat}"]["xmax"] - 2.01
#      MVA2_sig_min = MVA_cuts['spline'][f"MVA2_sig_in_{cat}"]["xmin"] + 0.2  # 0.92
#      MVA2_sig_max = MVA_cuts['spline'][f"MVA2_sig_in_{cat}"]["xmax"] - 0.1  # 0.998
#      MVA2_bkg_min = MVA_cuts['spline'][f"MVA2_bkg_in_{cat}"]["xmin"] + 1e-4 # 0.05
#      MVA2_bkg_max = MVA_cuts['spline'][f"MVA2_bkg_in_{cat}"]["xmax"] - 1    # 0.0025
#
#    # coarse scan in wide range
#    MVA1_vals     = np.linspace( MVA1_min,     MVA1_max,     50)
#    MVA2_sig_vals = np.linspace( MVA2_sig_min, MVA2_sig_max, 20) 
#    MVA2_bkg_vals = np.linspace( MVA2_bkg_min, MVA2_bkg_max, 50)

    # fine scan in more specific region
    if cat == 'bc':
      (MVA1_min,     MVA1_max)     = (8.8, 9.0)
      (MVA2_sig_min, MVA2_sig_max) = (2.2, 2.3) #2.2 is out of lower bound, basically not in use
      (MVA2_bkg_min, MVA2_bkg_max) = (5.6, 6.2)
    if cat == 'bu':
      (MVA1_min,     MVA1_max)     = (7.6, 7.9)
      (MVA2_sig_min, MVA2_sig_max) = (2.29, 2.39) #2.2 is out of lower bound, basically not in use
      (MVA2_bkg_min, MVA2_bkg_max) = (4.33, 4.43)
    MVA1_vals     = np.linspace( MVA1_min,     MVA1_max,     50)
    MVA2_sig_vals = np.linspace( MVA2_sig_min, MVA2_sig_max, 2)
    MVA2_bkg_vals = np.linspace( MVA2_bkg_min, MVA2_bkg_max, 60)


#    MVA2_sig_vals = [0.9] # for validating bkg scan only
    print (MVA1_vals)
    print (MVA2_sig_vals)
    print (MVA2_bkg_vals)

    for cut1 in MVA1_vals:
      for cut2_sig in MVA2_sig_vals:  #do not loop sig if validating bkg scan only
        for cut2_bkg in MVA2_bkg_vals:
            cut_str = f'log_EVT_MVA1 > {cut1} and log_EVT_MVA2_sig > {cut2_sig} and log_EVT_MVA2_bkg > {cut2_bkg}'
            n_sig   = len(df_sig.query(cut_str))   / N_gen_sig   * N_sig2TauNu
            if n_sig < Nsig_min: continue 
            n_other = len(df_other.query(cut_str)) / N_gen_other * N_other2TauNu
            for flav in ['bb', 'cc']:
                eff1[flav] = interpolate.splev(cut1, spline['MVA1'][flav])
                eff2[flav]  = spline['MVA2'][flav].ev(cut2_sig, cut2_bkg)
#                eff2[flav] = interpolate.splev(cut2_bkg, spline['MVA2'][flav])  #for validating bkg scan only

                # if negative because of spline fit behavior
                if eff1['bb'] < 0 or eff2['bb'] < 0: continue
                if flav == 'cc' and eff2[flav] < 0: eff2[flav] = 0.0 
                n_bkg[flav] = N_tight[flav] * eff1[flav] * eff2[flav]
            if eff1['bb'] < 0 or eff2['bb'] < 0:
                print ('Found a region with negative interpolation. Skip it.')
                continue
            purity = n_sig / (n_sig + n_bkg['bb'] + n_bkg['cc'])
            if purity > best['purity']:
                best = {'purity': purity,  'MVA1'   : cut1,     'MVA2_sig': cut2_sig,    'MVA2_bkg': cut2_bkg,
                        'n_sig' : n_sig,   'n_other': n_other,  'bkg_bb'  : n_bkg['bb'], 'bkg_cc'  : n_bkg['cc']}
                print ('\nFound new optimal at:')
                print (f'MVA1: {cut1}, MVA2_sig: {cut2_sig}, MVA2_bkg: {cut2_bkg}')
                print (f'{cat}: {n_sig :.2f},  {other}: {n_other :.2f}')
                print (f"bb: {n_bkg['bb'] :.2f},  cc: {n_bkg['cc'] :.2f}")
                print (f"eff1: {eff1['bb'] :.2},  eff2: {eff2['bb'] :.2}")
                print (f"eff1: {eff1['cc'] :.2},  eff2: {eff2['cc'] :.2}")
                print (f"Purity: {purity}")

    time_stop = time.time()
    print (f'Time to find final selection: {time_stop - time_start}')
    with open(f'{loc.JSON}/optimal_yields_{cat}_with_{NZ}Z_{Nsig_min:.4}sig.json', 'w') as fp:
        json.dump(best, fp)


def main():
    parser = argparse.ArgumentParser(description='Estimate optimal cuts and associated yields')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--cat", choices=['bu','bc'],required=False,default='bc')
    args = parser.parse_args()

    run(args.NZ,args.cat)

if __name__ == '__main__':
    main()


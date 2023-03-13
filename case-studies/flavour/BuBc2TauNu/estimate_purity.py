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
from userConfig import loc, mode_names, train_vars, train_vars_vtx, train_vars_2, Ediff_cut, Nsig_min, MVA_cuts, bkg_scaling
import plotting
import utils as ut
from decay_mode_xs import modes as bkg_modes
from decay_mode_xs import prod

VERBOSE = False

def run(nz, Sig, mva2):

    #BDT variables to optimise, and the hemisphere energy difference which we cut on > 10 GeV
    vars = ["EVT_MVA1Bis","EVT_MVA2_bu","EVT_MVA2_bc", "EVT_MVA2_bkg", "EVT_ThrustDiff_E"]
    cut_list = MVA_cuts
    print (cut_list['sig_cut_for_bkg_scan'][Sig])

    #scanning range should always be within spline range
    scan_limit1 = 1. - np.exp(-cut_list['spline'][f'MVA1_in_{Sig}']['xmax']+0.2) 
    scan_limit2 = 1. - np.exp(-cut_list['spline'][f'MVA2_sig_in_{Sig}']['xmax']+0.2)
    MVA1_vals = np.linspace(0.98,scan_limit1,30)
    MVA2_vals = np.linspace(0.98,scan_limit2,30)
    if mva2 == 'sig' and Sig == 'bc':
      MVA2_vals = np.linspace(0.96,scan_limit2,30)
    if mva2 == 'bkg':
      scan_limit2 = np.exp(-cut_list['spline'][f'MVA2_bkg_in_{Sig}']['xmax']+0.2)
      MVA2_vals = np.linspace(scan_limit2,0.02,30)

    print (MVA1_vals)
    print (MVA2_vals)
  
    EVT_MVA2 = 'EVT_MVA2_bc'
    other = 'bu'
    name_sig = 'Bc2TauNu'
    name_other = 'Bu2TauNu'
    if Sig == 'bu':
      EVT_MVA2 = 'EVT_MVA2_bu'
      other = 'bc'
      name_sig = 'Bu2TauNu'
      name_other = 'Bc2TauNu'

    path = loc.ANALYSIS

    modes = OrderedDict()
    file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
    #Signal and B+ modes
    modes["Bc2TauNu"] = [f"{file_prefix}_Bc2TauNuTAUHADNU"]
    modes["Bu2TauNu"] = [f"{file_prefix}_Bu2TauNuTAUHADNU"]
    #Background decays
    for b in bkg_modes:
        for d in bkg_modes[b]:
            #First entry is the file name, second is hadron prod frac, third is the decay mode B
            modes[f"{b}_{d}"] = [f"{file_prefix}_{b}2{d}", prod[b], bkg_modes[b][d]]
    tree_gen = {}
    tree = {}
    events_gen = {}
    events = {}
    df_gen = {}
    df = {}
    N_gen = {}

    #Hemisphere energy difference cut and baseline BDT cuts
    cut = f"EVT_ThrustDiff_E > {Ediff_cut} and EVT_MVA1Bis > {cut_list['base']['MVA1']} and {EVT_MVA2} > {cut_list['base']['MVA2']}"

    for m in modes:
        print (modes[m][0])
        N_gen[m] = uproot.open(f"{path}/{modes[m][0]}.root")["eventsProcessed"].value
        print(f"Number generated for {m}: {N_gen[m]}")

        tree[m] = uproot.open(f"{path}/{modes[m][0]}.root")["events"]
        df[m] = tree[m].arrays(library="pd", how="zip", filter_name=vars)

        df[m] = df[m].query(cut)
        print (f"{m} : {len(df[m])}")

    #Estimated yields in FCC-ee before any selection

    #Number of Z's expected
    N_Z = float(nz) * 1e12
    #PDG BF(Z -> bb)
    BF_Zbb = 0.1512
    #Factor 2 from having 2 b quarks from Z
    N_bb = N_Z * BF_Zbb * 2

    #Number of events for each bakcground type
    N_bkg_tot = {}

    for b in bkg_modes:
        for d in bkg_modes[b]:
            #Yield for a particular mode is N_bb * B hadron prod frac * B decay BF
            N_bkg_tot[f"{b}_{d}"] = N_bb * modes[f"{b}_{d}"][1] * modes[f"{b}_{d}"][2]
            print(f"N total for {b}2{d} mode = ", end ="")
            print(N_bkg_tot[f"{b}_{d}"])

    #Olcyr calculation of BF(Bc -> tau nu)
    BF_Bc2TauNu = 1.94e-2
    #PDG values
    BF_Bu2TauNu = 1.09e-4
    BF_Tau23Pi = 0.0931

    #Pythia Bc production fraction
    Bu_prod_frac = prod["Bu"]
    Bc_prod_frac = 0.0004

    N_Bc2TauNu = N_bb * Bc_prod_frac * BF_Bc2TauNu * BF_Tau23Pi
    print("N(Bc -> tau nu): %.0f" % N_Bc2TauNu)
    N_Bu2TauNu = N_bb * Bu_prod_frac * BF_Bu2TauNu * BF_Tau23Pi
    print("N(Bu -> tau nu): %.0f" % N_Bu2TauNu)

    N_sig2TauNu = N_Bc2TauNu
    N_other2TauNu = N_Bu2TauNu
    if Sig == 'bu':
      N_sig2TauNu = N_Bu2TauNu
      N_other2TauNu = N_Bc2TauNu

    eff = {}

    N_sig = {}
    N_other = {}
    N_bkg_summed = {}
    N_tot = {}
    P = {}

    P_best = 0
    MVA1_best = 0
    MVA2_pre = 0
    MVA2_best = 0
    N_sig_best = 0
    N_other_best = 0
    N_bkg_best = 0
    eff_best = {}

    #MVA splines which parametrise the MVA efficiencies in excluisve background above the loose cuts
    with open(f'{loc.PKL}/MVA1_{Sig}_scan_{mva2}_spline.pkl', 'rb') as f:
        spline_MVA1 = pickle.load(f)
    with open(f'{loc.PKL}/MVA2_{Sig}_scan_{mva2}_spline.pkl', 'rb') as f:
        spline_MVA2 = pickle.load(f)

    df_cut = {}
    print (modes)
    for cut1 in MVA1_vals:
        for m in modes:
          #Apply actual cut to signal, but only spline base range to background
          #background is adjusted by the spline factors for each MVA later
          cut_val = 0.
          if(m=="Bc2TauNu" or m=="Bu2TauNu"):
              cut_val = cut1
          else:
              cut_val = 1. - np.exp(-cut_list['spline'][f'MVA1_in_{Sig}']['xmin'])
          df[m] = df[m].query(f"EVT_MVA1Bis > {cut_val}")

        # optional second cut, a pre-cut on EVT_MVA2_bc when scanning EVT_MVA2_bkg 
        for cut2 in cut_list['sig_cut_for_bkg_scan'][Sig]:
            # scan of second stage MVA
            for cut3 in MVA2_vals:
              for m in modes:
                  cut_val = 0.
                  if mva2 == 'sig':
                    if(m=="Bc2TauNu" or m=="Bu2TauNu"):
                      cut_val = cut3
                    else:
                      cut_val = 1. - np.exp(-cut_list['spline'][f'MVA2_{mva2}_in_{Sig}']['xmin'])
                    n_pass = float(len(df[m].query(f"{EVT_MVA2} > {cut_val} and {EVT_MVA2} > {cut2}")))
                  else:
                    if(m=="Bc2TauNu" or m=="Bu2TauNu"):
                      cut_val = cut3
                    else:    
                      cut_val = np.exp(-cut_list['spline'][f'MVA2_{mva2}_in_{Sig}']['xmin']) 
                    n_pass = float(len(df[m].query(f"EVT_MVA2_bkg < {cut_val} and {EVT_MVA2} > {cut2}"))) 
                  eff[m] = n_pass / N_gen[m]

              N_sig[f"{cut1}_{cut2}_{cut3}"] = N_sig2TauNu * eff[name_sig]
              N_other[f"{cut1}_{cut2}_{cut3}"] = N_other2TauNu * eff[name_other]
              N_bkg = {}
              N_bkg_summed[f"{cut1}_{cut2}_{cut3}"] = 0. 
              #Do not consider other signal as background
              #Number for each background decay
              for b in bkg_modes:
                  for d in bkg_modes[b]:
                      #Spline efficiencies given by ratio of full spline integral and the integral above cut value
                      MVA1_min = cut_list['spline'][f'MVA1_in_{Sig}']['xmin']
                      MVA1_max = cut_list['spline'][f'MVA1_in_{Sig}']['xmax']
                      MVA1_cut_val = -np.log(1. - cut1)
                      MVA_1_full_int = interpolate.splint(MVA1_min, MVA1_max, spline_MVA1)
                      MVA_1_cut_int = interpolate.splint(MVA1_cut_val, MVA1_max, spline_MVA1)

                      #make sure do not count the region already excluded by cut2
                      MVA2_min = max(-np.log(1.-cut2), cut_list['spline'][f'MVA2_{mva2}_in_{Sig}']['xmin'])
                      MVA2_max =                       cut_list['spline'][f'MVA2_{mva2}_in_{Sig}']['xmax']
                      if mva2 == 'sig': MVA2_cut_val = -np.log(1. - cut3)
                      else:             MVA2_cut_val = -np.log(cut3)
                      MVA_2_full_int = interpolate.splint(MVA2_min, MVA2_max, spline_MVA2)
                      MVA_2_cut_int = interpolate.splint(MVA2_cut_val, MVA2_max, spline_MVA2)

                      eff_MVA1 = MVA_1_cut_int / MVA_1_full_int
                      eff_MVA2 = MVA_2_cut_int / MVA_2_full_int

                      #0.90 efficiency multipled by the spline efficiencies for each MVA, to give total eff
                      eff[f"{b}_{d}"] = eff[f"{b}_{d}"] * eff_MVA1 * eff_MVA2

                      N_bkg[f"{b}_{d}"] = bkg_scaling[f"cat_{Sig}"] * N_bkg_tot[f"{b}_{d}"] * eff[f"{b}_{d}"]
                      #Cumulative background level
                      N_bkg_summed[f"{cut1}_{cut2}_{cut3}"] += N_bkg[f"{b}_{d}"]
              N_tot[f"{cut1}_{cut2}_{cut3}"] = N_sig[f"{cut1}_{cut2}_{cut3}"] + N_bkg_summed[f"{cut1}_{cut2}_{cut3}"]
              #Treat Bu and Bc as signal in the purity
              P[f"{cut1}_{cut2}_{cut3}"] = N_sig[f"{cut1}_{cut2}_{cut3}"] / N_tot[f"{cut1}_{cut2}_{cut3}"]
              #Require > 4k signal for 5e12 Z's, scale according to lumi for other N_Z
              if(P[f"{cut1}_{cut2}_{cut3}"] > P_best and N_sig[f"{cut1}_{cut2}_{cut3}"] > float(nz)*(Nsig_min/5.)):
                  N_sig_best = N_sig[f"{cut1}_{cut2}_{cut3}"]
                  N_other_best = N_other[f"{cut1}_{cut2}_{cut3}"]
                  N_bkg_best = N_bkg_summed[f"{cut1}_{cut2}_{cut3}"]
                  N_bkg_mode_best = {}
                  for b in bkg_modes:
                      for d in bkg_modes[b]:
                          N_bkg_mode_best[f"{b}_{d}"] = N_bkg[f"{b}_{d}"]
                  for m in modes:
                      eff_best[m] = eff[m]
                  P_best = P[f"{cut1}_{cut2}_{cut3}"]
                  MVA1_best = cut1
                  MVA2_pre  = cut2
                  MVA2_best = cut3
                  print(f"Best purity: {P_best}")
                  print(f"Best N_{name_sig}: {N_sig_best}")
                  print(f"Best N_{name_other}: {N_other_best}")
                  if VERBOSE:
                    for b in bkg_modes:
                      for d in bkg_modes[b]:
                          print(f"Best N_{b}2{d}: ", end ="")
                          print(N_bkg_mode_best[f"{b}_{d}"])
                          if mva2 == 'sig': print(f"Raw N_{b}2{d} = %d" %len(df[f'{b}_{d}'].query(f"{EVT_MVA2} > {cut_val}")))
                          else:             print(f"Raw N_{b}2{d} = %d" %len(df[f'{b}_{d}'].query(f"EVT_MVA2_bkg < {cut_val}")))
                    for m in modes:
                      print(f"Best eff_{m}: {eff_best[m]}")
                  print(f"Best N_bkg: {N_bkg_best}")                  
                  print(f"Best MVA1 cut: {MVA1_best}")
                  print(f"Best MVA2 precut: {MVA2_pre}")
                  print(f"Best MVA2 cut: {MVA2_best}")
                  print("=====")

    #Persist the best result yields for each mode, to use in template fit
    res = {}
    res["N_"+name_sig] = N_sig_best
    res["eff_"+name_sig] = eff_best[name_sig]
    res["N_"+name_other] = N_other_best
    res["eff_"+name_other] = eff_best[name_other]
    for b in bkg_modes:
        for d in bkg_modes[b]:
            #Total MC generated
            res[f"N_{b}2{d}_gen"] = int(N_gen[f"{b}_{d}"])
            #Total expected for mode in FCC-ee
            res[f"N_{b}2{d}_tot"] = N_bkg_tot[f"{b}_{d}"]
            #Number expected after all cuts
            res[f"N_{b}2{d}"] = N_bkg_mode_best[f"{b}_{d}"]
            #MC efficiency of cuts
            res[f"eff_{b}2{d}"] = eff_best[f"{b}_{d}"]
    #Best cuts
    res["MVA1"] = MVA1_best
    res["MVA2_precut"] = MVA2_pre
    res["MVA2"] = MVA2_best

    #Write the optmisation results to JSON
    with open(f'{loc.JSON}/optimal_yields_{Sig}_scan_{mva2}_{nz}.json', 'w') as fp:
        json.dump(res, fp)

def main():
    parser = argparse.ArgumentParser(description='Estimate optimal cuts and associated yields')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--Sig", choices=['bu','bc'],required=False,default='bc')
    parser.add_argument("--mva2", choices=['sig','bkg'],required=False,default='bkg')
    args = parser.parse_args()

    run(args.NZ,args.Sig,args.mva2)

if __name__ == '__main__':
    main()

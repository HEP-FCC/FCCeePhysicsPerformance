import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
from decay_mode_xs import modes as bkg_modes
from decay_mode_xs import prod, b_hadrons, c_hadrons

#Local code
from userConfig import loc, train_vars, train_vars_vtx, Ediff_cut, NBin_MVA_fit, MVA_cuts, Eff, Nsig_min
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)


#BDT variables to optimise, and the hemisphere energy difference which we cut on > 10 GeV
var_list = ["EVT_MVA1Bis", "EVT_MVA2_bc", "EVT_MVA2_bu", "EVT_MVA2_bkg", "EVT_ThrustEmax_E", "EVT_ThrustEmin_E"]
path = loc.ANALYSIS

truth_bc = 'CUT_CandTruth ==1'
truth_bu = 'CUT_CandTruth2==1'

Cut_sel = f'CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
cut = f"EVT_MVA1Bis > {MVA_cuts['tight']['MVA1']} and 1 - EVT_MVA2_bkg > {MVA_cuts['tight']['MVA2_bkg']} and {Cut_sel}"

file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
print ('open tree')
tree_bc = uproot.open(f"{path}/{file_prefix}_Bc2TauNuTAUHADNU.root")["events"]
print ('load array')
df_bc = tree_bc.arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
print ('apply cut')
df_bc = df_bc.query(f'{truth_bc} and {cut}')
df_bc = df_bc[var_list]
df_bc["log_EVT_MVA1"]     = -np.log(1. - df_bc["EVT_MVA1Bis"])
df_bc["log_EVT_MVA2_bkg"] = -np.log(df_bc["EVT_MVA2_bkg"])
df_bc["log_EVT_MVA2_bc"]  = -np.log(1. - df_bc["EVT_MVA2_bc"])
df_bc["log_EVT_MVA2_bu"]  = -np.log(1. - df_bc["EVT_MVA2_bu"])
print (f"process Bc : {len(df_bc)}")

tree_bu = uproot.open(f"{path}/{file_prefix}_Bu2TauNuTAUHADNU.root")["events"]
df_bu = tree_bu.arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
df_bu = df_bu.query(f'{truth_bu} and {cut}')
df_bu = df_bu[var_list]
df_bu["log_EVT_MVA1"]     = -np.log(1. - df_bu["EVT_MVA1Bis"])
df_bu["log_EVT_MVA2_bkg"] = -np.log(df_bu["EVT_MVA2_bkg"])
df_bu["log_EVT_MVA2_bu"]  = -np.log(1. - df_bu["EVT_MVA2_bu"])
df_bu["log_EVT_MVA2_bc"]  = -np.log(1. - df_bu["EVT_MVA2_bc"])
print (f"process Bu : {len(df_bu)}")



df_Bc_in_bc = df_bc.query(f"EVT_MVA2_bc > {MVA_cuts['tight']['MVA2_sig']}")
df_Bc_in_bc.to_pickle(f"{loc.PKL}/final/Bc_evt_in_bc_cat_for_final_sel.pkl")
print (f"Bc in bc: {len(df_Bc_in_bc)}")

df_Bu_in_bc = df_bu.query(f"EVT_MVA2_bc > {MVA_cuts['tight']['MVA2_sig']}")
df_Bu_in_bc.to_pickle(f"{loc.PKL}/final/Bu_evt_in_bc_cat_for_final_sel.pkl")
print (f"Bu in bc: {len(df_Bu_in_bc)}")

df_Bc_in_bu = df_bc.query(f"EVT_MVA2_bu > {MVA_cuts['tight']['MVA2_sig']}")
df_Bc_in_bu.to_pickle(f"{loc.PKL}/final/Bc_evt_in_bu_cat_for_final_sel.pkl")
print (f"Bc in bu: {len(df_Bc_in_bu)}")

df_Bu_in_bu = df_bu.query(f"EVT_MVA2_bu > {MVA_cuts['tight']['MVA2_sig']}")
df_Bu_in_bu.to_pickle(f"{loc.PKL}/final/Bu_evt_in_bu_cat_for_final_sel.pkl")
print (f"Bu in bu: {len(df_Bu_in_bu)}")


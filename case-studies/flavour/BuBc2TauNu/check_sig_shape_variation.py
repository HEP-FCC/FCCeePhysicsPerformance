import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
import zfit
from decay_mode_xs import modes as bkg_modes

#Local code
from userConfig import loc, Ediff_cut, MVA_cuts, FCC_label
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def create_hist(df, bins, branches, weights=None,
                with_edges=False, with_err=False,
                ranges=None,
                normalise=False, weight_branch=None,
               **kwargs):
    """ Create a histogram.

    Parameters
    ----------
    df: pd.DataFrame
        dataframe from which the histogram is created
    bins: int or array-like
        number of bins, or bin edges
    weights: 1D array-like
        weights
    with_edges: bool
        Do we return the bin edges as well?
    branches: list(str)
        branches in the dataframe that the histograms
        need to be created for
    ranges: list([float, float])
        Low and high values for each branch
    weight_branch: str
        name of the branch of supplementary weights
    **kwargs:
        passed to ``numpy.histogramdd``

    Returns
    -------
    hist: array-like
        Counts in data for the ``branches``
    edges: array-like, *optional*
        If ``with_edges``. Bin edges.
    """

    sample = np.array(df[branches])
    hist, edges = np.histogramdd(
        sample, bins=bins,
        range=ranges,
        weights=weights,
        **kwargs)
    if with_err:
        err = np.sqrt(hist)
    if normalise:
        norm = hist.sum()
        hist = hist / norm
        if with_err:
            err = err / norm

    if with_edges:
        if with_err:
            return hist, err, edges
        else:
            return hist, edges
    else:
        if with_err:
            return hist, err
        else:
            return hist

def run(nz, free_mubb, bkg_sf, bkg_syst, ntoys):

    bkg_sf   = int(bkg_sf)
    bkg_syst = int(bkg_syst)

    #Fetch signal and bkg yields from optimisation
    yields = {}
    with open(f'{loc.JSON}/optimal_yields_bc_with_{nz}Z_1e+04sig.json') as fbc:
      yields['bc'] = json.load(fbc)
      yields['bc']['Bc2TauNu'] = yields['bc']['n_sig']
      yields['bc']['Bu2TauNu'] = yields['bc']['n_other']
      yields['bc']['bb'] = yields['bc']['bkg_bb']
      yields['bc']['cc'] = yields['bc']['bkg_cc']
    with open(f'{loc.JSON}/optimal_yields_bu_with_{nz}Z_1e+04sig.json') as fbu:
      yields['bu'] = json.load(fbu)
      yields['bu']['Bc2TauNu'] = yields['bu']['n_other']
      yields['bu']['Bu2TauNu'] = yields['bu']['n_sig']
      yields['bu']['bb'] = yields['bu']['bkg_bb']
      yields['bu']['cc'] = yields['bu']['bkg_cc']

    settings = OrderedDict()
    settings['Bc2TauNu'] = {'color': '#508273', 'label': '$B_c^+ \\to \\tau^+ \\nu_\\tau$' } 
    settings['Bu2TauNu'] = {'color': '#b2182b', 'label': '$B^+ \\to \\tau^+ \\nu_\\tau$' }
    settings['bb']       = {'color': '#2166ac', 'label': '$Z^0 \\to b\\bar{b}$ Bkg' }
    settings['cc']       = {'color': '#fdae61', 'label': '$Z^0 \\to c\\bar{c}$ Bkg' }  
   

    # this loading step is very fast, no need to trim further 
    file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
    tree_bb = uproot.open(f"{loc.ANALYSIS}/p8_ee_Zbb_ecm91.root")["events"]
    df_bb = tree_bb.arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
    tree_cc = uproot.open(f"{loc.ANALYSIS}/p8_ee_Zcc_ecm91.root")["events"]
    df_cc = tree_cc.arrays(library="pd", how="zip", filter_name=["EVT_*", "CUT_*"])
    df = {}
    for cat in ['bc', 'bu']:
      cat_sel = f'log_EVT_MVA1 > {yields[cat]["MVA1"]} and log_EVT_MVA2_{cat} > {yields[cat]["MVA2_sig"]} and log_EVT_MVA2_bkg > {yields[cat]["MVA2_bkg"]}'
      df[cat] = {}
      df[cat]['Bc2TauNu'] = pd.read_pickle(f"{loc.PKL}/final/Bc_evt_in_{cat}_cat_for_final_sel.pkl")
      df[cat]['Bc2TauNu'] = df[cat]['Bc2TauNu'].query(cat_sel)
      df[cat]['Bu2TauNu'] = pd.read_pickle(f"{loc.PKL}/final/Bu_evt_in_{cat}_cat_for_final_sel.pkl")
      df[cat]['Bu2TauNu'] = df[cat]['Bu2TauNu'].query(cat_sel)

#      Cut_truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'
#      Cut_sel = f'{Cut_truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
#      cut = f"EVT_MVA1Bis > {MVA_cuts['base']['MVA1']} and EVT_MVA2_{cat} > {MVA_cuts['base']['MVA2_sig']} and 1 - EVT_MVA2_bkg > {MVA_cuts['base']['MVA2_bkg']} and {Cut_sel}"
#      df[cat]['bb'] = df_bb.query(cut)
#      df[cat]['cc'] = df_cc.query(cut)

      print (f"In {cat} cat:")
      for m in df[cat]:
        print (f"use {len(df[cat][m])} {m} MC to model {yields[cat][m] :.5} data")


    # Fit variables
    # could take multiple variables, just to compare performance in each.
    # should not fit many variables in the same fit (effectively fitting a few times more data)
    fit_vars = {
                "EVT_ThrustEmax_E": {"name": "Maximum hemisphere E", "low": 22., "high": 52., "unit": "GeV"},
                }

    #Number of bins in each variable
    #30 bins for the 5e12 Z's scenario, scale down for lower lumi
    bins = int(40*np.sqrt(float(nz)/5.))

    #Histogram templates for each mode and variable
    #Templates are normalised
    h = {}
    h['bc'] = {}
    h['bu'] = {}
    bin_edges = {}
    bin_centres = {}
    bin_width = {}

    for cat in df:
      for v in fit_vars:
        for m in df[cat]:
            # get shape and normalization for each process
#            cat_sel = f'log_EVT_MVA1 > {yields[cat]["MVA1"]} -0.7 and log_EVT_MVA2_{cat} > {yields[cat]["MVA2_sig"]} and log_EVT_MVA2_bkg > {yields[cat]["MVA2_bkg"]}-0.7'
            cat_sel = f'log_EVT_MVA1 > {yields[cat]["MVA1"]} and log_EVT_MVA2_{cat} > {yields[cat]["MVA2_sig"]} and log_EVT_MVA2_bkg > {yields[cat]["MVA2_bkg"]}'
            df[cat][m] = df[cat][m].query(cat_sel)
            if m == "Bu2TauNu": df[cat][m] = pd.concat([df[cat][m]]*3, ignore_index=True)
            df[cat][m] = df[cat][m].sample(frac=1).reset_index(drop=True)
            df_temp = np.array_split(df[cat][m], 3)
            print (len(df_temp[0]))
            h[cat][f"{m}_{v}_set0"], bin_edges[v] = create_hist(df_temp[0], bins, [v],
                                                           ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)
            h[cat][f"{m}_{v}_set1"], bin_edges[v] = create_hist(df_temp[1], bins, [v],
                                                           ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)
            h[cat][f"{m}_{v}_set2"], bin_edges[v] = create_hist(df_temp[2], bins, [v],
                                                           ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)


            bin_centres[v] = (bin_edges[v][0][1:] + bin_edges[v][0][:-1]) / 2
            bin_width[v] = bin_edges[v][0][1] - bin_edges[v][0][0]
            h[cat][f"{m}_{v}_set0"] = h[cat][f"{m}_{v}_set0"] + 1e-10
            h[cat][f"{m}_{v}_set1"] = h[cat][f"{m}_{v}_set1"] + 1e-10
            h[cat][f"{m}_{v}_set2"] = h[cat][f"{m}_{v}_set2"] + 1e-10
            h[cat][f"{m}_{v}_ratio1"] = h[cat][f"{m}_{v}_set1"] / h[cat][f"{m}_{v}_set0"]
            h[cat][f"{m}_{v}_ratio2"] = h[cat][f"{m}_{v}_set2"] / h[cat][f"{m}_{v}_set0"]

            
            h[cat][f"{m}_{v}_error0"] = 1.0 / np.sqrt( yields[cat][m] * h[cat][f"{m}_{v}_set0"] ) 
      
        # plot shape comparisons
        fig, (ax1, ax2) = plt.subplots(2, figsize=(10,10))
        shape = {}
        for m in df[cat]:
            if m == 'Bu2TauNu' and cat == 'bc': continue
            if m == 'Bc2TauNu' and cat == 'bu': continue
            shape[m] = ax1.stairs(h[cat][f"{m}_{v}_set0"], bin_edges[v][0], color=settings[m]["color"], linewidth=2, label=settings[m]["label"]+" part1")
            shape[m] = ax1.stairs(h[cat][f"{m}_{v}_set1"], bin_edges[v][0], color=settings[m]["color"], linewidth=2, label=settings[m]["label"]+" part2",linestyle='dashed')
            shape[m] = ax1.stairs(h[cat][f"{m}_{v}_set2"], bin_edges[v][0], color=settings[m]["color"], linewidth=2, label=settings[m]["label"]+" part3",linestyle='dotted')

            shape[m] = ax2.stairs(1+h[cat][f"{m}_{v}_error0"], bin_edges[v][0], color='gray',  fill=True, alpha=0.5, linewidth=0, label='Poisson error')
            shape[m] = ax2.stairs(1-h[cat][f"{m}_{v}_error0"], bin_edges[v][0], color='white', fill=True, linewidth=0, label='Poisson error')
            shape[m] = ax2.stairs(h[cat][f"{m}_{v}_ratio1"], bin_edges[v][0], color=settings[m]["color"], linewidth=2, label=settings[m]["label"],linestyle='dashed')
            shape[m] = ax2.stairs(h[cat][f"{m}_{v}_ratio2"], bin_edges[v][0], color=settings[m]["color"], linewidth=2, label=settings[m]["label"],linestyle='dotted')

        ax1.legend(fontsize=20,loc = "upper left")
        ax1.tick_params(axis='both', which='major', labelsize=25)
        ax2.tick_params(axis='both', which='major', labelsize=25)
        ax1.set_title( FCC_label, loc='right', fontsize=20)
        ax1.set_xlim(fit_vars[v]["low"], fit_vars[v]["high"])
        ax2.set_xlim(fit_vars[v]["low"], fit_vars[v]["high"])
        ax2.set_xlabel(f"{fit_vars[v]['name']} ({fit_vars[v]['unit']})",fontsize=30)
        ax1.set_ylabel("Normalised dist. (a.u.)",fontsize=25)
        ax2.set_ylabel("Ratio to part1", fontsize=25)
        ymin,ymax = ax1.get_ylim()
        ax1.set_ylim(0, 1.2*ymax)
        ax2.set_ylim(0.75,1.25)
        ax2.grid(alpha=0.4,which="both")
        plt.tight_layout()
        fig.savefig(f"{loc.PLOTS}/{cat}_{v}_shape_variation.png")

#    sys.exit()






def main():
    parser = argparse.ArgumentParser(description='Run toy fits to measure the signal yield')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--free_mubb", choices=[True, False],required=False,help="whether to set mubb as free or constrained param",default=True)
    parser.add_argument("--bkgSF", required=False,help="Scale factor for background, for optimistic or pessimistic estimates",default=1) 
    # The bkgSF is an uniform factor applied to all toys. It is an exaggeration of bkg norm, not an uncertainty
    parser.add_argument("--bkgSyst", required=False,help="lognormal sigma on systematics of background normalization",default=1) 
    # The bkgSyst is a random factor applied to each toy. The value indicates where the positive bound of 68% coverage lies in the distribution of bkg scaling. 
    # It should be a value greater than 1. (1 means it is a Delta function at 1 and no spread, i.e. no syst uncertainty.) 
    parser.add_argument("--Ntoys", required=False,help="Number of toys to run (if 1, runs a single toy and plots it)",default=1)
    args = parser.parse_args()

    run(args.NZ, args.free_mubb, args.bkgSF, args.bkgSyst, args.Ntoys)

if __name__ == '__main__':
    main()

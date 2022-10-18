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

def run(nz, bkg_sf, bkg_syst, ntoys):

    #Fetch signal and bkg yields from optimisation
    yields = {}
    with open(f'{loc.JSON}/optimal_yields_bc_with_{nz}Z_5000sig.json') as fbc:
      yields['bc'] = json.load(fbc)
      yields['bc']['Bc2TauNu'] = yields['bc']['n_sig']
      yields['bc']['Bu2TauNu'] = yields['bc']['n_other']
      yields['bc']['bb'] = yields['bc']['bkg_bb']
      yields['bc']['cc'] = yields['bc']['bkg_cc']
    with open(f'{loc.JSON}/optimal_yields_bu_with_{nz}Z_5000sig.json') as fbu:
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

      Cut_truth = 'CUT_CandTruth==0 and CUT_CandTruth2==0'
      Cut_sel = f'{Cut_truth} and CUT_CandRho==1 and CUT_CandVtxThrustEmin==1 and EVT_CandMass < 1.8 and EVT_ThrustDiff_E > {Ediff_cut}'
      cut = f"EVT_MVA1Bis > {MVA_cuts['base']['MVA1']} and EVT_MVA2_{cat} > {MVA_cuts['base']['MVA2']} and {Cut_sel}"
      df[cat]['bb'] = df_bb.query(cut)
      df[cat]['cc'] = df_cc.query(cut)

      print (f"In {cat} cat:")
      for m in df[cat]:
        print (f"use {len(df[cat][m])} {m} MC to model {yields[cat][m] :.5} data")

 #   sys.exit()

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
            h[cat][f"{m}_{v}"], bin_edges[v] = create_hist(df[cat][m], bins, [v], 
                                                           ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)
            h[cat][f"{m}_{v}"] = h[cat][f"{m}_{v}"] * yields[cat][m]
            bin_centres[v] = (bin_edges[v][0][1:] + bin_edges[v][0][:-1]) / 2
            bin_width[v] = bin_edges[v][0][1] - bin_edges[v][0][0]
      
        # plot shape comparisons
        fig, ax = plt.subplots(figsize=(10,8))
        shape = {}
        for m in df[cat]:
            shape[m] = plt.stairs(h[cat][f"{m}_{v}"] / yields[cat][m], bin_edges[v][0], color=settings[m]["color"], linewidth=2, label=settings[m]["label"])
        plt.legend(fontsize=20,loc = "upper left")
        ax.tick_params(axis='both', which='major', labelsize=25)
        ax.set_title( FCC_label, loc='right', fontsize=20)
        plt.xlim(fit_vars[v]["low"], fit_vars[v]["high"])
        plt.xlabel(f"{fit_vars[v]['name']} ({fit_vars[v]['unit']})",fontsize=30)
        plt.ylabel("Normalised distribution (a.u.)",fontsize=30)
        ymin,ymax = plt.ylim()
        plt.ylim(0.,1.5*ymax)
        plt.tight_layout()
        fig.savefig(f"{loc.PLOTS}/{cat}_{v}_template_compare.pdf")

    # generate toys and perform fit
    data = {}
    scale_bb = {}
    scale_cc = {}
    for cat in df:
      data[cat] = {}   
      scale_bb[cat] = {}
      scale_cc[cat] = {}

    # apply scale factor of exaggeration for bkg, to study the performance with more backgrounds
    for cat in df:
      for v in fit_vars:
        for m in ['bb', 'cc']:
          h[cat][f'{m}_{v}'] = bkg_sf * h[cat][f'{m}_{v}']

    n_toys = int(ntoys)
    for i in range(0,n_toys):
      np.random.seed(i+2)
      for cat in df:
        # random scale for bkg systematics, logonormal(0, 0) gives 1.0
        lognorm_sigma = np.log(bkg_syst)
        scale_bb[cat][f'{i}'] = np.random.lognormal(0, lognorm_sigma)
        scale_cc[cat][f'{i}'] = np.random.lognormal(0, lognorm_sigma)
        for v in fit_vars:
            tot_hist = h[cat][f"Bc2TauNu_{v}"] + h[cat][f"Bu2TauNu_{v}"] + scale_bb[cat][f'{i}'] * h[cat][f"bb_{v}"] + scale_cc[cat][f'{i}'] * h[cat][f"cc_{v}"]
            data[cat][f"{i}_{v}"] = np.random.poisson(tot_hist)
            print (f"{i} toy")
            print (f"bb scale: {scale_bb[cat][f'{i}']}")
            print (f"cc scale: {scale_cc[cat][f'{i}']}")

    #Make the total template for the fit in each dimension
    def get_templates(mu_Bc, mu_Bu, mu_bb_bc, mu_cc_bc, mu_bb_bu, mu_cc_bu, var):
        return ( (mu_Bc    * h['bc'][f"Bc2TauNu_{var}"] + 
                  mu_Bu    * h['bc'][f"Bu2TauNu_{var}"] + 
                  mu_bb_bc * h['bc'][f"bb_{var}"]       +
                  mu_cc_bc * h['bc'][f"cc_{var}"] ) ,

                 (mu_Bc    * h['bu'][f"Bc2TauNu_{var}"] +
                  mu_Bu    * h['bu'][f"Bu2TauNu_{var}"] +
                  mu_bb_bu * h['bu'][f"bb_{var}"]       +
                  mu_cc_bu * h['bu'][f"cc_{var}"] )
               )

    def binned_nll(template_bc, template_bu, sample_hist_bc, sample_hist_bu):
      return np.sum(template_bc - sample_hist_bc + sample_hist_bc * np.log((sample_hist_bc + 1e-14) / (template_bc + 1e-14))) + \
             np.sum(template_bu - sample_hist_bu + sample_hist_bu * np.log((sample_hist_bu + 1e-14) / (template_bu + 1e-14)))
             # 1e-14 added in case there are empty bins

    #Loop over toys
    results_dict = {}
    results_dict["mu_Bc"] = {}
    results_dict["mu_Bu"] = {}
    results_dict["bb_bc"] = {}
    results_dict["cc_bc"] = {}
    results_dict["bb_bu"] = {}
    results_dict["cc_bu"] = {}

    for i in range(0,n_toys):
        #Loss function including nll for each of the fit dimensions
        def loss(x):
            # by default, `x` is an `OrderedSet` of zfit parameters.
            x = np.array(x)

            #print("Value of the parameters", x) # can be commented out, just to see how x evolves during the minimisation

            # The first parameter is the strength multiplier of the Bc signal template
            mu_Bc = x[0]
            mu_Bu = x[1]
            mu_bb_bc = x[2]
            mu_cc_bc = x[3]
            mu_bb_bu = x[4]
            mu_cc_bu = x[5]

            template_bc = {}
            template_bu = {}
            nll = {}
            tot_nll = 0

            for v in fit_vars:
                template_bc[v], template_bu[v] = get_templates(mu_Bc, mu_Bu, mu_bb_bc, mu_cc_bc, mu_bb_bu, mu_cc_bu, v)  
                nll[v] = binned_nll(template_bc[v], template_bu[v], data['bc'][f"{i}_{v}"], data['bu'][f"{i}_{v}"])
                tot_nll += nll[v]

            # set pulls on bkg uncertainty as a log likelihood of a lognormal distribution
            # 1/2 * ( log(x) - mean ) ** 2 / sigma ** 2, x = mu * yield, mean = 0, sigma = bkg_syst * yield
            # yield cancels, leaving the form below
            tot_nll += 0.5 * ( np.log(mu_bb_bc)**2 + np.log(mu_cc_bc)**2 + np.log(mu_bb_bu)**2 + np.log(mu_cc_bu)**2 ) / (bkg_syst ** 2)

            return tot_nll

        loss.errordef = 0.5 # 0.5 for a log-likelihood, 1 for chi2

        #Starting values for the yields
        initial_params = []
        initial_params.append( zfit.Parameter(f'mu_Bc_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'mu_Bu_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'bb_bc_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'cc_bc_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'bb_bu_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'cc_bu_{i}', 1.0, 0.01, 100.) )

        if (bkg_sf == 0): # for testing signal only stats uncert
          initial_params[2].floating = False
          initial_params[3].floating = False
          initial_params[4].floating = False
          initial_params[5].floating = False
        minimiser = zfit.minimize.Minuit(verbosity=5)
        #Since we're using numpy histograms, we need to disable the graph mode of zfit
        zfit.run.set_autograd_mode(False)
        zfit.run.set_graph_mode(False)

        result = minimiser.minimize(loss, initial_params)
        param_hesse = result.hesse() # Computation of the errors
        corr = result.correlation(method="minuit_hesse")
        print(corr)

        print(result.info['original'])
        params = result.params
        print(params)

        for p in params:
            results_dict["%s" % (p.name[0:5])][f"{i}"] = [params[p]['value'], param_hesse[p]]


        #Plot fit for the first toy
        if(n_toys==1):
          for cat in df:
            for v in fit_vars:
                ################ plot bc cat ##################
                fig, ax = plt.subplots(figsize=(10,8))

                #Plot the toy dataset
                Data = plt.errorbar(x=bin_centres[v], y =data[cat][f"{i}_{v}"], yerr=np.sqrt(data[cat][f"{i}_{v}"]), 
                                    fmt="o", markersize=4, color="k", label="Generated data")
                h_cc     =        results_dict[f"cc_{cat}"][f"{i}"][0] * h[cat][f"cc_{v}"]
                h_bkg    = h_cc + results_dict[f"bb_{cat}"][f"{i}"][0] * h[cat][f"bb_{v}"]
                if cat == 'bc':
                  h_nonsig = h_bkg    + results_dict["mu_Bu"][f"{i}"][0] * h[cat][f"Bu2TauNu_{v}"]
                  h_tot    = h_nonsig + results_dict["mu_Bc"][f"{i}"][0] * h[cat][f"Bc2TauNu_{v}"]
                if cat == 'bu':
                  h_nonsig = h_bkg    + results_dict["mu_Bc"][f"{i}"][0] * h[cat][f"Bc2TauNu_{v}"]
                  h_tot    = h_nonsig + results_dict["mu_Bu"][f"{i}"][0] * h[cat][f"Bu2TauNu_{v}"]

                if cat == 'bc':
                    Total = plt.stairs(h_tot, bin_edges[v][0], color="k", linewidth=2, label="Total fit")
                    Bc = plt.stairs(h_tot,    bin_edges[v][0], color=settings["Bc2TauNu"]["color"], fill=True,  alpha=0.8, label=settings["Bc2TauNu"]["label"])
                    Bu = plt.stairs(h_nonsig, bin_edges[v][0], color=settings["Bu2TauNu"]["color"], fill=True,  alpha=0.8, label=settings["Bu2TauNu"]["label"])
                    BB = plt.stairs(h_bkg,    bin_edges[v][0], color=settings["bb"]["color"],       fill=True,  alpha=0.8, label=settings["bb"]["label"])
                    CC = plt.stairs(h_cc,     bin_edges[v][0], color=settings["cc"]["color"],       fill=True,  alpha=0.8, label=settings["cc"]["label"])
                if cat == 'bu':
                    Total = plt.stairs(h_tot, bin_edges[v][0], color="k", linewidth=2, label="Total fit")
                    Bu = plt.stairs(h_tot,    bin_edges[v][0], color=settings["Bu2TauNu"]["color"], fill=True,  alpha=0.8, label=settings["Bu2TauNu"]["label"])
                    Bc = plt.stairs(h_nonsig, bin_edges[v][0], color=settings["Bc2TauNu"]["color"], fill=True,  alpha=0.8, label=settings["Bc2TauNu"]["label"])
                    BB = plt.stairs(h_bkg,    bin_edges[v][0], color=settings["bb"]["color"],       fill=True,  alpha=0.8, label=settings["bb"]["label"])
                    CC = plt.stairs(h_cc,     bin_edges[v][0], color=settings["cc"]["color"],       fill=True,  alpha=0.8, label=settings["cc"]["label"])
           
                plt.legend(fontsize=20, loc = "upper left")
                ax.tick_params(axis='both', which='major', labelsize=25)
                ax.set_title( FCC_label, loc='right', fontsize=20)
                plt.xlim(fit_vars[v]["low"], fit_vars[v]["high"])
                plt.xlabel(f"{fit_vars[v]['name']} ({fit_vars[v]['unit']})",fontsize=30)
                plt.ylabel("Candidates / (%.1f %s)" % (bin_width[v], fit_vars[v]["unit"]),fontsize=30)
                #plt.yscale('log')
                ymin,ymax = plt.ylim()
                plt.ylim(0.,1.2*ymax)
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/{cat}_{v}_template_fit_{bkg_sf}bkg_{bkg_syst}Syst_{nz}Z.pdf")


    #Store toy results to json
    if(n_toys!=1):
        with open(f'{loc.JSON}/toy_simultaneous_template_fit_results_{bkg_sf}bkg_{bkg_syst}Syst_{nz}Z.json', 'w') as fp:
            json.dump(results_dict, fp)

def main():
    parser = argparse.ArgumentParser(description='Run toy fits to measure the signal yield')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--bkgSF", required=False,help="Scale factor for background, for optimistic or pessimistic estimates",default=1) 
    # The bkgSF is an uniform factor applied to all toys. It is an exaggeration of bkg norm, not an uncertainty
    parser.add_argument("--bkgSyst", required=False,help="lognormal sigma on systematics of background normalization",default=5) 
    # The bkgSyst is a random factor applied to each toy. The value indicates where the positive bound of 68% coverage lies in the distribution of bkg scaling. 
    # It should be a value greater than 1. (1 means it is a Delta function at 1 and no spread, i.e. no syst uncertainty.) 
    parser.add_argument("--Ntoys", required=False,help="Number of toys to run (if 1, runs a single toy and plots it)",default=2000)
    args = parser.parse_args()

    run(args.NZ, args.bkgSF, args.bkgSyst, args.Ntoys)

if __name__ == '__main__':
    main()

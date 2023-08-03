import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
import tensorflow as tf
import zfit
from decay_mode_xs import modes as bkg_modes

#Local code
from userConfig import loc
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

def run(nz, bkg_sf, ntoys,cat, fit2D):

    #Fetch signal and bkg yields from optimisation
    with open(f'{loc.JSON}/optimal_yields_bc_scan_bkg_{nz}.json') as fbc:
      yields_bc = json.load(fbc)
    with open(f'{loc.JSON}/optimal_yields_bu_scan_bkg_{nz}.json') as fbu:
      yields_bu = json.load(fbu)

    modes = OrderedDict()

    file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
    #Signal and B+ modes
    modes["Bc2TauNu"] = {"name": f"{file_prefix}_Bc2TauNuTAUHADNU", "color": "#b2182b", "label": "$B_c^+ \\to \\tau^+ \\nu_\\tau$", "N_bc": yields_bc["N_Bc2TauNu"], "N_bu": yields_bu["N_Bc2TauNu"]}
    modes["Bu2TauNu"] = {"name": f"{file_prefix}_Bu2TauNuTAUHADNU", "color": "#fdae61", "label": "$B^+ \\to \\tau^+ \\nu_\\tau$", "N_bc": yields_bc["N_Bu2TauNu"], "N_bu": yields_bu["N_Bu2TauNu"], "N_err": yields_bc["N_Bu2TauNu"]*0.05} #Belle II B+ -> tau nu precision
    modes["Zbb"] = {"name": "p8_ee_Zbb_ecm91"}
    #Background decays
    for b in bkg_modes:
        for d in bkg_modes[b]:
            modes[f"{b}_{d}"] = {"name": f"{file_prefix}_{b}2{d}", "N_bc": yields_bc[f"N_{b}2{d}"], "N_bu": yields_bu[f"N_{b}2{d}"]}

    #Total bkg yield
    N_bkg_tot_bc = 0.
    N_bkg_tot_bu = 0.
    for b in bkg_modes:
        for d in bkg_modes[b]:
            N_bkg_tot_bc += modes[f"{b}_{d}"]["N_bc"]
            N_bkg_tot_bu += modes[f"{b}_{d}"]["N_bu"]
    print("Total bkg expected in Bc cat: %s" % N_bkg_tot_bc)
    print("Total bkg expected in Bu cat: %s" % N_bkg_tot_bu)

    #Load dataframes for each mode to make templates
    df = {}
    for m in modes:
        df[m] = pd.read_pickle(f"{loc.PKL}/{m}_selected_for_fit.pkl")

    #Fit variables
    fit_vars = {
                "EVT_ThrustEmax_E": {"name": "Maximum hemisphere E", "low": 22., "high": 52., "unit": "GeV/$c^2$"},
                "EVT_ThrustEmin_E": {"name": "Minimum hemisphere E", "low": 2.,  "high": 42., "unit": "GeV/$c^2$"},
#                "EVT_Nominal_B_E":  {"name": "Nominal B Energy",     "low": 25., "high": 65., "unit": "GeV/$c^2$"},
                }

    #Number of bins in each variable
    #30 bins for the 5e12 Z's scenario, scale down for lower lumi
    bins = int(2*np.sqrt(float(nz)/5.))

    #Histogram templates for each mode and variable
    #Templates are normalised
    h = {}
    h['bc'] = {}
    h['bu'] = {}

    for m in modes:
        ranges = []
        for v in fit_vars:
            ranges.append([fit_vars[v]["low"], fit_vars[v]["high"]])
        h['bc'][f"{m}"] = create_hist(df[m].query("EVT_MVA1Bis > 0.95 and EVT_MVA2_bc > 0.95"),
                                                        bins, fit_vars, ranges=ranges, normalise=True)
        h['bu'][f"{m}"] = create_hist(df[m].query("EVT_MVA1Bis > 0.95 and EVT_MVA2_bu > 0.95"),
                                                        bins, fit_vars, ranges=ranges, normalise=True)
        if fit2D == "two1D":
          for i, v in enumerate(fit_vars):
            h['bc'][f"{m}_{v}"] = h['bc'][f"{m}"].sum(axis=i)
            h['bu'][f"{m}_{v}"] = h['bu'][f"{m}"].sum(axis=i)

    #Combine the background histograms according to relative yields from the optimisation
    h['bc'][f"bkg"] = 0
    h['bu'][f"bkg"] = 0
    for b in bkg_modes:
        for d in bkg_modes[b]:
            h['bc'][f"bkg"] += modes[f"{b}_{d}"]["N_bc"] * h['bc'][f"{b}_{d}"]
            h['bu'][f"bkg"] += modes[f"{b}_{d}"]["N_bu"] * h['bu'][f"{b}_{d}"]
    #Normalise to the total number of bkg events
    h['bc'][f"bkg"] = h['bc'][f"bkg"] / N_bkg_tot_bc
    h['bu'][f"bkg"] = h['bu'][f"bkg"] / N_bkg_tot_bu

    if fit2D == "two1D":
      for v in fit_vars:
        h['bc'][f"bkg_{v}"] = 0
        h['bu'][f"bkg_{v}"] = 0
        for b in bkg_modes:
            for d in bkg_modes[b]:
                h['bc'][f"bkg_{v}"] += modes[f"{b}_{d}"]["N_bc"] * h['bc'][f"{b}_{d}_{v}"]
                h['bu'][f"bkg_{v}"] += modes[f"{b}_{d}"]["N_bu"] * h['bu'][f"{b}_{d}_{v}"]
        #Normalise to the total number of bkg events
        h['bc'][f"bkg_{v}"] = h['bc'][f"bkg_{v}"] / N_bkg_tot_bc
        h['bu'][f"bkg_{v}"] = h['bu'][f"bkg_{v}"] / N_bkg_tot_bu


    print("Scale bkg by factor %d for alternative cases" % bkg_sf)
    N_bkg_tot_bc = N_bkg_tot_bc * bkg_sf
    N_bkg_tot_bu = N_bkg_tot_bu * bkg_sf

    #Create a total histgoram of signal + background and then Poisson vary each bin to make a toy dataset
    tot_hist_bc = {}
    tot_hist_bu = {}
    data_bc = {}
    data_bu = {}
    data_err_bc = {}
    data_err_bu = {}
    #Make toy datasets
    n_toys = int(ntoys)
    for i in range(0,n_toys):
        np.random.seed(i+1)
        tot_hist_bc['2D'] = modes["Bc2TauNu"]["N_bc"]*h['bc'][f"Bc2TauNu"] + modes["Bu2TauNu"]["N_bc"]*h['bc'][f"Bu2TauNu"] + N_bkg_tot_bc*h['bc'][f"bkg"]
        tot_hist_bu['2D'] = modes["Bc2TauNu"]["N_bu"]*h['bu'][f"Bc2TauNu"] + modes["Bu2TauNu"]["N_bu"]*h['bu'][f"Bu2TauNu"] + N_bkg_tot_bu*h['bu'][f"bkg"]
        data_bc[f"{i}"] = np.random.poisson(tot_hist_bc['2D'])
        data_bu[f"{i}"] = np.random.poisson(tot_hist_bu['2D'])
        data_err_bc[f"{i}"] = np.sqrt(data_bc[f"{i}"])
        data_err_bu[f"{i}"] = np.sqrt(data_bu[f"{i}"])

        if fit2D == "two1D":
          for n, v in enumerate(fit_vars):
            data_bc[f"{i}_{v}"] = data_bc[f"{i}"].sum(axis=n)
            data_bu[f"{i}_{v}"] = data_bu[f"{i}"].sum(axis=n)
            data_err_bc[f"{i}_{v}"] = np.sqrt(data_bc[f"{i}_{v}"])
            data_err_bu[f"{i}_{v}"] = np.sqrt(data_bu[f"{i}_{v}"])
 

    #Make the total template for the fit in each dimension
    def get_templates(mu_Bc, mu_Bu, mu_bkg_bc, mu_bkg_bu, var):
        if var != '': var = '_'+var
        return ( (mu_Bc * modes["Bc2TauNu"]["N_bc"] * h['bc'][f"Bc2TauNu{var}"] + 
                  mu_Bu * modes["Bu2TauNu"]["N_bc"] * h['bc'][f"Bu2TauNu{var}"] + 
                  mu_bkg_bc * N_bkg_tot_bc * h['bc'][f"bkg{var}"] ) ,
                 (mu_Bc * modes["Bc2TauNu"]["N_bu"] * h['bu'][f"Bc2TauNu{var}"] +
                  mu_Bu * modes["Bu2TauNu"]["N_bu"] * h['bu'][f"Bu2TauNu{var}"] +
                  mu_bkg_bu * N_bkg_tot_bu * h['bu'][f"bkg{var}"] )
               )

    def binned_nll(template_bc, template_bu, sample_hist_bc, sample_hist_bu):
      return np.sum(template_bc - sample_hist_bc + sample_hist_bc * np.log((sample_hist_bc + 1e-14) / (template_bc + 1e-14))) + \
             np.sum(template_bu - sample_hist_bu + sample_hist_bu * np.log((sample_hist_bu + 1e-14) / (template_bu + 1e-14)))
      # 1e-14 added in case there are empty bins

    #Loop over toys
    results_dict = {}
    results_dict["mu_Bc"] = {}
    results_dict["mu_Bu"] = {}
    results_dict["mubbc"] = {}
    results_dict["mubbu"] = {}

    for i in range(0,n_toys):

        #Loss function including nll for each of the fit dimensions
        def loss(x):
            # by default, `x` is an `OrderedSet` of
            # zfit parameters.
            x = np.array(x)

            #print("Value of the parameters", x) # can be commented out, just to see how x evolves during
            # the minimisation

            # The first parameter is the strength multiplier of the Bc signal template
#            yield_Bc = x[0]
            mu_Bc = x[0]
            # The second parameter is the strength multiplier of the Bu template
#            yield_Bu = x[1]
            mu_Bu = x[1]
            # The third parameter is the strength multiplier of the bkg template
#            yield_bkg = x[2]
            mu_bkg_bc = x[2]
            mu_bkg_bu = x[3]

            template_bc = {}
            template_bu = {}
            nll = {}
            tot_nll = 0

            if fit2D == "one2D":
              template_bc, template_bu = get_templates(mu_Bc, mu_Bu, mu_bkg_bc, mu_bkg_bu, '')  
              tot_nll = binned_nll(template_bc, template_bu, data_bc[f"{i}"], data_bu[f"{i}"])
            else:
              for v in fit_vars:
                template_bc[v], template_bu[v] = get_templates(mu_Bc, mu_Bu, mu_bkg_bc, mu_bkg_bu, v)
                nll[v] = binned_nll(template_bc[v], template_bu[v], data_bc[f"{i}_{v}"], data_bu[f"{i}_{v}"])
                tot_nll += nll[v]


            #Gaussian constraint on B+ -> tau nu yield
            #tot_nll += (yield_Bu - modes["Bu2TauNu"]["N"])**2/2./modes["Bu2TauNu"]["N_err"]**2

            return tot_nll

        loss.errordef = 0.5 # 0.5 for a log-likelihood, 1 for chi2

        #Starting values for the yields
        initial_params = []
        initial_params.append( zfit.Parameter(f'mu_Bc_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'mu_Bu_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'mubbc_{i}', 1.0, 0.01, 100.) )
        initial_params.append( zfit.Parameter(f'mubbu_{i}', 1.0, 0.01, 100.) )

#        {
#            'value': [1., 1., 1., 1.],
#            'lower' : [0.01, 0.01, 0.01, 0.01], # optional
#            'upper':  [100., 100., 100., 100.], # optional
#            'name': [f'mu_Bc_{i}', f'mu_Bu_{i}', f'mubbc_{i}', f'mubbu_{i}'] # optional
#        }

        if (bkg_sf == 0):
          initial_params[2].floating = False
          initial_params[3].floating = False
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


    #Store toy results to json
    if(n_toys!=1):
        with open(f'{loc.JSON}/toy_2D_simultaneous_template_fit_results_{bkg_sf}bkg_{nz}Z.json', 'w') as fp:
            json.dump(results_dict, fp)

def main():
    parser = argparse.ArgumentParser(description='Run toy fits to measure the signal yield')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--bkgSF", required=False,help="Scale factor for background, for optimistic or pessimistic estimates",default=1)
    parser.add_argument("--cat", choices=["bc","bu","both"],required=False,default="bc")
    parser.add_argument("--Ntoys", required=False,help="Number of toys to run (if 1, runs a single toy and plots it)",default=1)
    parser.add_argument("--fit2D", choices=["two1D","one2D"],required=False,default="one2D")
    args = parser.parse_args()

    run(args.NZ, args.bkgSF, args.Ntoys, args.cat, args.fit2D)

if __name__ == '__main__':
    main()

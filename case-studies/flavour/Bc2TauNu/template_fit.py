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

def run(nz,ntoys):

    #Fetch signal and bkg yields from optimisation
    with open(f'{loc.JSON}/optimal_yields_{nz}.json') as f:
      yields = json.load(f)

    modes = OrderedDict()

    file_prefix = "p8_ee_Zbb_ecm91_EvtGen"
    #Signal and B+ modes
    modes["Bc2TauNu"] = {"name": f"{file_prefix}_Bc2TauNuTAUHADNU", "color": "#b2182b", "label": "$B_c^+ \\to \\tau^+ \\nu_\\tau$", "N": yields["N_Bc2TauNu"]}
    modes["Bu2TauNu"] = {"name": f"{file_prefix}_Bu2TauNuTAUHADNU", "color": "#fdae61", "label": "$B^+ \\to \\tau^+ \\nu_\\tau$", "N": yields["N_Bu2TauNu"], "N_err": yields["N_Bu2TauNu"]*0.05} #Belle II B+ -> tau nu precision
    modes["Zbb"] = {"name": "p8_ee_Zbb_ecm91"}
    #Background decays
    for b in bkg_modes:
        for d in bkg_modes[b]:
            modes[f"{b}_{d}"] = {"name": f"{file_prefix}_{b}2{d}", "N": yields[f"N_{b}2{d}"]}

    #Total bkg yield
    N_bkg_tot = 0.
    for b in bkg_modes:
        for d in bkg_modes[b]:
            N_bkg_tot += modes[f"{b}_{d}"]["N"]
    print("Total bkg expected: %s" % N_bkg_tot)

    #Load dataframes for each mode to make templates
    df = {}
    for m in modes:
        df[m] = pd.read_pickle(f"{loc.PKL}/{m}_selected_for_fit.pkl")

    #Fit variables
    fit_vars = {
                "EVT_ThrustEmax_E": {"name": "Maximum hemisphere E", "low": 22., "high": 52., "unit": "GeV/$c^2$"},
                }

    #Number of bins in each variable
    #30 bins for the 5e12 Z's scenario, scale down for lower lumi
    bins = int(30*np.sqrt(float(nz)/5.))

    #Histogram templates for each mode and variable
    #Templates are normalised
    h = {}
    bin_edges = {}
    bin_centres = {}
    bin_width = {}

    for m in modes:
        for v in fit_vars:
            h[f"{m}_{v}"], bin_edges[v] = create_hist(df[m], bins, [v], ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)
            bin_centres[v] = (bin_edges[v][0][1:] + bin_edges[v][0][:-1]) / 2
            bin_width[v] = bin_edges[v][0][1] - bin_edges[v][0][0]

    #Combine the background histograms according to relative yields from the optimisation
    for v in fit_vars:
        h[f"bkg_{v}"] = 0
        for b in bkg_modes:
            for d in bkg_modes[b]:
                h[f"bkg_{v}"] += modes[f"{b}_{d}"]["N"] * h[f"{b}_{d}_{v}"]
        #Normalise to the total number of bkg events
        h[f"bkg_{v}"] = h[f"bkg_{v}"] / N_bkg_tot

    #Create a total histgoram of signal + background and then Poisson vary each bin to make a toy dataset
    tot_hist = {}
    data = {}
    data_err = {}
    #Make toy datasets
    n_toys = int(ntoys)
    for i in range(0,n_toys):
        np.random.seed(i+1)
        for v in fit_vars:
            tot_hist[v] = modes["Bc2TauNu"]["N"]*h[f"Bc2TauNu_{v}"] + modes["Bu2TauNu"]["N"]*h[f"Bu2TauNu_{v}"] + N_bkg_tot*h[f"bkg_{v}"] #   h[f"Zbb_{v}"]
            data[f"{i}_{v}"] = np.random.poisson(tot_hist[v])
            data_err[f"{i}_{v}"] = np.sqrt(data[f"{i}_{v}"])

    #Make the total template for the fit in each dimension
    def get_template(yield_Bc, yield_Bu, yield_bkg, var):
        return yield_Bc * h[f"Bc2TauNu_{var}"] + yield_Bu * h[f"Bu2TauNu_{var}"] + yield_bkg * h[f"bkg_{var}"]

    def binned_nll(template, sample_hist):
      return np.sum(template - sample_hist + sample_hist * np.log((sample_hist + 1e-14) / (template+1e-14)))
      # 1e-14 added in case there are empty bins

    #Loop over toys
    results_dict = {}
    results_dict["N_Bc"] = {}
    results_dict["N_Bu"] = {}
    results_dict["N_bg"] = {}

    for i in range(0,n_toys):

        #Loss function including nll for each of the fit dimensions
        def loss(x):
            # by default, `x` is an `OrderedSet` of
            # zfit parameters.
            x = np.array(x)

            #print("Value of the parameters", x) # can be commented out, just to see how x evolves during
            # the minimisation

            # The first parameter is the yield of the Bc signal template
            yield_Bc = x[0]
            # The second parameter is the yield of the Bu template
            yield_Bu = x[1]
            # The third parameter is the yield of the bkg template
            yield_bkg = x[2]

            template = {}
            nll = {}
            tot_nll = 0

            for v in fit_vars:
                template[v] = get_template(yield_Bc, yield_Bu, yield_bkg, v)
                nll[v] = binned_nll(template[v], data[f"{i}_{v}"])
                tot_nll += nll[v]

            #Gaussian constraint on B+ -> tau nu yield
            tot_nll += (yield_Bu - modes["Bu2TauNu"]["N"])**2/2./modes["Bu2TauNu"]["N_err"]**2

            return tot_nll

        loss.errordef = 0.5 # 0.5 for a log-likelihood, 1 for chi2

        #Starting values for the yields
        initial_params = {
            'value': [modes["Bc2TauNu"]["N"], modes["Bu2TauNu"]["N"], N_bkg_tot],
            'lower' : [-1000., -1000., -1000.], # optional
            'upper': [100000., 100000., 100000.], # optional
            'name': [f'N_Bc_{i}', f'N_Bu_{i}', f'N_bg_{i}'] # optional
        }

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
            results_dict["%s" % (p.name[0:4])][f"{i}"] = [params[p]['value'], param_hesse[p]]

        #Plot first toy
        if(n_toys==1):
            for v in fit_vars:
                fig, ax = plt.subplots(figsize=(10,8))

                #Plot the toy dataset
                Data = plt.errorbar(x=bin_centres[v], y =data[f"{i}_{v}"], yerr=data_err[f"{i}_{v}"], fmt="o", markersize=4, color="k")#,label="Generated data")

                #Total
                h_tot = results_dict["N_Bc"][f"{i}"][0] * h[f"Bc2TauNu_{v}"] + results_dict["N_Bu"][f"{i}"][0] * h[f"Bu2TauNu_{v}"] + results_dict["N_bg"][f"{i}"][0] * h[f"bkg_{v}"]
                #h_tot = results_dict["N_Bc"][f"{i}"][0] * h[f"Bc2TauNu_{v}"] + results_dict["N_Bu"][f"{i}"][0] * h[f"Bu2TauNu_{v}"] + results_dict["N_bg"][f"{i}"][0] * h[f"Zbb_{v}"]

                Bc = plt.stairs(h_tot, bin_edges[v][0], color=modes["Bc2TauNu"]["color"], fill=True, alpha=0.8)#, label=modes["Bc2TauNu"]["label"])
                Total = plt.stairs(h_tot, bin_edges[v][0], color="k", linewidth=2)#, label="Total fit")

                #Bu
                h_Bu = results_dict["N_Bu"][f"{i}"][0] * h[f"Bu2TauNu_{v}"] + results_dict["N_bg"][f"{i}"][0] * h[f"bkg_{v}"]
                #h_Bu = results_dict["N_Bu"][f"{i}"][0] * h[f"Bu2TauNu_{v}"] + results_dict["N_bg"][f"{i}"][0] * h[f"Zbb_{v}"]
                Bu = plt.stairs(h_Bu, bin_edges[v][0], color=modes["Bu2TauNu"]["color"], fill=True)#, label=modes["Bu2TauNu"]["label"])

                #Bkg
                h_bkg = results_dict["N_bg"][f"{i}"][0] * h[f"bkg_{v}"]
                #h_bkg = results_dict["N_bg"][f"{i}"][0] * h[f"Zbb_{v}"]
                Bkg = plt.stairs(h_bkg, bin_edges[v][0], color="#2166ac", fill=True)#, label="Background") #label="$Z \\to B^0/B^+/B_s^0/\\Lambda_b^0 X$")

                plt.legend((Data, Total, Bc, Bu, Bkg),
                           ("Generated data", "Total fit", modes["Bc2TauNu"]["label"], modes["Bu2TauNu"]["label"], "Background"),
                           fontsize=22,
                           loc = "upper left"
                          )

                ax.tick_params(axis='both', which='major', labelsize=25)
                plt.xlim(fit_vars[v]["low"], fit_vars[v]["high"])
                if(fit_vars[v]["unit"]!=""):
                    unit_str = "[%s]" % fit_vars[v]["unit"]
                    unit_space = " "
                else:
                    unit_str = ""
                    unit_space = ""
                plt.xlabel(fit_vars[v]["name"]+" %s" % unit_str,fontsize=30)
                plt.ylabel("Candidates / (%.1f%s%s)" % (bin_width[v], unit_space, fit_vars[v]["unit"]),fontsize=30)
                #plt.yscale('log')
                ymin,ymax = plt.ylim()
                plt.ylim(0.,1.2*ymax)
                #plt.legend(fontsize=22,loc="upper left")
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/{v}_template_fit_{nz}.pdf")

                #Plot the signal, B+ and background histograms normalised for comparison
                fig, ax = plt.subplots(figsize=(10,8))

                h_Bc = h[f"Bc2TauNu_{v}"]
                Bc = plt.stairs(h_Bc, bin_edges[v][0], color=modes["Bc2TauNu"]["color"], linewidth=2)

                h_Bu = h[f"Bu2TauNu_{v}"]
                Bu = plt.stairs(h_Bu, bin_edges[v][0], color=modes["Bu2TauNu"]["color"], linewidth=2)

                h_bkg = h[f"bkg_{v}"]
                Bkg = plt.stairs(h_bkg, bin_edges[v][0], color="#2166ac", linewidth=2)

                #h_inc = h[f"Zbb_{v}"]
                #Inc = plt.stairs(h_inc, bin_edges[v][0], color="#92c5de", linewidth=2)

                plt.legend((Bc, Bu, Bkg), #, Inc),
                           (modes["Bc2TauNu"]["label"], modes["Bu2TauNu"]["label"], "Exclusive background"), #, "Incluisve $Z \\to b\\bar{b}$"),
                           fontsize=22,
                           loc = "upper left"
                          )

                ax.tick_params(axis='both', which='major', labelsize=25)
                plt.xlim(fit_vars[v]["low"], fit_vars[v]["high"])
                if(fit_vars[v]["unit"]!=""):
                    unit_str = "[%s]" % fit_vars[v]["unit"]
                    unit_space = " "
                else:
                    unit_str = ""
                    unit_space = ""
                plt.xlabel(fit_vars[v]["name"]+" %s" % unit_str,fontsize=30)
                plt.ylabel("Density / (%.1f%s%s)" % (bin_width[v], unit_space, fit_vars[v]["unit"]),fontsize=30)
                #plt.yscale('log')
                ymin,ymax = plt.ylim()
                plt.ylim(0.,1.2*ymax)
                #plt.legend(fontsize=22,loc="upper left")
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/{v}_template_compare_{nz}.pdf")

    #Store toy results to json
    if(n_toys!=1):
        with open(f'{loc.JSON}/toy_template_fit_results_{nz}.json', 'w') as fp:
            json.dump(results_dict, fp)

def main():
    parser = argparse.ArgumentParser(description='Run toy fits to measure the signal yield')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--Ntoys", required=True,help="Number of toys to run (if 1, runs a single toy and plots it)",default=1)
    args = parser.parse_args()

    run(args.NZ, args.Ntoys)

if __name__ == '__main__':
    main()

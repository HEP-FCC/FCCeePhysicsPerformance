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

def run(nz,ntoys,cat):

    #Fetch signal and bkg yields from optimisation
    with open(f'{loc.JSON}/optimal_yields_bc_{nz}.json') as fbc:
      yields_bc = json.load(fbc)
    with open(f'{loc.JSON}/optimal_yields_bu_{nz}.json') as fbu:
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
                }

    #Number of bins in each variable
    #30 bins for the 5e12 Z's scenario, scale down for lower lumi
    bins = int(30*np.sqrt(float(nz)/5.))

    #Histogram templates for each mode and variable
    #Templates are normalised
    h = {}
    h['bc'] = {}
    h['bu'] = {}
    bin_edges = {}
    bin_centres = {}
    bin_width = {}

    for m in modes:
        for v in fit_vars:
            h['bc'][f"{m}_{v}"], bin_edges[v] = create_hist(df[m].query("EVT_MVA1Bis > 0.98 and EVT_MVA2_bc > 0.95"),
                                                            bins, [v], ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)
            h['bu'][f"{m}_{v}"], bin_edges[v] = create_hist(df[m].query("EVT_MVA1Bis > 0.98 and EVT_MVA2_bu > 0.95"),
                                                            bins, [v], ranges=[[fit_vars[v]["low"], fit_vars[v]["high"]]], normalise=True, with_edges=True)
            bin_centres[v] = (bin_edges[v][0][1:] + bin_edges[v][0][:-1]) / 2
            bin_width[v] = bin_edges[v][0][1] - bin_edges[v][0][0]

    #Combine the background histograms according to relative yields from the optimisation
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
        for v in fit_vars:
            tot_hist_bc[v] = modes["Bc2TauNu"]["N_bc"]*h['bc'][f"Bc2TauNu_{v}"] + modes["Bu2TauNu"]["N_bc"]*h['bc'][f"Bu2TauNu_{v}"] + N_bkg_tot_bc*h['bc'][f"bkg_{v}"] #   h[f"Zbb_{v}"]
            tot_hist_bu[v] = modes["Bc2TauNu"]["N_bu"]*h['bu'][f"Bc2TauNu_{v}"] + modes["Bu2TauNu"]["N_bu"]*h['bu'][f"Bu2TauNu_{v}"] + N_bkg_tot_bu*h['bu'][f"bkg_{v}"]
            data_bc[f"{i}_{v}"] = np.random.poisson(tot_hist_bc[v])
            data_bu[f"{i}_{v}"] = np.random.poisson(tot_hist_bu[v])
            data_err_bc[f"{i}_{v}"] = np.sqrt(data_bc[f"{i}_{v}"])
            data_err_bu[f"{i}_{v}"] = np.sqrt(data_bu[f"{i}_{v}"])

    #Make the total template for the fit in each dimension
    def get_templates(mu_Bc, mu_Bu, mu_bkg_bc, mu_bkg_bu, var):
        return ( (mu_Bc * modes["Bc2TauNu"]["N_bc"] * h['bc'][f"Bc2TauNu_{var}"] + 
                  mu_Bu * modes["Bu2TauNu"]["N_bc"] * h['bc'][f"Bu2TauNu_{var}"] + 
                  mu_bkg_bc * N_bkg_tot_bc * h['bc'][f"bkg_{var}"] ) ,
                 (mu_Bc * modes["Bc2TauNu"]["N_bu"] * h['bu'][f"Bc2TauNu_{var}"] +
                  mu_Bu * modes["Bu2TauNu"]["N_bu"] * h['bu'][f"Bu2TauNu_{var}"] +
                  mu_bkg_bu * N_bkg_tot_bu * h['bu'][f"bkg_{var}"] )
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

            for v in fit_vars:
                template_bc[v], template_bu[v] = get_templates(mu_Bc, mu_Bu, mu_bkg_bc, mu_bkg_bu, v)  
                nll[v] = binned_nll(template_bc[v], template_bu[v], data_bc[f"{i}_{v}"], data_bu[f"{i}_{v}"])
                tot_nll += nll[v]

            #Gaussian constraint on B+ -> tau nu yield
            #tot_nll += (yield_Bu - modes["Bu2TauNu"]["N"])**2/2./modes["Bu2TauNu"]["N_err"]**2

            return tot_nll

        loss.errordef = 0.5 # 0.5 for a log-likelihood, 1 for chi2

        #Starting values for the yields
        initial_params = {
            'value': [1., 1., 1., 1.],
            'lower' : [0.01, 0.01, 0.01, 0.01], # optional
            'upper':  [100., 100., 100., 100.], # optional
            'name': [f'mu_Bc_{i}', f'mu_Bu_{i}', f'mubbc_{i}', f'mubbu_{i}'] # optional
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
            results_dict["%s" % (p.name[0:5])][f"{i}"] = [params[p]['value'], param_hesse[p]]


        #Plot first toy
        if(n_toys==1):
            for v in fit_vars:
                ################ plot bc cat ##################
                fig, ax = plt.subplots(figsize=(10,8))

                #Plot the toy dataset
                Data = plt.errorbar(x=bin_centres[v], y =data_bc[f"{i}_{v}"], yerr=data_err_bc[f"{i}_{v}"], fmt="o", markersize=4, color="k")#,label="Generated data")

                #Total
                h_tot = results_dict["mu_Bc"][f"{i}"][0] * modes["Bc2TauNu"]["N_bc"] * h['bc'][f"Bc2TauNu_{v}"] + results_dict["mu_Bu"][f"{i}"][0] * modes["Bu2TauNu"]["N_bc"] * h['bc'][f"Bu2TauNu_{v}"] + results_dict["mubbc"][f"{i}"][0] * N_bkg_tot_bc * h['bc'][f"bkg_{v}"]

                Bc = plt.stairs(h_tot, bin_edges[v][0], color=modes["Bc2TauNu"]["color"], fill=True, alpha=0.8)#, label=modes["Bc2TauNu"]["label"])
                Total = plt.stairs(h_tot, bin_edges[v][0], color="k", linewidth=2)#, label="Total fit")

                #Bu
                h_Bu = results_dict["mu_Bu"][f"{i}"][0] * modes["Bu2TauNu"]["N_bc"] * h['bc'][f"Bu2TauNu_{v}"] + results_dict["mubbc"][f"{i}"][0] * N_bkg_tot_bc * h['bc'][f"bkg_{v}"]
                Bu = plt.stairs(h_Bu, bin_edges[v][0], color=modes["Bu2TauNu"]["color"], fill=True)#, label=modes["Bu2TauNu"]["label"])

                #Bkg
                h_bkg = results_dict["mubbc"][f"{i}"][0] * N_bkg_tot_bc * h['bc'][f"bkg_{v}"]
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
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/bc_{v}_template_fit_{nz}.pdf")

                #Plot the signal, B+ and background histograms normalised for comparison
                fig, ax = plt.subplots(figsize=(10,8))

                h_Bc = h['bc'][f"Bc2TauNu_{v}"]
                Bc = plt.stairs(h_Bc, bin_edges[v][0], color=modes["Bc2TauNu"]["color"], linewidth=2)

                h_Bu = h['bc'][f"Bu2TauNu_{v}"]
                Bu = plt.stairs(h_Bu, bin_edges[v][0], color=modes["Bu2TauNu"]["color"], linewidth=2)

                h_bkg = h['bc'][f"bkg_{v}"]
                Bkg = plt.stairs(h_bkg, bin_edges[v][0], color="#2166ac", linewidth=2)

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
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/bc_{v}_template_compare_{nz}.pdf")
                ############# plotted bc cat #####################

                ################ plot bu cat ##################
                fig, ax = plt.subplots(figsize=(10,8))

                #Plot the toy dataset
                Data = plt.errorbar(x=bin_centres[v], y =data_bu[f"{i}_{v}"], yerr=data_err_bu[f"{i}_{v}"], fmt="o", markersize=4, color="k")#,label="Generated data")

                #Total
                h_tot = results_dict["mu_Bc"][f"{i}"][0] * modes["Bc2TauNu"]["N_bu"] * h['bu'][f"Bc2TauNu_{v}"] + results_dict["mu_Bu"][f"{i}"][0] * modes["Bu2TauNu"]["N_bu"] * h['bu'][f"Bu2TauNu_{v}"] + results_dict["mubbu"][f"{i}"][0] * N_bkg_tot_bu * h['bu'][f"bkg_{v}"]

                Bu = plt.stairs(h_tot, bin_edges[v][0], color=modes["Bu2TauNu"]["color"], fill=True, alpha=0.8)#, label=modes["Bc2TauNu"]["label"])
                Total = plt.stairs(h_tot, bin_edges[v][0], color="k", linewidth=2)#, label="Total fit")

                #Bu
                h_Bc = results_dict["mu_Bc"][f"{i}"][0] * modes["Bc2TauNu"]["N_bu"] * h['bu'][f"Bc2TauNu_{v}"] + results_dict["mubbu"][f"{i}"][0] * N_bkg_tot_bu * h['bu'][f"bkg_{v}"]
                Bc = plt.stairs(h_Bc, bin_edges[v][0], color=modes["Bc2TauNu"]["color"], fill=True)#, label=modes["Bu2TauNu"]["label"])

                #Bkg
                h_bkg = results_dict["mubbu"][f"{i}"][0] * N_bkg_tot_bu * h['bu'][f"bkg_{v}"]
                Bkg = plt.stairs(h_bkg, bin_edges[v][0], color="#2166ac", fill=True)#, label="Background") #label="$Z \\to B^0/B^+/B_s^0/\\Lambda_b^0 X$")

                plt.legend((Data, Total, Bu, Bc, Bkg),
                           ("Generated data", "Total fit", modes["Bu2TauNu"]["label"], modes["Bc2TauNu"]["label"], "Background"),
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
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/bu_{v}_template_fit_{nz}.pdf")

                #Plot the signal, B+ and background histograms normalised for comparison
                fig, ax = plt.subplots(figsize=(10,8))

                h_Bu = h['bu'][f"Bu2TauNu_{v}"]
                Bu = plt.stairs(h_Bu, bin_edges[v][0], color=modes["Bu2TauNu"]["color"], linewidth=2)

                h_Bc = h['bu'][f"Bc2TauNu_{v}"]
                Bc = plt.stairs(h_Bc, bin_edges[v][0], color=modes["Bc2TauNu"]["color"], linewidth=2)

                h_bkg = h['bu'][f"bkg_{v}"]
                Bkg = plt.stairs(h_bkg, bin_edges[v][0], color="#2166ac", linewidth=2)

                plt.legend((Bu, Bc, Bkg), #, Inc),
                           (modes["Bu2TauNu"]["label"], modes["Bc2TauNu"]["label"], "Exclusive background"), #, "Incluisve $Z \\to b\\bar{b}$"),
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
                plt.tight_layout()
                fig.savefig(f"{loc.PLOTS}/bu_{v}_template_compare_{nz}.pdf")
                ############# plotted bu cat #####################
                
              

    #Store toy results to json
    if(n_toys!=1):
        with open(f'{loc.JSON}/toy_simultaneous_template_fit_results_{nz}.json', 'w') as fp:
            json.dump(results_dict, fp)

def main():
    parser = argparse.ArgumentParser(description='Run toy fits to measure the signal yield')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    parser.add_argument("--cat", choices=["bc","bu","both"],required=False,default="bc")
    parser.add_argument("--Ntoys", required=False,help="Number of toys to run (if 1, runs a single toy and plots it)",default=1)
    args = parser.parse_args()

    run(args.NZ, args.Ntoys, args.cat)

if __name__ == '__main__':
    main()

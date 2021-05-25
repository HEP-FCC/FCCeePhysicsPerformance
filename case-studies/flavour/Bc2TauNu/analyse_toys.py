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
from userConfig import loc, train_vars, train_vars_vtx

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def run(nz):
    #Load toy results from json
    with open(f'{loc.JSON}/toy_template_fit_results_{nz}.json') as f:
        results_dict = json.load(f)

    #Yields generated
    with open(f'{loc.JSON}/optimal_yields_{nz}.json') as f:
        opt = json.load(f)

    #Get the signal yield results
    vals = []
    errs = []
    pulls = []

    #Generated Bc -> tau nu signal yield
    N_Bc_gen = opt["N_Bc2TauNu"]
    par_name = "N_Bc"

    for x in results_dict[par_name]:
        val = results_dict[par_name][x][0]
        err = results_dict[par_name][x][1]["error"]
        vals.append(val)
        errs.append(err)
        pull = (val - N_Bc_gen)/err
        pulls.append(pull)

    #Fit the N_Bc values distribution, and plot the generated value as a vertical line to compare
    min = N_Bc_gen - 4*np.mean(errs)
    max = N_Bc_gen + 4*np.mean(errs)
    obs = zfit.Space('x', limits=(min, max))
    mu = zfit.Parameter("mu", N_Bc_gen, 0., 10000.)
    sigma = zfit.Parameter("sigma", 110.,  0., 1000.)

    gauss = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sigma)

    data = zfit.Data.from_numpy(obs=obs, array=np.array(vals))

    nll = zfit.loss.UnbinnedNLL(model=gauss, data=data)

    minimizer = zfit.minimize.Minuit()

    result = minimizer.minimize(nll)
    param_hesse = result.hesse() # Computation of the errors

    print(result.info['original'])
    params = result.params
    print(params)

    toy_dict = {}
    for p in params:
        toy_dict["%s" % p.name] = [params[p]['value'], param_hesse[p]]
    print(toy_dict)

    bins = 50
    counts, bin_edges = np.histogram(vals, bins, range=(min, max))
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    err = np.sqrt(counts)

    fig,ax = plt.subplots(figsize=(8,8))
    plt.errorbar(bin_centres, counts, yerr=err, fmt='o', color='xkcd:black')

    x_plot = np.linspace(min, max, num=1000)
    y_plot = zfit.run(gauss.pdf(x_plot, norm_range=obs))

    plt.plot(x_plot, y_plot*len(vals)/bins*obs.area(), color='xkcd:blue')
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlabel("$N(B_c^+ \\to \\tau^+ \\nu_\\tau)$",fontsize=30)
    plt.ylabel("Number of toys",fontsize=30)
    plt.axvline(N_Bc_gen,color="gray",alpha=0.4,linestyle="--")
    ymin, ymax = plt.ylim()
    plt.xlim(min,max)
    plt.ylim(0,1.1*ymax)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/toy_results_{nz}.pdf")

    #Persist the toy results to json
    with open(f'{loc.JSON}/toy_results_{nz}.json', 'w') as fp:
        json.dump(toy_dict, fp)

def main():
    parser = argparse.ArgumentParser(description='Analyse toys for template fit')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    args = parser.parse_args()

    run(args.NZ)

if __name__ == '__main__':
    main()

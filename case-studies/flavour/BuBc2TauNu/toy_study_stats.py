import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
#import tensorflow as tf
import zfit
from userConfig import loc, train_vars, train_vars_vtx, FCC_label
from double_sided_gaussian import DSGauss

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def run(bkg_sf, bkg_syst, nz):
    #Load toy results from json
    with open(f'{loc.JSON}/sig_shape_syst_toy_simultaneous_template_fit_results_{bkg_sf}bkg_{bkg_syst}Syst_{nz}Z.json') as f:     
        results_dict = json.load(f)


    sig_labels = {'Bc': '$B_c^+ \\to \\tau^+ \\nu_\\tau$',
                  'Bu': '$B^+ \\to \\tau^+ \\nu_\\tau$'  } 

    for sig in ['Bc', 'Bu']:
      vals = []
      errs = []
      par_name = 'mu_' + sig
      for x in results_dict[par_name]:
          val = results_dict[par_name][x][0]
          err = results_dict[par_name][x][1]["error"]
          vals.append(val)
          errs.append(err)
          pull = (val - 1.0)/err
  
      #Fit the N_Bc values distribution, and plot the generated value as a vertical line to compare
      min = 1.0 - 3.1*np.mean(errs)
      max = 1.0 + 2.9*np.mean(errs)
      obs = zfit.Space('x', limits=(min, max))
      mu_name = 'mu'+sig
      sigma_L_name = 'sigma_L'+sig
      sigma_R_name = 'sigma_R'+sig

      mu = zfit.Parameter(mu_name, 1.0, 0., 2.)
      sigma_L = zfit.Parameter(sigma_L_name, 0.05,  0., 0.3)
      sigma_R = zfit.Parameter(sigma_R_name, 0.05,  0., 0.3)
  
      gauss = DSGauss(obs=obs, mu=mu, sigma_L=sigma_L, sigma_R=sigma_R)
  
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
      plt.errorbar(bin_centres, counts, yerr=err, fmt='o', markersize=4, color='xkcd:black')
  
      x_plot = np.linspace(min, max, num=1000)
      y_plot = zfit.run(gauss.pdf(x_plot, norm_range=obs))
  
      plt.plot(x_plot, y_plot*len(vals)/bins*obs.area(), color='xkcd:blue')
      ax.tick_params(axis='both', which='major', labelsize=25)
      ax.set_title( FCC_label, loc='right', fontsize=20)
      plt.xlabel(f"$\\mu$({sig_labels[sig]})",fontsize=30)
      plt.ylabel("Number of toys",fontsize=30)
      plt.axvline(1.0,color="gray",alpha=0.4,linestyle="--")
      ymin, ymax = plt.ylim()
      plt.xlim(min,max)
      plt.ylim(0,1.2*ymax)
      leg = [mpl.lines.Line2D([0],[0], label="$\\mu ~$ = %.4f" %params[mu_name]['value']),
             mpl.lines.Line2D([0],[0], label="$\\sigma_L$ = %.4f" %params[sigma_L_name]['value']),
             mpl.lines.Line2D([0],[0], label="$\\sigma_R$ = %.4f" %params[sigma_R_name]['value'])]
      plt.legend(handles=leg, loc="upper left",fontsize=20)
      plt.tight_layout()
      fig.savefig(f"{loc.PLOTS}/sig_shape_syst_toy_results_{sig}_{bkg_sf}bkg_{bkg_syst}Syst_{nz}Z.pdf")

      #Persist the toy results to json
      with open(f'{loc.JSON}/sig_shape_syst_toy_results_{sig}_{bkg_sf}bkg_{bkg_syst}Syst_{nz}Z.json', 'w') as fp:
        json.dump(toy_dict, fp)

def main():
    parser = argparse.ArgumentParser(description='Analyse toys for template fit')
    parser.add_argument("--bkgSF", required=False,help="Scale factor for background, for optimistic or pessimistic estimates",default=1)
    parser.add_argument("--bkgSyst", required=False,help="lognormal sigma on systematics of background normalization",default=1)
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    args = parser.parse_args()

    run(args.bkgSF, args.bkgSyst, args.NZ)

if __name__ == '__main__':
    main()

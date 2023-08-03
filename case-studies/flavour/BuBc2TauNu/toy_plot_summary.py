import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import joblib
from collections import OrderedDict
import uproot
from userConfig import loc, train_vars, train_vars_vtx, FCC_label

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def run(nz):
    #Load toy results from json

    sig_labels = {'Bc': '$B_c^+ \\to \\tau^+ \\nu_\\tau$',
                  'Bu': '$B^+ \\to \\tau^+ \\nu_\\tau$'  }

    sens = {}
    sf_list   = [1,2,5,10]
    syst_list = [1,2,5,10]

   
    for sig in ['Bc', 'Bu']: 
      for bkg_sf in sf_list:
        sens[f'{sig}_{bkg_sf}'] = []
        for bkg_syst in syst_list:  
            with open(f'{loc.JSON}/toy_results_{sig}_{bkg_sf}bkg_{bkg_syst}Syst_{nz}Z.json') as f:
              results_dict = json.load(f)
            sens[f'{sig}_{bkg_sf}'].append( (results_dict[f'sigma_R{sig}'][0]+results_dict[f'sigma_L{sig}'][0])/2 )

    print (sens)

    colors = {1:  "#2166ac",
              2:  "#4d8bd1",
              5:  "#92c5de",
              10: "#d1e5f0"
              }
    #syst_list[0] = 0
    for sig in ['Bc', 'Bu']: 
      fig,ax = plt.subplots(figsize=(10,8))
      for bkg_sf in sf_list:
        # latex LARGE probably with respect to 12pt, still smaller than fontsize 30
        line_label = 'Background inflation:'+f' {bkg_sf}'+'$\\times N_\\textrm{\\LARGE{bkg}}^\\textrm{\\LARGE{exp}}$'
        # marker 'o' does not show as filled circle in UNIX $display, but is actually properly filled in other pdf viewers
        ax.plot( syst_list, sens[f'{sig}_{bkg_sf}'], marker='o', markersize=4, color=colors[bkg_sf], mfc=colors[bkg_sf], label=line_label)
  
      ax.tick_params(axis='both', which='major', labelsize=25)
      ax.set_title( FCC_label, loc='right', fontsize=20)
      plt.xlabel("Relative $\\sigma_\\textrm{\\LARGE{bkg}}$ of background fluctuation",fontsize=30)
      plt.ylabel("Relative $\\sigma$"+f"({sig_labels[sig]})",fontsize=30)
      ymin, ymax = plt.ylim()
      plt.xlim(0,11)
      plt.ylim(0,0.062)
      #if sig == 'Bc': plt.ylim(0,0.034)
      plt.legend(loc="upper left",fontsize=20)
      plt.grid(alpha=0.4,which="major",axis='y')
      plt.tight_layout()
      fig.savefig(f"{loc.PLOTS}/expected_sens_scan_{sig}_{nz}Z.pdf")


def main():
    parser = argparse.ArgumentParser(description='Analyse toys for template fit')
    parser.add_argument("--NZ", choices=["0.5","1","2","3","4","5"],required=False,help="Number of Z's (x 10^12)",default="5")
    args = parser.parse_args()

    run(args.NZ)

if __name__ == '__main__':
    main()

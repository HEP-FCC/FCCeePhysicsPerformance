import sys, os, argparse
import json
import numpy as np
from uncertainties import *
import matplotlib.pyplot as plt

#Local code
from userConfig import loc, train_vars, train_vars_vtx
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

number_of_zs = [0.5,1,2,3,4,5]
syst = [0,0.25,0.5,1]
params = {"N_Bc2TauNu": {"name": "$N(B_c^+ \\to \\tau^+ \\nu_\\tau)$","low": 0.02, "high": 0.12},
          "BF_Bc2TauNu": {"name": "$\\mathcal{B}(B_c^+ \\to \\tau^+ \\nu_\\tau)$", "low": 0.08, "high": 0.15},
          "BF_ratio": {"name": "$R_c$", "low": 0.02, "high": 0.12}
         }

with open(f'{loc.JSON}/BF_vals.json') as f:
    vals = json.load(f)

for p in params:
    print("\\renewcommand{\\arraystretch}{1.4}{")
    print("\\begin{table[h!]")
    print("\\centering")
    print("\\small")
    print("\\begin{tabular}{ll}")
    print("$N_Z (\\times 10^{12})$ & Relative $\\sigma$ ($\\sigma_{syst}^N = [0, 0.25, 0.5, 1] \\times \\sigma_{stat}^N$) \\\\ \\hline")
    for nz in number_of_zs:
        print(f"{nz} & ", end ="")
        print("[", end="")
        for s in syst:
            x = round(vals[f"{p}_{nz}_{s}"][2],3)
            if(s!=1):
                print(x, end=", ")
            else:
                print(x, end="")
        print("]", end="")
        print(" \\\\")
    print("\\hline")
    print("\\end{tabular}")
    print("\\caption{Estimated relative precision on %s as a function of $N_Z$, where four different levels of systematic uncertainty on the signal yield are shown.}" % params[p]['name'])
    print("\\label{tab:%s_vs_NZ}" % p)
    print("\\end{table}")
    print("}")

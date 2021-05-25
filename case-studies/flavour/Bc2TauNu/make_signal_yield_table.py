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

print("\\renewcommand{\\arraystretch}{1.2}{")
print("\\begin{table}[]")
print("\\centering")
print("\\begin{tabular}{ccc}")
print("$N_Z (\\times 10^{12})$ & $N(B_c^+ \\to \\tau^+ \\nu_\\tau)$ & Relative $\\sigma$ (\\%) \\\\ \\hline")
for nz in number_of_zs:
    with open(f'{loc.JSON}/toy_results_{nz}.json') as f:
        toys = json.load(f)
    x = toys["mu"][0]
    x_err = toys["sigma"][0]
    r = 100*(x_err / x)
    r = round(r, 1)
    x = int(x)
    x_err = int(x_err)
    suff = ""
    suff_err = ""
    if(x < 1000.):
        suff = "\\phantom{0}"
    if(x_err < 100.):
        suff_err = "\\phantom{0}"
    print(f"{nz} & ${x}{suff} \\pm {x_err}{suff_err}$ & {r} \\\\")
print("\\hline")
print("\\end{tabular}")
print("\\caption{Estimated signal yields as a function of $N_Z$, where the uncertainties quoted are statistical only. The yield central values are determined from the cut optimisation procedure, and the uncertainties from pseudoexperiment fits.}")
print("\\label{tab:NBc_vs_NZ}")
print("\\end{table}")
print("}")

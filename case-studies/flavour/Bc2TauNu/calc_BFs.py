import sys, os, argparse
import json
import numpy as np
from uncertainties import *
import matplotlib.pyplot as plt

#Local code
from userConfig import loc, train_vars, train_vars_vtx
import plotting
import utils as ut
import matplotlib.ticker as plticker

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

number_of_zs = [0.5,1,2,3,4,5]
#Systematic uncertainty on signal yield relative to stat (plotted in different colurs)
syst = {"0": "#08306b",
        "0.25": "#2171b5",
        "0.5": "#6baed6",
        "1": "#c6dbef"
        }

vals = {}

for nz in number_of_zs:
    #Total number of Z's produced
    N_Z = float(nz) * 1e12
    #Z -> bb branching ratio
    BF_Zbb = 0.1512
    #Total number of b quarks
    N_bb = N_Z*BF_Zbb*2
    #Production fractions for Bc and B+
    f_Bc = 0.0004
    f_Bu = 0.43
    #Total number of Bc and B+ produced
    N_Bc = N_bb * f_Bc
    N_Bu = N_bb * f_Bu

    ################################
    ### Bc -> tau nu calculation ###
    ################################

    #BF(Bc -> tau nu) = N(Bc -> tau nu) / N(Bc -> J/psi mu nu) * [eff(Bc -> J/psi mu nu) / eff(Bc -> tau nu)] * [BF(J/psi -> mu mu) / BF(tau -> 3pi nu)] * BF_pred(Bc -> J/psi mu nu)

    #Theory prediction for BF(Bc -> J/psi mu nu) from Olcyr
    BF_pred_Bc2JpsiMuNu = ufloat(0.0135,0.0011)

    #Full efficiency of Bc -> J/psi mu nu analysis (assume high efficiency apart from mass window > 5.3 GeV)
    #Mass window looks about 30% efficient on LHCb MC (from arXiv:1407.2126), so assume 0.3*0.5 = 0.15
    #Assume 1% relative uncertainty on the efficiency
    eff_Bc2JpsiMuNu = ufloat(0.1,0.0011)

    #PDG average J/psi -> mu mu BF
    BF_Jpsi2MuMu = ufloat(5.961e-2, 0.033e-2)

    #Numer of expected Bc -> J/psi mu nu
    N_Bc2JpsiMuNu =  N_Bc * BF_pred_Bc2JpsiMuNu.n * BF_Jpsi2MuMu * eff_Bc2JpsiMuNu
    #Error is just sqrt(N) as this mode will be very clean (no significant systematics)
    N_Bc2JpsiMuNu_err = np.sqrt(N_Bc2JpsiMuNu.n)
    N_Bc2JpsiMuNu_obs = ufloat(N_Bc2JpsiMuNu.n, N_Bc2JpsiMuNu_err)

    #PDG average tau -> 3pi nu BF
    BF_Tau23Pi = ufloat(9.31e-2,0.05e-2)

    #Theory expectation for Bc -> tau nu (not so important, just sets the level of expected signal and our central value estimated BF)
    #Olcyr value from paper
    BF_Bc2TauNu_expected = 1.94e-2

    #Full efficiency of Bc -> tau nu analysis, known to 1% uncertainty
    #Read value from optimisation
    with open(f'{loc.JSON}/optimal_yields_{nz}.json') as f:
      eff = json.load(f)
    eff_Bc2TauNu = ufloat(eff["eff_Bc2TauNu"],0.01*eff["eff_Bc2TauNu"])

    #Expected number of signal events
    N_Bc2TauNu_expected = N_Bc * BF_Bc2TauNu_expected * BF_Tau23Pi * eff_Bc2TauNu

    #Actual number of Bc -> tau nu observed - values from the toy results
    with open(f'{loc.JSON}/toy_results_{nz}.json') as f:
        toys = json.load(f)

    #Loop over potential levels of systemaitcs (relative to signal fit error)
    for s in syst:

        #Assume that the systematics are similar to the stat error, so a sqrt(2) inflation
        error = np.sqrt(toys["sigma"][0]**2 + float(s)*toys["sigma"][0]**2)
        N_Bc2TauNu_obs = ufloat(toys["mu"][0], error)
        N_Bc2TauNu_obs_rel_err = N_Bc2TauNu_obs.s / N_Bc2TauNu_obs.n

        #print(f"BF(J/psi -> mu mu): {BF_Jpsi2MuMu.n} +/- {BF_Jpsi2MuMu.s}")
        #print(f"BF(tau -> 3pi nu): {BF_Tau23Pi.n} +/- {BF_Tau23Pi.s}")
        #print(f"Bc -> tau nu efficiency: {eff_Bc2TauNu.n} +/- {eff_Bc2TauNu.s}")
        #print(f"N(Bc -> (tau -> 3pi nu) nu) observed: {N_Bc2TauNu_obs.n} +/- {N_Bc2TauNu_obs.s}")
        #print(f"N(Bc -> (J/psi -> mu mu) mu nu) observed: {N_Bc2JpsiMuNu_obs.n} +/- {N_Bc2JpsiMuNu_obs.s}")
        #print(f"BF(Bc -> J/psi mu nu) from theory: {BF_pred_Bc2JpsiMuNu.n} +/- {BF_pred_Bc2JpsiMuNu.s}")

        #Build the measured BF(Bc -> tau nu)
        BF_Bc2TauNu = (N_Bc2TauNu_obs / N_Bc2JpsiMuNu_obs) * (eff_Bc2JpsiMuNu / eff_Bc2TauNu) * (BF_Jpsi2MuMu / BF_Tau23Pi) * BF_pred_Bc2JpsiMuNu
        #print(f"Estimated BF(Bc -> tau nu): {BF_Bc2TauNu.n} +/- {BF_Bc2TauNu.s}")
        BF_Bc2TauNu_rel_error = BF_Bc2TauNu.s / BF_Bc2TauNu.n
        #print(f"Relative precision: {BF_Bc2TauNu_rel_error}")
        BF_ratio = (N_Bc2TauNu_obs / N_Bc2JpsiMuNu_obs) * (eff_Bc2JpsiMuNu / eff_Bc2TauNu) * (BF_Jpsi2MuMu / BF_Tau23Pi)
        #print(f"Estimated BF(Bc -> tau nu) / BF(Bc -> J/psi mu nu): {BF_ratio.n} +/- {BF_ratio.s}")
        BF_ratio_rel_error = BF_ratio.s / BF_ratio.n
        #print("====================================================")

        #Write results to dict in json
        vals[f"BF_Jpsi2MuMu_{nz}_{s}"] = [BF_Jpsi2MuMu.n, BF_Jpsi2MuMu.s]
        vals[f"BF_Tau23Pi_{nz}_{s}"] = [BF_Tau23Pi.n, BF_Tau23Pi.s]
        vals[f"eff_Bc2TauNu_{nz}_{s}"] = [eff_Bc2TauNu.n, eff_Bc2TauNu.s]
        vals[f"eff_Bc2JpsiMuNu_{nz}_{s}"] = [eff_Bc2JpsiMuNu.n, eff_Bc2JpsiMuNu.s]
        vals[f"N_Bc2TauNu_{nz}_{s}"] = [N_Bc2TauNu_obs.n, N_Bc2TauNu_obs.s, N_Bc2TauNu_obs_rel_err]
        vals[f"N_Bc2JpsiMuNu_{nz}_{s}"] = [N_Bc2JpsiMuNu_obs.n, N_Bc2JpsiMuNu_obs.s]
        vals[f"BF_Bc2JpsiMuNu_{nz}_{s}"] = [BF_pred_Bc2JpsiMuNu.n, BF_pred_Bc2JpsiMuNu.s]
        vals[f"BF_Bc2TauNu_{nz}_{s}"] = [BF_Bc2TauNu.n, BF_Bc2TauNu.s, BF_Bc2TauNu_rel_error]
        vals[f"BF_ratio_{nz}_{s}"] = [BF_ratio.n, BF_ratio.s, BF_ratio_rel_error]

    #Write values to LaTeX (assuming maximal systematics)
    f = open(f"{loc.TEX}/BF_vals_{nz}.tex",'w')

    x = vals[f"BF_Jpsi2MuMu_{nz}_1"][0]*1e2
    x_err = vals[f"BF_Jpsi2MuMu_{nz}_1"][1]*1e2
    f.write("\\def\\BFJpsitoMuMu{" + "(%.2f" % x + " \\pm %.2f" % x_err + ") \\times 10^{-2}}\n")
    x = vals[f"BF_Tau23Pi_{nz}_1"][0]*1e2
    x_err = vals[f"BF_Tau23Pi_{nz}_1"][1]*1e2
    f.write("\\def\\BFTautoThreePi{" + "(%.2f" % x + " \\pm %.2f" % x_err + ") \\times 10^{-2}}\n")
    x = vals[f"eff_Bc2TauNu_{nz}_1"][0]*1e3
    x_err = vals[f"eff_Bc2TauNu_{nz}_1"][1]*1e3
    f.write("\\def\\effBctoTauNu{" + "(%.2f" % x + " \\pm %.2f" % x_err + ") \\times 10^{-3}}\n")
    x = vals[f"eff_Bc2JpsiMuNu_{nz}_1"][0]
    x_err = vals[f"eff_Bc2JpsiMuNu_{nz}_1"][1]
    f.write("\\def\\effBctoJpsiMuNu{" + "%.3f" % x + " \\pm %.3f" % x_err+"}\n")
    x = int(vals[f"N_Bc2TauNu_{nz}_1"][0])
    x_err = int(vals[f"N_Bc2TauNu_{nz}_1"][1])
    f.write("\\def\\NBctoTauNu{" + "%.0f" % x + " \\pm %.0f" % x_err+"}\n")
    x = int(vals[f"N_Bc2JpsiMuNu_{nz}_1"][0])
    x_err = int(vals[f"N_Bc2JpsiMuNu_{nz}_1"][1])
    f.write("\\def\\NBctoJpsiMuNu{" + "%.0f" % x + " \\pm %.0f" % x_err+"}\n")
    x = vals[f"BF_Bc2JpsiMuNu_{nz}_1"][0]
    x_err = vals[f"BF_Bc2JpsiMuNu_{nz}_1"][1]
    f.write("\\def\\BFBctoJpsiMuNu{" + "%.3f" % x + " \\pm %.3f" % x_err+"}\n")
    x = vals[f"BF_Bc2TauNu_{nz}_1"][0]*1e2
    x_err = vals[f"BF_Bc2TauNu_{nz}_1"][1]*1e2
    f.write("\\def\\BFBctoTauNu{" + "(%.3f" % x + " \\pm %.3f" % x_err + ") \\times 10^{-2}}\n")
    x = vals[f"BF_Bc2TauNu_{nz}_1"][2]*1e2
    f.write("\\def\\BFBctoTauNuRelErr{" + "%.1f}\n" % x)

#Make trend plots as a function of NZ for different variables
params = {"N_Bc2TauNu": {"name": "$N(B_c^+ \\to \\tau^+ \\nu_\\tau)$ relative $\\sigma$","low": 0.02, "high": 0.12},
          "BF_Bc2TauNu": {"name": "$\\mathcal{B}(B_c^+ \\to \\tau^+ \\nu_\\tau)$ relative $\\sigma$", "low": 0.08, "high": 0.15},
          "BF_ratio": {"name": "$R_c$ relative $\\sigma$", "low": 0.02, "high": 0.12}
         }
for v in params:
    fig, ax = plt.subplots(figsize=(9,8))
    x = {}
    for s in syst:
        x[s] = []
    for nz in number_of_zs:
        for s in syst:
            x[s].append(vals[f"{v}_{nz}_{s}"][2])
    for s in syst:
        plt.errorbar(x=number_of_zs,y=x[s],xerr=None,yerr=None,color=syst[s],fmt="o-",label="$\\sigma_{syst} = %s \\times \\sigma_{stat}$" % s)
    ax.tick_params(axis='both', which='major', labelsize=25)
    #plt.grid(which="both",axis="y")
    lmax = plticker.MultipleLocator(base=0.02)
    lmin = plticker.MultipleLocator(base=0.01)
    ax.yaxis.set_major_locator(lmax)
    ax.yaxis.set_minor_locator(lmin)
    # Add the grid
    ax.grid(which='both', axis='y', linestyle='-')
    plt.ylabel(params[v]["name"],fontsize=30)
    plt.xlabel("$N_Z (\\times 10^{12})$",fontsize=30)
    plt.ylim(params[v]["low"],params[v]["high"])
    if(v=="N_Bc2TauNu"):
        plt.legend(loc="upper right",fontsize=25)
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/{v}_trend_vs_NZ.pdf")

#Store all values in JSON dict
with open(f'{loc.JSON}/BF_vals.json', 'w') as fp:
    json.dump(vals, fp)

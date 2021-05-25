import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot
import joblib
import glob
from decay_mode_xs import modes, prod
from num2tex import num2tex
from num2tex import configure as num2tex_configure
num2tex_configure(exp_format='times')

with open('optimal_yields.json') as f:
    yields = json.load(f)

hadron_names = {"Bu": "B^+",
                "Bd": "B^0",
                "Bs": "B_s^0",
                "Lb": "\\Lambda_b^0"
               }

decay_names = {"Bd": {"DTauNu": "D^- \\tau^+ \\nu_\\tau",
                      "DstTauNu": "D^{*-} \\tau^+ \\nu_\\tau",
                      "D3Pi": "D^- 3\\pi",
                      "Dst3Pi": "D^{*-} 3\\pi",
                      "DDs": "D^- D_s^+",
                      "DstDs": "D^{*-} D_s^+",
                      "DstDsst": "D^{*-} D_s^{*+}"
                      },

               "Bu": {"D0TauNu": "\\bar{D}^0 \\tau^+ \\nu_\\tau",
                      "Dst0TauNu": "\\bar{D}^{*0} \\tau^+ \\nu_\\tau",
                      "D03Pi": "\\bar{D}^0 3\\pi",
                      "Dst03Pi": "\\bar{D}^{*0} 3\\pi",
                      "D0Ds": "\\bar{D}^0 D_s^+",
                      "Dst0Ds": "\\bar{D}^{*0} D_s^+",
                      "Dst0Dsst": "\\bar{D}^{*0} D_s^{*+}"
                      },

               "Bs": {"DsTauNu": "D_s^- \\tau^+ \\nu_\\tau",
                      "DsstTauNu": "D_s^{*-} \\tau^+ \\nu_\\tau",
                      "Ds3Pi": "D_s^- 3\\pi",
                      "Dsst3Pi": "D_s^{*-} 3\\pi",
                      "DsDs": "D_s^- D_s^+",
                      "DsstDs": "D_s^{*-} D_s^+",
                      "DsstDsst": "D_s^{*-} D_s^{*+}"
                      },

               "Lb": {"LcTauNu": "\\Lambda_c^- \\tau^+ \\nu_\\tau",
                      "LcstTauNu": "\\Lambda_c^{*-} \\tau^+ \\nu_\\tau",
                      "Lc3Pi": "\\Lambda_c^- 3\\pi",
                      "Lcst3Pi": "\\Lambda_c^{*-} 3\\pi",
                      "LcDs": "\\Lambda_c^- D_s^+",
                      "LcstDs": "\\Lambda_c^{*-} D_s^+",
                      "LcstDsst": "\\Lambda_c^{*-} D_s^{*+}"
                      }
              }

print("\\renewcommand{\\arraystretch}{1.15}{")
print("\\begin{table}[]")
print("\\centering")
print("\\tiny")
print("\\begin{tabular}{lllll}")
print("Decay mode & N(expected) & N(generated) & Expected / Generated & Final $\\epsilon$ \\\\ \\hline")

for b in hadron_names:
    for d in decay_names[b]:
        yield_gen_exp = "{:e}".format(yields[f"N_{b}2{d}_gen"])
        yield_gen = num2tex(yield_gen_exp,precision=3)

        yield_exp_exp = "{:e}".format(yields[f"N_{b}2{d}_tot"])
        yield_exp = num2tex(yield_exp_exp,precision=3)

        r = float(yields[f"N_{b}2{d}_tot"])/yields[f"N_{b}2{d}_gen"]
        r = round(r, 1)

        if(yields[f"eff_{b}2{d}"]==0):
            eff = 0
        else:
            eff_exp = "{:e}".format(yields[f"eff_{b}2{d}"])
            eff = num2tex(eff_exp,precision=3)

        print(f"${hadron_names[b]} \\to {decay_names[b][d]}$ & ${yield_exp}$ & ${yield_gen}$ & ${r}$ & ${eff}$ \\\\")
    print("\\hline")
print("\\end{tabular}")
print("\\end{table}")
print("}")

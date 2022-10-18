import json

Z_bb_xs = 6645.46 #pb
Z_cc_xs = 5287.36 #pb

b_hadrons = ["Bu", "Bd", "Bs", "Lb"]
c_hadrons = ["Dd", "Ds", "Lc"]

#B hadron production fractions
prod = {"Bu": 0.43  * Z_bb_xs,
        "Bd": 0.43  * Z_bb_xs,
        "Bs": 0.096 * Z_bb_xs,
        "Lb": 0.037 * Z_bb_xs,

        "Dd": 0.238 * Z_cc_xs,
        "Ds": 0.116 * Z_cc_xs,
        "Lc": 0.079 * Z_cc_xs
        }
# charm production fractions from https://link.springer.com/article/10.1007/s100520000421 

modes = {}
modes["Bu"] = {}
modes["Bd"] = {}
modes["Bs"] = {}
modes["Lb"] = {}
modes["Dd"] = {}
modes["Ds"] = {}
modes["Lc"] = {}

modes["Bd"]["DENu"] = 0.0224   # from PDG
modes["Bd"]["DMuNu"] = 0.0224  # from PDG
modes["Bd"]["DTauNu"] = 0.0108 # from PDG
modes["Bd"]["DstENu"] = 0.0497   # from PDG
modes["Bd"]["DstMuNu"] = 0.0497  # from PDG
modes["Bd"]["DstTauNu"] = 0.0157 # from PDG
modes["Bd"]["D3Pi"] = 0.006
modes["Bd"]["Dst3Pi"] = 0.00721
modes["Bd"]["DDs"] = 0.0078
modes["Bd"]["DstDs"] = 0.0068 + 0.0067 # D + Ds* was not generated, use this sample for D* + Ds and D + Ds* , numbers from Heavy Flavor Average
modes["Bd"]["DstDsst"] = 0.0177

modes["Bu"]["D0ENu"] = 0.023    # from PDG
modes["Bu"]["D0MuNu"] = 0.023   # from PDG
modes["Bu"]["D0TauNu"] = 0.0077 # from PDG
modes["Bu"]["Dst0ENu"] = 0.0558   # from PDG
modes["Bu"]["Dst0MuNu"] = 0.0558  # from PDG
modes["Bu"]["Dst0TauNu"] = 0.0188 # from PDG
modes["Bu"]["D03Pi"] = 0.0056
modes["Bu"]["Dst03Pi"] = 0.0103
modes["Bu"]["D0Ds"] = 0.0133
modes["Bu"]["Dst0Ds"] = 0.0121 + 0.0093 # D0 + Ds* was not generated, use this sample for D0* + Ds and D0 + Ds*, numbers from Heavy Flavor Average
modes["Bu"]["Dst0Dsst"] = 0.0171

modes["Bs"]["DsENu"] = 0.0243   # assume to be the same as mu nu
modes["Bs"]["DsMuNu"] = 0.0243  # from PDG
modes["Bs"]["DsTauNu"] = 0.0243 # not sure where from
modes["Bs"]["DsstENu"] = 0.053    # assume to be the same as mu nu
modes["Bs"]["DsstMuNu"] = 0.053   # from PDG
modes["Bs"]["DsstTauNu"] = 0.0162 # not sure where from
modes["Bs"]["Ds3Pi"] = 0.0061
modes["Bs"]["Dsst3Pi"] = 0.00721
modes["Bs"]["DsDs"] = 0.0044
modes["Bs"]["DsstDs"] = 0.0139
modes["Bs"]["DsstDsst"] = 0.0144

modes["Lb"]["LcENu"] = 0.0327     # assume to be the same as tau nu (~3.1% from PDG)
modes["Lb"]["LcMuNu"] = 0.0327    # assume to be the same as tau nu (~3.1% from PDG)
modes["Lb"]["LcTauNu"] = 0.0327   # not sure where from, no measurement so far. But is close to 3.1%
modes["Lb"]["LcstENu"] = 0.0327   # same as above
modes["Lb"]["LcstMuNu"] = 0.0327  # same as above
modes["Lb"]["LcstTauNu"] = 0.0327 # same as above
modes["Lb"]["Lc3Pi"] = 0.0077
modes["Lb"]["Lcst3Pi"] = 0.0077
modes["Lb"]["LcDs"] = 0.011
modes["Lb"]["LcstDs"] = 0.011
modes["Lb"]["LcstDsst"] = 0.011


modes["Dd"]["K3Pi"] = 0.6 # use this sample to model Dd -> K0 + anything
modes["Dd"]["TauNu"] = 1.2e-3 # from PDG

modes["Ds"]["EtapRho"] = 0.3  # use this sample to model Ds -> eta + anything and Ds -> eta prime + anything
modes["Ds"]["TauNu"] = 0.0532 # from PDG

modes["Lc"]["LENu"]     = 0.036  #from PDG
modes["Lc"]["LMuNu"]    = 0.035  #from PDG
modes["Lc"]["LRhoPi"]   = 0.102  # use this sample to model Lc -> Lambda0 + 3 charged pi
modes["Lc"]["Sigma2Pi"] = 0.15   # use this sample to model Lc -> Sigma+  + 2 charged pi


xs = {}
for p in prod:
    xs[p] = {}
    for m in modes[p]:
        xs[p][m] = modes[p][m] * prod[p] 

#print(json.dumps(xs, sort_keys=True, indent=4))

import json

Z_bb_xs = 6645.46 #pb

#B hadron production fractions
prod = {"Bu": 0.43,
        "Bd": 0.43,
        "Bs": 0.096,
        "Lb": 0.037
        }

modes = {}
modes["Bu"] = {}
modes["Bd"] = {}
modes["Bs"] = {}
modes["Lb"] = {}

modes["Bd"]["DTauNu"] = 0.0108
modes["Bd"]["DMuNu"] = 0.0224
modes["Bd"]["DENu"] = 0.0224
modes["Bd"]["DstTauNu"] = 0.0157
modes["Bd"]["DstMuNu"] = 0.0497
modes["Bd"]["DstENu"] = 0.0497
modes["Bd"]["D3Pi"] = 0.006
modes["Bd"]["DRho"] = 0.0076
modes["Bd"]["Dst3Pi"] = 0.00721
modes["Bd"]["DstRho"] = 0.015
modes["Bd"]["DDs"] = 0.0072
modes["Bd"]["DstDs"] = 0.008
modes["Bd"]["DstDsst"] = 0.0177

modes["Bu"]["D0TauNu"] = 0.0077
modes["Bu"]["D0MuNu"] = 0.023
modes["Bu"]["D0ENu"] = 0.023
modes["Bu"]["Dst0TauNu"] = 0.0188
modes["Bu"]["Dst0MuNu"] = 0.0558
modes["Bu"]["Dst0ENu"] = 0.0558
modes["Bu"]["D03Pi"] = 0.0056
modes["Bu"]["D0Rho"] = 0.0134
modes["Bu"]["Dst03Pi"] = 0.0103
modes["Bu"]["Dst0Rho"] = 0.0098
modes["Bu"]["D0Ds"] = 0.009
modes["Bu"]["Dst0Ds"] = 0.0076
modes["Bu"]["Dst0Dsst"] = 0.0171

modes["Bs"]["DsTauNu"] = 0.0118
modes["Bs"]["DsMuNu"] = 0.0244
modes["Bs"]["DsENu"] = 0.0244
modes["Bs"]["DsstTauNu"] = 0.0167
modes["Bs"]["DsstMuNu"] = 0.053
modes["Bs"]["DsstENu"] = 0.053
modes["Bs"]["Ds3Pi"] = 0.0061
modes["Bs"]["DsRho"] = 0.0068
modes["Bs"]["Dsst3Pi"] = 0.00721
modes["Bs"]["DsstRho"] = 0.0095
modes["Bs"]["DsDs"] = 0.0044
modes["Bs"]["DsstDs"] = 0.0139
modes["Bs"]["DsstDsst"] = 0.0144

modes["Lb"]["LcTauNu"] = 0.015
modes["Lb"]["LcMuNu"] = 0.062
modes["Lb"]["LcENu"] = 0.062
modes["Lb"]["LcstTauNu"] = 0.004
modes["Lb"]["LcstMuNu"] = 0.013
modes["Lb"]["LcstENu"] = 0.013
modes["Lb"]["Lc3Pi"] = 0.0077
modes["Lb"]["LcRho"] = 0.0077
modes["Lb"]["Lcst3Pi"] = 0.0077
modes["Lb"]["LcstRho"] = 0.0077
modes["Lb"]["LcDs"] = 0.011
modes["Lb"]["LcstDs"] = 0.011
modes["Lb"]["LcstDsst"] = 0.011

xs = {}
for p in prod:
    xs[p] = {}
    for m in modes[p]:
        xs[p][m] = modes[p][m] * Z_bb_xs * prod[p]

#print(json.dumps(xs, sort_keys=True, indent=4))

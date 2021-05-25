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
modes["Bd"]["DstTauNu"] = 0.0157
modes["Bd"]["D3Pi"] = 0.006
modes["Bd"]["Dst3Pi"] = 0.00721
modes["Bd"]["DDs"] = 0.0072
modes["Bd"]["DstDs"] = 0.008
modes["Bd"]["DstDsst"] = 0.0177

modes["Bu"]["D0TauNu"] = 0.0077
modes["Bu"]["Dst0TauNu"] = 0.0188
modes["Bu"]["D03Pi"] = 0.0056
modes["Bu"]["Dst03Pi"] = 0.0103
modes["Bu"]["D0Ds"] = 0.009
modes["Bu"]["Dst0Ds"] = 0.0076
modes["Bu"]["Dst0Dsst"] = 0.0171

modes["Bs"]["DsTauNu"] = 0.0243
modes["Bs"]["DsstTauNu"] = 0.0162
modes["Bs"]["Ds3Pi"] = 0.0061
modes["Bs"]["Dsst3Pi"] = 0.00721
modes["Bs"]["DsDs"] = 0.0044
modes["Bs"]["DsstDs"] = 0.0139
modes["Bs"]["DsstDsst"] = 0.0144

modes["Lb"]["LcTauNu"] = 0.0327
modes["Lb"]["LcstTauNu"] = 0.0327
modes["Lb"]["Lc3Pi"] = 0.0077
modes["Lb"]["Lcst3Pi"] = 0.0077
modes["Lb"]["LcDs"] = 0.011
modes["Lb"]["LcstDs"] = 0.011
modes["Lb"]["LcstDsst"] = 0.011

xs = {}
for p in prod:
    xs[p] = {}
    for m in modes[p]:
        xs[p][m] = modes[p][m] * Z_bb_xs * prod[p]

#print(json.dumps(xs, sort_keys=True, indent=4))

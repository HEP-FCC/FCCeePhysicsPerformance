import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "read_EDM4HEP/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "myFCCee_procDict_spring2021_IDEA.json"
process_list=['HNL_eenu_10GeV_1p41e-6Ve',
              'HNL_eenu_30GeV_1p41e-6Ve',
              'HNL_eenu_50GeV_1p41e-6Ve',
              'HNL_eenu_70GeV_1p41e-6Ve']

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {
    #"sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100"
    "sel0": "HNL_mass.size() > 0",
}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.

variables = {

    #gen variables
    "HNL_mass":     {"name":"HNL_mass",     "title":"Gen N mass [GeV]",      "bin":100,"xmin":0 ,"xmax":100},
    "HNL_pT":       {"name":"HNL_pT",       "title":"Gen N p_{T} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "HNL_eta":      {"name":"HNL_eta",      "title":"Gen N #eta",            "bin":60, "xmin":-3,"xmax":3},
    "HNL_phi":      {"name":"HNL_phi",      "title":"Gen N #phi",            "bin":64, "xmin":-3.2,"xmax":3.2},
    "HNL_lifetime": {"name":"HNL_lifetime", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-9},
    "L_xy":         {"name":"L_xy",         "title":"Gen N L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "HNL_vertex_x": {"name":"HNL_vertex_x", "title":"Gen N production vertex x [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "HNL_vertex_y": {"name":"HNL_vertex_y", "title":"Gen N production vertex y [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "HNL_vertex_z": {"name":"HNL_vertex_z", "title":"Gen N production vertex z [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    
    "electron_pT":       {"name":"electron_pT",       "title":"Gen e^{#font[122]{\55}} p_{T} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "positron_pT":       {"name":"positron_pT",       "title":"Gen e^{+} p_{T} [GeV]",                                 "bin":100,"xmin":0 ,"xmax":50},
    "electron_eta":      {"name":"electron_eta",      "title":"Gen e^{#font[122]{\55}} #eta",                          "bin":60, "xmin":-3,"xmax":3},
    "positron_eta":      {"name":"positron_eta",      "title":"Gen e^{+} #eta",                                        "bin":60, "xmin":-3,"xmax":3},
    "electron_phi":      {"name":"electron_phi",      "title":"Gen e^{#font[122]{\55}} #phi",                          "bin":64, "xmin":-3.2,"xmax":3.2},
    "positron_phi":      {"name":"positron_phi",      "title":"Gen e^{+} #phi",                                        "bin":64, "xmin":-3.2,"xmax":3.2},
    "electron_vertex_x": {"name":"electron_vertex_x", "title":"Gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "electron_vertex_y": {"name":"electron_vertex_y", "title":"Gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "electron_vertex_z": {"name":"electron_vertex_z", "title":"Gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    #reco variables
    "ntracks":                         {"name":"ntracks",                        "title":"Total number of reco tracks",           "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoHNLTracks":                 {"name":"n_RecoHNLTracks",                "title":"Number of reco HNL tracks",             "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "RecoHNL_DecayVertex_x":           {"name":"RecoHNLDecayVertex.position.x",  "title":"Reco N decay vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_y":           {"name":"RecoHNLDecayVertex.position.y",  "title":"Reco N decay vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_z":           {"name":"RecoHNLDecayVertex.position.z",  "title":"Reco N decay vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_chi2":        {"name":"RecoHNLDecayVertex.chi2",        "title":"Reco N decay vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "RecoHNL_DecayVertex_probability": {"name":"RecoHNLDecayVertex.probability", "title":"Reco N decay vertex probability",       "bin":100,"xmin":0 ,"xmax":10},
    
    "RecoElectron_pT":       {"name":"RecoElectron_pT",       "title":"Reco e^{#font[122]{\55}} p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPositron_pT":       {"name":"RecoPositron_pT",       "title":"Reco e^{+} p_{T} [GeV]",                "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco e^{#font[122]{\55}} #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoPositron_eta":      {"name":"RecoPositron_eta",      "title":"Reco e^{+} #eta",                       "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco e^{#font[122]{\55}} #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoPositron_phi":      {"name":"RecoPositron_phi",      "title":"Reco e^{+} #phi",                       "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco e^{#font[122]{\55}} charge",       "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoPositron_charge":   {"name":"RecoPositron_charge",   "title":"Reco e^{+} charge",                     "bin":3, "xmin":-1.5,"xmax":1.5},

    #gen-reco
    "GenMinusRecoElectron_pT":   {"name":"GenMinusRecoElectron_pT",   "title":"Gen e^{#font[122]{\55}} p_{T} - Reco e^{#font[122]{\55}} p_{T} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoPositron_pT":   {"name":"GenMinusRecoPositron_pT",   "title":"Gen e^{+} p_{T} - Reco e^{+} p_{T} [GeV]",                              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoElectron_eta":  {"name":"GenMinusRecoElectron_eta",  "title":"Gen e^{#font[122]{\55}} #eta - Reco e^{#font[122]{\55}} #eta",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoPositron_eta":  {"name":"GenMinusRecoPositron_eta",  "title":"Gen e^{+} #eta - Reco e^{+} #eta",                                      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoElectron_phi":  {"name":"GenMinusRecoElectron_phi",  "title":"Gen e^{#font[122]{\55}} #phi - Reco e^{#font[122]{\55}} #phi",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoPositron_phi":  {"name":"GenMinusRecoPositron_phi",  "title":"Gen e^{+} #phi - Reco e^{+} #phi",                                      "bin":100,"xmin":-5 ,"xmax":5},

    "GenMinusRecoHNL_DecayVertex_x":  {"name":"GenMinusRecoHNL_DecayVertex_x",  "title":"Gen N decay vertex x - Reco N decay vertex x [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_DecayVertex_y":  {"name":"GenMinusRecoHNL_DecayVertex_y",  "title":"Gen N decay vertex y - Reco N decay vertex y [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_DecayVertex_z":  {"name":"GenMinusRecoHNL_DecayVertex_z",  "title":"Gen N decay vertex z - Reco N decay vertex z [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
}

###Number of CPUs to use
NUM_CPUS = 2

###Produce TTrees
DO_TREE=True

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS, doTree=DO_TREE)

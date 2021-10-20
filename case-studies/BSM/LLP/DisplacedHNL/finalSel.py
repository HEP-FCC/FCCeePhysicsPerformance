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
    "sel0": "GenHNL_mass.size() > 0",
    "sel1": "GenHNL_mass.size() > 0 && n_RecoElectrons > 1",
}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.

variables = {

    #gen variables
    "GenHNL_mass":     {"name":"GenHNL_mass",     "title":"Gen N mass [GeV]",      "bin":100,"xmin":0 ,"xmax":100},
    "GenHNL_pt":       {"name":"GenHNL_pt",       "title":"Gen N p_{T} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_eta":      {"name":"GenHNL_eta",      "title":"Gen N #eta",            "bin":60, "xmin":-3,"xmax":3},
    "GenHNL_phi":      {"name":"GenHNL_phi",      "title":"Gen N #phi",            "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNL_lifetime": {"name":"GenHNL_lifetime", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-9},
    "GenHNL_Lxy":      {"name":"GenHNL_Lxy",      "title":"Gen N L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "GenHNL_vertex_x": {"name":"GenHNL_vertex_x", "title":"Gen N production vertex x [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNL_vertex_y": {"name":"GenHNL_vertex_y", "title":"Gen N production vertex y [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNL_vertex_z": {"name":"GenHNL_vertex_z", "title":"Gen N production vertex z [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    
    "GenHNLElectron_pt":       {"name":"GenHNLElectron_pt",       "title":"Gen e^{#font[122]{\55}} p_{T} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLPositron_pt":       {"name":"GenHNLPositron_pt",       "title":"Gen e^{+} p_{T} [GeV]",                                 "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_pt":       {"name":"GenHNLNeutrino_pt",       "title":"Gen #nu p_{T} [GeV]",                                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_eta":      {"name":"GenHNLElectron_eta",      "title":"Gen e^{#font[122]{\55}} #eta",                          "bin":60, "xmin":-3,"xmax":3},
    "GenHNLPositron_eta":      {"name":"GenHNLPositron_eta",      "title":"Gen e^{+} #eta",                                        "bin":60, "xmin":-3,"xmax":3},
    "GenHNLNeutrino_eta":      {"name":"GenHNLNeutrino_eta",      "title":"Gen #nu #eta",                                          "bin":60, "xmin":-3,"xmax":3},
    "GenHNLElectron_phi":      {"name":"GenHNLElectron_phi",      "title":"Gen e^{#font[122]{\55}} #phi",                          "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNLPositron_phi":      {"name":"GenHNLPositron_phi",      "title":"Gen e^{+} #phi",                                        "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNLNeutrino_phi":      {"name":"GenHNLNeutrino_phi",      "title":"Gen #nu #phi",                                          "bin":64, "xmin":-3.2,"xmax":3.2},
    
    "GenHNLElectron_vertex_x": {"name":"GenHNLElectron_vertex_x", "title":"Gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNLElectron_vertex_y": {"name":"GenHNLElectron_vertex_y", "title":"Gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNLElectron_vertex_z": {"name":"GenHNLElectron_vertex_z", "title":"Gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    #reco variables
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",           "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoHNLTracks":                 {"name":"n_RecoHNLTracks",                "title":"Number of reco HNL tracks",             "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "RecoHNL_DecayVertex_x":           {"name":"RecoHNLDecayVertex.position.x",  "title":"Reco N decay vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_y":           {"name":"RecoHNLDecayVertex.position.y",  "title":"Reco N decay vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_z":           {"name":"RecoHNLDecayVertex.position.z",  "title":"Reco N decay vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_chi2":        {"name":"RecoHNLDecayVertex.chi2",        "title":"Reco N decay vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "RecoHNL_DecayVertex_probability": {"name":"RecoHNLDecayVertex.probability", "title":"Reco N decay vertex probability",       "bin":100,"xmin":0 ,"xmax":10},
    
    "RecoHNLElectron_pt":       {"name":"RecoHNLElectron_pt",       "title":"Reco e^{#font[122]{\55}} (from HNL) p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLPositron_pt":       {"name":"RecoHNLPositron_pt",       "title":"Reco e^{+} (from HNL) p_{T} [GeV]",                "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_eta":      {"name":"RecoHNLElectron_eta",      "title":"Reco e^{#font[122]{\55}} (from HNL) #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoHNLPositron_eta":      {"name":"RecoHNLPositron_eta",      "title":"Reco e^{+} (from HNL) #eta",                       "bin":60, "xmin":-3,"xmax":3},
    "RecoHNLElectron_phi":      {"name":"RecoHNLElectron_phi",      "title":"Reco e^{#font[122]{\55}} (from HNL) #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoHNLPositron_phi":      {"name":"RecoHNLPositron_phi",      "title":"Reco e^{+} (from HNL) #phi",                       "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoHNLElectron_charge":   {"name":"RecoHNLElectron_charge",   "title":"Reco e^{#font[122]{\55}} (from HNL) charge",       "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoHNLPositron_charge":   {"name":"RecoHNLPositron_charge",   "title":"Reco e^{+} (from HNL) charge",                     "bin":3, "xmin":-1.5,"xmax":1.5},

    "n_RecoJets":       {"name":"n_RecoJets",      "title":"Total number of reco jets",         "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoPhotons":    {"name":"n_RecoPhotons",   "title":"Total number of reco photons",      "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoElectrons":  {"name":"n_RecoElectrons", "title":"Total number of reco electrons",    "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoMuons":      {"name":"n_RecoMuons",     "title":"Total number of reco muons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "RecoJet_pt":       {"name":"RecoJet_pt",       "title":"Reco jet p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_eta":      {"name":"RecoJet_eta",      "title":"Reco jet #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoJet_phi":      {"name":"RecoJet_phi",      "title":"Reco jet #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoJet_charge":   {"name":"RecoJet_charge",   "title":"Reco jet charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoPhoton_pt":       {"name":"RecoPhoton_pt",       "title":"Reco photon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_eta":      {"name":"RecoPhoton_eta",      "title":"Reco photon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoPhoton_phi":      {"name":"RecoPhoton_phi",      "title":"Reco photon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":   {"name":"RecoPhoton_charge",   "title":"Reco photon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuon_pt":       {"name":"RecoMuon_pt",       "title":"Reco muon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_eta":      {"name":"RecoMuon_eta",      "title":"Reco muon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoMuon_phi":      {"name":"RecoMuon_phi",      "title":"Reco muon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":   {"name":"RecoMuon_charge",   "title":"Reco muon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMET":       {"name":"RecoMET",       "title":"Reco MET [GeV]",    "bin":100,"xmin":0 ,"xmax":50},
    "RecoMET_x":     {"name":"RecoMET_x",     "title":"Reco MET x [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMET_y":     {"name":"RecoMET_y",     "title":"Reco MET y [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMET_phi":   {"name":"RecoMET_phi",   "title":"Reco MET #phi",     "bin":64,"xmin":-3.2 ,"xmax":3.2},

    #gen-reco
    "GenMinusRecoHNLElectron_pt":   {"name":"GenMinusRecoHNLElectron_pt",   "title":"Gen e^{#font[122]{\55}} p_{T} - Reco e^{#font[122]{\55}} p_{T} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_pt":   {"name":"GenMinusRecoHNLPositron_pt",   "title":"Gen e^{+} p_{T} - Reco e^{+} p_{T} [GeV]",                              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_eta":  {"name":"GenMinusRecoHNLElectron_eta",  "title":"Gen e^{#font[122]{\55}} #eta - Reco e^{#font[122]{\55}} #eta",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_eta":  {"name":"GenMinusRecoHNLPositron_eta",  "title":"Gen e^{+} #eta - Reco e^{+} #eta",                                      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_phi":  {"name":"GenMinusRecoHNLElectron_phi",  "title":"Gen e^{#font[122]{\55}} #phi - Reco e^{#font[122]{\55}} #phi",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLPositron_phi":  {"name":"GenMinusRecoHNLPositron_phi",  "title":"Gen e^{+} #phi - Reco e^{+} #phi",                                      "bin":100,"xmin":-5 ,"xmax":5},

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

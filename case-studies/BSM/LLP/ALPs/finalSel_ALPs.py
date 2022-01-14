import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "read_EDM4HEP/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "../DisplacedHNL/myFCCee_procDict_spring2021_IDEA.json"
process_list=[
    'ALP_Z_aa_1GeV_cYY_0p5',
    'ALP_Z_aa_1GeV_cYY_0p9',
    'ALP_Z_aa_1GeV_cYY_1p0',
    'ALP_Z_aa_1GeV_cYY_1p5',
    'ALP_Z_aa_1GeV_cYY_1p9',
]

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file

cut_list = {
    #"sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100"
    "selNone": "n_RecoTracks > -1",
    "sel0": "GenALP_mass.size() > 0",
    "sel1": "GenALP_mass.size() > 0 && n_RecoElectrons > 1",
}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.

variables = {

    #gen variables
    "All_n_GenALP":                    {"name":"All_n_GenALP",                   "title":"Total number of gen ALPs",                   "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "AllGenALP_mass":                  {"name":"AllGenALP_mass",                 "title":"All gen ALP mass [GeV]",                       "bin":100,"xmin":0 ,"xmax":10},
    "AllGenALP_e":                     {"name":"AllGenALP_e",                    "title":"All gen ALP energy [GeV]",                     "bin":100,"xmin":0 ,"xmax":100},
    "AllGenALP_p":                     {"name":"AllGenALP_p",                    "title":"All gen ALP p [GeV]",                          "bin":100,"xmin":0 ,"xmax":50},
    "AllGenALP_pt":                    {"name":"AllGenALP_pt",                   "title":"All gen ALP p_{T} [GeV]",                      "bin":100,"xmin":0 ,"xmax":50},
    "AllGenALP_pz":                    {"name":"AllGenALP_pz",                   "title":"All gen ALP p_{z} [GeV]",                      "bin":100,"xmin":0 ,"xmax":50},
    "AllGenALP_eta":                   {"name":"AllGenALP_eta",                  "title":"All gen ALP #eta",                             "bin":60, "xmin":-3,"xmax":3},
    "AllGenALP_theta":                 {"name":"AllGenALP_theta",                "title":"All gen ALP #theta",                           "bin":64, "xmin":0,"xmax":3.2},
    "AllGenALP_phi":                   {"name":"AllGenALP_phi",                  "title":"All gen ALP #phi",                             "bin":64, "xmin":-3.2,"xmax":3.2},

    "n_FSGenElectron":                 {"name":"n_FSGenElectron",                "title":"Number of final state gen electrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenPositron":                 {"name":"n_FSGenPositron",                "title":"Number of final state gen positrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenNeutrino":                 {"name":"n_FSGenNeutrino",                "title":"Number of final state gen neutrinos",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenAntiNeutrino":             {"name":"n_FSGenAntiNeutrino",            "title":"Number of final state gen anti-neutrinos",   "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenPhoton":                   {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",          "bin":8,"xmin":-0.5 ,"xmax":7.5},

    # "n_FSGenElectron_forFS2GenPhotons":                 {"name":"n_FSGenElectron_forFS2GenPhotons",                "title":"Number of final state gen electrons for events with 2 FS photons",        "bin":7,"xmin":-2.5 ,"xmax":4.5},
    # "n_FSGenPositron_forFS2GenPhotons":                 {"name":"n_FSGenPositron_forFS2GenPhotons",                "title":"Number of final state gen positrons for events with 2 FS photons",        "bin":7,"xmin":-2.5 ,"xmax":4.5},

    "FSGenElectron_e":                 {"name":"FSGenElectron_e",                "title":"Final state gen electrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_p":                 {"name":"FSGenElectron_p",                "title":"Final state gen electrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pt":                {"name":"FSGenElectron_pt",               "title":"Final state gen electrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pz":                {"name":"FSGenElectron_pz",               "title":"Final state gen electrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_eta":               {"name":"FSGenElectron_eta",              "title":"Final state gen electrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenElectron_theta":             {"name":"FSGenElectron_theta",            "title":"Final state gen electrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":               {"name":"FSGenElectron_phi",              "title":"Final state gen electrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenPositron_e":                 {"name":"FSGenPositron_e",                "title":"Final state gen positrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_p":                 {"name":"FSGenPositron_p",                "title":"Final state gen positrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_pt":                {"name":"FSGenPositron_pt",               "title":"Final state gen positrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_pz":                {"name":"FSGenPositron_pz",               "title":"Final state gen positrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPositron_eta":               {"name":"FSGenPositron_eta",              "title":"Final state gen positrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenPositron_theta":             {"name":"FSGenPositron_theta",            "title":"Final state gen positrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenPositron_phi":               {"name":"FSGenPositron_phi",              "title":"Final state gen positrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenNeutrino_e":                 {"name":"FSGenNeutrino_e",                "title":"Final state gen neutrino energy [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_p":                 {"name":"FSGenNeutrino_p",                "title":"Final state gen neutrino p [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pt":                {"name":"FSGenNeutrino_pt",               "title":"Final state gen neutrino p_{T} [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pz":                {"name":"FSGenNeutrino_pz",               "title":"Final state gen neutrino p_{z} [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_eta":               {"name":"FSGenNeutrino_eta",              "title":"Final state gen neutrinos #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenNeutrino_theta":             {"name":"FSGenNeutrino_theta",            "title":"Final state gen neutrinos #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenNeutrino_phi":               {"name":"FSGenNeutrino_phi",              "title":"Final state gen neutrinos #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenAntiNeutrino_e":             {"name":"FSGenAntiNeutrino_e",            "title":"Final state gen anti-neutrino energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "FSGenAntiNeutrino_p":             {"name":"FSGenAntiNeutrino_p",            "title":"Final state gen anti-neutrino p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenAntiNeutrino_pt":            {"name":"FSGenAntiNeutrino_pt",           "title":"Final state gen anti-neutrino p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "FSGenAntiNeutrino_pz":            {"name":"FSGenAntiNeutrino_pz",           "title":"Final state gen anti-neutrino p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "FSGenAntiNeutrino_eta":           {"name":"FSGenAntiNeutrino_eta",          "title":"Final state gen anti-neutrinos #eta",        "bin":60, "xmin":-3,"xmax":3},
    "FSGenAntiNeutrino_theta":         {"name":"FSGenAntiNeutrino_theta",        "title":"Final state gen anti-neutrinos #theta",      "bin":64, "xmin":0,"xmax":3.2},
    "FSGenAntiNeutrino_phi":           {"name":"FSGenAntiNeutrino_phi",          "title":"Final state gen anti-neutrinos #phi",        "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenPhoton_e":                   {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_p":                   {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pt":                  {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pz":                  {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_eta":                 {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",               "bin":60, "xmin":-3,"xmax":3},
    "FSGenPhoton_theta":               {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",             "bin":64, "xmin":0,"xmax":3.2},
    "FSGenPhoton_phi":                 {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},

    # "FSGenPhoton0_e":                 {"name":"FSGenPhoton0_e",                "title":"Final state gen photon_{0} energy [GeV]",               "bin":64, "xmin":-3.2,"xmax":3.2},
    # "FSGenPhoton1_e":                 {"name":"FSGenPhoton1_e",                "title":"Final state gen photon_{1} energy [GeV]",               "bin":64, "xmin":-3.2,"xmax":3.2},
    # "FSGenPhoton2_e":                 {"name":"FSGenPhoton2_e",                "title":"Final state gen photon_{2} energy [GeV]",               "bin":64, "xmin":-3.2,"xmax":3.2},
    # "FSGenPhoton0_p":                   {"name":"FSGenPhoton0_p",                  "title":"Final state gen photon_{0} p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenPhoton1_p":                   {"name":"FSGenPhoton1_p",                  "title":"Final state gen photon_{1} p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenPhoton2_p":                   {"name":"FSGenPhoton2_p",                  "title":"Final state gen photon_{2} p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenPhoton0_pt":                  {"name":"FSGenPhoton0_pt",                 "title":"Final state gen photon_{0} p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenPhoton1_pt":                  {"name":"FSGenPhoton1_pt",                 "title":"Final state gen photon_{1} p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    # "FSGenPhoton2_pt":                  {"name":"FSGenPhoton2_pt",                 "title":"Final state gen photon_{2} p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},

    "FSGenPhoton_vertex_x": {"name":"FSGenPhoton_vertex_x", "title":"Final state gen photon production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenPhoton_vertex_y": {"name":"FSGenPhoton_vertex_y", "title":"Final state gen photon production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenPhoton_vertex_z": {"name":"FSGenPhoton_vertex_z", "title":"Final state gen photon production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "FSGen_lifetime_xy": {"name":"FSGen_lifetime_xy", "title":"Gen ALP (FS eles) #tau_{xy} [s]",        "bin":100,"xmin":0 ,"xmax":1E-10},
    "FSGen_lifetime_xyz": {"name":"FSGen_lifetime_xyz", "title":"Gen ALP (FS eles) #tau_{xyz} [s]",        "bin":100,"xmin":0 ,"xmax":1E-10},
    "FSGen_Lxy":      {"name":"FSGen_Lxy",      "title":"Gen ALP (FS eles) L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "FSGen_Lxyz":     {"name":"FSGen_Lxyz",     "title":"Gen ALP (FS eles) L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},

    # "FSGen_a0a1_invMass":   {"name":"FSGen_a0a1_invMass",   "title":"Gen FS photons m_{01} [GeV]",           "bin":105,"xmin":-5, "xmax":100},
    # "FSGen_a0a2_invMass":   {"name":"FSGen_a0a2_invMass",   "title":"Gen FS photons m_{02} [GeV]",           "bin":105,"xmin":-5, "xmax":100},
    # "FSGen_a1a2_invMass":   {"name":"FSGen_a1a2_invMass",   "title":"Gen FS photons m_{12} [GeV]",           "bin":105,"xmin":-5, "xmax":100},
    # "FSGen_aaa_invMass":   {"name":"FSGen_aaa_invMass",   "title":"Gen FS m_{#gamma #gamma #gamma} [GeV]",           "bin":105,"xmin":-5, "xmax":100},

    "GenALP_mass":     {"name":"GenALP_mass",     "title":"Gen ALP mass [GeV]",      "bin":100,"xmin":0 ,"xmax":10},
    "GenALP_p":        {"name":"GenALP_p",        "title":"Gen ALP p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "GenALP_pt":       {"name":"GenALP_pt",       "title":"Gen ALP p_{T} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenALP_pz":       {"name":"GenALP_pz",       "title":"Gen ALP p_{z} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenALP_eta":      {"name":"GenALP_eta",      "title":"Gen ALP #eta",            "bin":60, "xmin":-3,"xmax":3},
    "GenALP_theta":    {"name":"GenALP_theta",    "title":"Gen ALP #theta",          "bin":64, "xmin":0,"xmax":3.2},
    "GenALP_phi":      {"name":"GenALP_phi",      "title":"Gen ALP #phi",            "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenALP_lifetime_xy": {"name":"GenALP_lifetime_xy", "title":"Gen ALP #tau_{xy} [s]",        "bin":100,"xmin":0 ,"xmax":1E-10},
    "GenALP_lifetime_xyz": {"name":"GenALP_lifetime_xyz", "title":"Gen ALP #tau_{xyz} [s]",        "bin":100,"xmin":0 ,"xmax":1E-10},
    "GenALP_Lxy":      {"name":"GenALP_Lxy",      "title":"Gen ALP L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "GenALP_Lxyz":     {"name":"GenALP_Lxyz",     "title":"Gen ALP L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    "GenALP_vertex_x": {"name":"GenALP_vertex_x", "title":"Gen ALP production vertex x [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenALP_vertex_y": {"name":"GenALP_vertex_y", "title":"Gen ALP production vertex y [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenALP_vertex_z": {"name":"GenALP_vertex_z", "title":"Gen ALP production vertex z [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},

    "GenALPPhoton1_e":        {"name":"GenALPPhoton1_e",        "title":"Gen photon_{1} energy [GeV]",                  "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton2_e":        {"name":"GenALPPhoton2_e",        "title":"Gen photon_{2} energy [GeV]",                                "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton1_p":        {"name":"GenALPPhoton1_p",        "title":"Gen photon_{1} p [GeV]",                       "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton2_p":        {"name":"GenALPPhoton2_p",        "title":"Gen photon_{2} p [GeV]",                                     "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton1_pt":       {"name":"GenALPPhoton1_pt",       "title":"Gen photon_{1} p_{T} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton2_pt":       {"name":"GenALPPhoton2_pt",       "title":"Gen photon_{2} p_{T} [GeV]",                                 "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton1_pz":       {"name":"GenALPPhoton1_pz",       "title":"Gen photon_{1} p_{z} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton2_pz":       {"name":"GenALPPhoton2_pz",       "title":"Gen photon_{2} p_{z} [GeV]",                                 "bin":100,"xmin":0 ,"xmax":50},
    "GenALPPhoton1_eta":      {"name":"GenALPPhoton1_eta",      "title":"Gen photon_{1} #eta",                          "bin":60, "xmin":-3,"xmax":3},
    "GenALPPhoton2_eta":      {"name":"GenALPPhoton2_eta",      "title":"Gen photon_{2} #eta",                                        "bin":60, "xmin":-3,"xmax":3},
    "GenALPPhoton1_theta":    {"name":"GenALPPhoton1_theta",    "title":"Gen photon_{1} #theta",                        "bin":64, "xmin":0,"xmax":3.2},
    "GenALPPhoton2_theta":    {"name":"GenALPPhoton2_theta",    "title":"Gen photon_{2} #theta",                                      "bin":64, "xmin":0,"xmax":3.2},
    "GenALPPhoton1_phi":      {"name":"GenALPPhoton1_phi",      "title":"Gen photon_{1} #phi",                          "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenALPPhoton2_phi":      {"name":"GenALPPhoton2_phi",      "title":"Gen photon_{2} #phi",                                        "bin":64, "xmin":-3.2,"xmax":3.2},

    "GenALPPhoton1_vertex_x": {"name":"GenALPPhoton1_vertex_x", "title":"Gen photon_{1} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenALPPhoton1_vertex_y": {"name":"GenALPPhoton1_vertex_y", "title":"Gen photon_{1} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenALPPhoton1_vertex_z": {"name":"GenALPPhoton1_vertex_z", "title":"Gen photon_{1} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "GenALP_aa_invMass":   {"name":"GenALP_aa_invMass",   "title":"Gen m_{#gamma #gamma} (from ALP) [GeV]",           "bin":100,"xmin":0, "xmax":10},

    #reco variables
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",           "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoALPTracks":                 {"name":"n_RecoALPTracks",                "title":"Number of reco ALP tracks",             "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "RecoALP_DecayVertex_x":           {"name":"RecoALPDecayVertex.position.x",  "title":"Reco ALP decay vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoALP_DecayVertex_y":           {"name":"RecoALPDecayVertex.position.y",  "title":"Reco ALP decay vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoALP_DecayVertex_z":           {"name":"RecoALPDecayVertex.position.z",  "title":"Reco ALP decay vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoALP_DecayVertex_chi2":        {"name":"RecoALPDecayVertex.chi2",        "title":"Reco ALP decay vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "RecoALP_DecayVertex_probability": {"name":"RecoALPDecayVertex.probability", "title":"Reco ALP decay vertex probability",       "bin":100,"xmin":0 ,"xmax":10},

    "RecoALPPhoton1_e":        {"name":"RecoALPPhoton1_e",        "title":"Reco photon_{1} (from ALP) energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton2_e":        {"name":"RecoALPPhoton2_e",        "title":"Reco photon_{2} (from ALP) energy [GeV]",               "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton1_p":        {"name":"RecoALPPhoton1_p",        "title":"Reco photon_{1} (from ALP) p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton2_p":        {"name":"RecoALPPhoton2_p",        "title":"Reco photon_{2} (from ALP) p [GeV]",                    "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton1_pt":       {"name":"RecoALPPhoton1_pt",       "title":"Reco photon_{1} (from ALP) p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton2_pt":       {"name":"RecoALPPhoton2_pt",       "title":"Reco photon_{2} (from ALP) p_{T} [GeV]",                "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton1_pz":       {"name":"RecoALPPhoton1_pz",       "title":"Reco photon_{1} (from ALP) p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton2_pz":       {"name":"RecoALPPhoton2_pz",       "title":"Reco photon_{2} (from ALP) p_{z} [GeV]",                "bin":100,"xmin":0 ,"xmax":50},
    "RecoALPPhoton1_eta":      {"name":"RecoALPPhoton1_eta",      "title":"Reco photon_{1} (from ALP) #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoALPPhoton2_eta":      {"name":"RecoALPPhoton2_eta",      "title":"Reco photon_{2} (from ALP) #eta",                       "bin":60, "xmin":-3,"xmax":3},
    "RecoALPPhoton1_theta":    {"name":"RecoALPPhoton1_theta",    "title":"Reco photon_{1} (from ALP) #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoALPPhoton2_theta":    {"name":"RecoALPPhoton2_theta",    "title":"Reco photon_{2} (from ALP) #theta",                     "bin":64, "xmin":0,"xmax":3.2},
    "RecoALPPhoton1_phi":      {"name":"RecoALPPhoton1_phi",      "title":"Reco photon_{1} (from ALP) #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoALPPhoton2_phi":      {"name":"RecoALPPhoton2_phi",      "title":"Reco photon_{2} (from ALP) #phi",                       "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoALPPhoton1_charge":   {"name":"RecoALPPhoton1_charge",   "title":"Reco photon_{1} (from ALP) charge",       "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoALPPhoton2_charge":   {"name":"RecoALPPhoton2_charge",   "title":"Reco photon_{2} (from ALP) charge",                     "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoALP_aa_invMass":   {"name":"RecoALP_aa_invMass",   "title":"Reco m_{#gamma #gamma} (from ALP) [GeV]",           "bin":100,"xmin":0, "xmax":100},

    "n_RecoJets":       {"name":"n_RecoJets",      "title":"Total number of reco jets",         "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoPhotons":    {"name":"n_RecoPhotons",   "title":"Total number of reco photons",      "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoElectrons":  {"name":"n_RecoElectrons", "title":"Total number of reco electrons",    "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoMuons":      {"name":"n_RecoMuons",     "title":"Total number of reco muons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "RecoJet_e":        {"name":"RecoJet_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_p":        {"name":"RecoJet_p",        "title":"Reco jet p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_pt":       {"name":"RecoJet_pt",       "title":"Reco jet p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_pz":       {"name":"RecoJet_pz",       "title":"Reco jet p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoJet_eta":      {"name":"RecoJet_eta",      "title":"Reco jet #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoJet_theta":    {"name":"RecoJet_theta",    "title":"Reco jet #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoJet_phi":      {"name":"RecoJet_phi",      "title":"Reco jet #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoJet_charge":   {"name":"RecoJet_charge",   "title":"Reco jet charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoElectron_e":        {"name":"RecoElectron_e",        "title":"Reco electron energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_p":        {"name":"RecoElectron_p",        "title":"Reco electron p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pz":       {"name":"RecoElectron_pz",       "title":"Reco electron p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_theta":    {"name":"RecoElectron_theta",    "title":"Reco electron #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoPhoton_e":        {"name":"RecoPhoton_e",        "title":"Reco photon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_p":        {"name":"RecoPhoton_p",        "title":"Reco photon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_pt":       {"name":"RecoPhoton_pt",       "title":"Reco photon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_pz":       {"name":"RecoPhoton_pz",       "title":"Reco photon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoPhoton_eta":      {"name":"RecoPhoton_eta",      "title":"Reco photon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoPhoton_theta":    {"name":"RecoPhoton_theta",    "title":"Reco photon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoPhoton_phi":      {"name":"RecoPhoton_phi",      "title":"Reco photon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":   {"name":"RecoPhoton_charge",   "title":"Reco photon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuon_e":        {"name":"RecoMuon_e",        "title":"Reco muon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_p":        {"name":"RecoMuon_p",        "title":"Reco muon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pt":       {"name":"RecoMuon_pt",       "title":"Reco muon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pz":       {"name":"RecoMuon_pz",       "title":"Reco muon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_eta":      {"name":"RecoMuon_eta",      "title":"Reco muon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoMuon_theta":    {"name":"RecoMuon_theta",    "title":"Reco muon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":      {"name":"RecoMuon_phi",      "title":"Reco muon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":   {"name":"RecoMuon_charge",   "title":"Reco muon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMissingEnergy_e":       {"name":"RecoMissingEnergy_e",       "title":"Reco Total Missing Energy [GeV]",    "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_p":       {"name":"RecoMissingEnergy_p",       "title":"Reco Total Missing p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pt":      {"name":"RecoMissingEnergy_pt",      "title":"Reco Missing p_{T} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_px":      {"name":"RecoMissingEnergy_px",      "title":"Reco Missing p_{x} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_py":      {"name":"RecoMissingEnergy_py",      "title":"Reco Missing p_{y} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pz":      {"name":"RecoMissingEnergy_pz",      "title":"Reco Missing p_{z} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_eta":     {"name":"RecoMissingEnergy_eta",     "title":"Reco Missing Energy #eta",           "bin":60,"xmin":-3 ,"xmax":3},
    "RecoMissingEnergy_theta":   {"name":"RecoMissingEnergy_theta",   "title":"Reco Missing Energy #theta",         "bin":64,"xmin":0 , "xmax":3.2},
    "RecoMissingEnergy_phi":     {"name":"RecoMissingEnergy_phi",     "title":"Reco Missing Energy #phi",           "bin":64,"xmin":-3.2 ,"xmax":3.2},

    #gen-reco
    "GenMinusRecoALPPhoton1_e":    {"name":"GenMinusRecoALPPhoton1_e",    "title":"Gen photon_{1} energy - Reco photon_{1} energy [GeV]","bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_e":    {"name":"GenMinusRecoALPPhoton2_e",    "title":"Gen photon_{2} energy - Reco photon_{2} energy [GeV]",                            "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton1_p":    {"name":"GenMinusRecoALPPhoton1_p",    "title":"Gen photon_{1} p - Reco photon_{1} p [GeV]",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_p":    {"name":"GenMinusRecoALPPhoton2_p",    "title":"Gen photon_{2} p - Reco photon_{2} p [GeV]",                                      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton1_pt":   {"name":"GenMinusRecoALPPhoton1_pt",   "title":"Gen photon_{1} p_{T} - Reco photon_{1} p_{T} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_pt":   {"name":"GenMinusRecoALPPhoton2_pt",   "title":"Gen photon_{2} p_{T} - Reco photon_{2} p_{T} [GeV]",                              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton1_pz":   {"name":"GenMinusRecoALPPhoton1_pz",   "title":"Gen photon_{1} p_{z} - Reco photon_{1} p_{z} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_pz":   {"name":"GenMinusRecoALPPhoton2_pz",   "title":"Gen photon_{2} p_{z} - Reco photon_{2} p_{z} [GeV]",                              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton1_eta":  {"name":"GenMinusRecoALPPhoton1_eta",  "title":"Gen photon_{1} #eta - Reco photon_{1} #eta",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_eta":  {"name":"GenMinusRecoALPPhoton2_eta",  "title":"Gen photon_{2} #eta - Reco photon_{2} #eta",                                      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton1_theta":{"name":"GenMinusRecoALPPhoton1_theta","title":"Gen photon_{1} #theta - Reco photon_{1} #theta",      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_theta":{"name":"GenMinusRecoALPPhoton2_theta","title":"Gen photon_{2} #theta - Reco photon_{2} #theta",                                  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton1_phi":  {"name":"GenMinusRecoALPPhoton1_phi",  "title":"Gen photon_{1} #phi - Reco photon_{1} #phi",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALPPhoton2_phi":  {"name":"GenMinusRecoALPPhoton2_phi",  "title":"Gen photon_{2} #phi - Reco photon_{2} #phi",                                      "bin":100,"xmin":-5 ,"xmax":5},

    "GenMinusRecoALP_DecayVertex_x":  {"name":"GenMinusRecoALP_DecayVertex_x",  "title":"Gen ALP decay vertex x - Reco ALP decay vertex x [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALP_DecayVertex_y":  {"name":"GenMinusRecoALP_DecayVertex_y",  "title":"Gen ALP decay vertex y - Reco ALP decay vertex y [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoALP_DecayVertex_z":  {"name":"GenMinusRecoALP_DecayVertex_z",  "title":"Gen ALP decay vertex z - Reco ALP decay vertex z [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
}

###Number of CPUs to use
NUM_CPUS = 2

###Produce TTrees
DO_TREE=False

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS, doTree=DO_TREE)

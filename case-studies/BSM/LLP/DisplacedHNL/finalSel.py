import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "read_EDM4HEP/"

###Integrated luminosity for scaling number of events
intLumi = 150e6 #pb^-1

###Link to the dictonary that contains all the cross section informations etc...
procDict = "myFCCee_procDict_spring2021_IDEA.json"
process_list=[
    #'HNL_eenu_40GeV_1e-3Ve',
    #'HNL_eenu_40GeV_1e-4Ve',
    #'HNL_eenu_40GeV_1e-5Ve',
    #'HNL_eenu_5GeV_1p41e-6Ve',
    #'HNL_eenu_10GeV_1p41e-6Ve',
    #'HNL_eenu_12GeV_1p41e-6Ve',
    #'HNL_eenu_15GeV_1p41e-6Ve',
    #'HNL_eenu_20GeV_1p41e-6Ve',
    #'HNL_eenu_30GeV_1p41e-6Ve',
    #'HNL_eenu_40GeV_1p41e-6Ve',
    #'HNL_eenu_50GeV_1p41e-6Ve',
    #'HNL_eenu_70GeV_1p41e-6Ve',
    #'HNL_eenu_90GeV_1p41e-6Ve',

    #'HNL_eenu_20GeV_0p1Ve',
    #'HNL_eenu_10GeV_0p1Ve',

    'HNL_eenu_20GeV_0p1Ve_withBothAntiNu',
    'HNL_eenu_20GeV_0p1Ve_withBothAntiNu_localDelphes',
    'HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu',
    'HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu_localDelphes',
]

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file

# cut_list = {
#     #"sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100"
#     "selNone": "n_RecoTracks > -1",
#     "sel0": "GenHNL_mass.size() > 0",
#     "sel1": "GenHNL_mass.size() > 0 && n_RecoElectrons > 1",
#     "selGenLxyzGt500": "GenHNL_mass.size() > 0 && GenHNL_Lxyz[0]>500", #>500 mm
# }
cut_list = {
    #"sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100"
    "selNone": "n_RecoTracks > -1",
    "sel1FSGenEle": "n_FSGenElectron>0",
    "sel1FSGenNu": "n_FSGenNeutrino>0",
    "sel2RecoEle": "n_RecoElectrons==2",
    "sel2RecoEle_vetoes": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0",
    "sel2RecoEle_absD0Gt0p1": "n_RecoElectrons==2 && RecoElectronTrack_absD0[0]>0.1 && RecoElectronTrack_absD0[1]>0.1", #both electrons displaced
    "sel2RecoEle_chi2Gt0p1": "n_RecoElectrons==2 && RecoHNLDecayVertex.chi2>0.1", #displaced vertex
    "sel2RecoEle_chi2Gt0p1_LxyzGt1": "n_RecoElectrons==2 && RecoHNLDecayVertex.chi2>0.1 && RecoHNL_Lxyz>1", #displaced vertex
    "sel2RecoEle_vetoes_MissingEnergyGt10": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoMissingEnergy_p[0]>10", #missing energy > 10 GeV
    "sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoMissingEnergy_p[0]>10 && RecoElectronTrack_absD0[0]>0.5 && RecoElectronTrack_absD0[1]>0.5", #both electrons displaced
    "sel2RecoEle_vetoes_MissingEnergyGt10_chi2Gt1_LxyzGt5": "n_RecoElectrons==2 && n_RecoMuons==0 && n_RecoPhotons==0 && n_RecoJets==0 && n_RecoPhotons==0 && RecoMissingEnergy_p[0]>10 && RecoHNLDecayVertex.chi2>1 && RecoHNL_Lxyz>5", #displaced vertex
}


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.

variables = {

    #gen variables
    "All_n_GenHNL":                    {"name":"All_n_GenHNL",                   "title":"Total number of gen HNLs",                   "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "AllGenHNL_mass":                  {"name":"AllGenHNL_mass",                 "title":"All gen N mass [GeV]",                       "bin":100,"xmin":0 ,"xmax":100},
    "AllGenHNL_e":                     {"name":"AllGenHNL_e",                    "title":"All gen N energy [GeV]",                     "bin":100,"xmin":0 ,"xmax":100},
    "AllGenHNL_p":                     {"name":"AllGenHNL_p",                    "title":"All gen N p [GeV]",                          "bin":100,"xmin":0 ,"xmax":50},
    "AllGenHNL_pt":                    {"name":"AllGenHNL_pt",                   "title":"All gen N p_{T} [GeV]",                      "bin":100,"xmin":0 ,"xmax":50},
    "AllGenHNL_pz":                    {"name":"AllGenHNL_pz",                   "title":"All gen N p_{z} [GeV]",                      "bin":100,"xmin":0 ,"xmax":50},
    "AllGenHNL_eta":                   {"name":"AllGenHNL_eta",                  "title":"All gen N #eta",                             "bin":60, "xmin":-3,"xmax":3},
    "AllGenHNL_theta":                 {"name":"AllGenHNL_theta",                "title":"All gen N #theta",                           "bin":64, "xmin":0,"xmax":3.2},
    "AllGenHNL_phi":                   {"name":"AllGenHNL_phi",                  "title":"All gen N #phi",                             "bin":64, "xmin":-3.2,"xmax":3.2},

    "n_FSGenElectron":                 {"name":"n_FSGenElectron",                "title":"Number of final state gen electrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenNeutrino":                 {"name":"n_FSGenNeutrino",                "title":"Number of final state gen neutrinos",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_FSGenPhoton":                   {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",          "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "FSGenElectron_e":                 {"name":"FSGenElectron_e",                "title":"Final state gen electrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_p":                 {"name":"FSGenElectron_p",                "title":"Final state gen electrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pt":                {"name":"FSGenElectron_pt",               "title":"Final state gen electrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_pz":                {"name":"FSGenElectron_pz",               "title":"Final state gen electrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenElectron_eta":               {"name":"FSGenElectron_eta",              "title":"Final state gen electrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenElectron_theta":             {"name":"FSGenElectron_theta",            "title":"Final state gen electrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":               {"name":"FSGenElectron_phi",              "title":"Final state gen electrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenNeutrino_e":                 {"name":"FSGenNeutrino_e",                "title":"Final state gen neutrino energy [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_p":                 {"name":"FSGenNeutrino_p",                "title":"Final state gen neutrino p [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pt":                {"name":"FSGenNeutrino_pt",               "title":"Final state gen neutrino p_{T} [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_pz":                {"name":"FSGenNeutrino_pz",               "title":"Final state gen neutrino p_{z} [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenNeutrino_eta":               {"name":"FSGenNeutrino_eta",              "title":"Final state gen neutrinos #eta",             "bin":60, "xmin":-3,"xmax":3},
    "FSGenNeutrino_theta":             {"name":"FSGenNeutrino_theta",            "title":"Final state gen neutrinos #theta",           "bin":64, "xmin":0,"xmax":3.2},
    "FSGenNeutrino_phi":               {"name":"FSGenNeutrino_phi",              "title":"Final state gen neutrinos #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenPhoton_e":                   {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_p":                   {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pt":                  {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_pz":                  {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    "FSGenPhoton_eta":                 {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",               "bin":60, "xmin":-3,"xmax":3},
    "FSGenPhoton_theta":               {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",             "bin":64, "xmin":0,"xmax":3.2},
    "FSGenPhoton_phi":                 {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},

    "FSGenElectron_vertex_x": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenElectron_vertex_y": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "FSGenElectron_vertex_z": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "FSGenElectron_vertex_x_prompt": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "FSGenElectron_vertex_y_prompt": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "FSGenElectron_vertex_z_prompt": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},

    "FSGen_lifetime_xy": {"name":"FSGen_lifetime_xy", "title":"Gen HNL (FS eles) #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-9},
    "FSGen_lifetime_xyz": {"name":"FSGen_lifetime_xyz", "title":"Gen HNL (FS eles) #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-9},
    "FSGen_lifetime_xyz_prompt": {"name":"FSGen_lifetime_xyz", "title":"Gen HNL (FS eles) #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-15},
    "FSGen_Lxy":      {"name":"FSGen_Lxy",      "title":"Gen HNL (FS eles) L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "FSGen_Lxyz":     {"name":"FSGen_Lxyz",     "title":"Gen HNL (FS eles) L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    "FSGen_Lxyz_prompt":     {"name":"FSGen_Lxyz",     "title":"Gen HNL (FS eles) L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":0.1},

    "FSGen_ee_invMass":   {"name":"FSGen_ee_invMass",   "title":"Gen FS m_{ee} [GeV]",           "bin":100,"xmin":0, "xmax":100},
    "FSGen_eenu_invMass": {"name":"FSGen_eenu_invMass", "title":"Gen FS m_{ee#nu} [GeV]",        "bin":100,"xmin":0, "xmax":100},

    "GenHNL_mass":     {"name":"GenHNL_mass",     "title":"Gen N mass [GeV]",      "bin":100,"xmin":0 ,"xmax":100},
    "GenHNL_p":        {"name":"GenHNL_p",        "title":"Gen N p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_pt":       {"name":"GenHNL_pt",       "title":"Gen N p_{T} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_pz":       {"name":"GenHNL_pz",       "title":"Gen N p_{z} [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    "GenHNL_eta":      {"name":"GenHNL_eta",      "title":"Gen N #eta",            "bin":60, "xmin":-3,"xmax":3},
    "GenHNL_theta":    {"name":"GenHNL_theta",    "title":"Gen N #theta",          "bin":64, "xmin":0,"xmax":3.2},
    "GenHNL_phi":      {"name":"GenHNL_phi",      "title":"Gen N #phi",            "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNL_lifetime_xy": {"name":"GenHNL_lifetime_xy", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-9},
    "GenHNL_lifetime_xyz": {"name":"GenHNL_lifetime_xyz", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-9},
    "GenHNL_lifetime_xyz_prompt": {"name":"GenHNL_lifetime_xyz", "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":10E-15},
    "GenHNL_Lxy":      {"name":"GenHNL_Lxy",      "title":"Gen N L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "GenHNL_Lxyz":     {"name":"GenHNL_Lxyz",     "title":"Gen N L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    "GenHNL_Lxyz_prompt":     {"name":"GenHNL_Lxyz",     "title":"Gen N L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":0.1},

    "GenHNL_vertex_x": {"name":"GenHNL_vertex_x", "title":"Gen N production vertex x [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNL_vertex_y": {"name":"GenHNL_vertex_y", "title":"Gen N production vertex y [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNL_vertex_z": {"name":"GenHNL_vertex_z", "title":"Gen N production vertex z [mm]",   "bin":100,"xmin":-1000 ,"xmax":1000},

    "GenHNLElectron_e":        {"name":"GenHNLElectron_e",        "title":"Gen e^{#font[122]{\55}}_{1} energy [GeV]",                  "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron2_e":       {"name":"GenHNLElectron2_e",       "title":"Gen e^{#font[122]{\55}}_{2} energy [GeV]",                  "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_e":        {"name":"GenHNLNeutrino_e",        "title":"Gen #nu energy [GeV]",                                      "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_p":        {"name":"GenHNLElectron_p",        "title":"Gen e^{#font[122]{\55}}_{1} p [GeV]",                       "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron2_p":       {"name":"GenHNLElectron2_p",       "title":"Gen e^{#font[122]{\55}}_{2} p [GeV]",                       "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_p":        {"name":"GenHNLNeutrino_p",        "title":"Gen #nu p [GeV]",                                           "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_pt":       {"name":"GenHNLElectron_pt",       "title":"Gen e^{#font[122]{\55}}_{1} p_{T} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron2_pt":      {"name":"GenHNLElectron2_pt",      "title":"Gen e^{#font[122]{\55}}_{2} p_{T} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_pt":       {"name":"GenHNLNeutrino_pt",       "title":"Gen #nu p_{T} [GeV]",                                       "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_pz":       {"name":"GenHNLElectron_pz",       "title":"Gen e^{#font[122]{\55}}_{1} p_{z} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron2_pz":      {"name":"GenHNLElectron2_pz",      "title":"Gen e^{#font[122]{\55}}_{2} p_{z} [GeV]",                   "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLNeutrino_pz":       {"name":"GenHNLNeutrino_pz",       "title":"Gen #nu p_{z} [GeV]",                                       "bin":100,"xmin":0 ,"xmax":50},
    "GenHNLElectron_eta":      {"name":"GenHNLElectron_eta",      "title":"Gen e^{#font[122]{\55}}_{1} #eta",                          "bin":60, "xmin":-3,"xmax":3},
    "GenHNLElectron2_eta":     {"name":"GenHNLElectron2_eta",     "title":"Gen e^{#font[122]{\55}}_{2} #eta",                          "bin":60, "xmin":-3,"xmax":3},
    "GenHNLNeutrino_eta":      {"name":"GenHNLNeutrino_eta",      "title":"Gen #nu #eta",                                              "bin":60, "xmin":-3,"xmax":3},
    "GenHNLElectron_theta":    {"name":"GenHNLElectron_theta",    "title":"Gen e^{#font[122]{\55}}_{1} #theta",                        "bin":64, "xmin":0,"xmax":3.2},
    "GenHNLElectron2_theta":   {"name":"GenHNLElectron2_theta",   "title":"Gen e^{#font[122]{\55}}_{2} #theta",                        "bin":64, "xmin":0,"xmax":3.2},
    "GenHNLNeutrino_theta":    {"name":"GenHNLNeutrino_theta",    "title":"Gen #nu #theta",                                            "bin":64, "xmin":0,"xmax":3.2},
    "GenHNLElectron_phi":      {"name":"GenHNLElectron_phi",      "title":"Gen e^{#font[122]{\55}}_{1} #phi",                          "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNLElectron2_phi":     {"name":"GenHNLElectron2_phi",     "title":"Gen e^{#font[122]{\55}}_{2} #phi",                          "bin":64, "xmin":-3.2,"xmax":3.2},
    "GenHNLNeutrino_phi":      {"name":"GenHNLNeutrino_phi",      "title":"Gen #nu #phi",                                              "bin":64, "xmin":-3.2,"xmax":3.2},

    "GenHNLElectron_vertex_x": {"name":"GenHNLElectron_vertex_x", "title":"Gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNLElectron_vertex_y": {"name":"GenHNLElectron_vertex_y", "title":"Gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    "GenHNLElectron_vertex_z": {"name":"GenHNLElectron_vertex_z", "title":"Gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    "GenHNLElectron_vertex_x_prompt": {"name":"GenHNLElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "GenHNLElectron_vertex_y_prompt": {"name":"GenHNLElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "GenHNLElectron_vertex_z_prompt": {"name":"GenHNLElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},

    "GenHNL_ee_invMass":   {"name":"GenHNL_ee_invMass",   "title":"Gen m_{ee} [GeV]",           "bin":100,"xmin":0, "xmax":100},
    "GenHNL_eenu_invMass": {"name":"GenHNL_eenu_invMass", "title":"Gen m_{ee#nu} [GeV]",        "bin":100,"xmin":0, "xmax":100},

    #reco variables
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",           "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoHNLTracks":                 {"name":"n_RecoHNLTracks",                "title":"Number of reco HNL tracks",             "bin":5,"xmin":-0.5 ,"xmax":4.5},

    "RecoHNLTracks_absD0":             {"name":"RecoHNLTracks_absD0",     "title":"Reco HNL tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoHNLTracks_absD0_prompt":      {"name":"RecoHNLTracks_absD0",     "title":"Reco HNL tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoHNLTracks_absZ0":             {"name":"RecoHNLTracks_absZ0",     "title":"Reco HNL tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoHNLTracks_absZ0_prompt":      {"name":"RecoHNLTracks_absZ0",     "title":"Reco HNL tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoHNLTracks_absD0sig":          {"name":"RecoHNLTracks_absD0sig",  "title":"Reco HNL tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoHNLTracks_absD0sig_prompt":   {"name":"RecoHNLTracks_absD0sig",  "title":"Reco HNL tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoHNLTracks_absZ0sig":          {"name":"RecoHNLTracks_absZ0sig",  "title":"Reco HNL tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoHNLTracks_absZ0sig_prompt":   {"name":"RecoHNLTracks_absZ0sig",  "title":"Reco HNL tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoHNLTracks_D0cov":      {"name":"RecoHNLTracks_D0cov",     "title":"Reco HNL tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoHNLTracks_Z0cov":      {"name":"RecoHNLTracks_Z0cov",     "title":"Reco HNL tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "RecoHNL_DecayVertex_x":           {"name":"RecoHNLDecayVertex.position.x",  "title":"Reco N decay vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_y":           {"name":"RecoHNLDecayVertex.position.y",  "title":"Reco N decay vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_z":           {"name":"RecoHNLDecayVertex.position.z",  "title":"Reco N decay vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "RecoHNL_DecayVertex_x_prompt":    {"name":"RecoHNLDecayVertex.position.x",  "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "RecoHNL_DecayVertex_y_prompt":    {"name":"RecoHNLDecayVertex.position.y",  "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "RecoHNL_DecayVertex_z_prompt":    {"name":"RecoHNLDecayVertex.position.z",  "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    "RecoHNL_DecayVertex_chi2":        {"name":"RecoHNLDecayVertex.chi2",        "title":"Reco N decay vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "RecoHNL_DecayVertex_probability": {"name":"RecoHNLDecayVertex.probability", "title":"Reco N decay vertex probability",       "bin":100,"xmin":0 ,"xmax":10},
    "RecoHNL_Lxy":                     {"name":"RecoHNL_Lxy",                    "title":"Reco N L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":1000},
    "RecoHNL_Lxyz":                    {"name":"RecoHNL_Lxyz",                   "title":"Reco N L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":1000},
    "RecoHNL_Lxyz_prompt":             {"name":"RecoHNL_Lxyz",                   "title":"Reco N L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":0.1},

    "RecoHNLElectron_e":        {"name":"RecoHNLElectron_e",        "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_p":        {"name":"RecoHNLElectron_p",        "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_pt":       {"name":"RecoHNLElectron_pt",       "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_pz":       {"name":"RecoHNLElectron_pz",       "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron_eta":      {"name":"RecoHNLElectron_eta",      "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoHNLElectron_theta":    {"name":"RecoHNLElectron_theta",    "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoHNLElectron_phi":      {"name":"RecoHNLElectron_phi",      "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoHNLElectron_charge":   {"name":"RecoHNLElectron_charge",   "title":"Reco e^{#font[122]{\55}}_{1} (from HNL) charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoHNLElectron2_e":        {"name":"RecoHNLElectron2_e",        "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron2_p":        {"name":"RecoHNLElectron2_p",        "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron2_pt":       {"name":"RecoHNLElectron2_pt",       "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron2_pz":       {"name":"RecoHNLElectron2_pz",       "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoHNLElectron2_eta":      {"name":"RecoHNLElectron2_eta",      "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoHNLElectron2_theta":    {"name":"RecoHNLElectron2_theta",    "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoHNLElectron2_phi":      {"name":"RecoHNLElectron2_phi",      "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoHNLElectron2_charge":   {"name":"RecoHNLElectron2_charge",   "title":"Reco e^{#font[122]{\55}}_{2} (from HNL) charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoHNL_ee_invMass":   {"name":"RecoHNL_ee_invMass",   "title":"Reco m_{ee} [GeV]",           "bin":100,"xmin":0, "xmax":100},

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

    "RecoJetTrack_absD0":             {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoJetTrack_absD0_prompt":      {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoJetTrack_absZ0":             {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoJetTrack_absZ0_prompt":      {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoJetTrack_absD0sig":          {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoJetTrack_absD0sig_prompt":   {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoJetTrack_absZ0sig":          {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoJetTrack_absZ0sig_prompt":   {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoJetTrack_D0cov":      {"name":"RecoJetTrack_D0cov",     "title":"Reco jet tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoJetTrack_Z0cov":      {"name":"RecoJetTrack_Z0cov",     "title":"Reco jet tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "RecoElectron_e":        {"name":"RecoElectron_e",        "title":"Reco electron energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_p":        {"name":"RecoElectron_p",        "title":"Reco electron p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pz":       {"name":"RecoElectron_pz",       "title":"Reco electron p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_theta":    {"name":"RecoElectron_theta",    "title":"Reco electron #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoElectronTrack_absD0":             {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absD0_prompt":      {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoElectronTrack_absZ0":             {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absZ0_prompt":      {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoElectronTrack_absD0sig":          {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absD0sig_prompt":   {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoElectronTrack_absZ0sig":          {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absZ0sig_prompt":   {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoElectronTrack_D0cov":      {"name":"RecoElectronTrack_D0cov",     "title":"Reco electron tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoElectronTrack_Z0cov":      {"name":"RecoElectronTrack_Z0cov",     "title":"Reco electron tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

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

    "RecoMuonTrack_absD0":             {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absD0_prompt":      {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoMuonTrack_absZ0":             {"name":"RecoMuonTrack_absZ0",     "title":"Reco muon tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absZ0_prompt":      {"name":"RecoMuonTrack_absZ0",     "title":"Reco muon tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoMuonTrack_absD0sig":          {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absD0sig_prompt":   {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoMuonTrack_absZ0sig":          {"name":"RecoMuonTrack_absZ0sig",  "title":"Reco muon tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absZ0sig_prompt":   {"name":"RecoMuonTrack_absZ0sig",  "title":"Reco muon tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoMuonTrack_D0cov":      {"name":"RecoMuonTrack_D0cov",     "title":"Reco muon tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoMuonTrack_Z0cov":      {"name":"RecoMuonTrack_Z0cov",     "title":"Reco muon tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

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
    "GenMinusRecoHNLElectron_e":    {"name":"GenMinusRecoHNLElectron_e",    "title":"Gen e^{#font[122]{\55}} energy - Reco e^{#font[122]{\55}} energy [GeV]","bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_p":    {"name":"GenMinusRecoHNLElectron_p",    "title":"Gen e^{#font[122]{\55}} p - Reco e^{#font[122]{\55}} p [GeV]",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_pt":   {"name":"GenMinusRecoHNLElectron_pt",   "title":"Gen e^{#font[122]{\55}} p_{T} - Reco e^{#font[122]{\55}} p_{T} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_pz":   {"name":"GenMinusRecoHNLElectron_pz",   "title":"Gen e^{#font[122]{\55}} p_{z} - Reco e^{#font[122]{\55}} p_{z} [GeV]",  "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_eta":  {"name":"GenMinusRecoHNLElectron_eta",  "title":"Gen e^{#font[122]{\55}} #eta - Reco e^{#font[122]{\55}} #eta",          "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_theta":{"name":"GenMinusRecoHNLElectron_theta","title":"Gen e^{#font[122]{\55}} #theta - Reco e^{#font[122]{\55}} #theta",      "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNLElectron_phi":  {"name":"GenMinusRecoHNLElectron_phi",  "title":"Gen e^{#font[122]{\55}} #phi - Reco e^{#font[122]{\55}} #phi",          "bin":100,"xmin":-5 ,"xmax":5},

    "GenMinusRecoHNL_DecayVertex_x":  {"name":"GenMinusRecoHNL_DecayVertex_x",  "title":"Gen N decay vertex x - Reco N decay vertex x [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_DecayVertex_y":  {"name":"GenMinusRecoHNL_DecayVertex_y",  "title":"Gen N decay vertex y - Reco N decay vertex y [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_DecayVertex_z":  {"name":"GenMinusRecoHNL_DecayVertex_z",  "title":"Gen N decay vertex z - Reco N decay vertex z [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_Lxy":            {"name":"GenMinusRecoHNL_Lxy",   "title":"Gen N L_{xy} - Reco N L_{xy} [mm]",                "bin":100,"xmin":-5 ,"xmax":5},
    "GenMinusRecoHNL_Lxyz":           {"name":"GenMinusRecoHNL_Lxyz",  "title":"Gen N L_{xyz} - Reco N L_{xyz} [mm]",              "bin":100,"xmin":-10 ,"xmax":10},
    "GenMinusRecoHNL_Lxyz_prompt":    {"name":"GenMinusRecoHNL_Lxyz",  "title":"Gen N L_{xyz} - Reco N L_{xyz} [mm]",              "bin":100,"xmin":-5 ,"xmax":5},
}

###Number of CPUs to use
NUM_CPUS = 2

###Produce TTrees
DO_TREE=False
DO_SCALE=True

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables,intLumi)
myana.run(ncpu=NUM_CPUS, doTree=DO_TREE, doScale=DO_SCALE)

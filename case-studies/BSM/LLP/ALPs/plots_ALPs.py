import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
#scaleSig       = 
ana_tex        = 'e^{+}e^{-} #rightarrow Z #rightarrow #gamma ALP #rightarrow 3#gamma'
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = 'read_EDM4HEP/'
#formats        = ['png','pdf']
formats        = ['png']
yaxis          = ['lin','log']
#stacksig       = ['stack','nostack']
stacksig       = ['nostack']
outdir         = 'plots/'

variables = [

    #gen variables
    "All_n_GenALP",
    "AllGenALP_mass",
    "AllGenALP_e",
    "AllGenALP_p",
    "AllGenALP_pt",
    "AllGenALP_pz",
    "AllGenALP_eta",
    "AllGenALP_theta",
    "AllGenALP_phi",

    "n_FSGenElectron",
    "n_FSGenPositron",
    "n_FSGenNeutrino",
    "n_FSGenAntiNeutrino",
    "n_FSGenPhoton",
    # "n_FSGenElectron_forFS2GenPhotons",
    # "n_FSGenPositron_forFS2GenPhotons",

    "FSGenElectron_e",
    "FSGenElectron_p",
    "FSGenElectron_pt",
    "FSGenElectron_pz",
    "FSGenElectron_eta",
    "FSGenElectron_theta",
    "FSGenElectron_phi",

    "FSGenPositron_e",
    "FSGenPositron_p",
    "FSGenPositron_pt",
    "FSGenPositron_pz",
    "FSGenPositron_eta",
    "FSGenPositron_theta",
    "FSGenPositron_phi",

    "FSGenNeutrino_e",
    "FSGenNeutrino_p",
    "FSGenNeutrino_pt",
    "FSGenNeutrino_pz",
    "FSGenNeutrino_eta",
    "FSGenNeutrino_theta",
    "FSGenNeutrino_phi",

    "FSGenAntiNeutrino_e",
    "FSGenAntiNeutrino_p",
    "FSGenAntiNeutrino_pt",
    "FSGenAntiNeutrino_pz",
    "FSGenAntiNeutrino_eta",
    "FSGenAntiNeutrino_theta",
    "FSGenAntiNeutrino_phi",

    "FSGenPhoton_e",
    "FSGenPhoton_p",
    "FSGenPhoton_pt",
    "FSGenPhoton_pz",
    "FSGenPhoton_eta",
    "FSGenPhoton_theta",
    "FSGenPhoton_phi",

    "FSGenPhoton_vertex_x",
    "FSGenPhoton_vertex_y",
    "FSGenPhoton_vertex_z",

    "FSGen_Lxy",
    "FSGen_Lxyz",
    "FSGen_lifetime_xy",
    "FSGen_lifetime_xyz",

    # "FSGenPhoton0_e",
    # "FSGenPhoton1_e",
    # "FSGenPhoton2_e",
    # "FSGenPhoton0_p",
    # "FSGenPhoton1_p",
    # "FSGenPhoton2_p",
    # "FSGenPhoton0_pt",
    # "FSGenPhoton1_pt",
    # "FSGenPhoton2_pt",
    # "FSGen_a0a1_invMass",
    # "FSGen_a0a2_invMass",
    # "FSGen_a1a2_invMass",
    # "FSGen_aaa_invMass",

    "GenALP_mass",
    "GenALP_p",
    "GenALP_pt",
    "GenALP_pz",
    "GenALP_eta",
    "GenALP_theta",
    "GenALP_phi",
    "GenALP_lifetime_xy",
    "GenALP_lifetime_xyz",
    "GenALP_Lxy",
    "GenALP_Lxyz",
    "GenALP_vertex_x",
    "GenALP_vertex_y",
    "GenALP_vertex_z",

    "GenALPPhoton1_e",
    "GenALPPhoton2_e",
    "GenALPPhoton1_p",
    "GenALPPhoton2_p",
    "GenALPPhoton1_pt",
    "GenALPPhoton2_pt",
    "GenALPPhoton1_pz",
    "GenALPPhoton2_pz",
    "GenALPPhoton1_eta",
    "GenALPPhoton2_eta",
    "GenALPPhoton1_theta",
    "GenALPPhoton2_theta",
    "GenALPPhoton1_phi",
    "GenALPPhoton2_phi",
    "GenALPPhoton1_vertex_x",
    "GenALPPhoton1_vertex_y",
    "GenALPPhoton1_vertex_z",

    "GenALP_aa_invMass",

    #reco variables
    "n_RecoTracks",
    "n_RecoALPTracks",
    "RecoALP_DecayVertex_x",
    "RecoALP_DecayVertex_y",
    "RecoALP_DecayVertex_z",
    "RecoALP_DecayVertex_chi2",
    "RecoALP_DecayVertex_probability",

    "RecoALPPhoton1_e",
    "RecoALPPhoton2_e",
    "RecoALPPhoton1_p",
    "RecoALPPhoton2_p",
    "RecoALPPhoton1_pt",
    "RecoALPPhoton2_pt",
    "RecoALPPhoton1_pz",
    "RecoALPPhoton2_pz",
    "RecoALPPhoton1_eta",
    "RecoALPPhoton2_eta",
    "RecoALPPhoton1_theta",
    "RecoALPPhoton2_theta",
    "RecoALPPhoton1_phi",
    "RecoALPPhoton2_phi",
    "RecoALPPhoton1_charge",
    "RecoALPPhoton2_charge",

    "n_RecoJets",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",

    "RecoJet_e",
    "RecoJet_p",
    "RecoJet_pt",
    "RecoJet_pz",
    "RecoJet_eta",
    "RecoJet_theta",
    "RecoJet_phi",
    "RecoJet_charge",

    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",
    "RecoElectron_charge",

    "RecoPhoton_e",
    "RecoPhoton_p",
    "RecoPhoton_pt",
    "RecoPhoton_pz",
    "RecoPhoton_eta",
    "RecoPhoton_theta",
    "RecoPhoton_phi",
    "RecoPhoton_charge",

    "RecoMuon_e",
    "RecoMuon_p",
    "RecoMuon_pt",
    "RecoMuon_pz",
    "RecoMuon_eta",
    "RecoMuon_theta",
    "RecoMuon_phi",
    "RecoMuon_charge",

    "RecoMissingEnergy_e",
    "RecoMissingEnergy_p",
    "RecoMissingEnergy_pt",
    "RecoMissingEnergy_px",
    "RecoMissingEnergy_py",
    "RecoMissingEnergy_pz",
    "RecoMissingEnergy_eta",
    "RecoMissingEnergy_theta",
    "RecoMissingEnergy_phi",
]

###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ALP']   = ["selNone"]#,"sel0","sel1"]

extralabel = {}
extralabel['selNone'] = "No selection"
#extralabel['sel0'] = "Selection: At least 1 N"
#extralabel['sel1'] = "Selection: At least 1 N, at least 2 reco electrons"

colors = {}
colors['ALP_Z_aa_1GeV_cYY_0p5'] = ROOT.kRed
colors['ALP_Z_aa_1GeV_cYY_0p9'] = ROOT.kBlue
colors['ALP_Z_aa_1GeV_cYY_1p0'] = ROOT.kBlack
colors['ALP_Z_aa_1GeV_cYY_1p5'] = ROOT.kGreen+2
colors['ALP_Z_aa_1GeV_cYY_1p9'] = ROOT.kMagenta

plots = {}
plots['ALP'] = {'signal':{
    'ALP_Z_aa_1GeV_cYY_0p5':['ALP_Z_aa_1GeV_cYY_0p5'],
    'ALP_Z_aa_1GeV_cYY_0p9':['ALP_Z_aa_1GeV_cYY_0p9'],
    'ALP_Z_aa_1GeV_cYY_1p0':['ALP_Z_aa_1GeV_cYY_1p0'],
    'ALP_Z_aa_1GeV_cYY_1p5':['ALP_Z_aa_1GeV_cYY_1p5'],
    'ALP_Z_aa_1GeV_cYY_1p9':['ALP_Z_aa_1GeV_cYY_1p9'],

},
                'backgrounds':{
                    #'WW':['p8_ee_WW_ecm240'],
                    #'ZZ':['p8_ee_ZZ_ecm240']
                    #'Ztotautau': ['p8_ee_Ztautau_ecm91'],
                }
                }


legend = {}
legend['ALP_Z_aa_1GeV_cYY_0p5'] = 'm_{ALP} = 1 GeV, c_{YY} = 0.5'
legend['ALP_Z_aa_1GeV_cYY_0p9'] = 'm_{ALP} = 1 GeV, c_{YY} = 0.9'
legend['ALP_Z_aa_1GeV_cYY_1p0'] = 'm_{ALP} = 1 GeV, c_{YY} = 1.0'
legend['ALP_Z_aa_1GeV_cYY_1p5'] = 'm_{ALP} = 1 GeV, c_{YY} = 1.5'
legend['ALP_Z_aa_1GeV_cYY_1p9'] = 'm_{ALP} = 1 GeV, c_{YY} = 1.9'

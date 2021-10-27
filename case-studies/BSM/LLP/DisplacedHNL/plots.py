import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
#scaleSig       = 
ana_tex        = 'e^{+}e^{-} #rightarrow N #nu, N #rightarrow ee#nu'
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = 'read_EDM4HEP/'
#formats        = ['png','pdf']
formats        = ['pdf']
yaxis          = ['lin','log']
#stacksig       = ['stack','nostack']
stacksig       = ['nostack']
outdir         = 'plots/'

variables = [

    #gen variables
    "All_n_GenHNL",
    "AllGenHNL_mass",
    "AllGenHNL_p",
    "AllGenHNL_pt",
    "AllGenHNL_pz",
    "AllGenHNL_eta",
    "AllGenHNL_phi",

    "n_FSGenElectron",
    "n_FSGenPositron",
    "n_FSGenNeutrino",
    "n_FSGenAntiNeutrino",
    "n_FSGenPhoton",

    "FSGenElectron_p",
    "FSGenElectron_pt",
    "FSGenElectron_pz",
    "FSGenElectron_eta",
    "FSGenElectron_phi",

    "FSGenPositron_p",
    "FSGenPositron_pt",
    "FSGenPositron_pz",
    "FSGenPositron_eta",
    "FSGenPositron_phi",

    "FSGenNeutrino_p",
    "FSGenNeutrino_pt",
    "FSGenNeutrino_pz",
    "FSGenNeutrino_eta",
    "FSGenNeutrino_phi",

    "FSGenAntiNeutrino_p",
    "FSGenAntiNeutrino_pt",
    "FSGenAntiNeutrino_pz",
    "FSGenAntiNeutrino_eta",
    "FSGenAntiNeutrino_phi",

    "FSGenPhoton_p",
    "FSGenPhoton_pt",
    "FSGenPhoton_pz",
    "FSGenPhoton_eta",
    "FSGenPhoton_phi",

    "FSGenElectron_vertex_x",
    "FSGenElectron_vertex_y",
    "FSGenElectron_vertex_z",

    "FSGen_Lxy",
    "FSGen_lifetime",

    "GenHNL_mass",
    "GenHNL_p",
    "GenHNL_pt",
    "GenHNL_pz",
    "GenHNL_eta",
    "GenHNL_phi",
    "GenHNL_lifetime",
    "GenHNL_Lxy",
    "GenHNL_vertex_x",
    "GenHNL_vertex_y",
    "GenHNL_vertex_z",

    "GenHNLElectron_p",
    "GenHNLPositron_p",
    "GenHNLNeutrino_p",
    "GenHNLElectron_pt",
    "GenHNLPositron_pt",
    "GenHNLNeutrino_pt",
    "GenHNLElectron_pz",
    "GenHNLPositron_pz",
    "GenHNLNeutrino_pz",
    "GenHNLElectron_eta",
    "GenHNLPositron_eta",
    "GenHNLNeutrino_eta",
    "GenHNLElectron_phi",
    "GenHNLPositron_phi",
    "GenHNLNeutrino_phi",
    "GenHNLElectron_vertex_x",
    "GenHNLElectron_vertex_y",
    "GenHNLElectron_vertex_z",

    #reco variables
    "n_RecoTracks",
    "n_RecoHNLTracks",
    "RecoHNL_DecayVertex_x",
    "RecoHNL_DecayVertex_y",
    "RecoHNL_DecayVertex_z",
    "RecoHNL_DecayVertex_chi2",
    "RecoHNL_DecayVertex_probability",

    "RecoHNLElectron_p",
    "RecoHNLPositron_p",
    "RecoHNLElectron_pt",
    "RecoHNLPositron_pt",
    "RecoHNLElectron_pz",
    "RecoHNLPositron_pz",
    "RecoHNLElectron_eta",
    "RecoHNLPositron_eta",
    "RecoHNLElectron_phi",
    "RecoHNLPositron_phi",
    "RecoHNLElectron_charge",
    "RecoHNLPositron_charge",

    "n_RecoJets",
    "n_RecoPhotons",
    "n_RecoElectrons",
    "n_RecoMuons",

    "RecoJet_p",
    "RecoJet_pt",
    "RecoJet_pz",
    "RecoJet_eta",
    "RecoJet_phi",
    "RecoJet_charge",

    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_phi",
    "RecoElectron_charge",

    "RecoPhoton_p",
    "RecoPhoton_pt",
    "RecoPhoton_pz",
    "RecoPhoton_eta",
    "RecoPhoton_phi",
    "RecoPhoton_charge",

    "RecoMuon_p",
    "RecoMuon_pt",
    "RecoMuon_pz",
    "RecoMuon_eta",
    "RecoMuon_phi",
    "RecoMuon_charge",

    "RecoMET",
    "RecoMET_x",
    "RecoMET_y",
    "RecoMET_phi",

    #gen-reco
    "GenMinusRecoHNLElectron_p",
    "GenMinusRecoHNLPositron_p",
    "GenMinusRecoHNLElectron_pt",
    "GenMinusRecoHNLPositron_pt",
    "GenMinusRecoHNLElectron_pz",
    "GenMinusRecoHNLPositron_pz",
    "GenMinusRecoHNLElectron_eta",
    "GenMinusRecoHNLPositron_eta",
    "GenMinusRecoHNLElectron_phi",
    "GenMinusRecoHNLPositron_phi",

    "GenMinusRecoHNL_DecayVertex_x",
    "GenMinusRecoHNL_DecayVertex_y",
    "GenMinusRecoHNL_DecayVertex_z",
    
             ]
    
###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HNL']   = ["selNone","sel0","sel1"]

extralabel = {}
extralabel['selNone'] = "No selection"
extralabel['sel0'] = "Selection: At least 1 N"
extralabel['sel1'] = "Selection: At least 1 N, at least 2 reco electrons"

colors = {}
#colors['HNL_eenu_5GeV_1p41e-6Ve'] = ROOT.kGreen+2
#colors['HNL_eenu_10GeV_1p41e-6Ve'] = ROOT.kBlack
#colors['HNL_eenu_12GeV_1p41e-6Ve'] = ROOT.kCyan
#colors['HNL_eenu_15GeV_1p41e-6Ve'] = ROOT.kBlue
#colors['HNL_eenu_20GeV_1p41e-6Ve'] = ROOT.kMagenta
#colors['HNL_eenu_30GeV_1p41e-6Ve'] = ROOT.kRed
colors['HNL_eenu_40GeV_1p41e-6Ve'] = ROOT.kRed
colors['HNL_eenu_50GeV_1p41e-6Ve'] = ROOT.kBlue
colors['HNL_eenu_70GeV_1p41e-6Ve'] = ROOT.kGreen+2
colors['HNL_eenu_90GeV_1p41e-6Ve'] = ROOT.kBlack
#colors['Ztotautau'] = ROOT.kRed

plots = {}
plots['HNL'] = {'signal':{
    #'HNL_eenu_5GeV_1p41e-6Ve':['HNL_eenu_5GeV_1p41e-6Ve'],
    #'HNL_eenu_10GeV_1p41e-6Ve':['HNL_eenu_10GeV_1p41e-6Ve'],
    #'HNL_eenu_12GeV_1p41e-6Ve':['HNL_eenu_12GeV_1p41e-6Ve'],
    #'HNL_eenu_15GeV_1p41e-6Ve':['HNL_eenu_15GeV_1p41e-6Ve'],
    #'HNL_eenu_20GeV_1p41e-6Ve':['HNL_eenu_20GeV_1p41e-6Ve'],
    #'HNL_eenu_30GeV_1p41e-6Ve':['HNL_eenu_30GeV_1p41e-6Ve'],
    'HNL_eenu_40GeV_1p41e-6Ve':['HNL_eenu_40GeV_1p41e-6Ve'],
    'HNL_eenu_50GeV_1p41e-6Ve':['HNL_eenu_50GeV_1p41e-6Ve'],
    'HNL_eenu_70GeV_1p41e-6Ve':['HNL_eenu_70GeV_1p41e-6Ve'],
    'HNL_eenu_90GeV_1p41e-6Ve':['HNL_eenu_90GeV_1p41e-6Ve'],
},
                'backgrounds':{
                    #'WW':['p8_ee_WW_ecm240'],
                    #'ZZ':['p8_ee_ZZ_ecm240']
                    #'Ztotautau': ['p8_ee_Ztautau_ecm91'],
                }
                }


legend = {}
#legend['HNL_eenu_5GeV_1p41e-6Ve']  = 'm_{N} = 5 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_10GeV_1p41e-6Ve'] = 'm_{N} = 10 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_12GeV_1p41e-6Ve'] = 'm_{N} = 12 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_15GeV_1p41e-6Ve'] = 'm_{N} = 15 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_20GeV_1p41e-6Ve'] = 'm_{N} = 20 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_30GeV_1p41e-6Ve'] = 'm_{N} = 30 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_40GeV_1p41e-6Ve'] = 'm_{N} = 40 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_50GeV_1p41e-6Ve'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_70GeV_1p41e-6Ve'] = 'm_{N} = 70 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_90GeV_1p41e-6Ve'] = 'm_{N} = 90 GeV, V_{e} = 1.41e-6'
#legend['Ztotautau'] = 'Z #rightarrow #tau#tau'

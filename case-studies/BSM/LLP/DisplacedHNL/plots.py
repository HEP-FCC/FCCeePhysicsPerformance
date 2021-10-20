import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
#scaleSig       = 
ana_tex        = 'e^{+}e^{-} #rightarrow N #nu, N #rightarrow ee#nu'
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = 'read_EDM4HEP/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
#stacksig       = ['stack','nostack']
stacksig       = ['nostack']
outdir         = 'plots/'

variables = [
    #gen variables
    "GenHNL_mass",
    "GenHNL_pt",
    "GenHNL_eta",
    "GenHNL_phi",
    "GenHNL_lifetime",
    "GenHNL_Lxy",
    "GenHNL_vertex_x",
    "GenHNL_vertex_y",
    "GenHNL_vertex_z",

    "GenHNLElectron_pt",
    "GenHNLPositron_pt",
    "GenHNLNeutrino_pt",
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

    "RecoHNLElectron_pt",
    "RecoHNLPositron_pt",
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

    "RecoJet_pt",
    "RecoJet_eta",
    "RecoJet_phi",
    "RecoJet_charge",

    "RecoElectron_pt",
    "RecoElectron_eta",
    "RecoElectron_phi",
    "RecoElectron_charge",

    "RecoPhoton_pt",
    "RecoPhoton_eta",
    "RecoPhoton_phi",
    "RecoPhoton_charge",

    "RecoMuon_pt",
    "RecoMuon_eta",
    "RecoMuon_phi",
    "RecoMuon_charge",

    "RecoMET",
    "RecoMET_x",
    "RecoMET_y",
    "RecoMET_phi",

    #gen-reco
    "GenMinusRecoHNLElectron_pt",
    "GenMinusRecoHNLPositron_pt",
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
selections['HNL']   = ["sel0","sel1"]

extralabel = {}
extralabel['sel0'] = "Selection: At least 1 N"
extralabel['sel1'] = "Selection: At least 1 N, at least 2 reco electrons"

colors = {}
colors['HNL_eenu_10GeV_1p41e-6Ve'] = ROOT.kBlack
colors['HNL_eenu_30GeV_1p41e-6Ve'] = ROOT.kRed
colors['HNL_eenu_50GeV_1p41e-6Ve'] = ROOT.kBlue
colors['HNL_eenu_70GeV_1p41e-6Ve'] = ROOT.kGreen+2
#colors['Ztotautau'] = ROOT.kRed

plots = {}
plots['HNL'] = {'signal':{
    'HNL_eenu_10GeV_1p41e-6Ve':['HNL_eenu_10GeV_1p41e-6Ve'],
    'HNL_eenu_30GeV_1p41e-6Ve':['HNL_eenu_30GeV_1p41e-6Ve'],
    'HNL_eenu_50GeV_1p41e-6Ve':['HNL_eenu_50GeV_1p41e-6Ve'],
    'HNL_eenu_70GeV_1p41e-6Ve':['HNL_eenu_70GeV_1p41e-6Ve'],
},
                'backgrounds':{
                    #'WW':['p8_ee_WW_ecm240'],
                    #'ZZ':['p8_ee_ZZ_ecm240']
                    #'Ztotautau': ['p8_ee_Ztautau_ecm91'],
                }
                }


legend = {}
legend['HNL_eenu_10GeV_1p41e-6Ve'] = 'm_{N} = 10 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_30GeV_1p41e-6Ve'] = 'm_{N} = 30 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_50GeV_1p41e-6Ve'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_70GeV_1p41e-6Ve'] = 'm_{N} = 70 GeV, V_{e} = 1.41e-6'
#legend['Ztotautau'] = 'Z #rightarrow #tau#tau'

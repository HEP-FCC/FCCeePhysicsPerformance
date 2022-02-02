import ROOT

# global parameters
intLumi        = 150.0e+06 #in pb-1

###If scaleSig=0 or scaleBack=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
###If scaleSig or scaleBack is not defined, plots will be normalized to 1
# scaleSig       = 0.
# scaleBack      = 0.
ana_tex        = ''
delphesVersion = '3.4.2'
energy         = 91
collider       = 'FCC-ee'
inputDir       = 'read_EDM4HEP/'
#formats        = ['png','pdf']
formats        = ['pdf']
yaxis          = ['lin','log']
#stacksig       = ['stack','nostack']
stacksig       = ['nostack']
outdir         = 'plots_general/'

variables = [

    #gen variables
    "n_FSGenElectron",
    "n_FSGenNeutrino",
    "n_FSGenPhoton",

    "FSGenElectron_e",
    "FSGenElectron_p",
    "FSGenElectron_pt",
    "FSGenElectron_pz",
    "FSGenElectron_eta",
    "FSGenElectron_theta",
    "FSGenElectron_phi",
    "FSGenElectron_charge",

    "FSGenNeutrino_e",
    "FSGenNeutrino_p",
    "FSGenNeutrino_pt",
    "FSGenNeutrino_pz",
    "FSGenNeutrino_eta",
    "FSGenNeutrino_theta",
    "FSGenNeutrino_phi",
    "FSGenNeutrino_charge",

    "FSGenPhoton_e",
    "FSGenPhoton_p",
    "FSGenPhoton_pt",
    "FSGenPhoton_pz",
    "FSGenPhoton_eta",
    "FSGenPhoton_theta",
    "FSGenPhoton_phi",
    "FSGenPhoton_charge",

    "FSGenElectron_vertex_x",
    "FSGenElectron_vertex_y",
    "FSGenElectron_vertex_z",
    "FSGenElectron_vertex_x_prompt",
    "FSGenElectron_vertex_y_prompt",
    "FSGenElectron_vertex_z_prompt",

    "FSGen_Lxy",
    "FSGen_Lxyz",
    "FSGen_Lxyz_prompt",

    "FSGen_ee_invMass",
    "FSGen_eenu_invMass",

    #reco variables
    "n_RecoTracks",
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

    "RecoJetTrack_absD0",
    "RecoJetTrack_absD0_prompt",
    "RecoJetTrack_absZ0",
    "RecoJetTrack_absZ0_prompt",
    "RecoJetTrack_absD0sig",
    "RecoJetTrack_absD0sig_prompt",
    "RecoJetTrack_absZ0sig",
    "RecoJetTrack_absZ0sig_prompt",
    "RecoJetTrack_D0cov",
    "RecoJetTrack_Z0cov",

    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",
    "RecoElectron_charge",

    "RecoElectronTrack_absD0",
    "RecoElectronTrack_absD0_prompt",
    "RecoElectronTrack_absZ0",
    "RecoElectronTrack_absZ0_prompt",
    "RecoElectronTrack_absD0sig",
    "RecoElectronTrack_absD0sig_prompt",
    "RecoElectronTrack_absZ0sig",
    "RecoElectronTrack_absZ0sig_prompt",
    "RecoElectronTrack_D0cov",
    "RecoElectronTrack_Z0cov",

    "Reco_DecayVertex_x",
    "Reco_DecayVertex_y",
    "Reco_DecayVertex_z",
    "Reco_DecayVertex_x_prompt",
    "Reco_DecayVertex_y_prompt",
    "Reco_DecayVertex_z_prompt",
    "Reco_DecayVertex_chi2",
    "Reco_DecayVertex_probability",
    "Reco_Lxy",
    "Reco_Lxyz",
    "Reco_Lxyz_prompt",

    "Reco_ee_invMass",

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

    "RecoMuonTrack_absD0",
    "RecoMuonTrack_absD0_prompt",
    "RecoMuonTrack_absZ0",
    "RecoMuonTrack_absZ0_prompt",
    "RecoMuonTrack_absD0sig",
    "RecoMuonTrack_absD0sig_prompt",
    "RecoMuonTrack_absZ0sig",
    "RecoMuonTrack_absZ0sig_prompt",
    "RecoMuonTrack_D0cov",
    "RecoMuonTrack_Z0cov",

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

effPlots = {
    #num: den
    "RecoElectron_p":"FSGenElectron_p",
}
    
###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HNL']  = [
    "selNone",
    "sel1FSGenEle",
    "sel1FSGenNu",
    "sel2RecoEle",
    "sel2RecoEle_vetoes",
    "sel2RecoEle_absD0Gt0p1",
    "sel2RecoEle_vetoes_MissingEnergyGt10",
    "sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5",
]

extralabel = {}
extralabel['selNone'] = "No selection"
extralabel['sel1FSGenEle'] = "Selection: At least 1 final state gen electron"
extralabel['sel1FSGenNu'] = "Selection: At least 1 final state gen neutrino"
extralabel['sel2RecoEle'] = "Selection: Exactly 2 reco electrons"
extralabel['sel2RecoEle_vetoes'] = "Selection: Exactly 2 reco electrons; No reco muons, jets, or photons"
extralabel['sel2RecoEle_absD0Gt0p1'] = "Selection: Exactly 2 reco electrons with |d_0|>0.1 mm"
extralabel['sel2RecoEle_vetoes_MissingEnergyGt10'] = "Selection: Exactly 2 reco electrons; No reco muons, jets, or photons; Missing energy > 10 GeV"
extralabel['sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5'] = "Selection: Exactly 2 reco electrons with |d_0|>0.5 mm; No reco muons, jets, or photons; Missing energy > 10 GeV"

colors = {}
colors['Zee'] = ROOT.kBlack
colors['Zbb'] = ROOT.kRed
colors['Ztautau'] = ROOT.kBlue
colors['Zcc'] = ROOT.kMagenta
colors['Zuds'] = ROOT.kCyan
# colors['HNL_eenu_30GeV_1p41e-6Ve'] = ROOT.kBlack
# colors['HNL_eenu_50GeV_1p41e-6Ve'] = ROOT.kRed
# colors['HNL_eenu_70GeV_1p41e-6Ve'] = ROOT.kGreen+2


plots = {}
plots['HNL'] = {'signal':{
                    # 'HNL_eenu_30GeV_1p41e-6Ve':['HNL_eenu_30GeV_1p41e-6Ve'],
                    # 'HNL_eenu_50GeV_1p41e-6Ve':['HNL_eenu_50GeV_1p41e-6Ve'],
                    # 'HNL_eenu_70GeV_1p41e-6Ve':['HNL_eenu_70GeV_1p41e-6Ve'],
},
                'backgrounds':{
                    'Zee':['p8_ee_Zee_ecm91'],
                    'Zbb':['p8_ee_Zbb_ecm91'],
                    'Ztautau': ['p8_ee_Ztautau_ecm91'],
                    'Zcc': ['p8_ee_Zcc_ecm91'],
                    'Zuds': ['p8_ee_Zuds_ecm91'],
                }
                }


legend = {}
legend['Zee'] = 'e^{+}e^{-} #rightarrow Z #rightarrow ee'
legend['Zbb'] = 'e^{+}e^{-} #rightarrow Z #rightarrow bb'
legend['Ztautau'] = 'e^{+}e^{-} #rightarrow Z #rightarrow #tau#tau'
legend['Zcc'] = 'e^{+}e^{-} #rightarrow Z #rightarrow cc'
legend['Zuds'] = 'e^{+}e^{-} #rightarrow Z #rightarrow uds'

# legend['HNL_eenu_30GeV_1p41e-6Ve'] = 'm_{N} = 30 GeV, V_{e} = 1.41e-6'
# legend['HNL_eenu_50GeV_1p41e-6Ve'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6'
# legend['HNL_eenu_70GeV_1p41e-6Ve'] = 'm_{N} = 70 GeV, V_{e} = 1.41e-6'

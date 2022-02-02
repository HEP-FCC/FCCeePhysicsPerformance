import ROOT

# global parameters
intLumi        = 150.0e+06 #in pb-1
# if scaleSig=0, we don't apply any additional scaling, on top of the normalization to cross section and integrated luminosity, as defined in finalSel.py
# if scaleSig is not defined, plots will be normalized to 1
#scaleSig       = 0.
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
    "AllGenHNL_e",
    "AllGenHNL_p",
    "AllGenHNL_pt",
    "AllGenHNL_pz",
    "AllGenHNL_eta",
    "AllGenHNL_theta",
    "AllGenHNL_phi",

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

    "FSGenNeutrino_e",
    "FSGenNeutrino_p",
    "FSGenNeutrino_pt",
    "FSGenNeutrino_pz",
    "FSGenNeutrino_eta",
    "FSGenNeutrino_theta",
    "FSGenNeutrino_phi",

    "FSGenPhoton_e",
    "FSGenPhoton_p",
    "FSGenPhoton_pt",
    "FSGenPhoton_pz",
    "FSGenPhoton_eta",
    "FSGenPhoton_theta",
    "FSGenPhoton_phi",

    "FSGenElectron_vertex_x",
    "FSGenElectron_vertex_y",
    "FSGenElectron_vertex_z",
    "FSGenElectron_vertex_x_prompt",
    "FSGenElectron_vertex_y_prompt",
    "FSGenElectron_vertex_z_prompt",

    "FSGen_Lxy",
    "FSGen_Lxyz",
    "FSGen_Lxyz_prompt",
    "FSGen_lifetime_xy",
    "FSGen_lifetime_xyz",
    "FSGen_lifetime_xyz_prompt",

    "FSGen_ee_invMass",
    "FSGen_eenu_invMass",

    "GenHNL_mass",
    "GenHNL_p",
    "GenHNL_pt",
    "GenHNL_pz",
    "GenHNL_eta",
    "GenHNL_theta",
    "GenHNL_phi",
    "GenHNL_lifetime_xy",
    "GenHNL_lifetime_xyz",
    "GenHNL_lifetime_xyz_prompt",
    "GenHNL_Lxy",
    "GenHNL_Lxyz",
    "GenHNL_Lxyz_prompt",
    "GenHNL_vertex_x",
    "GenHNL_vertex_y",
    "GenHNL_vertex_z",

    "GenHNLElectron_e",
    "GenHNLElectron_p",
    "GenHNLElectron_pt",
    "GenHNLElectron_pz",
    "GenHNLElectron_eta",
    "GenHNLElectron_theta",
    "GenHNLElectron_phi",

    "GenHNLElectron2_e",
    "GenHNLElectron2_p",
    "GenHNLElectron2_pt",
    "GenHNLElectron2_pz",
    "GenHNLElectron2_eta",
    "GenHNLElectron2_theta",
    "GenHNLElectron2_phi",

    "GenHNLNeutrino_e",
    "GenHNLNeutrino_p",
    "GenHNLNeutrino_pt",
    "GenHNLNeutrino_pz",
    "GenHNLNeutrino_eta",
    "GenHNLNeutrino_theta",
    "GenHNLNeutrino_phi",

    "GenHNLElectron_vertex_x",
    "GenHNLElectron_vertex_y",
    "GenHNLElectron_vertex_z",
    "GenHNLElectron_vertex_x_prompt",
    "GenHNLElectron_vertex_y_prompt",
    "GenHNLElectron_vertex_z_prompt",

    "GenHNL_ee_invMass",
    "GenHNL_eenu_invMass",

    #reco variables
    "n_RecoTracks",
    "n_RecoHNLTracks",

    "RecoHNLTracks_absD0",
    "RecoHNLTracks_absD0_prompt",
    "RecoHNLTracks_absZ0",
    "RecoHNLTracks_absZ0_prompt",
    "RecoHNLTracks_absD0sig",
    "RecoHNLTracks_absD0sig_prompt",
    "RecoHNLTracks_absZ0sig",
    "RecoHNLTracks_absZ0sig_prompt",
    "RecoHNLTracks_D0cov",
    "RecoHNLTracks_Z0cov",

    "RecoHNL_DecayVertex_x",
    "RecoHNL_DecayVertex_y",
    "RecoHNL_DecayVertex_z",
    "RecoHNL_DecayVertex_x_prompt",
    "RecoHNL_DecayVertex_y_prompt",
    "RecoHNL_DecayVertex_z_prompt",
    "RecoHNL_DecayVertex_chi2",
    "RecoHNL_DecayVertex_probability",
    "RecoHNL_Lxy",
    "RecoHNL_Lxyz",
    "RecoHNL_Lxyz_prompt",

    "RecoHNLElectron_e",
    "RecoHNLElectron_p",
    "RecoHNLElectron_pt",
    "RecoHNLElectron_pz",
    "RecoHNLElectron_eta",
    "RecoHNLElectron_theta",
    "RecoHNLElectron_phi",
    "RecoHNLElectron_charge",

    "RecoHNLElectron2_e",
    "RecoHNLElectron2_p",
    "RecoHNLElectron2_pt",
    "RecoHNLElectron2_pz",
    "RecoHNLElectron2_eta",
    "RecoHNLElectron2_theta",
    "RecoHNLElectron2_phi",
    "RecoHNLElectron2_charge",

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

    "RecoHNL_ee_invMass",

    #gen-reco
    "GenMinusRecoHNLElectron_e",
    "GenMinusRecoHNLElectron_p",
    "GenMinusRecoHNLElectron_pt",
    "GenMinusRecoHNLElectron_pz",
    "GenMinusRecoHNLElectron_eta",
    "GenMinusRecoHNLElectron_theta",
    "GenMinusRecoHNLElectron_phi",

    "GenMinusRecoHNL_DecayVertex_x",
    "GenMinusRecoHNL_DecayVertex_y",
    "GenMinusRecoHNL_DecayVertex_z",
    "GenMinusRecoHNL_Lxy",
    "GenMinusRecoHNL_Lxyz",
    "GenMinusRecoHNL_Lxyz_prompt",
    
             ]
    
###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
# selections['HNL']   = [
#     "selNone",
#     "selGenLxyzGt500",
# ] #,"sel0","sel1"]
selections['HNL']  = [
    "selNone",
    "sel1FSGenEle",
    "sel1FSGenNu",
    "sel2RecoEle",
    "sel2RecoEle_vetoes",
    "sel2RecoEle_absD0Gt0p1",
    "sel2RecoEle_chi2Gt0p1",
    "sel2RecoEle_vetoes_MissingEnergyGt10",
    "sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5",
]

extralabel = {}
# extralabel['selNone'] = "No selection"
# extralabel['sel0'] = "Selection: At least 1 N"
# extralabel['sel1'] = "Selection: At least 1 N, at least 2 reco electrons"
# extralabel['selGenLxyzGt500'] = "Selection: At least 1 N with gen L_{xyz}>50 cm"
extralabel['selNone'] = "No selection"
extralabel['sel1FSGenEle'] = "Selection: At least 1 final state gen electron"
extralabel['sel1FSGenNu'] = "Selection: At least 1 final state gen neutrino"
extralabel['sel2RecoEle'] = "Selection: Exactly 2 reco electrons"
extralabel['sel2RecoEle_vetoes'] = "Selection: Exactly 2 reco electrons; No reco muons, jets, or photons"
extralabel['sel2RecoEle_absD0Gt0p1'] = "Selection: Exactly 2 reco electrons with |d_0|>0.1 mm"
extralabel['sel2RecoEle_chi2Gt0p1'] = "Selection: Exactly 2 reco electrons with #chi^{2}>0.1"
extralabel['sel2RecoEle_vetoes_MissingEnergyGt10'] = "Selection: Exactly 2 reco electrons; No reco muons, jets, or photons; Missing energy > 10 GeV"
extralabel['sel2RecoEle_vetoes_MissingEnergyGt10_absD0Gt0p5'] = "Selection: Exactly 2 reco electrons with |d_0|>0.5 mm; No reco muons, jets, or photons; Missing energy > 10 GeV"

colors = {}
# colors['HNL_50'] = ROOT.kBlack
# colors['HNL_50_old'] = ROOT.kRed
#colors['HNL_eenu_40GeV_1e-3Ve'] = ROOT.kBlack
#colors['HNL_eenu_40GeV_1e-4Ve'] = ROOT.kCyan
#colors['HNL_eenu_40GeV_1e-5Ve'] = ROOT.kRed
#colors['HNL_eenu_5GeV_1p41e-6Ve'] = ROOT.kGreen+2
#colors['HNL_eenu_10GeV_1p41e-6Ve'] = ROOT.kCyan
#colors['HNL_eenu_10GeV_0p1Ve'] = ROOT.kBlue
#colors['HNL_eenu_12GeV_1p41e-6Ve'] = ROOT.kCyan
#colors['HNL_eenu_15GeV_1p41e-6Ve'] = ROOT.kBlue
#colors['HNL_eenu_20GeV_1p41e-6Ve'] = ROOT.kMagenta
#colors['HNL_eenu_20GeV_0p1Ve'] = ROOT.kRed
colors['HNL_eenu_20GeV_0p1Ve_withBothAntiNu'] = ROOT.kMagenta
colors['HNL_eenu_20GeV_0p1Ve_withBothAntiNu_localDelphes'] = ROOT.kRed
colors['HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu'] = ROOT.kCyan
colors['HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu_localDelphes'] = ROOT.kBlue


#colors['HNL_eenu_30GeV_1p41e-6Ve'] = ROOT.kBlack
#colors['HNL_eenu_40GeV_1p41e-6Ve'] = ROOT.kRed
#colors['HNL_eenu_50GeV_1p41e-6Ve'] = ROOT.kRed
#colors['HNL_eenu_70GeV_1p41e-6Ve'] = ROOT.kGreen+2
#colors['HNL_eenu_90GeV_1p41e-6Ve'] = ROOT.kBlack
#colors['HNL_eenu_90GeV_1p41e-6Ve'] = ROOT.kBlue
#colors['Ztotautau'] = ROOT.kRed

plots = {}
plots['HNL'] = {'signal':{
    # 'HNL_50':['HNL_50'],
    # 'HNL_50_old':['HNL_50_old'],
    #'HNL_eenu_40GeV_1e-3Ve':['HNL_eenu_40GeV_1e-3Ve'],
    #'HNL_eenu_40GeV_1e-4Ve':['HNL_eenu_40GeV_1e-4Ve'],
    #'HNL_eenu_40GeV_1e-5Ve':['HNL_eenu_40GeV_1e-5Ve'],
    #'HNL_eenu_5GeV_1p41e-6Ve':['HNL_eenu_5GeV_1p41e-6Ve'],
    #'HNL_eenu_10GeV_1p41e-6Ve':['HNL_eenu_10GeV_1p41e-6Ve'],
    #'HNL_eenu_10GeV_0p1Ve':['HNL_eenu_10GeV_0p1Ve'],
    #'HNL_eenu_12GeV_1p41e-6Ve':['HNL_eenu_12GeV_1p41e-6Ve'],
    #'HNL_eenu_15GeV_1p41e-6Ve':['HNL_eenu_15GeV_1p41e-6Ve'],
    #'HNL_eenu_20GeV_1p41e-6Ve':['HNL_eenu_20GeV_1p41e-6Ve'],
    #'HNL_eenu_20GeV_0p1Ve':['HNL_eenu_20GeV_0p1Ve'],
    'HNL_eenu_20GeV_0p1Ve_withBothAntiNu':['HNL_eenu_20GeV_0p1Ve_withBothAntiNu'],
    'HNL_eenu_20GeV_0p1Ve_withBothAntiNu_localDelphes':['HNL_eenu_20GeV_0p1Ve_withBothAntiNu_localDelphes'],
    'HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu':['HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu'],
    'HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu_localDelphes':['HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu_localDelphes'],
    #'HNL_eenu_30GeV_1p41e-6Ve':['HNL_eenu_30GeV_1p41e-6Ve'],
    #'HNL_eenu_40GeV_1p41e-6Ve':['HNL_eenu_40GeV_1p41e-6Ve'],
    #'HNL_eenu_50GeV_1p41e-6Ve':['HNL_eenu_50GeV_1p41e-6Ve'],
    #'HNL_eenu_70GeV_1p41e-6Ve':['HNL_eenu_70GeV_1p41e-6Ve'],
    #'HNL_eenu_90GeV_1p41e-6Ve':['HNL_eenu_90GeV_1p41e-6Ve'],
},
                'backgrounds':{
                    #'WW':['p8_ee_WW_ecm240'],
                    #'ZZ':['p8_ee_ZZ_ecm240']
                    #'Ztotautau': ['p8_ee_Ztautau_ecm91'],
                }
                }


legend = {}
# legend['HNL_50']  = 'New'
# legend['HNL_50_old']  = 'Old'
#legend['HNL_eenu_40GeV_1e-3Ve']  = 'm_{N} = 40 GeV, V_{e} = 1e-3'
#legend['HNL_eenu_40GeV_1e-4Ve']  = 'm_{N} = 40 GeV, V_{e} = 1e-4'
#legend['HNL_eenu_40GeV_1e-5Ve']  = 'm_{N} = 40 GeV, V_{e} = 1e-5'
#legend['HNL_eenu_5GeV_1p41e-6Ve']  = 'm_{N} = 5 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_10GeV_1p41e-6Ve'] = 'm_{N} = 10 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_10GeV_0p1Ve'] = 'm_{N} = 10 GeV, V_{e} = 0.1'
#legend['HNL_eenu_12GeV_1p41e-6Ve'] = 'm_{N} = 12 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_15GeV_1p41e-6Ve'] = 'm_{N} = 15 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_20GeV_1p41e-6Ve'] = 'm_{N} = 20 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_20GeV_0p1Ve'] = 'm_{N} = 20 GeV, V_{e} = 0.1'
legend['HNL_eenu_20GeV_0p1Ve_withBothAntiNu'] = 'm_{N} = 20 GeV, V_{e} = 0.1, Delphes 3.4.2'
legend['HNL_eenu_20GeV_0p1Ve_withBothAntiNu_localDelphes'] = 'm_{N} = 20 GeV, V_{e} = 0.1, Delphes 3.5.1.pre01'
legend['HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6, Delphes 3.4.2'
legend['HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu_localDelphes'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6, Delphes 3.5.1.pre01'
#legend['HNL_eenu_30GeV_1p41e-6Ve'] = 'm_{N} = 30 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_40GeV_1p41e-6Ve'] = 'm_{N} = 40 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_50GeV_1p41e-6Ve'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_70GeV_1p41e-6Ve'] = 'm_{N} = 70 GeV, V_{e} = 1.41e-6'
#legend['HNL_eenu_90GeV_1p41e-6Ve'] = 'm_{N} = 90 GeV, V_{e} = 1.41e-6'
#legend['Ztotautau'] = 'Z #rightarrow #tau#tau'

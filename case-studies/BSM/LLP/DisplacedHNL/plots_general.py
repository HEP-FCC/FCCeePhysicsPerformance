import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
#scaleSig       = 
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

    "RecoElectron_e",
    "RecoElectron_p",
    "RecoElectron_pt",
    "RecoElectron_pz",
    "RecoElectron_eta",
    "RecoElectron_theta",
    "RecoElectron_phi",
    "RecoElectron_charge",

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

    "RecoMET",
    "RecoMET_x",
    "RecoMET_y",
    "RecoMET_phi",
    
             ]
    
###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HNL']  = [
    "selNone",
    "sel1FSGenEle",
    "sel1FSGenNu",
    #"sel2RecoEle",
]

extralabel = {}
extralabel['selNone'] = "No selection"
extralabel['sel1FSGenEle'] = "Selection: At least 1 final state gen electron"
extralabel['sel1FSGenNu'] = "Selection: At least 1 final state gen neutrino"
extralabel['sel2RecoEle'] = "Selection: At least 2 reco electrons"

colors = {}
colors['Zee'] = ROOT.kBlack
colors['Zbb'] = ROOT.kRed
colors['Ztautau'] = ROOT.kBlue


plots = {}
plots['HNL'] = {'signal':{
},
                'backgrounds':{
                    'Zee':['p8_ee_Zee_ecm91'],
                    'Zbb':['p8_ee_Zbb_ecm91'],
                    'Ztautau': ['p8_ee_Ztautau_ecm91'],
                }
                }


legend = {}
legend['Zee'] = 'e^{+}e^{-} #rightarrow Z #rightarrow ee'
legend['Zbb'] = 'e^{+}e^{-} #rightarrow Z #rightarrow bb'
legend['Ztautau'] = 'e^{+}e^{-} #rightarrow Z #rightarrow #tau#tau'

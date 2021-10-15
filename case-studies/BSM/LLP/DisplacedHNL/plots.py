import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
#scaleSig       = 
ana_tex        = 'e^{+}e^{-} #rightarrow N #nu, N #rightarrow ee#nu'
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-ee'
inputDir       = 'read_EDM4HEP/'
formats        = ['png','pdf']
yaxis          = ['lin','log']
#stacksig       = ['stack','nostack']
stacksig       = ['nostack']
outdir         = 'plots/'

variables = [
    #gen variables
    "HNL_mass",     
    "HNL_pT",       
    "HNL_eta",      
    "HNL_phi",      
    "HNL_lifetime", 
    "L_xy",         
    "HNL_vertex_x", 
    "HNL_vertex_y", 
    "HNL_vertex_z", 

    "electron_pT",       
    "positron_pT",       
    "electron_eta",      
    "positron_eta",      
    "electron_phi",      
    "positron_phi",      
    "electron_vertex_x", 
    "electron_vertex_y", 
    "electron_vertex_z", 

    #reco variables
    "ntracks",               
    "n_RecoHNLTracks",
    "RecoHNL_DecayVertex_x",
    "RecoHNL_DecayVertex_y",
    "RecoHNL_DecayVertex_z",
    "RecoHNL_DecayVertex_chi2",
    "RecoHNL_DecayVertex_probability",

    "RecoElectron_pT",       
    "RecoPositron_pT",       
    "RecoElectron_eta",      
    "RecoPositron_eta",      
    "RecoElectron_phi",      
    "RecoPositron_phi",      
    "RecoElectron_charge",   
    "RecoPositron_charge",   

    #gen-reco
    "GenMinusRecoElectron_pT",
    "GenMinusRecoPositron_pT",
    "GenMinusRecoElectron_eta",
    "GenMinusRecoPositron_eta",
    "GenMinusRecoElectron_phi",
    "GenMinusRecoPositron_phi",

    "GenMinusRecoHNL_DecayVertex_x",
    "GenMinusRecoHNL_DecayVertex_y",
    "GenMinusRecoHNL_DecayVertex_z",
    
             ]
    
###Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['HNL']   = ["sel0"]

extralabel = {}
extralabel['sel0'] = "Selection: At least 1 N"

colors = {}
#colors['HNL_eenu_10GeV_1p41e-6Ve'] = ROOT.kBlack
colors['HNL_eenu_30GeV_1p41e-6Ve'] = ROOT.kRed
colors['HNL_eenu_50GeV_1p41e-6Ve'] = ROOT.kBlue
colors['HNL_eenu_70GeV_1p41e-6Ve'] = ROOT.kGreen+2
#colors['Ztotautau'] = ROOT.kRed

plots = {}
plots['HNL'] = {'signal':{
    #'HNL_eenu_10GeV_1p41e-6Ve':['HNL_eenu_10GeV_1p41e-6Ve'],
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
#legend['HNL_eenu_10GeV_1p41e-6Ve'] = 'm_{N} = 10 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_30GeV_1p41e-6Ve'] = 'm_{N} = 30 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_50GeV_1p41e-6Ve'] = 'm_{N} = 50 GeV, V_{e} = 1.41e-6'
legend['HNL_eenu_70GeV_1p41e-6Ve'] = 'm_{N} = 70 GeV, V_{e} = 1.41e-6'
#legend['Ztotautau'] = 'Z #rightarrow #tau#tau'

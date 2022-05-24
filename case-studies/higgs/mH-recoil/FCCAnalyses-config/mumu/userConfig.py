import os
#repo = os.getenv('PWD')
repo = "/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil"
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output_trained/'
loc.DATA = loc.ROOT+'data'
loc.CSV = loc.DATA+'/csv'
loc.PKL = loc.DATA+'/pkl'
loc.ROOTFILES = loc.DATA+'/ROOT'
loc.PLOTS = loc.OUT+'plots_test'
loc.TEX = loc.OUT+'tex'
loc.JSON = loc.OUT+'json'

#EOS location for files used in analysis
loc.EOS = "/eos/home-l/lia/FCCee/MVA"

#Output BDT model location - used in official sample production to assign MVA weights
loc.BDT = f"{loc.EOS}/BDT_test"

#Loaction of prod_04 tuples used in analysis
loc.PROD = f"{loc.EOS}"

#Samples for first stage BDT training
loc.TRAIN = f"{loc.PROD}/flatNtuples"

#Samples for second stage training
loc.TRAIN2 = f"{loc.PROD}/Training_4stage2/"

#Samples for final analysis
loc.ANALYSIS = f"{loc.PROD}/Analysis_stage2/"

#First stage BDT including event-level vars
train_vars = [
                #muons
                "selected_muons_delta_max",
                "selected_muons_delta_min",
                #"selected_muons_delta_avg",
                "muon_leading_pt",
                "muon_leading_px",
                "muon_leading_py",
                "muon_leading_pz",
                "muon_leading_eta",
                #"muon_leading_phi",
                #"muon_leading_y",  
                #"muon_leading_p",  
                "muon_leading_e",  
                #"muon_leading_m",  
                "muon_leading_theta",
                "muon_subleading_pt",
                "muon_subleading_px",
                "muon_subleading_py",
                "muon_subleading_pz",
                "muon_subleading_eta",
                #"muon_subleading_phi",  
                #"muon_subleading_y",
                #"muon_subleading_p",
                "muon_subleading_e",
                #"muon_subleading_m",
                "muon_subleading_theta",
                #Zed
                "Z_leptonic_m",      
                "Z_leptonic_pt",     
                "Z_leptonic_y",      
                "Z_leptonic_p",      
                #"Z_leptonic_e",      
                "Z_leptonic_px",     
                "Z_leptonic_py",     
                "Z_leptonic_pz",     
                "Z_leptonic_eta",    
                "Z_leptonic_theta",  
                #"Z_leptonic_phi",    
              ]

#First stage BDT including event-level vars and vertex vars
#This is the default list used in the analysis
train_vars_vtx = ["EVT_ThrustEmin_E",
                  "EVT_ThrustEmax_E",
                  "EVT_ThrustEmin_Echarged",
                  "EVT_ThrustEmax_Echarged",
                  "EVT_ThrustEmin_Eneutral",
                  "EVT_ThrustEmax_Eneutral",
                  "EVT_ThrustEmin_Ncharged",
                  "EVT_ThrustEmax_Ncharged",
                  "EVT_ThrustEmin_Nneutral",
                  "EVT_ThrustEmax_Nneutral",
                  "EVT_NtracksPV",
                  "EVT_NVertex",
                  "EVT_NTau23Pi",
                  "EVT_ThrustEmin_NDV",
                  "EVT_ThrustEmax_NDV",
                  "EVT_dPV2DVmin",
                  "EVT_dPV2DVmax",
                  "EVT_dPV2DVave"
                  ]


#Decay modes used in first stage training and their respective file names
mode_names = {"mumuH": "wzp6_ee_mumuH_ecm240",
              "ZZ": "p8_ee_ZZ_ecm240",
              "WWmumu": "p8_ee_WW_mumu_ecm240",
              "Zll": "wzp6_ee_mumu_ecm240",
              "egamma": "wzp6_egamma_eZ_Zmumu_ecm240",
              "gammae": "wzp6_gammae_eZ_Zmumu_ecm240"
              }

#Second stage training variables
train_vars_2 = ["EVT_CandMass",
                "EVT_CandRho1Mass",
                "EVT_CandRho2Mass",
                "EVT_CandN",
                "EVT_CandVtxFD",
                "EVT_CandVtxChi2",
                "EVT_CandPx",
                "EVT_CandPy",
                "EVT_CandPz",
                "EVT_CandP",
                "EVT_CandD0",
                "EVT_CandZ0",
                "EVT_CandAngleThrust",
                "EVT_DVd0_min",
                "EVT_DVd0_max",
                "EVT_DVd0_ave",
                "EVT_DVz0_min",
                "EVT_DVz0_max",
                "EVT_DVz0_ave",
                "EVT_PVmass",
                "EVT_Nominal_B_E"
               ]

#Hemipshere energy difference cut, applied offline prior to MVA2 optimisation
Ediff_cut = ">10."

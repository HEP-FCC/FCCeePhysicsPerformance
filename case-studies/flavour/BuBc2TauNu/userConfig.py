import os
import numpy as np
repo = os.getenv('PWD')
if 'xzuo' in repo:
  repo = "/afs/cern.ch/work/x/xzuo/public/FCC_files/BuBc2TauNu"
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output/'
loc.DATA = loc.ROOT+'data'
loc.CSV = loc.DATA+'/csv'
loc.PKL = loc.DATA+'/pkl'
loc.ROOTFILES = loc.DATA+'/ROOT'
loc.PLOTS = loc.OUT+'plots'
loc.TEXT = loc.OUT+'text'
loc.JSON = loc.OUT+'json'

#EOS location for files used in analysis
#loc.EOS = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu"
loc.EOS = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/BuBc2TauNu"

#Output BDT model location - used in official sample production to assign MVA weights
loc.BDT = loc.ROOTFILES #loc.EOS+""

#Loaction of prod_04 tuples used in analysis
loc.PROD = f"{loc.EOS}/flatNtuples/spring2021/prod_04"

#Samples for first stage BDT training
loc.TRAIN = f"{loc.PROD}/training_stage1/"

loc.TEST = f"{loc.PROD}/testing_stage1/"

#Samples for second stage training
#loc.TRAIN2 = f"{loc.PROD}/Training_4stage2/"
loc.TRAIN2 = f"{loc.PROD}/training_stage2/"


#Samples for final analysis
loc.ANALYSIS = f"{loc.PROD}/analysis_stage2/"

#Samples for background composition survey
loc.EXTRA = f"{loc.PROD}/analysis_extra_bkg_composition"


FCC_label = '\\textbf{FCC-ee Simulation (IDEA Delphes)}'

#First stage BDT including event-level vars
train_vars = ["EVT_ThrustEmin_E",
              "EVT_ThrustEmax_E",
              "EVT_ThrustEmin_Echarged",
              "EVT_ThrustEmax_Echarged",
              "EVT_ThrustEmin_Eneutral",
              "EVT_ThrustEmax_Eneutral",
              "EVT_ThrustEmin_Ncharged",
              "EVT_ThrustEmax_Ncharged",
              "EVT_ThrustEmin_Nneutral",
              "EVT_ThrustEmax_Nneutral"
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
mode_names = {"Bc2TauNu": "p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU",
              "Bu2TauNu": "p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU",
              "uds": "p8_ee_Zuds_ecm91",
              "cc": "p8_ee_Zcc_ecm91",
              "bb": "p8_ee_Zbb_ecm91"
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

# test stage2 including information on D-meson-like vertex
train_vars_2_Dvtx = ["EVT_CandMass",
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
                     "EVT_Nominal_B_E",
                     "EVT_DVmass_Dmeson_Emin", 
                     "EVT_d2PVz_Dmeson_Emin",
                     "EVT_d2PVd0_Dmeson_Emin"
                    ]


train_vars_2_Dvtx_trim1 = ["EVT_CandMass",
                           "EVT_CandRho1Mass",
                           "EVT_CandRho2Mass",
                           "EVT_CandN",
                           "EVT_CandVtxFD",
                           "EVT_CandP",
                           "EVT_CandPz",
                           "EVT_CandD0",
                           "EVT_CandAngleThrust",
                           "EVT_DVd0_min",
                           "EVT_DVd0_max",
                           "EVT_DVz0_min",
                           "EVT_DVz0_max",
                           "EVT_PVmass",
                           "EVT_Nominal_B_E",
                           "EVT_DVmass_Dmeson_Emin",
                           "EVT_d2PVz_Dmeson_Emin",
                           "EVT_d2PVd0_Dmeson_Emin"
                          ]


#Hemipshere energy difference cut, applied offline prior to MVA2 optimisation
Ediff_cut = "10."

#Different cuts for MVA category and bkg estimate
MVA_cuts = {}
MVA_cuts['base']   = {"MVA1": 0.9,  "MVA2_bkg": 0.9, "MVA2_sig": 0.6}
MVA_cuts['tight']  = {"MVA1": 0.99, "MVA2_bkg": 0.95, "MVA2_sig": 0.6}
MVA_cuts['spline'] = {"MVA1_in_bu":     {"xmin": -np.log(1. - MVA_cuts['tight']['MVA1']), "xmax": 10},      # e^-10 ~ 0.00005
                      "MVA1_in_bc":     {"xmin": -np.log(1. - MVA_cuts['tight']['MVA1']), "xmax": 10},     # e^-9  ~ 0.0001
                      "MVA2_sig_in_bu": {"xmin": -np.log(1. - MVA_cuts['tight']['MVA2_sig']), "xmax": 6},      # e^-7  ~ 0.001 
                      "MVA2_sig_in_bc": {"xmin": -np.log(1. - MVA_cuts['tight']['MVA2_sig']), "xmax": 6},
                      "MVA2_bkg_in_bu": {"xmin": -np.log(1. - MVA_cuts['tight']['MVA2_bkg']), "xmax": 7},   # e^-3 ~ 0.05
                      "MVA2_bkg_in_bc": {"xmin": -np.log(1. - MVA_cuts['tight']['MVA2_bkg']), "xmax": 8}    # e^-8 ~ 0.0003
                     } 
# xmin does not have to start from the tight cut, as efficiencies are always calculated with the correct passing value
# xmax has to end at the limit (close to 1.0), otherwise the rest of the good events will not be included


MVA_cuts['sig_cut_for_bkg_scan'] = {#"bu": [0.95],
                                    #"bc": [0.95],
                                    #IMPORTANT: these values must be tighter than the baseline and looser than the scanning range
                                    "bu": [0.965, 0.966, 0.967, 0.968, 0.969, 0.97, 0.971, 0.972, 0.973, 0.974, 0.975, 0.976, 0.977, 0.978, 0.979, 0.98], 
                                    "bc": [0.95, 0.951, 0.952, 0.953, 0.954, 0.955, 0.956, 0.957, 0.958, 0.959, 0.96, 0.961, 0.962, 0.963, 0.964, 0.965]
                                   }


Eff = {}
#Eff['base'] =  {"bu": {"Zbb": 3.005e-5, "Zcc": 5.642e-6},  # 29445 inc bb events, 5642 inc cc events after baseline cut for bu cat
#                "bc": {"Zbb": 9.278e-6, "Zcc": 2.576e-6},  #  9092 inc bb events, 2576 inc cc events after baseline cut for bc cat
#               } 
#Eff['tight'] = {"bu": {"Zbb": 1.091e-1, "Zcc": 6.770e-2},  # 90895 total exc bb events,  511 total exc cc events after baseline cut for bu cat
#                "bc": {"Zbb": 1.156e-1, "Zcc": 1.565e-1},  # 27124 total exc bb events, 2822 total exc cc events after baseline cut for bc cat
#               }

Eff['base'] =  {"bu": {"Zbb": 2.756e-5, "Zcc": 5.794e-6},  # 27004 inc bb events, 5794 inc cc events after baseline cut for bu cat
                "bc": {"Zbb": 1.992e-5, "Zcc": 4.634e-6},  # 19526 inc bb events, 4634 inc cc events after baseline cut for bc cat
               }
Eff['tight'] = {"bu": {"Zbb": 7.389e-2, "Zcc": 7.628e-2},  # 68087 total exc bb events, 1651 total exc cc events after baseline cut for bu cat
                "bc": {"Zbb": 1.388e-1, "Zcc": 1.974e-1},  # 82727 total exc bb events, 9220 total exc cc events after baseline cut for bc cat
               }



#Number of bins to use in MVA spline fit 
NBin_MVA_fit = {'MVA1': 1000, 'MVA2_sig': 300, 'MVA2_bkg': 300} # could use less bins for MVA2, but does not take any resource (finishes in 1 second)
Nsig_min = 10000.


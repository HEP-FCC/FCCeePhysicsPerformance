import os
#repo = os.getenv('PWD')
repo = "/afs/cern.ch/work/d/dhill/Bc2TauNu"
#repo can be changed, but by default writes locally
class loc : pass
loc.ROOT = repo+'/'
loc.OUT = loc.ROOT+'output/'
loc.DATA = loc.ROOT+'data'
loc.CSV = loc.DATA+'/csv'
loc.PKL = loc.DATA+'/pkl'
loc.ROOTFILES = loc.DATA+'/ROOT'
loc.PLOTS = loc.OUT+'plots'
loc.TEX = loc.OUT+'tex'
loc.JSON = loc.OUT+'json'

#EOS location for files used in analysis
loc.EOS = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu"

#Output BDT model location - used in official sample production to assign MVA weights
loc.BDT = loc.EOS+""

#Loaction of prod_04 tuples used in analysis
loc.PROD = f"{loc.EOS}/flatNtuples/spring2021/prod_04"

#Samples for first stage BDT training
loc.TRAIN = f"{loc.PROD}/Batch_Training_4stage1/"

#Samples for second stage training
loc.TRAIN2 = f"{loc.PROD}/Training_4stage2/"

#Samples for final analysis
loc.ANALYSIS = f"{loc.PROD}/Analysis_stage2/"

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

#Hemipshere energy difference cut, applied offline prior to MVA2 optimisation
Ediff_cut = ">10."

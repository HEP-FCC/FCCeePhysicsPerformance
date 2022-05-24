#python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
from config.common_defaults import deffccdicts

import sys, os

#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/user/l/lia/FCCee/MVA/flatNtuples"

#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/user/l/lia/FCCee/MVA/flatNtuples/final"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"
#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
procDictAdd={"MySample_p8_ee_ZH_ecm240":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.201868, "kfactor": 1.0, "matchingEfficiency": 1.0}}
###Process list that should match the produced files.
processList=['p8_ee_ZZ_ecm240',
              'p8_ee_WW_mumu_ecm240',
              'wzp6_ee_mumuH_ecm240',
              'wzp6_ee_mumu_ecm240',
              'wzp6_egamma_eZ_Zmumu_ecm240',
              'wzp6_gammae_eZ_Zmumu_ecm240']

###Add MySample_p8_ee_ZH_ecm240 as it is not an offical process

#Number of CPUs to use
nCPUS = 2
#produces ROOT TTrees, default is False
doTree = False
###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {"sel0":"return true;",
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mz":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom1":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":200,"xmin":80,"xmax":100},
    "mz_zoom2":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":100,"xmin":86,"xmax":96},
    "mz_zoom3":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":250,"xmin":75,"xmax":100},
    "mz_zoom4":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":235,"xmin":73,"xmax":120},
    "leptonic_recoil_m":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom1":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":80,"xmax":160},
    "leptonic_recoil_m_zoom2":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom3":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom4":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":70,"xmin":123,"xmax":130},
    "selected_muons_delta_max":{"name":"selected_muons_delta_max","title":"selected_muons_delta_max","bin":100,"xmin":0,"xmax":5},
    "selected_muons_delta_min":{"name":"selected_muons_delta_min","title":"selected_muons_delta_min","bin":100,"xmin":0,"xmax":5},
    "selected_muons_delta_avg":{"name":"selected_muons_delta_avg","title":"selected_muons_delta_avg","bin":100,"xmin":0,"xmax":5},
    "muon_leading_pt":{"name":"muon_leading_pt","title":"muon_leading_pt","bin":100,"xmin":0,"xmax":100},
    "muon_leading_px":{"name":"muon_leading_px","title":"muon_leading_px","bin":100,"xmin":0,"xmax":100},
    "muon_leading_py":{"name":"muon_leading_py","title":"muon_leading_py","bin":100,"xmin":0,"xmax":100},
    "muon_leading_pz":{"name":"muon_leading_pz","title":"muon_leading_pz","bin":100,"xmin":0,"xmax":100},
    "muon_leading_eta":{"name":"muon_leading_eta","title":"muon_leading_eta","bin":100,"xmin":-10,"xmax":10},
    "muon_leading_phi":{"name":"muon_leading_phi","title":"muon_leading_phi","bin":100,"xmin":-5,"xmax":5},
    "muon_leading_y":{"name":"muon_leading_y","title":"muon_leading_y","bin":100,"xmin":-10,"xmax":10},
    "muon_leading_p":{"name":"muon_leading_p","title":"muon_leading_p","bin":100,"xmin":0,"xmax":100}, 
    "muon_leading_e":{"name":"muon_leading_e","title":"muon_leading_e","bin":100,"xmin":0,"xmax":100},
    "muon_leading_m":{"name":"muon_leading_m","title":"muon_leading_m","bin":100,"xmin":0,"xmax":2}, 
    "muon_leading_theta":{"name":"muon_leading_theta","title":"muon_subleading_theta","bin":100,"xmin":-5,"xmax":5},
    "muon_subleading_pt":{"name":"muon_subleading_pt","title":"muon_subleading_pt","bin":100,"xmin":0,"xmax":100},
    "muon_subleading_px":{"name":"muon_subleading_px","title":"muon_subleading_px","bin":100,"xmin":0,"xmax":100},
    "muon_subleading_py":{"name":"muon_subleading_py","title":"muon_subleading_py","bin":100,"xmin":0,"xmax":100},
    "muon_subleading_pz":{"name":"muon_subleading_pz","title":"muon_subleading_pz","bin":100,"xmin":0,"xmax":100}, 
    "muon_subleading_eta":{"name":"muon_subleading_eta","title":"muon_subleading_eta","bin":100,"xmin":-10,"xmax":10},
    "muon_subleading_phi":{"name":"muon_subleading_phi","title":"muon_subleading_phi","bin":100,"xmin":-5,"xmax":5},
    "muon_subleading_y":{"name":"muon_subleading_y","title":"muon_subleading_y","bin":100,"xmin":-10,"xmax":10},
    "muon_subleading_p":{"name":"muon_subleading_p","title":"muon_subleading_p","bin":100,"xmin":0,"xmax":100}, 
    "muon_subleading_e":{"name":"muon_subleading_e","title":"muon_subleading_e","bin":100,"xmin":0,"xmax":100},
    "muon_subleading_m":{"name":"muon_subleading_m","title":"muon_subleading_m","bin":100,"xmin":0,"xmax":2}, 
    "muon_subleading_theta":{"name":"muon_subleading_theta","title":"muon_subleading_theta","bin":100,"xmin":-5,"xmax":5},
    #Zed
    "Z_leptonic_m":{"name":"Z_leptonic_m","title":"Z_leptonic_m","bin":100,"xmin":0,"xmax":200},      
    "Z_leptonic_pt":{"name":"Z_leptonic_pt","title":"Z_leptonic_pt","bin":100,"xmin":0,"xmax":100},    
    "Z_leptonic_y":{"name":"Z_leptonic_y","title":"Z_leptonic_y","bin":100,"xmin":-10,"xmax":10},  
    "Z_leptonic_p":{"name":"Z_leptonic_p","title":"Z_leptonic_p","bin":100,"xmin":0,"xmax":100},     
    "Z_leptonic_e":{"name":"Z_leptonic_e","title":"Z_leptonic_e","bin":100,"xmin":0,"xmax":5},    
    "Z_leptonic_px":{"name":"Z_leptonic_px","title":"Z_leptonic_px","bin":100,"xmin":0,"xmax":100},   
    "Z_leptonic_py":{"name":"Z_leptonic_py","title":"Z_leptonic_py","bin":100,"xmin":0,"xmax":100},   
    "Z_leptonic_pz":{"name":"Z_leptonic_pz","title":"Z_leptonic_pz","bin":100,"xmin":0,"xmax":100},   
    "Z_leptonic_eta":{"name":"Z_leptonic_eta","title":"Z_leptonic_eta","bin":100,"xmin":-10,"xmax":10},
    "Z_leptonic_theta":{"name":"Z_leptonic_theta","title":"Z_leptonic_theta","bin":100,"xmin":-5,"xmax":5}, 
    "Z_leptonic_phi":{"name":"Z_leptonic_phi","title":"Z_leptonic_phi","bin":100,"xmin":-5,"xmax":5},
    #Recoil
    "zed_leptonic_recoil_m":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200}
        
}


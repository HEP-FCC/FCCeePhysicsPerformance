#python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py

from config.common_defaults import deffccdicts

import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "/eos/user/l/lia/FCCee/MVA/trainedNtuples/"

###Link to the dictonary that contains all the cross section informations etc...
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_spring2021_IDEA.json"

###Process list that should match the produced files.
process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','wzp6_ee_mumuH_ecm240','p8_ee_Zll_ecm240']

###Add MySample_p8_ee_ZH_ecm240 as it is not an offical process

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"return true;",
            "sel_MV02":"MVAScore1>0.2;",
            "sel_MV06":"MVAScore1>0.6;",
            "sel_Baseline":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel_Baseline_MVA02":"MVAScore1>0.2 && zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel_Baseline_MVA06":"MVAScore1>0.6 && zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98" 
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "mz":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":125,"xmin":0,"xmax":250},
    "mz_zoom1":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":200,"xmin":80,"xmax":100},
    "mz_zoom2":{"name":"Z_leptonic_m","title":"m_{Z} [GeV]","bin":100,"xmin":86,"xmax":96},
    "leptonic_recoil_m":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom1":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":80,"xmax":160},
    "leptonic_recoil_m_zoom2":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":100,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom3":{"name":"zed_leptonic_recoil_m","title":"Z leptonic recoil [GeV]","bin":200,"xmin":120,"xmax":140},

}

###Number of CPUs to use
NUM_CPUS = 2

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)

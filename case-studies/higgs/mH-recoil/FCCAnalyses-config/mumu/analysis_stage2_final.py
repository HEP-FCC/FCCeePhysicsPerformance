#python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py
#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/user/l/lia/FCCee/MVA/flatNtuples_stage2"

#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/user/l/lia/FCCee/MVA/flatNtuples_stage2/final"

###Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"
#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
procDictAdd={"MySample_p8_ee_ZH_ecm240":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.201868, "kfactor": 1.0, "matchingEfficiency": 1.0}}
###Process list that should match the produced files.
processList=[
             "wzp6_ee_mumuH_ecm240",
             "wzp6_ee_mumuH_mH-lower-50MeV_ecm240",
             "wzp6_ee_mumuH_mH-lower-100MeV_ecm240",
             "wzp6_ee_mumuH_mH-higher-100MeV_ecm240",
             "wzp6_ee_mumuH_mH-higher-50MeV_ecm240",
          
             "wzp6_ee_mumuH_noISR_ecm240",
             "wzp6_ee_mumuH_noFSR_ecm240",
          
             "wzp6_ee_mumuH_BES-higher-6pc_ecm240",  
             "wzp6_ee_mumuH_BES-lower-6pc_ecm240",
             "wzp6_ee_mumuH_BES-higher-1pc_ecm240",
             "wzp6_ee_mumuH_BES-lower-1pc_ecm240",

             "wzp6_ee_tautauH_ecm240",
             "wzp6_ee_eeH_ecm240",
             "wzp6_ee_nunuH_ecm240",
             "wzp6_ee_qqH_ecm240",

             "p8_ee_WW_mumu_ecm240",
             "p8_ee_ZZ_ecm240",
             "wzp6_ee_mumu_ecm240",

             "wzp6_egamma_eZ_Zmumu_ecm240",
             "wzp6_gammae_eZ_Zmumu_ecm240",
             "wzp6_gaga_mumu_60_ecm240",
             "wzp6_gaga_tautau_60_ecm240"]

###Add MySample_p8_ee_ZH_ecm240 as it is not an offical process

#Number of CPUs to use
nCPUS = 2
#produces ROOT TTrees, default is False
doTree = False

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {#"sel0":"return true;",
            #"sel_MVA08":"MVAScore0>0.8;",
            #"sel_Baseline":"zed_leptonic_m.size()==1 &&  zed_leptonic_m[0]> 86 && zed_leptonic_m[0]  < 96 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && zed_leptonic_pt[0]  > 20 && zed_leptonic_pt[0]  <70 &&cosTheta_miss.size() ==1 && cosTheta_miss[0]  > -0.98 && cosTheta_miss[0]  < 0.98",
            "sel_MRecoil_Mll_73_120_pTll_05_MVA08":"MVAScore0>0.8 &&   zed_leptonic_m.size()==1 &&  zed_leptonic_m[0]> 73 && zed_leptonic_m[0]  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && zed_leptonic_pt[0]  > 5",
            "sel_MRecoil_Mll_73_120_pTll_05_MVA09":"MVAScore0>0.9 &&   zed_leptonic_m.size()==1 &&  zed_leptonic_m[0]> 73 && zed_leptonic_m[0]  < 120 &&zed_leptonic_recoil_m.size()==1 && zed_leptonic_recoil_m[0]  > 120 &&zed_leptonic_recoil_m[0]  <140 && zed_leptonic_pt[0]  > 5"
            }


###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
                "selected_muons_pt":{"name": "selected_muons_pt", "title": "selected_muons_pt", "bin": 20000, "xmin": 0, "xmax": 200 },
                "selected_muons_pt_muscaleup":{"name": "selected_muons_pt_muscaleup", "title": "selected_muons_pt_muscaleup", "bin": 20000, "xmin": 0, "xmax": 200 },
                "selected_muons_pt_muscaledw":{"name": "selected_muons_pt_muscaledw", "title": "selected_muons_pt_muscaledw", "bin": 20000, "xmin": 0, "xmax": 200 },

                "selected_muons_no":{"name": "selected_muons_no", "title": "selected_muons_no", "bin": 10, "xmin": 0, "xmax": 10 },

                "zed_leptonic_m":{"name": "zed_leptonic_m", "title": "zed_leptonic_m", "bin":300000,"xmin":0,"xmax":300 },
                "zed_leptonic_m_muscaleup":{"name": "zed_leptonic_m_muscaleup", "title": "zed_leptonic_m_muscaleup", "bin":300000,"xmin":0,"xmax":300 },
                "zed_leptonic_m_muscaledw":{"name": "zed_leptonic_m_muscaledw", "title": "zed_leptonic_m_muscaledw", "bin":300000,"xmin":0,"xmax":300 },

                "zed_leptonic_n":{"name": "zed_leptonic_n", "title": "zed_leptonic_no", "bin":10,"xmin":0,"xmax":10 },
                "zed_leptonic_no_muscaleup":{"name": "zed_leptonic_no_muscaleup", "title": "zed_leptonic_no_muscaleup", "bin":10,"xmin":0,"xmax":10 },
                "zed_leptonic_no_muscaledw":{"name": "zed_leptonic_no_muscaledw", "title": "zed_leptonic_no_muscaledw", "bin":10,"xmin":0,"xmax":10 },

                "zed_leptonic_pt":{"name": "zed_leptonic_pt", "title": "zed_leptonic_pt", "bin":200000,"xmin":0,"xmax":200 },
                "zed_leptonic_pt_muscaleup":{"name": "zed_leptonic_pt_muscaleup", "title": "zed_leptonic_pt_muscaleup", "bin":200000,"xmin":0,"xmax":200 },
                "zed_leptonic_pt_muscaledw":{"name": "zed_leptonic_pt_muscaledw", "title": "zed_leptonic_pt_muscaledw", "bin":200000,"xmin":0,"xmax":200 },

                "zed_leptonic_recoil_m":{"name": "zed_leptonic_recoil_m", "title": "zed_leptonic_recoil_m", "bin":200000,"xmin":0,"xmax":200 },
                "zed_leptonic_recoil_m_muscaleup":{"name": "zed_leptonic_recoil_m_muscaleup", "title": "zed_leptonic_recoil_m_muscaleup", "bin":200000,"xmin":0,"xmax":200 },
                "zed_leptonic_recoil_m_muscaledw":{"name": "zed_leptonic_recoil_m_muscaledw", "title": "zed_leptonic_recoil_m_muscaledw", "bin":200000,"xmin":0,"xmax":200 },
                "zed_leptonic_recoil_m_sqrtsup":{"name": "zed_leptonic_recoil_m_sqrtsup", "title": "zed_leptonic_recoil_m_sqrtsup", "bin":200000,"xmin":0,"xmax":200 },
                "zed_leptonic_recoil_m_sqrtsdw":{"name": "zed_leptonic_recoil_m_sqrtsdw", "title": "zed_leptonic_recoil_m_sqrtsdw", "bin":200000,"xmin":0,"xmax":200 },

                "cosTheta_miss":{"name": "cosTheta_miss", "title": "cosTheta_miss", "bin":100000,"xmin":-1,"xmax":1 },
                #hists["sf_kkmcp8_wzp6"]                     = {"name": "sf_kkmcp8_wzp6", "title": "", "bin":4000,"xmin":0.8,"xmax":1.2 }
}




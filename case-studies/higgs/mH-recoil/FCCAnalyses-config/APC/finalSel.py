#python examples/FCCee/higgs/mH-recoil/mumu/finalSel.py 

from config.common_defaults import deffccdicts

import sys, os
import ROOT

###Input directory where the files produced at the pre-selection level are
baseDir  = "outputs/FCCee/higgs/mH-recoil/mumu/"

###Link to the dictonary that contains all the cross section informations etc...
#procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_fcc_tmp.json"
procDict = os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "FCCee_procDict_spring2021_IDEA.json"
#procDict = "/afs/cern.ch/work/l/lia/private/FCC/test/FCCAnalyses_0519/FCCee_procDict_spring2021_IDEA.json"
#process_list=['p8_ee_ZH_ecm240']
#process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']
#process_list=['p8_noBES_ee_ZZ_ecm240','p8_noBES_ee_WW_ecm240','p8_noBES_ee_ZH_ecm240']
#process_list=['p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','p8_ee_ZH_ecm240']
#process_list=['wzp6_ee_mumuH_ecm240_v2']
#process_list=['p8_ee_Zqq_ecm240','p8_ee_Zll_ecm240','p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','p8_ee_ZH_ecm240']
#process_list=['wzp6_gammae_eZ_Zmumu_ecm240','wzp6_egamma_eZ_Zmumu_ecm240','p8_ee_Zqq_ecm240','p8_ee_Zll_ecm240','p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','wzp6_ee_mumuH_ecm240','wzp6_ee_tautauH_ecm240','wzp6_ee_qqH_ecm240']
process_list=['p8_ee_ZH_ecm240','wzp6_gaga_mumu_60_ecm240','wzp6_gaga_tautau_60_ecm240','wzp6_gammae_eZ_Zmumu_ecm240','wzp6_egamma_eZ_Zmumu_ecm240','p8_ee_Zqq_ecm240','p8_ee_Zll_ecm240','p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','wzp6_ee_mumuH_ecm240','wzp6_ee_tautauH_ecm240','wzp6_ee_qqH_ecm240','wzp6_ee_nunuH_ecm240','wzp6_ee_eeH_ecm240']
#process_list=['wzp6_gaga_mumu_60_ecm240','wzp6_gaga_tautau_60_ecm240','wzp6_gammae_eZ_Zmumu_ecm240','wzp6_egamma_eZ_Zmumu_ecm240','p8_ee_Zqq_ecm240','p8_ee_Zll_ecm240','p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','p8_ee_ZH_ecm240']
ROOT.gInterpreter.Declare("""
bool myFilter(ROOT::VecOps::RVec<float> z_mass,ROOT::VecOps::RVec<float> muon_pT,ROOT::VecOps::RVec<TLorentzVector> muon_tlv) {
  //cout << "begin" << endl;
  //cout << "z_mass.size() = " << z_mass.size() << endl;
  //cout << "z" << endl;
  //if(z_mass.size()>1||z_mass.size()<1) return false;
  if(z_mass.size()<2) return false;
  //cout << "e" << endl;
  //if (z_mass.at(0)<80. || z_mass.at(0)>100.) return false;
  //cout << "c" << endl;
  //for (ROOT::VecOps::RVec<float>::iterator it = muon_pT.begin(); it != muon_pT.end(); ++it){
  //for (size_t i = 0; i < muon_pT.size(); ++i){
  //  if (muon_pT.at(i) < 20){
  //    return false;
  //  }
  //}
  //cout << "d" << endl;
  //if (muon_tlv.size()!=2) return false;
  //cout << "a" << endl;
  //float angle = (muon_tlv.at(0).Px()*muon_tlv.at(1).Px()+muon_tlv.at(0).Py()*muon_tlv.at(1).Py()+muon_tlv.at(0).Pz()*muon_tlv.at(1).Pz())/(muon_tlv.at(0).P()*muon_tlv.at(1).P());
  //cout << "b" << endl;
  //if (angle < -0.99619469809) return false;
  return true;
}
""")

ROOT.gInterpreter.Declare("""
bool myFilter1(ROOT::VecOps::RVec<float> mass) {
  if (mass.size()<2) return false;
  for (size_t i = 0; i < mass.size(); ++i) {
  if (mass.at(i)<80. || mass.at(i)>100.)
    return false;
  }
  return true;
}
""")

ROOT.gInterpreter.Declare("""
bool pTmuFilter(ROOT::VecOps::RVec<float> pTmuon, float min) {
  for (size_t i = 0; i < pTmuon.size(); ++i) {
    if (pTmuon.at(i) < min){
      return false;
    }
  }
  return true;
}
""")

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cut_list = {"sel0":"return true;",
            "sel1":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100",
            "sel2":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 40 && zed_leptonic_recoil_m[0] <160 ",
            "sel3":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 40 && zed_leptonic_recoil_m[0] <160 && zed_leptonic_pt[0] > 20",
            "sel4":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 ",
            "sel5":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_recoil_m[0] <140 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel6":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20",
            "sel7":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <100 " ,
            "sel8":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <80 " ,
            "sel9":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 " ,
            "sel10":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel11":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 124 && zed_leptonic_recoil_m[0] <126 ",
            "sel12":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 80 &&  zed_leptonic_m[0] < 100 && zed_leptonic_recoil_m[0] > 124 && zed_leptonic_recoil_m[0] <126 && zed_leptonic_pt[0] > 20",
            "sel13":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96",
            "sel14":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 40 && zed_leptonic_recoil_m[0] <160 ",
            "sel15":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 40 && zed_leptonic_recoil_m[0] <160 && zed_leptonic_pt[0] > 20",
            "sel16":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 ",
            "sel17":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel18":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20",
            "sel19":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel20":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <100 ",
            "sel21":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <80 ",
            "sel22":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 ",
            "sel23":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel24":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 124 && zed_leptonic_recoil_m[0] <126 ",
            "sel25":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_recoil_m[0] > 124 && zed_leptonic_recoil_m[0] <126 && zed_leptonic_pt[0] > 20",
            "sel26":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 73 &&  zed_leptonic_m[0] < 120 && zed_leptonic_recoil_m[0] > 110 && zed_leptonic_recoil_m[0] <155 && zed_leptonic_pt[0] > 10 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel27":"zed_leptonic_m.size() == 1 && zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",
            "sel28":"zed_leptonic_m.size() == 1 && zed_leptonic_recoil_m[0] > 120 && zed_leptonic_recoil_m[0] <140 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98",  
            "sel29":"zed_leptonic_m.size() == 1 && zed_leptonic_recoil_m[0] > 124 && zed_leptonic_recoil_m[0] <126 && zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] <70 && missingET_costheta.size() ==1 && missingET_costheta[0] > -0.98 && missingET_costheta[0] < 0.98"
    }



###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
variables = {
    "MET_costheta":{"name":"missingET_costheta","title":"cos#theta_{missing}","bin":200,"xmin":-1,"xmax":1},
    "Nmu_plus":{"name":"selected_muons_plus_n","title":"muon plus number","bin":12,"xmin":-1.5,"xmax":10.5},
    "Nmu_minus":{"name":"selected_muons_minus_n","title":"muon minus number","bin":12,"xmin":-1.5,"xmax":10.5},
    "Nmu":{"name":"selected_muons_n","title":"muon number","bin":12,"xmin":-1.5,"xmax":10.5},
    "Cz":{"name":"zed_leptonic_charge","title":"Reconstructed Z charge","bin":23,"xmin":-11.5,"xmax":11.5},
    "Nz":{"name":"zed_leptonic_n","title":"#mu^{+}#mu^{-} pair number","bin":12,"xmin":-1.5,"xmax":10.5},
    "mz":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":250,"xmin":0,"xmax":250},
    "mz_zoom1":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":40,"xmin":80,"xmax":100},
    "mz_zoom2":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":470,"xmin":73,"xmax":120},
    "mz_zoom3":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":300,"xmin":80,"xmax":110},
    "mz_zoom4":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":200,"xmin":80,"xmax":100},
    "mz_zoom5":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":140,"xmin":84,"xmax":98},
    "mz_zoom6":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":100,"xmin":86,"xmax":96},
    "mz_zoom7":{"name":"zed_leptonic_m","title":"m_{#mu^{+}#mu^{-}} [GeV]","bin":470,"xmin":73,"xmax":120},
    "z_pt":{"name":"zed_leptonic_pt","title":"p_{T}^{#mu^{+}#mu^{-}} [GeV]","bin":400,"xmin":0,"xmax":150},
    "z_y":{"name":"zed_leptonic_y","title":"y^{#mu^{+}#mu^{-}} [GeV]","bin":120,"xmin":-3.0,"xmax":3.0},
    "z_p":{"name":"zed_leptonic_p","title":"p^{#mu^{+}#mu^{-}} [GeV]","bin":300,"xmin":0,"xmax":150.0},
    "z_e":{"name":"zed_leptonic_e","title":"E^{#mu^{+}#mu^{-}} [GeV]","bin":300,"xmin":0,"xmax":150.0},
    "leptonic_recoil_m":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":100,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom1":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":240,"xmin":116,"xmax":140},
    "leptonic_recoil_m_zoom2":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":200,"xmin":120,"xmax":140},
    "leptonic_recoil_m_zoom3":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":200,"xmin":116,"xmax":136},
    "leptonic_recoil_m_zoom4":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":40,"xmin":124,"xmax":128},
    "leptonic_recoil_m_zoom5":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":120,"xmin":128,"xmax":140},
    "leptonic_recoil_m_zoom6":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":300,"xmin":80,"xmax":110},
    "leptonic_recoil_m_zoom7":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":200,"xmin":80,"xmax":100},
    "leptonic_recoil_m_zoom8":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":100,"xmin":86,"xmax":96},
    "leptonic_recoil_m_zoom9":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":600,"xmin":40,"xmax":160},
    "leptonic_recoil_m_zoom10":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":400,"xmin":0,"xmax":200},
    "leptonic_recoil_m_zoom11":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":450,"xmin":110,"xmax":155},
    "leptonic_recoil_m_zoom12":{"name":"zed_leptonic_recoil_m","title":"M_{recoil} [GeV]","bin":240,"xmin":40,"xmax":160},
    "muon_y":{"name":"selected_muons_y","title":"y_{#mu}","bin":160,"xmin":-4,"xmax":4},
    "muon_pT":{"name":"selected_muons_pt","title":"p_T^{#mu} [GeV]","bin":400,"xmin":0,"xmax":200},
    "muon_p":{"name":"selected_muons_p","title":"p^{#mu} [GeV]","bin":400,"xmin":0,"xmax":200},
    "muon_costheta":{"name":"selected_muons_costheta","title":"cos#theta_{#mu}","bin":200,"xmin":-1,"xmax":1},
    "muon_e":{"name":"selected_muons_e","title":"E_{#mu} [GeV]","bin":200,"xmin":0,"xmax":100},  
    "muon_m":{"name":"selected_muons_m","title":"m_{#mu}","bin":200,"xmin":0,"xmax":100}
  }

###Number of CPUs to use
NUM_CPUS = 5

###This part is standard to all analyses
import config.runDataFrameFinal as rdf
myana=rdf.runDataFrameFinal(baseDir,procDict,process_list,cut_list,variables)
myana.run(ncpu=NUM_CPUS)

import ROOT
#Mandatory: List of processes
processList = {
    'wzp6_ee_mumuH_ecm240':{'chunks':5},
    'p8_ee_WW_mumu_ecm240':{'chunks':5},
    'wzp6_ee_mumu_ecm240':{'chunks':5},
    'p8_ee_ZZ_ecm240':{'chunks':5},
    'wzp6_egamma_eZ_Zmumu_ecm240':{'chunks':5},
    'wzp6_gammae_eZ_Zmumu_ecm240':{'chunks':5}
    #'wzp6_ee_mumuH_ecm240':{'fraction':0.1}
    }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local dir
#outputDir="/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/ZH_mumu_recoil_batch/stage1/trainedNtuples"
outputDirEos= "/eos/user/l/lia/FCCee/MVA/trainedNtuples"
eosType = "eosuser"
#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = True
#runBatch    = False
#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

userBatchConfig="/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/FCCAnalyses-config/mumu/userBatch.Config"
#USER DEFINED CODE
ROOT.gInterpreter.ProcessLine('''
    TMVA::Experimental::RBDT<> bdt("ZH_Recoil_BDT", "/eos/user/l/lia/FCCee/MVA/BDT/xgb_bdt_normal.root");
    computeModel1 = TMVA::Experimental::Compute<25, float>(bdt);
    ''')
#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df
            #############################################
            ## Alias for muon and MC truth informations##
            #############################################
            .Alias("Muon0", "Muon#0.index")
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            
            
            ##-----------------------------------------##
            ##     Build Trust                         ##
            ##-----------------------------------------##
            .Define("stable",  "FCCAnalyses::MCParticle::sel_genStatus(2) (Particle)")
            ###
            #Muon
            ###
            .Define("theGenLevelMuminus",  "FCCAnalyses::MCParticle::sel_pdgID( 13, false) (stable)")
            .Define("theGenLevelMuplus",  "FCCAnalyses::MCParticle::sel_pdgID( -13, false) (stable)")
            .Define("theGenLevelMuminus_tlv", "FCCAnalyses::MCParticle::get_tlv(theGenLevelMuminus) ")
            .Define("theGenLevelMuplus_tlv", "FCCAnalyses::MCParticle::get_tlv(theGenLevelMuplus) ")
            ###
            #Higgs
            ###
            .Define("theGenLevelHiggs", "FCCAnalyses::MCParticle::sel_pdgID( 25, false) (stable)")
            .Define("theGenLevelHiggs_tlv", "FCCAnalyses::MCParticle::get_tlv(theGenLevelHiggs) ")
            
            ###
            #mumu
            ###
            .Define("gen_pt_mumu", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1) return  float((theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0]).Pt()); else return -std::numeric_limits<float>::max() ")
            .Define("gen_mass_mumu", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1) return float((theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0]).M()); else return -std::numeric_limits<float>::max() ")
            ###
            #ZH
            ###
            .Define("gen_pt_ZH", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1 && theGenLevelHiggs_tlv.size()==1) return float(( theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0] + theGenLevelHiggs_tlv[0] ).Pt()); else return -std::numeric_limits<float>::max()" )
            .Define("gen_mass_ZH", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1 && theGenLevelHiggs_tlv.size()==1) return float(( theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0] + theGenLevelHiggs_tlv[0] ).M()); else return -std::numeric_limits<float>::max()")             
            
            ##-----------------------------------------##
            ##          ReconstrucedParticle           ##
            ##-----------------------------------------##
            
            ###
            #Missinginformstion 
            ###
            .Define('missingET_costheta', 'APCHiggsTools::get_cosTheta(MissingET)')
            ###
            #Muon
            ###
            # define the muon collection
            .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            #.Filter("muon_check(muons)")
            #.Define("selected_muons", "return muons") 
            .Define("selected_muons", "APCHiggsTools::muon_quality_check(muons)")
            .Define("selected_muons_plus", "ReconstructedParticle::sel_charge(1.0,false)(selected_muons)")
            .Define("selected_muons_minus", "ReconstructedParticle::sel_charge(-1.0,false)(selected_muons)")
            .Define("selected_muons_plus_n", "ReconstructedParticle::get_n(selected_muons_plus)")
            .Define("selected_muons_minus_n", "ReconstructedParticle::get_n(selected_muons_minus)")
            .Define("selected_muons_plus_pt", "ReconstructedParticle::get_pt(selected_muons_plus)")
            .Define("selected_muons_minus_pt", "ReconstructedParticle::get_pt(selected_muons_minus)")
            .Define("selected_muons_n", "ReconstructedParticle::get_n(selected_muons)")
            .Define("selected_muons_pt", "ReconstructedParticle::get_pt(selected_muons)")
            .Define("selected_muons_y",  "ReconstructedParticle::get_y(selected_muons)")
            .Define("selected_muons_p",     "ReconstructedParticle::get_p(selected_muons)")
            .Define("selected_muons_e",     "ReconstructedParticle::get_e(selected_muons)")
            .Define("selected_muons_m",     "ReconstructedParticle::get_mass(selected_muons)")
            .Define("selected_muons_costheta",  "APCHiggsTools::get_cosTheta(selected_muons)")
            .Define("selected_muons_delta_max", "ReconstructedParticle::angular_separationBuilder(0)(selected_muons)")
            .Define("selected_muons_delta_min", "ReconstructedParticle::angular_separationBuilder(1)(selected_muons)")
            .Define("selected_muons_delta_avg", "ReconstructedParticle::angular_separationBuilder(2)(selected_muons)") 
            .Define("sorted_muons",  "APCHiggsTools::sort_greater(selected_muons)")
            .Define("sorted_muons_pt",  "ReconstructedParticle::get_pt(sorted_muons)")
            .Define("sorted_muons_px",  "ReconstructedParticle::get_px(sorted_muons)") 
            .Define("sorted_muons_py",  "ReconstructedParticle::get_py(sorted_muons)")
            .Define("sorted_muons_pz",  "ReconstructedParticle::get_pz(sorted_muons)")
            .Define("sorted_muons_y",  "ReconstructedParticle::get_y(sorted_muons)")
            .Define("sorted_muons_eta",     "ReconstructedParticle::get_eta(sorted_muons)")
            .Define("sorted_muons_phi",     "ReconstructedParticle::get_phi(sorted_muons)") 
            .Define("sorted_muons_p",     "ReconstructedParticle::get_p(sorted_muons)")
            .Define("sorted_muons_e",     "ReconstructedParticle::get_e(sorted_muons)")
            .Define("sorted_muons_m",     "ReconstructedParticle::get_mass(sorted_muons)")
            .Define("sorted_muons_theta",  "ReconstructedParticle::get_theta(sorted_muons)")
            .Define("muon_leading_pt",  "return sorted_muons_pt.at(0)")
            .Define("muon_leading_px",  "return sorted_muons_px.at(0)")
            .Define("muon_leading_py",  "return sorted_muons_py.at(0)")
            .Define("muon_leading_pz",  "return sorted_muons_pz.at(0)") 
            .Define("muon_leading_eta",  "return sorted_muons_eta.at(0)")
            .Define("muon_leading_phi",  "return sorted_muons_phi.at(0)") 
            .Define("muon_leading_y",  "return sorted_muons_y.at(0)")
            .Define("muon_leading_p",  "return sorted_muons_p.at(0)")
            .Define("muon_leading_e",  "return sorted_muons_e.at(0)")
            .Define("muon_leading_m",  "return sorted_muons_m.at(0)")
            .Define("muon_leading_theta",  "return sorted_muons_theta.at(0)")
            .Define("muon_subleading_pt",  "return sorted_muons_pt.at(1)")
            .Define("muon_subleading_px",  "return sorted_muons_px.at(1)")
            .Define("muon_subleading_py",  "return sorted_muons_py.at(1)")
            .Define("muon_subleading_pz",  "return sorted_muons_pz.at(1)") 
            .Define("muon_subleading_eta",  "return sorted_muons_eta.at(1)")
            .Define("muon_subleading_phi",  "return sorted_muons_phi.at(1)")  
            .Define("muon_subleading_y",  "return sorted_muons_y.at(1)")
            .Define("muon_subleading_p",  "return sorted_muons_p.at(1)")
            .Define("muon_subleading_e",  "return sorted_muons_e.at(1)")
            .Define("muon_subleading_m",  "return sorted_muons_m.at(1)")
            .Define("muon_subleading_theta",  "return sorted_muons_theta.at(1)")


            #.Define("Selected_muons_plus_pt", "if(selected_muons_plus_pt.size()>0) return selected_muons_plus_pt.at(0); else return -std::numeric_limits<float>::max()")
            #.Define("Selected_muons_minus_pt", "if(selected_muons_plus_pt.size()>0) return selected_muons_minus_pt.at(0); else return -std::numeric_limits<float>::max()")
            ###
            #Rconstruct Zed from Z->mumu
            ###
            .Define("zed_leptonic",         "APCHiggsTools::resonanceZBuilder(91)(selected_muons)")
            .Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
            .Define("zed_leptonic_n",       "ReconstructedParticle::get_n(zed_leptonic)")
            .Define("zed_leptonic_charge",   "ReconstructedParticle::get_charge(zed_leptonic)")
            .Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
            .Define("zed_leptonic_y",      "ReconstructedParticle::get_y(zed_leptonic)")
            .Define("zed_leptonic_p",      "ReconstructedParticle::get_p(zed_leptonic)")
            .Define("zed_leptonic_e",      "ReconstructedParticle::get_e(zed_leptonic)")
            .Define("zed_leptonic_costheta",  "APCHiggsTools::get_cosTheta(zed_leptonic)")
            .Define("zed_leptonic_px",      "ReconstructedParticle::get_px(zed_leptonic)")
            .Define("zed_leptonic_py",      "ReconstructedParticle::get_py(zed_leptonic)")
            .Define("zed_leptonic_pz",      "ReconstructedParticle::get_pz(zed_leptonic)")
            .Define("zed_leptonic_eta",      "ReconstructedParticle::get_eta(zed_leptonic)")
            .Define("zed_leptonic_theta",      "ReconstructedParticle::get_theta(zed_leptonic)") 
            .Define("zed_leptonic_phi",      "ReconstructedParticle::get_phi(zed_leptonic)")
            
            
            .Filter("zed_leptonic.size()>0")
            .Define("Z_leptonic_m",             "if(zed_leptonic_m.size()>0) return zed_leptonic_m.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_n",             "float (zed_leptonic_n)")
            .Define("Z_leptonic_charge",        "if(zed_leptonic_charge.size()>0) return zed_leptonic_charge.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_pt",            "if(zed_leptonic_pt.size()>0) return zed_leptonic_pt.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_y",             "if(zed_leptonic_y.size()>0) return zed_leptonic_y.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_p",             "if(zed_leptonic_p.size()>0) return zed_leptonic_p.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_e",             "if(zed_leptonic_e.size()>0) return zed_leptonic_e.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_costheta",      "if(zed_leptonic_costheta.size()>0) return zed_leptonic_costheta.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_px",            "if(zed_leptonic_px.size()>0) return zed_leptonic_px.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_py",            "if(zed_leptonic_py.size()>0) return zed_leptonic_py.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_pz",            "if(zed_leptonic_pz.size()>0) return zed_leptonic_pz.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_eta",           "if(zed_leptonic_eta.size()>0) return zed_leptonic_eta.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_theta",       "if(zed_leptonic_theta.size()>0) return zed_leptonic_theta.at(0); else return -std::numeric_limits<float>::max()") 
            .Define("Z_leptonic_phi",           "if(zed_leptonic_phi.size()>0) return zed_leptonic_phi.at(0); else return -std::numeric_limits<float>::max()") 
            ###
            #Reconstruct recoil object of ee->Z(mumu)H 
            ###
            .Define("zed_leptonic_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
            .Define("zed_leptonic_recoil_m","ReconstructedParticle::get_mass(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_charge","ReconstructedParticle::get_charge(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_n","ReconstructedParticle::get_n(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_pt","ReconstructedParticle::get_pt(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_y","ReconstructedParticle::get_y(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_p","ReconstructedParticle::get_p(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_e","ReconstructedParticle::get_e(zed_leptonic_recoil)")
            .Define("zed_leptonic_recoil_costheta","APCHiggsTools::get_cosTheta(zed_leptonic_recoil)")
         
            # Filter at least one candidate
            #.Filter("zed_leptonic_recoil_m.size()>0")
                   
            ###
            #Define MVA 
            ###
            .Define("MVAVec", ROOT.computeModel1, (#muons
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
                                                    "Z_leptonic_theta"))  
                                                    #"Z_leptonic_phi",    
            .Define("MVAScore0", "MVAVec.at(0)")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            #"Z_leptonic_m_test",
            ##Reconstructed Particle
            "gen_pt_mumu", 
            "gen_mass_mumu",
            "gen_pt_ZH",
            "gen_mass_ZH", 
            'missingET_costheta', 
            #muons
            "selected_muons_delta_max",
            "selected_muons_delta_min",
            "selected_muons_delta_avg",
            "muon_leading_pt",
            "muon_leading_px",
            "muon_leading_py",
            "muon_leading_pz",
            "muon_leading_eta",
            "muon_leading_phi",
            "muon_leading_y",  
            "muon_leading_p",  
            "muon_leading_e",  
            "muon_leading_m",  
            "muon_leading_theta",
            "muon_subleading_pt",
            "muon_subleading_px",
            "muon_subleading_py",
            "muon_subleading_pz",
            "muon_subleading_eta",
            "muon_subleading_phi",  
            "muon_subleading_y",
            "muon_subleading_p",
            "muon_subleading_e",
            "muon_subleading_m",
            "muon_subleading_theta",
            #Zed
            "Z_leptonic_m",      
            "Z_leptonic_pt",     
            "Z_leptonic_y",      
            "Z_leptonic_p",      
            "Z_leptonic_e",      
            "Z_leptonic_px",     
            "Z_leptonic_py",     
            "Z_leptonic_pz",     
            "Z_leptonic_eta",    
            "Z_leptonic_theta",  
            "Z_leptonic_phi",    
            #Recoil
            "zed_leptonic_recoil_m",
        
            #MVA
            "MVAVec",
            "MVAScore0"
       ]
        return branchList

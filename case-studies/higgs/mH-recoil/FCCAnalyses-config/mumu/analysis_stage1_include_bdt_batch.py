import ROOT
#Mandatory: List of processes
processList = {
    'wzp6_ee_mumuH_ecm240':{'chunks':5},
    'p8_ee_WW_mumu_ecm240':{'chunks':5},
    'p8_ee_Zll_ecm240':{'chunks':5},
    'p8_ee_ZZ_ecm240':{'chunks':5}
    #'wzp6_ee_mumuH_ecm240':{'fraction':0.1}
    }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local dir
outputDir="/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/ZH_mumu_recoil_batch/stage1/trainedNtuples"
#outputDirEos= "/eos/user/l/lia/FCCee/MVA/ZH_mumu_recoil_batch/"
#eosType = "eosuser"
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
    computeModel1 = TMVA::Experimental::Compute<6, float>(bdt);
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
            .Define("stable",  "MCParticle::sel_genStatus(2) (Particle)")
            ###
            #Muon
            ###
            .Define("theGenLevelMuminus",  "MCParticle::sel_pdgID( 13, false) (stable)")
            .Define("theGenLevelMuplus",  "MCParticle::sel_pdgID( -13, false) (stable)")
            .Define("theGenLevelMuminus_tlv", "MCParticle::get_tlv(theGenLevelMuminus) ")
            .Define("theGenLevelMuplus_tlv", "MCParticle::get_tlv(theGenLevelMuplus) ")
            ###
            #Higgs
            ###
            .Define("theGenLevelHiggs", "MCParticle::sel_pdgID( 25, false) (stable)")
            .Define("theGenLevelHiggs_tlv", "MCParticle::get_tlv(theGenLevelHiggs) ")
            
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
            .Define("Selected_muons_plus_pt", "if(selected_muons_plus_pt.size()>0) return selected_muons_plus_pt.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Selected_muons_minus_pt", "if(selected_muons_plus_pt.size()>0) return selected_muons_minus_pt.at(0); else return -std::numeric_limits<float>::max()")
            ###
            #Rconstruct Zed from Z->mumu
            ###
            .Define("zed_leptonic",         "ReconstructedParticle::resonanceBuilder(91)(selected_muons)")
            .Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
            .Define("zed_leptonic_n",       "ReconstructedParticle::get_n(zed_leptonic)")
            .Define("zed_leptonic_charge",   "ReconstructedParticle::get_charge(zed_leptonic)")
            .Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
            .Define("zed_leptonic_y",      "ReconstructedParticle::get_y(zed_leptonic)")
            .Define("zed_leptonic_p",      "ReconstructedParticle::get_p(zed_leptonic)")
            .Define("zed_leptonic_e",      "ReconstructedParticle::get_e(zed_leptonic)")
            .Define("zed_leptonic_costheta",  "APCHiggsTools::get_cosTheta(zed_leptonic)")
            .Define("zed_leptonic_acolinearity",  "ReconstructedParticle::acolinearity(selected_muons)")
            .Define("zed_leptonic_acoplanarity",  "ReconstructedParticle::acoplanarity(selected_muons)")
            .Filter("zed_leptonic.size()>0")
            .Define("Z_leptonic_m",             "if(zed_leptonic_m.size()>0) return zed_leptonic_m.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_n",             "float (zed_leptonic_n)")
            .Define("Z_leptonic_charge",        "if(zed_leptonic_charge.size()>0) return zed_leptonic_charge.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_pt",            "if(zed_leptonic_pt.size()>0) return zed_leptonic_pt.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_y",             "if(zed_leptonic_y.size()>0) return zed_leptonic_y.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_p",             "if(zed_leptonic_p.size()>0) return zed_leptonic_p.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_e",             "if(zed_leptonic_e.size()>0) return zed_leptonic_e.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_costheta",      "if(zed_leptonic_costheta.size()>0) return zed_leptonic_costheta.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_acolinearity",  "if(zed_leptonic_acolinearity.size()>0) return zed_leptonic_acolinearity.at(0); else return -std::numeric_limits<float>::max()")
            .Define("Z_leptonic_acoplanarity",  "if(zed_leptonic_acoplanarity.size()>0) return zed_leptonic_acoplanarity.at(0); else return -std::numeric_limits<float>::max()")
            
            ###
            #Define MVA 
            ###
            .Define("MVAVec1", ROOT.computeModel1, ("Z_leptonic_m", 
                                                    "Z_leptonic_pt",
                                                    "Z_leptonic_costheta", 
                                                    "Z_leptonic_acolinearity",
                                                    "Selected_muons_minus_pt",
                                                    "Selected_muons_plus_pt"))
            .Define("MVAScore1", "MVAVec1.at(0)")
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
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            #"Z_leptonic_m_test",
            ##Reconstructed Particle
            #muons
            "selected_muons_pt",
            "selected_muons_y",
            "selected_muons_p",
            "selected_muons_e",
            "selected_muons_m",
            "selected_muons_n",
            "selected_muons_plus_n",
            "selected_muons_minus_n",
            "selected_muons_plus_pt",
            "selected_muons_minus_pt",
            "Selected_muons_plus_pt",
            "Selected_muons_minus_pt",
            #Zed
            "zed_leptonic_pt",
            "zed_leptonic_y",
            "zed_leptonic_p",
            "zed_leptonic_e",
            "zed_leptonic_m",
            "zed_leptonic_n",
            "zed_leptonic_costheta",
            "zed_leptonic_charge",
            "zed_leptonic_acolinearity",
            "zed_leptonic_acoplanarity",
            "Z_leptonic_pt",
            "Z_leptonic_y",
            "Z_leptonic_p",
            "Z_leptonic_e",
            "Z_leptonic_m",
            "Z_leptonic_n",
            "Z_leptonic_costheta",
            "Z_leptonic_charge",
            "Z_leptonic_acolinearity",
            "Z_leptonic_acoplanarity",
            #Recoil
            "zed_leptonic_recoil_m",
            "zed_leptonic_recoil_y",
            "zed_leptonic_recoil_p",
            "zed_leptonic_recoil_e",
            "zed_leptonic_recoil_n",
            "zed_leptonic_recoil_costheta",
            "zed_leptonic_recoil_charge",
            "zed_leptonic_recoil_pt",
            #Missing Information
            "missingET_costheta",
            ##MC Particles
            "gen_pt_mumu",
            "gen_mass_mumu",
            "gen_pt_ZH",
            "gen_mass_ZH",
            #MVA
            "MVAVec1",
            "MVAScore1"
       ]
        return branchList

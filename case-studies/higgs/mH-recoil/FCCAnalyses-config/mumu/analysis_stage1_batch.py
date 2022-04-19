#Mandatory: List of processes
processList = {
    'wzp6_ee_mumuH_ecm240':{},
    'wzp6_ee_tautauH_ecm240':{},
    'wzp6_ee_eeH_ecm240':{},
    'wzp6_ee_nunuH_ecm240':{},
    'wzp6_ee_qqH_ecm240':{},
    'p8_ee_WW_mumu_ecm240':{},
    'p8_ee_ZZ_Zll_ecm240':{},
    'wzp6_egamma_eZ_Zmumu_ecm240':{},
    'wzp6_gammae_eZ_Zmumu_ecm240':{},
    'wzp6_gaga_mumu_60_ecm240':{},
    'wzp6_gaga_tautau_60_ecm240':{},
    'p8_ee_Zll_ecm240':{},
    'p8_ee_Zqq_ecm240':{},
    'wzp6_ee_mumu_ecm240':{},
    'wzp6_ee_tautau_ecm240':{},
    'wzp6_ee_ee_Mee_30_150_ecm240':{},
    'p8_ee_ZZ_ecm240':{},
    'p8_ee_WW_ecm240':{},
    'p8_ee_ZH_ecm240':{} 
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local dir
outputDir="/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/ZH_mumu_recoil_batch/stage1"
outputDirEos= "/eos/user/l/lia/FCCee/MVA/ZH_mumu_recoil_batch/test"
eosType = "eosuser"
#Optional: ncpus, default is 4
nCPUS       = 4

#Optional running on HTCondor, default is False
runBatch    = True

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

userBatchConfig="/afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/FCCAnalyses-config/mumu/userBatch.Config"
#USER DEFINED CODE

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
            .Define("selected_muons_n", "ReconstructedParticle::get_n(selected_muons)")
            .Define("selected_muons_pt", "ReconstructedParticle::get_pt(selected_muons)")
            .Define("selected_muons_y",  "ReconstructedParticle::get_y(selected_muons)")
            .Define("selected_muons_p",     "ReconstructedParticle::get_p(selected_muons)")
            .Define("selected_muons_e",     "ReconstructedParticle::get_e(selected_muons)")
            .Define("selected_muons_m",     "ReconstructedParticle::get_mass(selected_muons)")
            .Define("selected_muons_costheta",  "APCHiggsTools::get_cosTheta(selected_muons)")
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
            .Define("zed_leptonic_acollinearity",  "ReconstructedParticle::acolinearity(selected_muons)")
            .Define("zed_leptonic_acoplanarity",  "ReconstructedParticle::acoplanarity(selected_muons)")
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
            .Define("gen_pt_mumu", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1) return  (theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0]).Pt(); else return -999. ")
            .Define("gen_mass_mumu", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1) return ( theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0]).M(); else return -999. ")
            ###
            #ZH
            ###
            .Define("gen_pt_ZH", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1 && theGenLevelHiggs_tlv.size()==1) return ( theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0] + theGenLevelHiggs_tlv[0] ).Pt(); else return -999." )
            .Define("gen_mass_ZH", "if ( theGenLevelMuminus_tlv.size() == 1 && theGenLevelMuplus_tlv.size() == 1 && theGenLevelHiggs_tlv.size()==1) return ( theGenLevelMuminus_tlv[0] + theGenLevelMuplus_tlv[0] + theGenLevelHiggs_tlv[0] ).M(); else return -999." )

            # Filter at least one candidate
            #.Filter("zed_leptonic_recoil_m.size()>0")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
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
            #Zed
            "zed_leptonic_pt",
            "zed_leptonic_y",
            "zed_leptonic_p",
            "zed_leptonic_e",
            "zed_leptonic_m",
            "zed_leptonic_n",
            "zed_leptonic_costheta",
            "zed_leptonic_charge",
            "zed_leptonic_acollinearity",
            "zed_leptonic_acoplanarity",
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
            "gen_mass_ZH"
       ]
        return branchList

# This is a basic example showing how to read different objects like electrons, jets, ETmiss etc. from the EDM4HEP files 
# and how to access and store some simple variables in an output ntuple.
# It has been edited in order to accomodate studies of HNLs using the FCC framework

import ROOT
import os
import argparse


### TODO: see if can be simplified/improved #####
#setup of the libraries, following the example:
print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gSystem.Load("libFCCAnalysesFlavour")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_HNL   = ROOT.dummyLoaderFlavour #### Needed to fix undeclared selMC_leg()

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

print ('Finished loading analyzers. Ready to go.')


#The analysis class handles which variables are defined and written to the output ntuple

class analysis():
        #__________________________________________________________
        def __init__(self, inputlist, outname, ncpu):
                self.outname = outname

                if ".root" not in outname:
                        self.outname+=".root"

                ROOT.ROOT.EnableImplicitMT(ncpu)

                self.df = ROOT.RDataFrame("events", inputlist)

	#__________________________________________________________
        def run(self):

                df2 = (self.df

                #Access the various objects and their properties with the following syntax: .Define("<your_variable>", "<accessor_fct (name_object)>")
		#This will create a column in the RDataFrame named <your_variable> and filled with the return value of the <accessor_fct> for the given collection/object 
		#Accessor functions are the functions found in the C++ analyzers code that return a certain variable, e.g. <namespace>::get_n(object) returns the number 
		#of these objects in the event and <namespace>::get_pt(object) returns the pt of the object. Here you can pick between two namespaces to access either
		#reconstructed (namespace = ReconstructedParticle) or MC-level objects (namespace = MCParticle). 
		#For the name of the object, in principle the names of the EDM4HEP collections are used - photons, muons and electrons are an exception, see below

		#OVERVIEW: Accessing different objects and counting them
               

                # Following code is written specifically for the HNL study
                ####################################################################################################
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
 
                ##### Added branch for MCParticle; finding PID of the MC particle for HNL
                .Define("GenHNL_PID", "MCParticle::sel_pdgID(9900012, false)(Particle)")
                .Define("GenHNL_decay", "MCParticle::get_list_of_particles_from_decay(0, GenHNL_PID, Particle1)")

                .Define("All_n_GenHNL", "MCParticle::get_n(GenHNL_PID)")
                .Define("AllGenHNL_mass", "MCParticle::get_mass(GenHNL_PID)") #finding the generator mass of the HNL through separate HNL branch
                .Define("AllGenHNL_e", "MCParticle::get_e(GenHNL_PID)")
                .Define("AllGenHNL_p", "MCParticle::get_p(GenHNL_PID)")
                .Define("AllGenHNL_pt", "MCParticle::get_pt(GenHNL_PID)")    #finding the pt of the HNL thorugh separate HNL branch
                .Define("AllGenHNL_px", "MCParticle::get_px(GenHNL_PID)")
                .Define("AllGenHNL_py", "MCParticle::get_py(GenHNL_PID)")
                .Define("AllGenHNL_pz", "MCParticle::get_pz(GenHNL_PID)")
                .Define("AllGenHNL_eta", "MCParticle::get_eta(GenHNL_PID)")
                .Define("AllGenHNL_theta", "MCParticle::get_theta(GenHNL_PID)")
                .Define("AllGenHNL_phi", "MCParticle::get_phi(GenHNL_PID)")
                .Define("AllGenHNL_charge", "MCParticle::get_charge(GenHNL_PID)")
                .Define("AllGenHNL_genStatus", "MCParticle::get_genStatus(GenHNL_PID)")

                #all final state gen electrons and positrons
                .Define("GenElectron_PID", "MCParticle::sel_pdgID(11, true)(Particle)")
                .Define("FSGenElectron", "MCParticle::sel_genStatus(1)(GenElectron_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenElectron", "MCParticle::get_n(FSGenElectron)")
                .Define("FSGenElectron_e", "MCParticle::get_e(FSGenElectron)")
                .Define("FSGenElectron_p", "MCParticle::get_p(FSGenElectron)")
                .Define("FSGenElectron_pt", "MCParticle::get_pt(FSGenElectron)")
                .Define("FSGenElectron_px", "MCParticle::get_px(FSGenElectron)")
                .Define("FSGenElectron_py", "MCParticle::get_py(FSGenElectron)")
                .Define("FSGenElectron_pz", "MCParticle::get_pz(FSGenElectron)")
                .Define("FSGenElectron_eta", "MCParticle::get_eta(FSGenElectron)")
                .Define("FSGenElectron_theta", "MCParticle::get_theta(FSGenElectron)")
                .Define("FSGenElectron_phi", "MCParticle::get_phi(FSGenElectron)")
                .Define("FSGenElectron_charge", "MCParticle::get_charge(FSGenElectron)")

                .Define("FSGenElectron_vertex_x", "MCParticle::get_vertex_x( FSGenElectron )")
                .Define("FSGenElectron_vertex_y", "MCParticle::get_vertex_y( FSGenElectron )")
                .Define("FSGenElectron_vertex_z", "MCParticle::get_vertex_z( FSGenElectron )")

                # Finding the Lxy of the HNL
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
                .Define("FSGen_Lxy", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y)")
                # Finding the Lxyz of the HNL
                .Define("FSGen_Lxyz", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y + FSGenElectron_vertex_z*FSGenElectron_vertex_z)")

                #all final state gen neutrinos and anti-neutrinos
                .Define("GenNeutrino_PID", "MCParticle::sel_pdgID(12, true)(Particle)")
                .Define("FSGenNeutrino", "MCParticle::sel_genStatus(1)(GenNeutrino_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenNeutrino", "MCParticle::get_n(FSGenNeutrino)")
                .Define("FSGenNeutrino_e", "MCParticle::get_e(FSGenNeutrino)")
                .Define("FSGenNeutrino_p", "MCParticle::get_p(FSGenNeutrino)")
                .Define("FSGenNeutrino_pt", "MCParticle::get_pt(FSGenNeutrino)")
                .Define("FSGenNeutrino_px", "MCParticle::get_px(FSGenNeutrino)")
                .Define("FSGenNeutrino_py", "MCParticle::get_py(FSGenNeutrino)")
                .Define("FSGenNeutrino_pz", "MCParticle::get_pz(FSGenNeutrino)")
                .Define("FSGenNeutrino_eta", "MCParticle::get_eta(FSGenNeutrino)")
                .Define("FSGenNeutrino_theta", "MCParticle::get_theta(FSGenNeutrino)")
                .Define("FSGenNeutrino_phi", "MCParticle::get_phi(FSGenNeutrino)")
                .Define("FSGenNeutrino_charge", "MCParticle::get_charge(FSGenNeutrino)")

                #all final state gen photons
                .Define("GenPhoton_PID", "MCParticle::sel_pdgID(22, false)(Particle)")
                .Define("FSGenPhoton", "MCParticle::sel_genStatus(1)(GenPhoton_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenPhoton", "MCParticle::get_n(FSGenPhoton)")
                .Define("FSGenPhoton_e", "MCParticle::get_e(FSGenPhoton)")
                .Define("FSGenPhoton_p", "MCParticle::get_p(FSGenPhoton)")
                .Define("FSGenPhoton_pt", "MCParticle::get_pt(FSGenPhoton)")
                .Define("FSGenPhoton_px", "MCParticle::get_px(FSGenPhoton)")
                .Define("FSGenPhoton_py", "MCParticle::get_py(FSGenPhoton)")
                .Define("FSGenPhoton_pz", "MCParticle::get_pz(FSGenPhoton)")
                .Define("FSGenPhoton_eta", "MCParticle::get_eta(FSGenPhoton)")
                .Define("FSGenPhoton_theta", "MCParticle::get_theta(FSGenPhoton)")
                .Define("FSGenPhoton_phi", "MCParticle::get_phi(FSGenPhoton)")
                .Define("FSGenPhoton_charge", "MCParticle::get_charge(FSGenPhoton)")

                # Calculating the lifetime of the HNL
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                .Define("FSGen_lifetime_xy", "return ( FSGen_Lxy.at(0) * AllGenHNL_mass / (AllGenHNL_pt * 3E8 * 1000))" )
                .Define("FSGen_lifetime_xyz", "return ( FSGen_Lxyz.at(0) * AllGenHNL_mass / (AllGenHNL_p * 3E8 * 1000))" )

                # Defining a vector containing the HNL and its daughters in order written
                # Name of vector is HNL_indices
                # bools: look for stable decay products? (yes), look for mother's charge conjugate? (doesn't matter, only 9900012 generated), look for daughters' charge conjugates? (yes), look for an inclusive decay? (yes)
                .Define("GenHNL_indices", "MCParticle::get_indices(9900012, {%s}, true, false, true, true)(Particle, Particle1)"%(daughters))

                # Defining the individual particles from the vector
                .Define("GenHNL", "selMC_leg(0)(GenHNL_indices, Particle)")
                .Define("GenHNLElectron", "selMC_leg(1)(GenHNL_indices, Particle)")

                # a bit hacky but based on the number of GenHNL indices, i figure out if it's eenu or ejj.
                # Then, i define GenHNLElectron2 and GenHNLNeutrino if it's eenu, and if it's ejj, I set GenHNLElectron2 to be the HNL leg (to serve as a dummy value)
                # and similar

                # eenu
                .Define("GenHNLElectron2", "if(GenHNL_indices.size()==4) return selMC_leg(2)(GenHNL_indices, Particle); else return GenHNL")
                .Define("GenHNLNeutrino",  "if(GenHNL_indices.size()==4) return selMC_leg(3)(GenHNL_indices, Particle); else return GenHNL")
                # ejj
                .Define("GenHNLPiZero",      "if(GenHNL_indices.size()==5) return selMC_leg(2)(GenHNL_indices, Particle); else return GenHNL")
                .Define("GenHNLPiPlusMinus", "if(GenHNL_indices.size()==5) return selMC_leg(3)(GenHNL_indices, Particle); else return GenHNL")
                .Define("GenHNLPhoton",      "if(GenHNL_indices.size()==5) return selMC_leg(4)(GenHNL_indices, Particle); else return GenHNL")




                # ee invariant mass
                .Define("FSGen_ee_energy", "return (FSGenElectron_e.at(0) + FSGenElectron_e.at(1))")
                .Define("FSGen_ee_px", "return (FSGenElectron_px.at(0) + FSGenElectron_px.at(1))")
                .Define("FSGen_ee_py", "return (FSGenElectron_py.at(0) + FSGenElectron_py.at(1))")
                .Define("FSGen_ee_pz", "return (FSGenElectron_pz.at(0) + FSGenElectron_pz.at(1))")
                .Define("FSGen_ee_invMass", "return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz )")

                # eenu invariant mass
                .Define("FSGen_eenu_energy", "return (FSGenElectron_e.at(0) + FSGenElectron_e.at(1) + FSGenNeutrino_e.at(0))")
                .Define("FSGen_eenu_px", "return (FSGenElectron_px.at(0) + FSGenElectron_px.at(1) + FSGenNeutrino_px.at(0))")
                .Define("FSGen_eenu_py", "return (FSGenElectron_py.at(0) + FSGenElectron_py.at(1) + FSGenNeutrino_py.at(0))")
                .Define("FSGen_eenu_pz", "return (FSGenElectron_pz.at(0) + FSGenElectron_pz.at(1) + FSGenNeutrino_pz.at(0))")
                .Define("FSGen_eenu_invMass", "return sqrt(FSGen_eenu_energy*FSGen_eenu_energy - FSGen_eenu_px*FSGen_eenu_px - FSGen_eenu_py*FSGen_eenu_py - FSGen_eenu_pz*FSGen_eenu_pz )")
                

                # Kinematics of the mother particle HNL
                .Define("GenHNL_mass", "MCParticle::get_mass( GenHNL )")
                .Define("GenHNL_e", "MCParticle::get_e( GenHNL )")
                .Define("GenHNL_p", "MCParticle::get_p( GenHNL )")
                .Define("GenHNL_pt", "MCParticle::get_pt( GenHNL )")
                .Define("GenHNL_px", "MCParticle::get_px( GenHNL )")
                .Define("GenHNL_py", "MCParticle::get_py( GenHNL )")
                .Define("GenHNL_pz", "MCParticle::get_pz( GenHNL )")
                .Define("GenHNL_eta", "MCParticle::get_eta( GenHNL )")
                .Define("GenHNL_theta", "MCParticle::get_theta( GenHNL )")
                .Define("GenHNL_phi", "MCParticle::get_phi( GenHNL )")
                .Define("GenHNL_charge", "MCParticle::get_charge( GenHNL )")
                .Define("GenHNL_genStatus", "MCParticle::get_genStatus( GenHNL )")

                # Finding the kinematics of each of these daughters
                .Define("GenHNLElectron_mass", "MCParticle::get_mass( GenHNLElectron )")
                .Define("GenHNLElectron_e", "MCParticle::get_e( GenHNLElectron )")
                .Define("GenHNLElectron2_e", "MCParticle::get_e( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_e", "MCParticle::get_e( GenHNLNeutrino )")
                .Define("GenHNLElectron_p", "MCParticle::get_p( GenHNLElectron )")
                .Define("GenHNLElectron2_p", "MCParticle::get_p( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_p", "MCParticle::get_p( GenHNLNeutrino )")
                .Define("GenHNLElectron_pt", "MCParticle::get_pt( GenHNLElectron )")
                .Define("GenHNLElectron2_pt", "MCParticle::get_pt( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_pt", "MCParticle::get_pt( GenHNLNeutrino )")
                .Define("GenHNLElectron_px", "MCParticle::get_px( GenHNLElectron )")
                .Define("GenHNLElectron2_px", "MCParticle::get_px( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_px", "MCParticle::get_px( GenHNLNeutrino )")
                .Define("GenHNLElectron_py", "MCParticle::get_py( GenHNLElectron )")
                .Define("GenHNLElectron2_py", "MCParticle::get_py( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_py", "MCParticle::get_py( GenHNLNeutrino )")
                .Define("GenHNLElectron_pz", "MCParticle::get_pz( GenHNLElectron )")
                .Define("GenHNLElectron2_pz", "MCParticle::get_pz( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_pz", "MCParticle::get_pz( GenHNLNeutrino )")
                .Define("GenHNLElectron_eta", "MCParticle::get_eta( GenHNLElectron )")
                .Define("GenHNLElectron2_eta", "MCParticle::get_eta( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_eta", "MCParticle::get_eta( GenHNLNeutrino )")
                .Define("GenHNLElectron_theta", "MCParticle::get_theta( GenHNLElectron )")
                .Define("GenHNLElectron2_theta", "MCParticle::get_theta( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_theta", "MCParticle::get_theta( GenHNLNeutrino )")
                .Define("GenHNLElectron_phi", "MCParticle::get_phi( GenHNLElectron )")
                .Define("GenHNLElectron2_phi", "MCParticle::get_phi( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_phi", "MCParticle::get_phi( GenHNLNeutrino )")
                .Define("GenHNLElectron_charge", "MCParticle::get_charge( GenHNLElectron )")
                .Define("GenHNLElectron2_charge", "MCParticle::get_charge( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_charge", "MCParticle::get_charge( GenHNLNeutrino )")
                .Define("GenHNLElectron_genStatus", "MCParticle::get_genStatus( GenHNLElectron )")
                .Define("GenHNLElectron2_genStatus", "MCParticle::get_genStatus( GenHNLElectron2 )")
                .Define("GenHNLNeutrino_genStatus", "MCParticle::get_genStatus( GenHNLNeutrino )")

                .Define("GenHNLPiZero_e", "MCParticle::get_e( GenHNLPiZero )")
                .Define("GenHNLPiZero_p", "MCParticle::get_p( GenHNLPiZero )")
                .Define("GenHNLPiZero_pt", "MCParticle::get_pt( GenHNLPiZero )")
                .Define("GenHNLPiZero_px", "MCParticle::get_px( GenHNLPiZero )")
                .Define("GenHNLPiZero_py", "MCParticle::get_py( GenHNLPiZero )")
                .Define("GenHNLPiZero_pz", "MCParticle::get_pz( GenHNLPiZero )")
                .Define("GenHNLPiZero_eta", "MCParticle::get_eta( GenHNLPiZero )")
                .Define("GenHNLPiZero_theta", "MCParticle::get_theta( GenHNLPiZero )")
                .Define("GenHNLPiZero_phi", "MCParticle::get_phi( GenHNLPiZero )")
                .Define("GenHNLPiZero_charge", "MCParticle::get_charge( GenHNLPiZero )")
                .Define("GenHNLPiZero_genStatus", "MCParticle::get_genStatus( GenHNLPiZero )")

                .Define("GenHNLPiPlusMinus_e", "MCParticle::get_e( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_p", "MCParticle::get_p( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_pt", "MCParticle::get_pt( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_px", "MCParticle::get_px( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_py", "MCParticle::get_py( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_pz", "MCParticle::get_pz( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_eta", "MCParticle::get_eta( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_theta", "MCParticle::get_theta( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_phi", "MCParticle::get_phi( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_charge", "MCParticle::get_charge( GenHNLPiPlusMinus )")
                .Define("GenHNLPiPlusMinus_genStatus", "MCParticle::get_genStatus( GenHNLPiPlusMinus )")

                .Define("GenHNLPhoton_e", "MCParticle::get_e( GenHNLPhoton )")
                .Define("GenHNLPhoton_p", "MCParticle::get_p( GenHNLPhoton )")
                .Define("GenHNLPhoton_pt", "MCParticle::get_pt( GenHNLPhoton )")
                .Define("GenHNLPhoton_px", "MCParticle::get_px( GenHNLPhoton )")
                .Define("GenHNLPhoton_py", "MCParticle::get_py( GenHNLPhoton )")
                .Define("GenHNLPhoton_pz", "MCParticle::get_pz( GenHNLPhoton )")
                .Define("GenHNLPhoton_eta", "MCParticle::get_eta( GenHNLPhoton )")
                .Define("GenHNLPhoton_theta", "MCParticle::get_theta( GenHNLPhoton )")
                .Define("GenHNLPhoton_phi", "MCParticle::get_phi( GenHNLPhoton )")
                .Define("GenHNLPhoton_charge", "MCParticle::get_charge( GenHNLPhoton )")
                .Define("GenHNLPhoton_genStatus", "MCParticle::get_genStatus( GenHNLPhoton )")


                # Finding the production vertex of the daughters (checking GenHNLElectron here)
                .Define("GenHNLElectron_vertex_x", "MCParticle::get_vertex_x( GenHNLElectron )")
                .Define("GenHNLElectron_vertex_y", "MCParticle::get_vertex_y( GenHNLElectron )")
                .Define("GenHNLElectron_vertex_z", "MCParticle::get_vertex_z( GenHNLElectron )")

                # Finding the Lxy of the HNL
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )  
                .Define("GenHNL_Lxy", "return sqrt(GenHNLElectron_vertex_x*GenHNLElectron_vertex_x + GenHNLElectron_vertex_y*GenHNLElectron_vertex_y)")
                .Define("GenHNL_Lxyz","return sqrt(GenHNLElectron_vertex_x*GenHNLElectron_vertex_x + GenHNLElectron_vertex_y*GenHNLElectron_vertex_y + GenHNLElectron_vertex_z*GenHNLElectron_vertex_z)")
                
                # Calculating the lifetime of the HNL
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                .Define("GenHNL_lifetime_xy", "return ( GenHNL_Lxy * GenHNL_mass / (GenHNL_pt * 3E8 * 1000))" )
                .Define("GenHNL_lifetime_xyz", "return ( GenHNL_Lxyz * GenHNL_mass / (GenHNL_p * 3E8 * 1000))" )


                # Finding the production vertex of the HNL which should be at (0,0,0) 
                .Define("GenHNL_vertex_x", "MCParticle::get_vertex_x(GenHNL_PID)")
                .Define("GenHNL_vertex_y", "MCParticle::get_vertex_y(GenHNL_PID)")
                .Define("GenHNL_vertex_z", "MCParticle::get_vertex_z(GenHNL_PID)")

                # ee invariant mass
                .Define("GenHNL_ee_energy", "return (GenHNLElectron_e + GenHNLElectron2_e)")
                .Define("GenHNL_ee_px", "return (GenHNLElectron_px + GenHNLElectron2_px)")
                .Define("GenHNL_ee_py", "return (GenHNLElectron_py + GenHNLElectron2_py)")
                .Define("GenHNL_ee_pz", "return (GenHNLElectron_pz + GenHNLElectron2_pz)")
                .Define("GenHNL_ee_invMass", "return sqrt(GenHNL_ee_energy*GenHNL_ee_energy - GenHNL_ee_px*GenHNL_ee_px - GenHNL_ee_py*GenHNL_ee_py - GenHNL_ee_pz*GenHNL_ee_pz )")

                # eenu invariant mass
                .Define("GenHNL_eenu_energy", "return (GenHNLElectron_e + GenHNLElectron2_e + GenHNLNeutrino_e)")
                .Define("GenHNL_eenu_px", "return (GenHNLElectron_px + GenHNLElectron2_px + GenHNLNeutrino_px)")
                .Define("GenHNL_eenu_py", "return (GenHNLElectron_py + GenHNLElectron2_py + GenHNLNeutrino_py)")
                .Define("GenHNL_eenu_pz", "return (GenHNLElectron_pz + GenHNLElectron2_pz + GenHNLNeutrino_pz)")
                .Define("GenHNL_eenu_invMass", "return sqrt(GenHNL_eenu_energy*GenHNL_eenu_energy - GenHNL_eenu_px*GenHNL_eenu_px - GenHNL_eenu_py*GenHNL_eenu_py - GenHNL_eenu_pz*GenHNL_eenu_pz )")

                # e pi+/- pi0 gamma invariant mass
                .Define("GenHNL_epipigamma_energy", "return (GenHNLElectron_e + GenHNLPiPlusMinus_e + GenHNLPiZero_e + GenHNLPhoton_e)")
                .Define("GenHNL_epipigamma_px", "return (GenHNLElectron_px + GenHNLPiPlusMinus_px + GenHNLPiZero_px + GenHNLPhoton_px)")
                .Define("GenHNL_epipigamma_py", "return (GenHNLElectron_py + GenHNLPiPlusMinus_py + GenHNLPiZero_py + GenHNLPhoton_py)")
                .Define("GenHNL_epipigamma_pz", "return (GenHNLElectron_pz + GenHNLPiPlusMinus_pz + GenHNLPiZero_pz + GenHNLPhoton_pz)")
                .Define("GenHNL_epipigamma_invMass", "return sqrt(GenHNL_epipigamma_energy*GenHNL_epipigamma_energy - GenHNL_epipigamma_px*GenHNL_epipigamma_px - GenHNL_epipigamma_py*GenHNL_epipigamma_py - GenHNL_epipigamma_pz*GenHNL_epipigamma_pz )")

                # Vertexing studies
                # Finding the vertex of the mother particle HNL using decicated Bs method
                .Define("GenHNLMCDecayVertex",   "BsMCDecayVertex( GenHNL_indices, Particle )")

                # MC event primary vertex
                .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

                # Reconstructed particles
                # Returns the RecoParticles associated with the HNL decay products
                .Define("RecoHNLParticles",  "ReconstructedParticle2MC::selRP_matched_to_list( GenHNL_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                # Reconstructing the tracks from the HNL
                .Define("RecoHNLTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoHNLParticles, EFlowTrack_1)")

                # Number of tracks in this RecoHNLTracks collection ( = the #tracks used to reconstruct the HNL reco decay vertex)
                .Define("n_RecoHNLTracks", "ReconstructedParticle2Track::getTK_n( RecoHNLTracks )")

                # properties of RecoHNLTracks
                .Define("RecoHNLTracks_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoHNLParticles,RecoHNLTracks))")
                .Define("RecoHNLTracks_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoHNLParticles,RecoHNLTracks))")
                .Define("RecoHNLTracks_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoHNLParticles,RecoHNLTracks))") #significance
                .Define("RecoHNLTracks_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoHNLParticles,RecoHNLTracks))")
                .Define("RecoHNLTracks_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoHNLParticles,RecoHNLTracks)") #variance (not sigma)
                .Define("RecoHNLTracks_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoHNLParticles,RecoHNLTracks)")

                # Now we reconstruct the HNL reco decay vertex using the reco'ed tracks
                # First the full object, of type Vertexing::FCCAnalysesVertex
                .Define("RecoHNLDecayVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, RecoHNLTracks)" )

                # from which we extract the edm4hep::VertexData object, which contains the vertex position in mm
                .Define("RecoHNLDecayVertex",  "VertexingUtils::get_VertexData( RecoHNLDecayVertexObject )")

                .Define("RecoHNL_Lxy", "return sqrt(RecoHNLDecayVertex.position.x*RecoHNLDecayVertex.position.x + RecoHNLDecayVertex.position.y*RecoHNLDecayVertex.position.y)")
                .Define("RecoHNL_Lxyz","return sqrt(RecoHNLDecayVertex.position.x*RecoHNLDecayVertex.position.x + RecoHNLDecayVertex.position.y*RecoHNLDecayVertex.position.y + RecoHNLDecayVertex.position.z*RecoHNLDecayVertex.position.z)")
                
                # We may want to look at the reco'ed HNLs legs: in the RecoHNLParticles vector,
                # the first particle (vector[0]) is the e-, etc :
                .Define("RecoHNLElectron",   "selRP_leg(0)( RecoHNLParticles )")
                .Define("RecoHNLElectron2",   "selRP_leg(1)( RecoHNLParticles )")
                
                # reconstruced electron, positron values
                .Define("RecoHNLElectron_e",  "ReconstructedParticle::get_e( RecoHNLElectron )")
                .Define("RecoHNLElectron2_e",  "ReconstructedParticle::get_e( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_p",  "ReconstructedParticle::get_p( RecoHNLElectron )")
                .Define("RecoHNLElectron2_p",  "ReconstructedParticle::get_p( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_pt",  "ReconstructedParticle::get_pt( RecoHNLElectron )")
                .Define("RecoHNLElectron2_pt",  "ReconstructedParticle::get_pt( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_px",  "ReconstructedParticle::get_px( RecoHNLElectron )")
                .Define("RecoHNLElectron2_px",  "ReconstructedParticle::get_px( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_py",  "ReconstructedParticle::get_py( RecoHNLElectron )")
                .Define("RecoHNLElectron2_py",  "ReconstructedParticle::get_py( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_pz",  "ReconstructedParticle::get_pz( RecoHNLElectron )")
                .Define("RecoHNLElectron2_pz",  "ReconstructedParticle::get_pz( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_eta",  "ReconstructedParticle::get_eta( RecoHNLElectron )")
                .Define("RecoHNLElectron2_eta",  "ReconstructedParticle::get_eta( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_theta",  "ReconstructedParticle::get_theta( RecoHNLElectron )")
                .Define("RecoHNLElectron2_theta",  "ReconstructedParticle::get_theta( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_phi",  "ReconstructedParticle::get_phi( RecoHNLElectron )")
                .Define("RecoHNLElectron2_phi",  "ReconstructedParticle::get_phi( RecoHNLElectron2 )")
                .Define("RecoHNLElectron_charge",  "ReconstructedParticle::get_charge( RecoHNLElectron )")
                .Define("RecoHNLElectron2_charge",  "ReconstructedParticle::get_charge( RecoHNLElectron2 )")
                #add dxy, dz, dxyz, and uncertainties

                # ee invariant mass
                .Define("RecoHNL_ee_energy", "return (RecoHNLElectron_e + RecoHNLElectron2_e)")
                .Define("RecoHNL_ee_px", "return (RecoHNLElectron_px + RecoHNLElectron2_px)")
                .Define("RecoHNL_ee_py", "return (RecoHNLElectron_py + RecoHNLElectron2_py)")
                .Define("RecoHNL_ee_pz", "return (RecoHNLElectron_pz + RecoHNLElectron2_pz)")
                .Define("RecoHNL_ee_invMass", "return sqrt(RecoHNL_ee_energy*RecoHNL_ee_energy - RecoHNL_ee_px*RecoHNL_ee_px - RecoHNL_ee_py*RecoHNL_ee_py - RecoHNL_ee_pz*RecoHNL_ee_pz )")

                #gen-reco
                .Define("GenMinusRecoHNLElectron_e",   "GenHNLElectron_e-RecoHNLElectron_e")
                .Define("GenMinusRecoHNLElectron2_e",   "GenHNLElectron2_e-RecoHNLElectron2_e")
                .Define("GenMinusRecoHNLElectron_p",   "GenHNLElectron_p-RecoHNLElectron_p")
                .Define("GenMinusRecoHNLElectron2_p",   "GenHNLElectron2_p-RecoHNLElectron2_p")
                .Define("GenMinusRecoHNLElectron_pt",   "GenHNLElectron_pt-RecoHNLElectron_pt")
                .Define("GenMinusRecoHNLElectron2_pt",   "GenHNLElectron2_pt-RecoHNLElectron2_pt")
                .Define("GenMinusRecoHNLElectron_px",   "GenHNLElectron_px-RecoHNLElectron_px")
                .Define("GenMinusRecoHNLElectron2_px",   "GenHNLElectron2_px-RecoHNLElectron2_px")
                .Define("GenMinusRecoHNLElectron_py",   "GenHNLElectron_py-RecoHNLElectron_py")
                .Define("GenMinusRecoHNLElectron2_py",   "GenHNLElectron2_py-RecoHNLElectron2_py")
                .Define("GenMinusRecoHNLElectron_pz",   "GenHNLElectron_pz-RecoHNLElectron_pz")
                .Define("GenMinusRecoHNLElectron2_pz",   "GenHNLElectron2_pz-RecoHNLElectron2_pz")
                .Define("GenMinusRecoHNLElectron_eta",  "GenHNLElectron_eta-RecoHNLElectron_eta")
                .Define("GenMinusRecoHNLElectron2_eta",  "GenHNLElectron2_eta-RecoHNLElectron2_eta")
                .Define("GenMinusRecoHNLElectron_theta",  "GenHNLElectron_theta-RecoHNLElectron_theta")
                .Define("GenMinusRecoHNLElectron2_theta",  "GenHNLElectron2_theta-RecoHNLElectron2_theta")
                .Define("GenMinusRecoHNLElectron_phi",  "GenHNLElectron_phi-RecoHNLElectron_phi")
                .Define("GenMinusRecoHNLElectron2_phi",  "GenHNLElectron2_phi-RecoHNLElectron2_phi")

                .Define("GenMinusRecoHNL_DecayVertex_x",  "GenHNLElectron_vertex_x-RecoHNLDecayVertex.position.x")
                .Define("GenMinusRecoHNL_DecayVertex_y",  "GenHNLElectron_vertex_y-RecoHNLDecayVertex.position.y")
                .Define("GenMinusRecoHNL_DecayVertex_z",  "GenHNLElectron_vertex_z-RecoHNLDecayVertex.position.z")
                .Define("GenMinusRecoHNL_Lxy", "GenHNL_Lxy-RecoHNL_Lxy")
                .Define("GenMinusRecoHNL_Lxyz", "GenHNL_Lxyz-RecoHNL_Lxyz")
                
                       
                ####################################################################################################
                # From here the general study begins

		#JETS
		.Define("n_RecoJets", "ReconstructedParticle::get_n(Jet)") #count how many jets are in the event in total

		#PHOTONS
		.Alias("Photon0", "Photon#0.index") 
		.Define("RecoPhotons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
		.Define("n_RecoPhotons",  "ReconstructedParticle::get_n(RecoPhotons)") #count how many photons are in the event in total

		#ELECTRONS AND MUONS
		#TODO: ADD EXPLANATION OF THE EXTRA STEPS
		.Alias("Electron0", "Electron#0.index")
		.Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
		.Define("n_RecoElectrons",  "ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total

		.Alias("Muon0", "Muon#0.index")
		.Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
		.Define("n_RecoMuons",  "ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total

		#OBJECT SELECTION: Consider only those objects that have pt > certain threshold
		#.Define("selected_jets", "ReconstructedParticle::sel_pt(0.)(Jet)") #select only jets with a pt > 50 GeV
		#.Define("selected_electrons", "ReconstructedParticle::sel_pt(0.)(electrons)") #select only electrons with a pt > 20 GeV
                #.Define("selected_photons", "ReconstructedParticle::sel_pt(0.)(photons)") #select only photons with a pt > 20 GeV
		#.Define("selected_muons", "ReconstructedParticle::sel_pt(0.)(muons)")

                #.Define("n_selJets", "ReconstructedParticle::get_n(selected_jets)")
                #.Define("n_selElectrons", "ReconstructedParticle::get_n(selected_electrons)")
                #.Define("n_selPhotons", "ReconstructedParticle::get_n(selected_photons)")
                #.Define("n_selMuons", "ReconstructedParticle::get_n(selected_muons)")

		#SIMPLE VARIABLES: Access the basic kinematic variables of the (selected) jets, works analogously for electrons, muons
		.Define("RecoJet_e",      "ReconstructedParticle::get_e(Jet)")
                .Define("RecoJet_p",      "ReconstructedParticle::get_p(Jet)") #momentum p
                .Define("RecoJet_pt",      "ReconstructedParticle::get_pt(Jet)") #transverse momentum pt
                .Define("RecoJet_px",      "ReconstructedParticle::get_px(Jet)")
                .Define("RecoJet_py",      "ReconstructedParticle::get_py(Jet)")
                .Define("RecoJet_pz",      "ReconstructedParticle::get_pz(Jet)")
		.Define("RecoJet_eta",     "ReconstructedParticle::get_eta(Jet)") #pseudorapidity eta
                .Define("RecoJet_theta",   "ReconstructedParticle::get_theta(Jet)")
		.Define("RecoJet_phi",     "ReconstructedParticle::get_phi(Jet)") #polar angle in the transverse plane phi
                .Define("RecoJet_charge",  "ReconstructedParticle::get_charge(Jet)") 
                .Define("RecoJetTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(Jet,EFlowTrack_1))")
                .Define("RecoJetTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(Jet,EFlowTrack_1))")
                .Define("RecoJetTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(Jet,EFlowTrack_1))") #significance
                .Define("RecoJetTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(Jet,EFlowTrack_1))")
                .Define("RecoJetTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(Jet,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoJetTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(Jet,EFlowTrack_1)")

                .Define("RecoElectron_e",      "ReconstructedParticle::get_e(RecoElectrons)")
                .Define("RecoElectron_p",      "ReconstructedParticle::get_p(RecoElectrons)")
                .Define("RecoElectron_pt",      "ReconstructedParticle::get_pt(RecoElectrons)")
                .Define("RecoElectron_px",      "ReconstructedParticle::get_px(RecoElectrons)")
                .Define("RecoElectron_py",      "ReconstructedParticle::get_py(RecoElectrons)")
                .Define("RecoElectron_pz",      "ReconstructedParticle::get_pz(RecoElectrons)")
		.Define("RecoElectron_eta",     "ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
                .Define("RecoElectron_theta",   "ReconstructedParticle::get_theta(RecoElectrons)")
		.Define("RecoElectron_phi",     "ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
                .Define("RecoElectron_charge",  "ReconstructedParticle::get_charge(RecoElectrons)")
                .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

                .Define("RecoPhoton_e",      "ReconstructedParticle::get_e(RecoPhotons)")
                .Define("RecoPhoton_p",      "ReconstructedParticle::get_p(RecoPhotons)")
                .Define("RecoPhoton_pt",      "ReconstructedParticle::get_pt(RecoPhotons)")
                .Define("RecoPhoton_px",      "ReconstructedParticle::get_px(RecoPhotons)")
                .Define("RecoPhoton_py",      "ReconstructedParticle::get_py(RecoPhotons)")
                .Define("RecoPhoton_pz",      "ReconstructedParticle::get_pz(RecoPhotons)")
		.Define("RecoPhoton_eta",     "ReconstructedParticle::get_eta(RecoPhotons)") #pseudorapidity eta
                .Define("RecoPhoton_theta",   "ReconstructedParticle::get_theta(RecoPhotons)")
		.Define("RecoPhoton_phi",     "ReconstructedParticle::get_phi(RecoPhotons)") #polar angle in the transverse plane phi
                .Define("RecoPhoton_charge",  "ReconstructedParticle::get_charge(RecoPhotons)")

                .Define("RecoMuon_e",      "ReconstructedParticle::get_e(RecoMuons)")
                .Define("RecoMuon_p",      "ReconstructedParticle::get_p(RecoMuons)")
                .Define("RecoMuon_pt",      "ReconstructedParticle::get_pt(RecoMuons)")
                .Define("RecoMuon_px",      "ReconstructedParticle::get_px(RecoMuons)")
                .Define("RecoMuon_py",      "ReconstructedParticle::get_py(RecoMuons)")
                .Define("RecoMuon_pz",      "ReconstructedParticle::get_pz(RecoMuons)")
		.Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
                .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
		.Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
                .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")
                .Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")


		#EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing energy (despite the name, the MissingET collection contains the total missing energy)
                .Define("RecoMissingEnergy_e", "ReconstructedParticle::get_e(MissingET)")
                .Define("RecoMissingEnergy_p", "ReconstructedParticle::get_p(MissingET)")
                .Define("RecoMissingEnergy_pt", "ReconstructedParticle::get_pt(MissingET)")
                .Define("RecoMissingEnergy_px", "ReconstructedParticle::get_px(MissingET)")
                .Define("RecoMissingEnergy_py", "ReconstructedParticle::get_py(MissingET)")
                .Define("RecoMissingEnergy_pz", "ReconstructedParticle::get_pz(MissingET)")
                .Define("RecoMissingEnergy_eta", "ReconstructedParticle::get_eta(MissingET)")
                .Define("RecoMissingEnergy_theta", "ReconstructedParticle::get_theta(MissingET)")
                .Define("RecoMissingEnergy_phi", "ReconstructedParticle::get_phi(MissingET)")

               )

		# select branches for output file
                branchList = ROOT.vector('string')()
                commonBranches = [
                        ######## Monte-Carlo particles #######
                        "All_n_GenHNL",
                        "AllGenHNL_mass",
                        "AllGenHNL_e",
                        "AllGenHNL_p",
                        "AllGenHNL_pt",
                        "AllGenHNL_px",
                        "AllGenHNL_py",
                        "AllGenHNL_pz",
                        "AllGenHNL_eta",
                        "AllGenHNL_theta",
                        "AllGenHNL_phi",
                        "AllGenHNL_genStatus",
                        "n_FSGenElectron",
                        "FSGenElectron_e",
                        "FSGenElectron_p",
                        "FSGenElectron_pt",
                        "FSGenElectron_px",
                        "FSGenElectron_py",
                        "FSGenElectron_pz",
                        "FSGenElectron_eta",
                        "FSGenElectron_theta",
                        "FSGenElectron_phi",
                        "FSGenElectron_vertex_x",
                        "FSGenElectron_vertex_y",
                        "FSGenElectron_vertex_z",
                        "FSGen_Lxy",
                        "FSGen_Lxyz",
                        "n_FSGenNeutrino",
                        "FSGenNeutrino_e",
                        "FSGenNeutrino_p",
                        "FSGenNeutrino_pt",
                        "FSGenNeutrino_px",
                        "FSGenNeutrino_py",
                        "FSGenNeutrino_pz",
                        "FSGenNeutrino_eta",
                        "FSGenNeutrino_theta",
                        "FSGenNeutrino_phi",
                        "n_FSGenPhoton",
                        "FSGenPhoton_e",
                        "FSGenPhoton_p",
                        "FSGenPhoton_pt",
                        "FSGenPhoton_px",
                        "FSGenPhoton_py",
                        "FSGenPhoton_pz",
                        "FSGenPhoton_eta",
                        "FSGenPhoton_theta",
                        "FSGenPhoton_phi",
                        "FSGen_lifetime_xy",
                        "FSGen_lifetime_xyz",
                        "GenHNL_mass",
                        "GenHNL_p",
                        "GenHNL_pt",
                        "GenHNL_pz",
                        "GenHNL_eta",
                        "GenHNL_theta",
                        "GenHNL_phi",
                        "GenHNL_charge",
                        "GenHNL_genStatus",
                        "GenHNLElectron_mass",
                        "GenHNLElectron_e",
                        "GenHNLElectron_p",
                        "GenHNLElectron_pt",
                        "GenHNLElectron_px",
                        "GenHNLElectron_py",
                        "GenHNLElectron_pz",
                        "GenHNLElectron_eta",
                        "GenHNLElectron_theta",
                        "GenHNLElectron_phi",
                        "GenHNLElectron_charge",
                        "GenHNLElectron_genStatus",
                        "GenHNLElectron_vertex_x",
                        "GenHNLElectron_vertex_y",
                        "GenHNLElectron_vertex_z",
                        "GenHNL_vertex_x",
                        "GenHNL_vertex_y",
                        "GenHNL_vertex_z",
                        "GenHNLMCDecayVertex",
                        "MC_PrimaryVertex",
                        "GenHNL_Lxy",
                        "GenHNL_Lxyz",
                        "GenHNL_lifetime_xy",
                        "GenHNL_lifetime_xyz",
                        ######## Reconstructed particles #######
                        "n_RecoTracks",
                        "RecoHNLParticles",
                        "RecoHNLTracks",
                        "n_RecoHNLTracks",
                        "RecoHNLTracks_absD0",
                        "RecoHNLTracks_absZ0",
                        "RecoHNLTracks_absD0sig",
                        "RecoHNLTracks_absZ0sig",
                        "RecoHNLTracks_D0cov",
                        "RecoHNLTracks_Z0cov",
                        "RecoHNLDecayVertexObject",
                        "RecoHNLDecayVertex",
                        "RecoHNL_Lxy",
                        "RecoHNL_Lxyz",
                        "RecoHNLElectron_e",
                        "RecoHNLElectron_p",
                        "RecoHNLElectron_pt",
                        "RecoHNLElectron_px",
                        "RecoHNLElectron_py",
                        "RecoHNLElectron_pz",
                        "RecoHNLElectron_eta",
                        "RecoHNLElectron_theta",
                        "RecoHNLElectron_phi",
                        "RecoHNLElectron_charge",
                        "GenMinusRecoHNLElectron_e",
                        "GenMinusRecoHNLElectron_p",
                        "GenMinusRecoHNLElectron_pt",
                        "GenMinusRecoHNLElectron_px",
                        "GenMinusRecoHNLElectron_py",
                        "GenMinusRecoHNLElectron_pz",
                        "GenMinusRecoHNLElectron_eta",
                        "GenMinusRecoHNLElectron_theta",
                        "GenMinusRecoHNLElectron_phi",
                        "GenMinusRecoHNL_DecayVertex_x",
                        "GenMinusRecoHNL_DecayVertex_y",
                        "GenMinusRecoHNL_DecayVertex_z",
                        "GenMinusRecoHNL_Lxy",
                        "GenMinusRecoHNL_Lxyz",
                        "n_RecoJets",
                        "n_RecoPhotons",
                        "n_RecoElectrons",
                        "n_RecoMuons",
                        "RecoJet_e",
                        "RecoJet_p",
                        "RecoJet_pt",
                        "RecoJet_px",
                        "RecoJet_py",
                        "RecoJet_pz",
                        "RecoJet_eta",
                        "RecoJet_theta",
                        "RecoJet_phi",
                        "RecoJet_charge",
                        "RecoJetTrack_absD0",
                        "RecoJetTrack_absZ0",
                        "RecoJetTrack_absD0sig",
                        "RecoJetTrack_absZ0sig",
                        "RecoJetTrack_D0cov",
                        "RecoJetTrack_Z0cov",
                        "RecoPhoton_e",
                        "RecoPhoton_p",
                        "RecoPhoton_pt",
                        "RecoPhoton_px",
                        "RecoPhoton_py",
                        "RecoPhoton_pz",
                        "RecoPhoton_eta",
                        "RecoPhoton_theta",
                        "RecoPhoton_phi",
                        "RecoPhoton_charge",
                        "RecoElectron_e",
                        "RecoElectron_p",
                        "RecoElectron_pt",
                        "RecoElectron_px",
                        "RecoElectron_py",
                        "RecoElectron_pz",
                        "RecoElectron_eta",
                        "RecoElectron_theta",
                        "RecoElectron_phi",
                        "RecoElectron_charge",
                        "RecoElectronTrack_absD0",
                        "RecoElectronTrack_absZ0",
                        "RecoElectronTrack_absD0sig",
                        "RecoElectronTrack_absZ0sig",
                        "RecoElectronTrack_D0cov",
                        "RecoElectronTrack_Z0cov",
                        "RecoMuon_e",
                        "RecoMuon_p",
                        "RecoMuon_pt",
                        "RecoMuon_px",
                        "RecoMuon_py",
                        "RecoMuon_pz",
                        "RecoMuon_eta",
                        "RecoMuon_theta",
                        "RecoMuon_phi",
                        "RecoMuon_charge",
                        "RecoMuonTrack_absD0",
                        "RecoMuonTrack_absZ0",
                        "RecoMuonTrack_absD0sig",
                        "RecoMuonTrack_absZ0sig",
                        "RecoMuonTrack_D0cov",
                        "RecoMuonTrack_Z0cov",
                        "RecoMissingEnergy_e",
                        "RecoMissingEnergy_p",
                        "RecoMissingEnergy_pt",
                        "RecoMissingEnergy_px",
                        "RecoMissingEnergy_py",
                        "RecoMissingEnergy_pz",
                        "RecoMissingEnergy_eta",
                        "RecoMissingEnergy_theta",
                        "RecoMissingEnergy_phi",
		]
                eenuBranches = [
                        "FSGen_ee_invMass",
                        "FSGen_eenu_invMass",
                        "GenHNLElectron2_e",
                        "GenHNLElectron2_p",
                        "GenHNLElectron2_pt",
                        "GenHNLElectron2_px",
                        "GenHNLElectron2_py",
                        "GenHNLElectron2_pz",
                        "GenHNLElectron2_eta",
                        "GenHNLElectron2_theta",
                        "GenHNLElectron2_phi",
                        "GenHNLElectron2_charge",
                        "GenHNLElectron2_genStatus",
                        "GenHNLNeutrino_e",
                        "GenHNLNeutrino_p",
                        "GenHNLNeutrino_pt",
                        "GenHNLNeutrino_px",
                        "GenHNLNeutrino_py",
                        "GenHNLNeutrino_pz",
                        "GenHNLNeutrino_eta",
                        "GenHNLNeutrino_theta",
                        "GenHNLNeutrino_phi",
                        "GenHNLNeutrino_charge",
                        "GenHNLNeutrino_genStatus",
                        "GenHNL_ee_invMass",
                        "GenHNL_eenu_invMass",
                        "RecoHNLElectron2_e",
                        "RecoHNLElectron2_p",
                        "RecoHNLElectron2_pt",
                        "RecoHNLElectron2_px",
                        "RecoHNLElectron2_py",
                        "RecoHNLElectron2_pz",
                        "RecoHNLElectron2_eta",
                        "RecoHNLElectron2_theta",
                        "RecoHNLElectron2_phi",
                        "RecoHNLElectron2_charge",
                        "RecoHNL_ee_invMass",
                        "GenMinusRecoHNLElectron2_e",
                        "GenMinusRecoHNLElectron2_p",
                        "GenMinusRecoHNLElectron2_pt",
                        "GenMinusRecoHNLElectron2_px",
                        "GenMinusRecoHNLElectron2_py",
                        "GenMinusRecoHNLElectron2_pz",
                        "GenMinusRecoHNLElectron2_eta",
                        "GenMinusRecoHNLElectron2_theta",
                        "GenMinusRecoHNLElectron2_phi",
                ]
                ejjBranches = [
                        "GenHNLPiZero_e",
                        "GenHNLPiZero_p",
                        "GenHNLPiZero_pt",
                        "GenHNLPiZero_px",
                        "GenHNLPiZero_py",
                        "GenHNLPiZero_pz",
                        "GenHNLPiZero_eta",
                        "GenHNLPiZero_theta",
                        "GenHNLPiZero_phi",
                        "GenHNLPiZero_charge",
                        "GenHNLPiZero_genStatus",
                        "GenHNLPiPlusMinus_e",
                        "GenHNLPiPlusMinus_p",
                        "GenHNLPiPlusMinus_pt",
                        "GenHNLPiPlusMinus_px",
                        "GenHNLPiPlusMinus_py",
                        "GenHNLPiPlusMinus_pz",
                        "GenHNLPiPlusMinus_eta",
                        "GenHNLPiPlusMinus_theta",
                        "GenHNLPiPlusMinus_phi",
                        "GenHNLPiPlusMinus_charge",
                        "GenHNLPiPlusMinus_genStatus",
                        "GenHNLPhoton_e",
                        "GenHNLPhoton_p",
                        "GenHNLPhoton_pt",
                        "GenHNLPhoton_px",
                        "GenHNLPhoton_py",
                        "GenHNLPhoton_pz",
                        "GenHNLPhoton_eta",
                        "GenHNLPhoton_theta",
                        "GenHNLPhoton_phi",
                        "GenHNLPhoton_charge",
                        "GenHNLPhoton_genStatus",
                        "GenHNL_epipigamma_invMass",
                ]

                for branchName in commonBranches:
                        branchList.push_back(branchName)
                if args.channel == "eenu":
                        for branchName in eenuBranches:
                                branchList.push_back(branchName)
                elif args.channel == "ejj":
                        for branchName in ejjBranches:
                                branchList.push_back(branchName)

                df2.Snapshot("events", self.outname, branchList)


if __name__ == "__main__":

	#TODO: UPDATE TO USE A DEDICATED TESTER FILE? 
        default_input_tester = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v04/pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic/events_000087952.root"
        default_out_dir = "./read_EDM4HEP/"
        default_channel = "eenu"

	#parse input arguments:
        parser = argparse.ArgumentParser(description="Basic example how to access objects and simple variables with FCCAnalyses.")
        parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="input_file", default=default_input_tester, help="Path to the input file. If not specified, runs over a default tester file.")
        parser.add_argument('--output', '-o', metavar="OUTPUTDIR", dest="out_dir", default=default_out_dir, help="Output directory. If not specified, sets to a subdirectory called read_EDM4HEP in the current working directory.")
        parser.add_argument('--channel', '-c', metavar="CHANNEL", dest="channel", default=default_channel, help="HNL decay channel. Options are eenu and ejj. If not specified, sets to eenu.")
        args = parser.parse_args()

	#create the output dir, if it doesnt exist yet:
        if not os.path.exists(args.out_dir):
                os.mkdir(args.out_dir)

	#build the name/path of the output file:
        output_file = os.path.join(args.out_dir, args.input_file.split("/")[-1])

        
	#TODO: CLEAN UP
	#now run:
        print("##### Running basic example analysis #####")
        print("Input file: ", args.input_file)
        print("Output file: ", output_file)
        print("Channel: ", args.channel)

        if args.channel == "eenu":
                daughters = "11, -11, 12"
        elif args.channel == "ejj":
                daughters = "11, 111, 211, 22"

        #run analysis
        ncpus = 4
        analysis = analysis(args.input_file, output_file, ncpus)
        analysis.run()




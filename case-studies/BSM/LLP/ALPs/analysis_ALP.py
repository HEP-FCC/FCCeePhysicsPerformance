# This is a basic example showing how to read different objects like electrons, jets, ETmiss etc. from the EDM4HEP files 
# and how to access and store some simple variables in an output ntuple.
# It has been edited in order to accomodate studies of ALPs using the FCC framework

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
_ALP   = ROOT.dummyLoaderFlavour #### Needed to fix undeclared selMC_leg()

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

print ('Finished loading analyzers. Ready to go.')


#The analysis class handles which variables are defined and written to the output ntuple

#right now, only set up for ALP decays
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
               

                # Following code is written specifically for the ALP study
                ####################################################################################################
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
 
                ##### Added branch for MCParticle; finding PID of the MC particle for ALP
                .Define("GenALP_PID", "MCParticle::sel_pdgID(9000005, false)(Particle)")
                .Define("GenALP_decay", "MCParticle::get_list_of_particles_from_decay(0, GenALP_PID, Particle1)")

                .Define("All_n_GenALP", "MCParticle::get_n(GenALP_PID)")
                .Define("AllGenALP_mass", "MCParticle::get_mass(GenALP_PID)") #finding the generator mass of the ALP through separate ALP branch
                .Define("AllGenALP_e", "MCParticle::get_e(GenALP_PID)")
                .Define("AllGenALP_p", "MCParticle::get_p(GenALP_PID)")
                .Define("AllGenALP_pt", "MCParticle::get_pt(GenALP_PID)")    #finding the pt of the ALP thorugh separate ALP branch
                .Define("AllGenALP_px", "MCParticle::get_px(GenALP_PID)")
                .Define("AllGenALP_py", "MCParticle::get_py(GenALP_PID)")
                .Define("AllGenALP_pz", "MCParticle::get_pz(GenALP_PID)")
                .Define("AllGenALP_eta", "MCParticle::get_eta(GenALP_PID)")
                .Define("AllGenALP_theta", "MCParticle::get_theta(GenALP_PID)")
                .Define("AllGenALP_phi", "MCParticle::get_phi(GenALP_PID)")
                .Define("AllGenALP_genStatus", "MCParticle::get_genStatus(GenALP_PID)")

                #all final state gen electrons
                .Define("GenElectron_PID", "MCParticle::sel_pdgID(11, false)(Particle)") #get MCParticle electrons, but not their charge conjugates
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

                #all final state gen positrons
                .Define("GenPositron_PID", "MCParticle::sel_pdgID(-11, false)(Particle)")
                .Define("FSGenPositron", "MCParticle::sel_genStatus(1)(GenPositron_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenPositron", "MCParticle::get_n(FSGenPositron)")
                .Define("FSGenPositron_e", "MCParticle::get_e(FSGenPositron)")
                .Define("FSGenPositron_p", "MCParticle::get_p(FSGenPositron)")
                .Define("FSGenPositron_pt", "MCParticle::get_pt(FSGenPositron)")
                .Define("FSGenPositron_px", "MCParticle::get_px(FSGenPositron)")
                .Define("FSGenPositron_py", "MCParticle::get_py(FSGenPositron)")
                .Define("FSGenPositron_pz", "MCParticle::get_pz(FSGenPositron)")
                .Define("FSGenPositron_eta", "MCParticle::get_eta(FSGenPositron)")
                .Define("FSGenPositron_theta", "MCParticle::get_theta(FSGenPositron)")
                .Define("FSGenPositron_phi", "MCParticle::get_phi(FSGenPositron)")

                #all final state gen neutrinos
                .Define("GenNeutrino_PID", "MCParticle::sel_pdgID(12, false)(Particle)")
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

                #all final state gen anti-neutrinos
                .Define("GenAntiNeutrino_PID", "MCParticle::sel_pdgID(-12, false)(Particle)")
                .Define("FSGenAntiNeutrino", "MCParticle::sel_genStatus(1)(GenAntiNeutrino_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenAntiNeutrino", "MCParticle::get_n(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_e", "MCParticle::get_e(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_p", "MCParticle::get_p(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_pt", "MCParticle::get_pt(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_px", "MCParticle::get_px(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_py", "MCParticle::get_py(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_pz", "MCParticle::get_pz(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_eta", "MCParticle::get_eta(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_theta", "MCParticle::get_theta(FSGenAntiNeutrino)")
                .Define("FSGenAntiNeutrino_phi", "MCParticle::get_phi(FSGenAntiNeutrino)")

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

                # Number of final state electrons and positrons when the number of final state photons is only 2
                # Returns -2 if the number of final state photons != 2, and therefore will be shown as -2 in the plots
                # .Define("n_FSGenElectron_forFS2GenPhotons", "if (n_FSGenPhoton == 2) {return (n_FSGenElectron); } else {return (-2); }")
                # .Define("n_FSGenPositron_forFS2GenPhotons", "if (n_FSGenPhoton == 2) {return (n_FSGenPositron); } else {return (-2); }")

                .Define("FSGenPhoton_vertex_x", "MCParticle::get_vertex_x( FSGenPhoton )")
                .Define("FSGenPhoton_vertex_y", "MCParticle::get_vertex_y( FSGenPhoton )")
                .Define("FSGenPhoton_vertex_z", "MCParticle::get_vertex_z( FSGenPhoton )")

                # Finding the Lxy of the ALP
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
                .Define("FSGen_Lxy", "return sqrt(FSGenPhoton_vertex_x*FSGenPhoton_vertex_x + FSGenPhoton_vertex_y*FSGenPhoton_vertex_y)")
                .Define("FSGen_Lxyz", "return sqrt(FSGenPhoton_vertex_x*FSGenPhoton_vertex_x + FSGenPhoton_vertex_y*FSGenPhoton_vertex_y + FSGenPhoton_vertex_z*FSGenPhoton_vertex_z)")

                # Calculating the lifetime of the ALP
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                .Define("FSGen_lifetime_xy", "return ( FSGen_Lxy.at(0) * AllGenALP_mass / (AllGenALP_pt * 3E8 * 1000))" )
                .Define("FSGen_lifetime_xyz", "return ( FSGen_Lxy.at(0) * AllGenALP_mass / (AllGenALP_p * 3E8 * 1000))" )

                # Separating the three first final state photons
                # Returns -2 if the number of final state photons != 2, and therefore will be shown as -2 in the plots
                # .Define("FSGenPhoton0_e", "return FSGenPhoton_e.at(0)")
                # .Define("FSGenPhoton1_e", "if (n_FSGenPhoton > 2) {return FSGenPhoton_e.at(1);} else {return (-2.0f); }")
                # .Define("FSGenPhoton2_e", "if (n_FSGenPhoton > 3) {return FSGenPhoton_e.at(2);} else {return (-2.0f); }")
                # .Define("FSGenPhoton0_p", "return FSGenPhoton_p.at(0)")
                # .Define("FSGenPhoton1_p", "if (n_FSGenPhoton > 2) {return FSGenPhoton_p.at(1);} else {return (-2.0f); }")
                # .Define("FSGenPhoton2_p", "if (n_FSGenPhoton > 2) {return FSGenPhoton_p.at(2);} else {return (-2.0f); }")
                # .Define("FSGenPhoton0_pt", "return FSGenPhoton_pt.at(0)")
                # .Define("FSGenPhoton1_pt", "if (n_FSGenPhoton > 2) {return FSGenPhoton_pt.at(1);} else {return (-2.0f); }")
                # .Define("FSGenPhoton2_pt", "if (n_FSGenPhoton > 3) {return FSGenPhoton_pt.at(2);} else {return (-2.0f); }")
                # .Define("FSGenPhoton0_px", "return FSGenPhoton_px.at(0)")
                # .Define("FSGenPhoton1_px", "if (n_FSGenPhoton > 2) {return FSGenPhoton_px.at(1);} else {return (-2.0f); }")
                # .Define("FSGenPhoton2_px", "if (n_FSGenPhoton > 3) {return FSGenPhoton_px.at(2);} else {return (-2.0f); }")
                # .Define("FSGenPhoton0_py", "return FSGenPhoton_py.at(0)")
                # .Define("FSGenPhoton1_py", "if (n_FSGenPhoton > 2) {return FSGenPhoton_py.at(1);} else {return (-2.0f); }")
                # .Define("FSGenPhoton2_py", "if (n_FSGenPhoton > 3) {return FSGenPhoton_py.at(2);} else {return (-2.0f); }")
                # .Define("FSGenPhoton0_pz", "return FSGenPhoton_pz.at(0)")
                # .Define("FSGenPhoton1_pz", "if (n_FSGenPhoton > 2) {return FSGenPhoton_pz.at(1);} else {return (-2.0f); }")
                # .Define("FSGenPhoton2_pz", "if (n_FSGenPhoton > 3) {return FSGenPhoton_pz.at(2);} else {return (-2.0f); }")

                # aa invariant mass - for all three combinations of the three first FS photons
                # returns -2 for events with only 1 number of photons
                # .Define("FSGen_a0a1_energy", "return (FSGenPhoton0_e + FSGenPhoton1_e)")
                # .Define("FSGen_a0a1_px", "return (FSGenPhoton0_px + FSGenPhoton1_px)")
                # .Define("FSGen_a0a1_py", "return (FSGenPhoton0_py + FSGenPhoton1_py)")
                # .Define("FSGen_a0a1_pz", "return (FSGenPhoton0_pz + FSGenPhoton1_pz)")
                # .Define("FSGen_a0a1_invMass", "if (n_FSGenPhoton > 1) { return sqrt(FSGen_a0a1_energy*FSGen_a0a1_energy - FSGen_a0a1_px*FSGen_a0a1_px - FSGen_a0a1_py*FSGen_a0a1_py - FSGen_a0a1_pz*FSGen_a0a1_pz ); } else {return -2.0f;}")

                # .Define("FSGen_a0a2_energy", "return (FSGenPhoton0_e + FSGenPhoton2_e)")
                # .Define("FSGen_a0a2_px", "return (FSGenPhoton0_px + FSGenPhoton2_px)")
                # .Define("FSGen_a0a2_py", "return (FSGenPhoton0_py + FSGenPhoton2_py)")
                # .Define("FSGen_a0a2_pz", "return (FSGenPhoton0_pz + FSGenPhoton2_pz)")
                # .Define("FSGen_a0a2_invMass", "if (n_FSGenPhoton > 1) { return sqrt(FSGen_a0a2_energy*FSGen_a0a2_energy - FSGen_a0a2_px*FSGen_a0a2_px - FSGen_a0a2_py*FSGen_a0a2_py - FSGen_a0a2_pz*FSGen_a0a2_pz ); } else {return -2.0f;}")

                # .Define("FSGen_a1a2_energy", "return (FSGenPhoton1_e + FSGenPhoton2_e)")
                # .Define("FSGen_a1a2_px", "return (FSGenPhoton1_px + FSGenPhoton2_px)")
                # .Define("FSGen_a1a2_py", "return (FSGenPhoton1_py + FSGenPhoton2_py)")
                # .Define("FSGen_a1a2_pz", "return (FSGenPhoton1_pz + FSGenPhoton2_pz)")
                # .Define("FSGen_a1a2_invMass", "if (n_FSGenPhoton > 1) { return sqrt(FSGen_a1a2_energy*FSGen_a1a2_energy - FSGen_a1a2_px*FSGen_a1a2_px - FSGen_a1a2_py*FSGen_a1a2_py - FSGen_a1a2_pz*FSGen_a1a2_pz ); } else {return -2.0f;}")

                # aaa invariant mass
                # Returns -2 for events with only 1 or 2 number of photons
                # .Define("FSGen_aaa_energy", "return (FSGenPhoton0_e + FSGenPhoton1_e + FSGenPhoton2_e)")
                # .Define("FSGen_aaa_px", "return (FSGenPhoton0_px + FSGenPhoton1_px + FSGenPhoton2_px)")
                # .Define("FSGen_aaa_py", "return (FSGenPhoton0_py + FSGenPhoton1_py + FSGenPhoton2_py)")
                # .Define("FSGen_aaa_pz", "return (FSGenPhoton0_pz + FSGenPhoton1_pz + FSGenPhoton2_pz)")
                # .Define("FSGen_aaa_invMass", "if (n_FSGenPhoton > 2) { return sqrt(FSGen_aaa_energy*FSGen_aaa_energy - FSGen_aaa_px*FSGen_aaa_px - FSGen_aaa_py*FSGen_aaa_py - FSGen_aaa_pz*FSGen_aaa_pz ); } else {return -2.0f;}")

                # Defining a vector containing the ALP and its daughters in order written
                # Name of vector is ALP_indices
                .Define("GenALP_indices", "MCParticle::get_indices(9000005, {22, 22}, true, false, false, true)(Particle, Particle1)")
                
                # Defining the individual particles from the vector
                .Define("GenALP", "selMC_leg(0)(GenALP_indices, Particle)")
                .Define("GenALPPhoton1", "selMC_leg(1)(GenALP_indices, Particle)")
                .Define("GenALPPhoton2", "selMC_leg(2)(GenALP_indices, Particle)")

                # Kinematics of the mother particle ALP
                .Define("GenALP_mass", "MCParticle::get_mass( GenALP )")
                .Define("GenALP_e", "MCParticle::get_e( GenALP )")
                .Define("GenALP_p", "MCParticle::get_p( GenALP )")
                .Define("GenALP_pt", "MCParticle::get_pt( GenALP )")
                .Define("GenALP_px", "MCParticle::get_px( GenALP )")
                .Define("GenALP_py", "MCParticle::get_py( GenALP )")
                .Define("GenALP_pz", "MCParticle::get_pz( GenALP )")
                .Define("GenALP_eta", "MCParticle::get_eta( GenALP )")
                .Define("GenALP_theta", "MCParticle::get_theta( GenALP )")
                .Define("GenALP_phi", "MCParticle::get_phi( GenALP )")
                .Define("GenALP_genStatus", "MCParticle::get_genStatus( GenALP )")

                # Finding the kinematics of each of these daughters
                .Define("GenALPPhoton1_e", "MCParticle::get_e( GenALPPhoton1 )")
                .Define("GenALPPhoton2_e", "MCParticle::get_e( GenALPPhoton2 )")
                .Define("GenALPPhoton1_p", "MCParticle::get_p( GenALPPhoton1 )")
                .Define("GenALPPhoton2_p", "MCParticle::get_p( GenALPPhoton2 )")
                .Define("GenALPPhoton1_pt", "MCParticle::get_pt( GenALPPhoton1 )")
                .Define("GenALPPhoton2_pt", "MCParticle::get_pt( GenALPPhoton2 )")
                .Define("GenALPPhoton1_px", "MCParticle::get_px( GenALPPhoton1 )")
                .Define("GenALPPhoton2_px", "MCParticle::get_px( GenALPPhoton2 )")
                .Define("GenALPPhoton1_py", "MCParticle::get_py( GenALPPhoton1 )")
                .Define("GenALPPhoton2_py", "MCParticle::get_py( GenALPPhoton2 )")
                .Define("GenALPPhoton1_pz", "MCParticle::get_pz( GenALPPhoton1 )")
                .Define("GenALPPhoton2_pz", "MCParticle::get_pz( GenALPPhoton2 )")
                .Define("GenALPPhoton1_eta", "MCParticle::get_eta( GenALPPhoton1 )")
                .Define("GenALPPhoton2_eta", "MCParticle::get_eta( GenALPPhoton2 )")
                .Define("GenALPPhoton1_theta", "MCParticle::get_theta( GenALPPhoton1 )")
                .Define("GenALPPhoton2_theta", "MCParticle::get_theta( GenALPPhoton2 )")
                .Define("GenALPPhoton1_phi", "MCParticle::get_phi( GenALPPhoton1 )")
                .Define("GenALPPhoton2_phi", "MCParticle::get_phi( GenALPPhoton2 )")
                .Define("GenALPPhoton1_genStatus", "MCParticle::get_genStatus( GenALPPhoton1 )")
                .Define("GenALPPhoton2_genStatus", "MCParticle::get_genStatus( GenALPPhoton2 )")

                # Finding the production vertex of the daughters (checking GenALPPhoton1 here)
                .Define("GenALPPhoton1_vertex_x", "MCParticle::get_vertex_x( GenALPPhoton1 )")
                .Define("GenALPPhoton1_vertex_y", "MCParticle::get_vertex_y( GenALPPhoton1 )")
                .Define("GenALPPhoton1_vertex_z", "MCParticle::get_vertex_z( GenALPPhoton1 )")

                # Finding the Lxy of the ALP
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )  
                .Define("GenALP_Lxy", "return sqrt(GenALPPhoton1_vertex_x*GenALPPhoton1_vertex_x + GenALPPhoton1_vertex_y*GenALPPhoton1_vertex_y)")
                # Finding the Lxyz of the ALP
                .Define("GenALP_Lxyz", "return sqrt(GenALPPhoton1_vertex_x*GenALPPhoton1_vertex_x + GenALPPhoton1_vertex_y*GenALPPhoton1_vertex_y + GenALPPhoton1_vertex_z*GenALPPhoton1_vertex_z)")
                
                # Calculating the lifetime of the ALP
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                .Define("GenALP_lifetime_xy", "return ( GenALP_Lxy * GenALP_mass / (GenALP_pt * 3E8 * 1000))" )
                .Define("GenALP_lifetime_xyz", "return ( GenALP_Lxyz * GenALP_mass / (GenALP_p * 3E8 * 1000))" )
               
                # Finding the production vertex of the ALP which should be at (0,0,0) 
                .Define("GenALP_vertex_x", "MCParticle::get_vertex_x(GenALP_PID)")
                .Define("GenALP_vertex_y", "MCParticle::get_vertex_y(GenALP_PID)")
                .Define("GenALP_vertex_z", "MCParticle::get_vertex_z(GenALP_PID)")

                # aa invariant mass
                .Define("GenALP_aa_energy", "return (GenALPPhoton1_e + GenALPPhoton2_e)")
                .Define("GenALP_aa_px", "return (GenALPPhoton1_px + GenALPPhoton2_px)")
                .Define("GenALP_aa_py", "return (GenALPPhoton1_py + GenALPPhoton2_py)")
                .Define("GenALP_aa_pz", "return (GenALPPhoton1_pz + GenALPPhoton2_pz)")
                .Define("GenALP_aa_invMass", "return sqrt(GenALP_aa_energy*GenALP_aa_energy - GenALP_aa_px*GenALP_aa_px - GenALP_aa_py*GenALP_aa_py - GenALP_aa_pz*GenALP_aa_pz )")

                # Vertexing studies
                # Finding the vertex of the mother particle ALP using decicated Bs method
                .Define("GenALPMCDecayVertex",   "BsMCDecayVertex( GenALP_indices, Particle )")

                # MC event primary vertex
                .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

                # Reconstructed particles
                # Returns the RecoParticles associated with the ALP decay products
                .Define("RecoALPParticles",  "ReconstructedParticle2MC::selRP_matched_to_list( GenALP_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                # Reconstructing the tracks from the ALP
                .Define("RecoALPTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoALPParticles, EFlowTrack_1)")

                # Number of tracks in this RecoALPTracks collection ( = the #tracks used to reconstruct the ALP reco decay vertex)
                .Define("n_RecoALPTracks", "ReconstructedParticle2Track::getTK_n( RecoALPTracks )")

                # Now we reconstruct the ALP reco decay vertex using the reco'ed tracks
                # First the full object, of type Vertexing::FCCAnalysesVertex
                .Define("RecoALPDecayVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, RecoALPTracks)" )

                # from which we extract the edm4hep::VertexData object, which contains the vertex position in mm
                .Define("RecoALPDecayVertex",  "VertexingUtils::get_VertexData( RecoALPDecayVertexObject )")
                
                # We may want to look at the reco'ed ALPs legs: in the RecoALPParticles vector,
                # the first particle (vector[0]) is the e-, etc :
                .Define("RecoALPPhoton1",   "selRP_leg(0)( RecoALPParticles )")
                .Define("RecoALPPhoton2",   "selRP_leg(1)( RecoALPParticles )")
                
                # reconstruced electron, positron values
                .Define("RecoALPPhoton1_e",  "ReconstructedParticle::get_e( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_e",  "ReconstructedParticle::get_e( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_p",  "ReconstructedParticle::get_p( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_p",  "ReconstructedParticle::get_p( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_pt",  "ReconstructedParticle::get_pt( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_pt",  "ReconstructedParticle::get_pt( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_px",  "ReconstructedParticle::get_px( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_px",  "ReconstructedParticle::get_px( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_py",  "ReconstructedParticle::get_py( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_py",  "ReconstructedParticle::get_py( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_pz",  "ReconstructedParticle::get_pz( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_pz",  "ReconstructedParticle::get_pz( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_eta",  "ReconstructedParticle::get_eta( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_eta",  "ReconstructedParticle::get_eta( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_theta",  "ReconstructedParticle::get_theta( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_theta",  "ReconstructedParticle::get_theta( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_phi",  "ReconstructedParticle::get_phi( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_phi",  "ReconstructedParticle::get_phi( RecoALPPhoton2 )")
                .Define("RecoALPPhoton1_charge",  "ReconstructedParticle::get_charge( RecoALPPhoton1 )")
                .Define("RecoALPPhoton2_charge",  "ReconstructedParticle::get_charge( RecoALPPhoton2 )")
                # add dxy, dz, dxyz, and uncertainties

                # aa invariant mass
                .Define("RecoALP_aa_energy", "return (RecoALPPhoton1_e + RecoALPPhoton2_e)")
                .Define("RecoALP_aa_px", "return (RecoALPPhoton1_px + RecoALPPhoton2_px)")
                .Define("RecoALP_aa_py", "return (RecoALPPhoton1_py + RecoALPPhoton2_py)")
                .Define("RecoALP_aa_pz", "return (RecoALPPhoton1_pz + RecoALPPhoton2_pz)")
                .Define("RecoALP_aa_invMass", "return sqrt(RecoALP_aa_energy*RecoALP_aa_energy - RecoALP_aa_px*RecoALP_aa_px - RecoALP_aa_py*RecoALP_aa_py - RecoALP_aa_pz*RecoALP_aa_pz )")

                #gen-reco
                .Define("GenMinusRecoALPPhoton1_e",   "GenALPPhoton1_e-RecoALPPhoton1_e")
                .Define("GenMinusRecoALPPhoton2_e",   "GenALPPhoton2_e-RecoALPPhoton2_e")
                .Define("GenMinusRecoALPPhoton1_p",   "GenALPPhoton1_p-RecoALPPhoton1_p")
                .Define("GenMinusRecoALPPhoton2_p",   "GenALPPhoton2_p-RecoALPPhoton2_p")
                .Define("GenMinusRecoALPPhoton1_pt",   "GenALPPhoton1_pt-RecoALPPhoton1_pt")
                .Define("GenMinusRecoALPPhoton2_pt",   "GenALPPhoton2_pt-RecoALPPhoton2_pt")
                .Define("GenMinusRecoALPPhoton1_px",   "GenALPPhoton1_px-RecoALPPhoton1_px")
                .Define("GenMinusRecoALPPhoton2_px",   "GenALPPhoton2_px-RecoALPPhoton2_px")
                .Define("GenMinusRecoALPPhoton1_py",   "GenALPPhoton1_py-RecoALPPhoton1_py")
                .Define("GenMinusRecoALPPhoton2_py",   "GenALPPhoton2_py-RecoALPPhoton2_py")
                .Define("GenMinusRecoALPPhoton1_pz",   "GenALPPhoton1_pz-RecoALPPhoton1_pz")
                .Define("GenMinusRecoALPPhoton2_pz",   "GenALPPhoton2_pz-RecoALPPhoton2_pz")
                .Define("GenMinusRecoALPPhoton1_eta",  "GenALPPhoton1_eta-RecoALPPhoton1_eta")
                .Define("GenMinusRecoALPPhoton2_eta",  "GenALPPhoton2_eta-RecoALPPhoton2_eta")
                .Define("GenMinusRecoALPPhoton1_theta",  "GenALPPhoton1_theta-RecoALPPhoton1_theta")
                .Define("GenMinusRecoALPPhoton2_theta",  "GenALPPhoton2_theta-RecoALPPhoton2_theta")
                .Define("GenMinusRecoALPPhoton1_phi",  "GenALPPhoton1_phi-RecoALPPhoton1_phi")
                .Define("GenMinusRecoALPPhoton2_phi",  "GenALPPhoton2_phi-RecoALPPhoton2_phi")

                .Define("GenMinusRecoALP_DecayVertex_x",  "GenALPPhoton1_vertex_x-RecoALPDecayVertex.position.x")
                .Define("GenMinusRecoALP_DecayVertex_y",  "GenALPPhoton1_vertex_y-RecoALPDecayVertex.position.y")
                .Define("GenMinusRecoALP_DecayVertex_z",  "GenALPPhoton1_vertex_z-RecoALPDecayVertex.position.z")
                
                       
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
		for branchName in [
                                ######## Monte-Carlo particles #######
                                "All_n_GenALP",
                                "AllGenALP_mass",
                                "AllGenALP_e",
                                "AllGenALP_p",
                                "AllGenALP_pt",
                                "AllGenALP_px",
                                "AllGenALP_py",
                                "AllGenALP_pz",
                                "AllGenALP_eta",
                                "AllGenALP_theta",
                                "AllGenALP_phi",
                                "AllGenALP_genStatus",
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
                                "FSGenPhoton_vertex_x",
                                "FSGenPhoton_vertex_y",
                                "FSGenPhoton_vertex_z",
                                # "n_FSGenElectron_forFS2GenPhotons",
                                # "n_FSGenPositron_forFS2GenPhotons",
                                "FSGen_Lxy",
                                "FSGen_Lxyz",
                                "FSGen_lifetime_xy",
                                "FSGen_lifetime_xyz",
                                "n_FSGenPositron",
                                "FSGenPositron_e",
                                "FSGenPositron_p",
                                "FSGenPositron_pt",
                                "FSGenPositron_px",
                                "FSGenPositron_py",
                                "FSGenPositron_pz",
                                "FSGenPositron_eta",
                                "FSGenPositron_theta",
                                "FSGenPositron_phi",
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
                                "n_FSGenAntiNeutrino",
                                "FSGenAntiNeutrino_e",
                                "FSGenAntiNeutrino_p",
                                "FSGenAntiNeutrino_pt",
                                "FSGenAntiNeutrino_px",
                                "FSGenAntiNeutrino_py",
                                "FSGenAntiNeutrino_pz",
                                "FSGenAntiNeutrino_eta",
                                "FSGenAntiNeutrino_theta",
                                "FSGenAntiNeutrino_phi",
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
                                # "FSGenPhoton0_e",
                                # "FSGenPhoton1_e",
                                # "FSGenPhoton2_e",
                                # "FSGenPhoton0_p",
                                # "FSGenPhoton1_p",
                                # "FSGenPhoton2_p",
                                # "FSGenPhoton0_pt",
                                # "FSGenPhoton1_pt",
                                # "FSGenPhoton2_pt",
                                # "FSGen_a0a1_invMass",
                                # "FSGen_a0a2_invMass",
                                # "FSGen_a1a2_invMass",
                                # "FSGen_aaa_invMass",
                                "GenALP_vertex_x",
                                "GenALP_vertex_y",
                                "GenALP_vertex_z",
                                "GenALP_aa_invMass",
                                "GenALP_mass",
                                "GenALP_p",
                                "GenALP_pt",
                                "GenALP_pz",
                                "GenALP_eta",
                                "GenALP_theta",
                                "GenALP_phi",
                                "GenALP_genStatus",
                                "GenALPPhoton1_e",
                                "GenALPPhoton2_e",
                                "GenALPPhoton1_p",
                                "GenALPPhoton2_p",
                                "GenALPPhoton1_pt",
                                "GenALPPhoton2_pt",
                                "GenALPPhoton1_px",
                                "GenALPPhoton2_px",
                                "GenALPPhoton1_py",
                                "GenALPPhoton2_py",
                                "GenALPPhoton1_pz",
                                "GenALPPhoton2_pz",
                                "GenALPPhoton1_eta",
                                "GenALPPhoton2_eta",
                                "GenALPPhoton1_theta",
                                "GenALPPhoton2_theta",
                                "GenALPPhoton1_phi",
                                "GenALPPhoton2_phi",
                                "GenALPPhoton1_genStatus",
                                "GenALPPhoton2_genStatus",
                                #"GenALP_decay",
                                "GenALPPhoton1_vertex_x",
                                "GenALPPhoton1_vertex_y",
                                "GenALPPhoton1_vertex_z",
                                "GenALP_Lxy",
                                "GenALP_Lxyz",
                                "GenALP_lifetime_xy",
                                "GenALP_lifetime_xyz",
                                #"GenALPMCDecayVertex",
                                "MC_PrimaryVertex",
                                "n_RecoTracks",
                                ######## Reconstructed particles #######
                                "RecoALPParticles",
                                "RecoALPTracks",
                                "n_RecoALPTracks",
                                "RecoALPDecayVertexObject",
                                "RecoALPDecayVertex",
                                "RecoALPPhoton1_e",
                                "RecoALPPhoton2_e",
                                "RecoALPPhoton1_p",
                                "RecoALPPhoton2_p",
                                "RecoALPPhoton1_pt",
                                "RecoALPPhoton2_pt",
                                "RecoALPPhoton1_px",
                                "RecoALPPhoton2_px",
                                "RecoALPPhoton1_py",
                                "RecoALPPhoton2_py",
                                "RecoALPPhoton1_pz",
                                "RecoALPPhoton2_pz",
                                "RecoALPPhoton1_eta",
                                "RecoALPPhoton2_eta",
                                "RecoALPPhoton1_theta",
                                "RecoALPPhoton2_theta",
                                "RecoALPPhoton1_phi",
                                "RecoALPPhoton2_phi",
                                "RecoALPPhoton1_charge",
                                "RecoALPPhoton2_charge",
                                "RecoALP_aa_invMass",
                                "GenMinusRecoALPPhoton1_e",
                                "GenMinusRecoALPPhoton2_e",
                                "GenMinusRecoALPPhoton1_p",
                                "GenMinusRecoALPPhoton2_p",
                                "GenMinusRecoALPPhoton1_pt",
                                "GenMinusRecoALPPhoton2_pt",
                                "GenMinusRecoALPPhoton1_px",
                                "GenMinusRecoALPPhoton2_px",
                                "GenMinusRecoALPPhoton1_py",
                                "GenMinusRecoALPPhoton2_py",
                                "GenMinusRecoALPPhoton1_pz",
                                "GenMinusRecoALPPhoton2_pz",
                                "GenMinusRecoALPPhoton1_eta",
                                "GenMinusRecoALPPhoton2_eta",
                                "GenMinusRecoALPPhoton1_theta",
                                "GenMinusRecoALPPhoton2_theta",
                                "GenMinusRecoALPPhoton1_phi",
                                "GenMinusRecoALPPhoton2_phi",
                                "GenMinusRecoALP_DecayVertex_x",
                                "GenMinusRecoALP_DecayVertex_y",
                                "GenMinusRecoALP_DecayVertex_z",
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
                                "RecoMissingEnergy_e",
                                "RecoMissingEnergy_p",
                                "RecoMissingEnergy_pt",
                                "RecoMissingEnergy_px",
                                "RecoMissingEnergy_py",
                                "RecoMissingEnergy_pz",
                                "RecoMissingEnergy_eta",
                                "RecoMissingEnergy_theta",
                                "RecoMissingEnergy_phi",

		]:
			branchList.push_back(branchName)
		df2.Snapshot("events", self.outname, branchList)

if __name__ == "__main__":

	#TODO: UPDATE TO USE A DEDICATED TESTER FILE? 
	default_input_tester = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v04/pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic/events_000087952.root"
	default_out_dir = "./read_EDM4HEP/"

	#parse input arguments:
	parser = argparse.ArgumentParser(description="Basic example how to access objects and simple variables with FCCAnalyses.")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="input_file", default=default_input_tester, help="Path to the input file. If not specified, runs over a default tester file.")
	parser.add_argument('--output', '-o', metavar="OUTPUTDIR", dest="out_dir", default=default_out_dir, help="Output directory. If not specified, sets to a subdirectory called read_EDM4HEP in the current working directory.")
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

	ncpus = 4
	analysis = analysis(args.input_file, output_file, ncpus)
	analysis.run()



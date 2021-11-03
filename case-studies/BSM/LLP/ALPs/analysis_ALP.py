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
                .Define("GenALP_decay", "MCParticle::list_of_particles_from_decay(0, GenALP_PID, Particle1)")

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

                .Define("FSGenElectron_vertex_x", "MCParticle::get_vertex_x( FSGenElectron )")
                .Define("FSGenElectron_vertex_y", "MCParticle::get_vertex_y( FSGenElectron )")
                .Define("FSGenElectron_vertex_z", "MCParticle::get_vertex_z( FSGenElectron )")

                # Finding the Lxy of the ALP
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
                #.Define("FSGen_Lxy", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y)")

                # Calculating the lifetime of the ALP
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                #.Define("FSGen_lifetime", "return ( FSGen_Lxy.at(0) * AllGenALP_mass / (AllGenALP_pt * 3E8 * 1000))" )

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

                # ee invariant mass
                #.Define("FSGen_ee_energy", "return (FSGenElectron_e.at(0) + FSGenPositron_e.at(0))")
                #.Define("FSGen_ee_px", "return (FSGenElectron_px.at(0) + FSGenPositron_px.at(0))")
                #.Define("FSGen_ee_py", "return (FSGenElectron_py.at(0) + FSGenPositron_py.at(0))")
                #.Define("FSGen_ee_pz", "return (FSGenElectron_pz.at(0) + FSGenPositron_pz.at(0))")
                #.Define("FSGen_ee_invMass", "return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz )")

                # eenu invariant mass
                #.Define("FSGen_eenu_energy", "return (FSGenElectron_e.at(0) + FSGenPositron_e.at(0) + FSGenNeutrino_e.at(0))")
                #.Define("FSGen_eenu_px", "return (FSGenElectron_px.at(0) + FSGenPositron_px.at(0) + FSGenNeutrino_px.at(0))")
                #.Define("FSGen_eenu_py", "return (FSGenElectron_py.at(0) + FSGenPositron_py.at(0) + FSGenNeutrino_py.at(0))")
                #.Define("FSGen_eenu_pz", "return (FSGenElectron_pz.at(0) + FSGenPositron_pz.at(0) + FSGenNeutrino_pz.at(0))")
                #.Define("FSGen_eenu_invMass", "return sqrt(FSGen_eenu_energy*FSGen_eenu_energy - FSGen_eenu_px*FSGen_eenu_px - FSGen_eenu_py*FSGen_eenu_py - FSGen_eenu_pz*FSGen_eenu_pz )")

                # Defining a vector containing the ALP and its daughters in order written
                # Name of vector is ALP_indices
                #.Define("GenALP_indices", "MCParticle::get_indices_InclusiveDecay(9000005, {11, -11, 12}, true, false)(Particle, Particle1)")
                #.Define("GenALP_indices", "MCParticle::get_indices_ExclusiveDecay(9000005, {11, -11, 12}, true, false)(Particle, Particle1)")
                #.Define("GenALP_indices", "MCParticle::get_indices_ExclusiveDecay(9000005, {11, -11, 12, 22, 22, 22, 22, 22, 22, 22}, true, false)(Particle, Particle1)")
                
                # Defining the individual particles from the vector
                #.Define("GenALP", "selMC_leg(0)(GenALP_indices, Particle)")
                #.Define("GenALPElectron", "selMC_leg(1)(GenALP_indices, Particle)")
                #.Define("GenALPPositron", "selMC_leg(2)(GenALP_indices, Particle)")
                #.Define("GenALPNeutrino", "selMC_leg(3)(GenALP_indices, Particle)")

                # Kinematics of the mother particle ALP
                #.Define("GenALP_mass", "MCParticle::get_mass( GenALP )")
                #.Define("GenALP_e", "MCParticle::get_e( GenALP )")
                #.Define("GenALP_p", "MCParticle::get_p( GenALP )")
                #.Define("GenALP_pt", "MCParticle::get_pt( GenALP )")
                #.Define("GenALP_px", "MCParticle::get_px( GenALP )")
                #.Define("GenALP_py", "MCParticle::get_py( GenALP )")
                #.Define("GenALP_pz", "MCParticle::get_pz( GenALP )")
                #.Define("GenALP_eta", "MCParticle::get_eta( GenALP )")
                #.Define("GenALP_theta", "MCParticle::get_theta( GenALP )")
                #.Define("GenALP_phi", "MCParticle::get_phi( GenALP )")
                #.Define("GenALP_genStatus", "MCParticle::get_genStatus( GenALP )")

                # Finding the kinematics of each of these daughters
                #.Define("GenALPElectron_mass", "MCParticle::get_mass( GenALPElectron )")
                #.Define("GenALPElectron_e", "MCParticle::get_e( GenALPElectron )")
                #.Define("GenALPPositron_e", "MCParticle::get_e( GenALPPositron )")
                #.Define("GenALPNeutrino_e", "MCParticle::get_e( GenALPNeutrino )")
                #.Define("GenALPElectron_p", "MCParticle::get_p( GenALPElectron )")
                #.Define("GenALPPositron_p", "MCParticle::get_p( GenALPPositron )")
                #.Define("GenALPNeutrino_p", "MCParticle::get_p( GenALPNeutrino )")
                #.Define("GenALPElectron_pt", "MCParticle::get_pt( GenALPElectron )")
                #.Define("GenALPPositron_pt", "MCParticle::get_pt( GenALPPositron )")
                #.Define("GenALPNeutrino_pt", "MCParticle::get_pt( GenALPNeutrino )")
                #.Define("GenALPElectron_px", "MCParticle::get_px( GenALPElectron )")
                #.Define("GenALPPositron_px", "MCParticle::get_px( GenALPPositron )")
                #.Define("GenALPNeutrino_px", "MCParticle::get_px( GenALPNeutrino )")
                #.Define("GenALPElectron_py", "MCParticle::get_py( GenALPElectron )")
                #.Define("GenALPPositron_py", "MCParticle::get_py( GenALPPositron )")
                #.Define("GenALPNeutrino_py", "MCParticle::get_py( GenALPNeutrino )")
                #.Define("GenALPElectron_pz", "MCParticle::get_pz( GenALPElectron )")
                #.Define("GenALPPositron_pz", "MCParticle::get_pz( GenALPPositron )")
                #.Define("GenALPNeutrino_pz", "MCParticle::get_pz( GenALPNeutrino )")
                #.Define("GenALPElectron_eta", "MCParticle::get_eta( GenALPElectron )")
                #.Define("GenALPPositron_eta", "MCParticle::get_eta( GenALPPositron )")
                #.Define("GenALPNeutrino_eta", "MCParticle::get_eta( GenALPNeutrino )")
                #.Define("GenALPElectron_theta", "MCParticle::get_theta( GenALPElectron )")
                #.Define("GenALPPositron_theta", "MCParticle::get_theta( GenALPPositron )")
                #.Define("GenALPNeutrino_theta", "MCParticle::get_theta( GenALPNeutrino )")
                #.Define("GenALPElectron_phi", "MCParticle::get_phi( GenALPElectron )")
                #.Define("GenALPPositron_phi", "MCParticle::get_phi( GenALPPositron )")
                #.Define("GenALPNeutrino_phi", "MCParticle::get_phi( GenALPNeutrino )")
                #.Define("GenALPElectron_genStatus", "MCParticle::get_genStatus( GenALPElectron )")
                #.Define("GenALPPositron_genStatus", "MCParticle::get_genStatus( GenALPPositron )")
                #.Define("GenALPNeutrino_genStatus", "MCParticle::get_genStatus( GenALPNeutrino )")

                # Finding the production vertex of the daughters (checking GenALPElectron here)
                #.Define("GenALPElectron_vertex_x", "MCParticle::get_vertex_x( GenALPElectron )")
                #.Define("GenALPElectron_vertex_y", "MCParticle::get_vertex_y( GenALPElectron )")
                #.Define("GenALPElectron_vertex_z", "MCParticle::get_vertex_z( GenALPElectron )")

                # Finding the Lxy of the ALP
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )  
                #.Define("GenALP_Lxy", "return sqrt(GenALPElectron_vertex_x*GenALPElectron_vertex_x + GenALPElectron_vertex_y*GenALPElectron_vertex_y)")
                
                # Calculating the lifetime of the ALP
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                #.Define("GenALP_lifetime", "return ( GenALP_Lxy * GenALP_mass / (GenALP_pt * 3E8 * 1000))" )
               
                # Finding the production vertex of the ALP which should be at (0,0,0) 
                #.Define("GenALP_vertex_x", "MCParticle::get_vertex_x(GenALP_PID)")
                #.Define("GenALP_vertex_y", "MCParticle::get_vertex_y(GenALP_PID)")
                #.Define("GenALP_vertex_z", "MCParticle::get_vertex_z(GenALP_PID)")

                # ee invariant mass
                #.Define("GenALP_ee_energy", "return (GenALPElectron_e + GenALPPositron_e)")
                #.Define("GenALP_ee_px", "return (GenALPElectron_px + GenALPPositron_px)")
                #.Define("GenALP_ee_py", "return (GenALPElectron_py + GenALPPositron_py)")
                #.Define("GenALP_ee_pz", "return (GenALPElectron_pz + GenALPPositron_pz)")
                #.Define("GenALP_ee_invMass", "return sqrt(GenALP_ee_energy*GenALP_ee_energy - GenALP_ee_px*GenALP_ee_px - GenALP_ee_py*GenALP_ee_py - GenALP_ee_pz*GenALP_ee_pz )")

                # eenu invariant mass
                #.Define("GenALP_eenu_energy", "return (GenALPElectron_e + GenALPPositron_e + GenALPNeutrino_e)")
                #.Define("GenALP_eenu_px", "return (GenALPElectron_px + GenALPPositron_px + GenALPNeutrino_px)")
                #.Define("GenALP_eenu_py", "return (GenALPElectron_py + GenALPPositron_py + GenALPNeutrino_py)")
                #.Define("GenALP_eenu_pz", "return (GenALPElectron_pz + GenALPPositron_pz + GenALPNeutrino_pz)")
                #.Define("GenALP_eenu_invMass", "return sqrt(GenALP_eenu_energy*GenALP_eenu_energy - GenALP_eenu_px*GenALP_eenu_px - GenALP_eenu_py*GenALP_eenu_py - GenALP_eenu_pz*GenALP_eenu_pz )")

                # Vertexing studies
                # Finding the vertex of the mother particle ALP using decicated Bs method
                #.Define("GenALPMCDecayVertex",   "BsMCDecayVertex( GenALP_indices, Particle )")

                # MC event primary vertex
                .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

                # Reconstructed particles
                # Returns the RecoParticles associated with the ALP decay products
                #.Define("RecoALPParticles",  "ReconstructedParticle2MC::selRP_matched_to_list( GenALP_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                # Reconstructing the tracks from the ALP
                #.Define("RecoALPTracks",   "ReconstructedParticle2Track::getRP2TRK( RecoALPParticles, EFlowTrack_1)")

                # Number of tracks in this RecoALPTracks collection ( = the #tracks used to reconstruct the ALP reco decay vertex)
                #.Define("n_RecoALPTracks", "ReconstructedParticle2Track::getTK_n( RecoALPTracks )")

                # Now we reconstruct the ALP reco decay vertex using the reco'ed tracks
                # First the full object, of type Vertexing::FCCAnalysesVertex
                #.Define("RecoALPDecayVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, RecoALPTracks)" )

                # from which we extract the edm4hep::VertexData object, which contains the vertex position in mm
                #.Define("RecoALPDecayVertex",  "VertexingUtils::get_VertexData( RecoALPDecayVertexObject )")
                
                # We may want to look at the reco'ed ALPs legs: in the RecoALPParticles vector,
                # the first particle (vector[0]) is the e-, etc :
                #.Define("RecoALPElectron",   "selRP_leg(0)( RecoALPParticles )")
                #.Define("RecoALPPositron",   "selRP_leg(1)( RecoALPParticles )")
                
                # reconstruced electron, positron values
                #.Define("RecoALPElectron_e",  "ReconstructedParticle::get_e( RecoALPElectron )")
                #.Define("RecoALPPositron_e",  "ReconstructedParticle::get_e( RecoALPPositron )")
                #.Define("RecoALPElectron_p",  "ReconstructedParticle::get_p( RecoALPElectron )")
                #.Define("RecoALPPositron_p",  "ReconstructedParticle::get_p( RecoALPPositron )")
                #.Define("RecoALPElectron_pt",  "ReconstructedParticle::get_pt( RecoALPElectron )")
                #.Define("RecoALPPositron_pt",  "ReconstructedParticle::get_pt( RecoALPPositron )")
                #.Define("RecoALPElectron_px",  "ReconstructedParticle::get_px( RecoALPElectron )")
                #.Define("RecoALPPositron_px",  "ReconstructedParticle::get_px( RecoALPPositron )")
                #.Define("RecoALPElectron_py",  "ReconstructedParticle::get_py( RecoALPElectron )")
                #.Define("RecoALPPositron_py",  "ReconstructedParticle::get_py( RecoALPPositron )")
                #.Define("RecoALPElectron_pz",  "ReconstructedParticle::get_pz( RecoALPElectron )")
                #.Define("RecoALPPositron_pz",  "ReconstructedParticle::get_pz( RecoALPPositron )")
                #.Define("RecoALPElectron_eta",  "ReconstructedParticle::get_eta( RecoALPElectron )")
                #.Define("RecoALPPositron_eta",  "ReconstructedParticle::get_eta( RecoALPPositron )")
                #.Define("RecoALPElectron_theta",  "ReconstructedParticle::get_theta( RecoALPElectron )")
                #.Define("RecoALPPositron_theta",  "ReconstructedParticle::get_theta( RecoALPPositron )")
                #.Define("RecoALPElectron_phi",  "ReconstructedParticle::get_phi( RecoALPElectron )")
                #.Define("RecoALPPositron_phi",  "ReconstructedParticle::get_phi( RecoALPPositron )")
                #.Define("RecoALPElectron_charge",  "ReconstructedParticle::get_charge( RecoALPElectron )")
                #.Define("RecoALPPositron_charge",  "ReconstructedParticle::get_charge( RecoALPPositron )")
                #add dxy, dz, dxyz, and uncertainties

                # ee invariant mass
                #.Define("RecoALP_ee_energy", "return (RecoALPElectron_e + RecoALPPositron_e)")
                #.Define("RecoALP_ee_px", "return (RecoALPElectron_px + RecoALPPositron_px)")
                #.Define("RecoALP_ee_py", "return (RecoALPElectron_py + RecoALPPositron_py)")
                #.Define("RecoALP_ee_pz", "return (RecoALPElectron_pz + RecoALPPositron_pz)")
                #.Define("RecoALP_ee_invMass", "return sqrt(RecoALP_ee_energy*RecoALP_ee_energy - RecoALP_ee_px*RecoALP_ee_px - RecoALP_ee_py*RecoALP_ee_py - RecoALP_ee_pz*RecoALP_ee_pz )")

                #gen-reco
                #.Define("GenMinusRecoALPElectron_e",   "GenALPElectron_e-RecoALPElectron_e")
                #.Define("GenMinusRecoALPPositron_e",   "GenALPPositron_e-RecoALPPositron_e")
                #.Define("GenMinusRecoALPElectron_p",   "GenALPElectron_p-RecoALPElectron_p")
                #.Define("GenMinusRecoALPPositron_p",   "GenALPPositron_p-RecoALPPositron_p")
                #.Define("GenMinusRecoALPElectron_pt",   "GenALPElectron_pt-RecoALPElectron_pt")
                #.Define("GenMinusRecoALPPositron_pt",   "GenALPPositron_pt-RecoALPPositron_pt")
                #.Define("GenMinusRecoALPElectron_px",   "GenALPElectron_px-RecoALPElectron_px")
                #.Define("GenMinusRecoALPPositron_px",   "GenALPPositron_px-RecoALPPositron_px")
                #.Define("GenMinusRecoALPElectron_py",   "GenALPElectron_py-RecoALPElectron_py")
                #.Define("GenMinusRecoALPPositron_py",   "GenALPPositron_py-RecoALPPositron_py")
                #.Define("GenMinusRecoALPElectron_pz",   "GenALPElectron_pz-RecoALPElectron_pz")
                #.Define("GenMinusRecoALPPositron_pz",   "GenALPPositron_pz-RecoALPPositron_pz")
                #.Define("GenMinusRecoALPElectron_eta",  "GenALPElectron_eta-RecoALPElectron_eta")
                #.Define("GenMinusRecoALPPositron_eta",  "GenALPPositron_eta-RecoALPPositron_eta")
                #.Define("GenMinusRecoALPElectron_theta",  "GenALPElectron_theta-RecoALPElectron_theta")
                #.Define("GenMinusRecoALPPositron_theta",  "GenALPPositron_theta-RecoALPPositron_theta")
                #.Define("GenMinusRecoALPElectron_phi",  "GenALPElectron_phi-RecoALPElectron_phi")
                #.Define("GenMinusRecoALPPositron_phi",  "GenALPPositron_phi-RecoALPPositron_phi")

                #.Define("GenMinusRecoALP_DecayVertex_x",  "GenALPElectron_vertex_x-RecoALPDecayVertex.position.x")
                #.Define("GenMinusRecoALP_DecayVertex_y",  "GenALPElectron_vertex_y-RecoALPDecayVertex.position.y")
                #.Define("GenMinusRecoALP_DecayVertex_z",  "GenALPElectron_vertex_z-RecoALPDecayVertex.position.z")
                
                       
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

		#EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing transverse energy
		.Define("RecoMET", "ReconstructedParticle::get_pt(MissingET)") #absolute value of RecoMET
		.Define("RecoMET_x", "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMET
		.Define("RecoMET_y", "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMET
		.Define("RecoMET_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMET

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
                                "FSGenElectron_vertex_x",
                                "FSGenElectron_vertex_y",
                                "FSGenElectron_vertex_z",
                                #"FSGen_Lxy",
                                #"FSGen_lifetime",
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
                                #"FSGen_ee_invMass",
                                #"FSGen_eenu_invMass",
                                #"GenALP_vertex_x",
                                #"GenALP_vertex_y",
                                #"GenALP_vertex_z",
                                #"GenALP_ee_invMass",
                                #"GenALP_eenu_invMass",
                                #"GenALP_mass",
                                #"GenALP_p",
                                #"GenALP_pt",
                                #"GenALP_pz",
                                #"GenALP_eta",
                                #"GenALP_theta",
                                #"GenALP_phi",
                                #"GenALP_genStatus",
                                #"GenALPElectron_mass",
                                #"GenALPElectron_e",
                                #"GenALPPositron_e",
                                #"GenALPNeutrino_e",
                                #"GenALPElectron_p",
                                #"GenALPPositron_p",
                                #"GenALPNeutrino_p",
                                #"GenALPElectron_pt",
                                #"GenALPPositron_pt",
                                #"GenALPNeutrino_pt",
                                #"GenALPElectron_px",
                                #"GenALPPositron_px",
                                #"GenALPNeutrino_px",
                                #"GenALPElectron_py",
                                #"GenALPPositron_py",
                                #"GenALPNeutrino_py",
                                #"GenALPElectron_pz",
                                #"GenALPPositron_pz",
                                #"GenALPNeutrino_pz",
                                #"GenALPElectron_eta",
                                #"GenALPPositron_eta",
                                #"GenALPNeutrino_eta",
                                #"GenALPElectron_theta",
                                #"GenALPPositron_theta",
                                #"GenALPNeutrino_theta",
                                #"GenALPElectron_phi",
                                #"GenALPPositron_phi",
                                #"GenALPNeutrino_phi",
                                #"GenALPElectron_genStatus",
                                #"GenALPPositron_genStatus",
                                #"GenALPNeutrino_genStatus",
                                #"GenALP_decay",
                                #"GenALPElectron_vertex_x",
                                #"GenALPElectron_vertex_y",
                                #"GenALPElectron_vertex_z",
                                #"GenALP_Lxy",
                                #"GenALP_lifetime",
                                #"GenALPMCDecayVertex",
                                "MC_PrimaryVertex",
                                "n_RecoTracks",
                                ######## Reconstructed particles #######
                                #"RecoALPParticles",
                                #"RecoALPTracks",
                                #"n_RecoALPTracks",
                                #"RecoALPDecayVertexObject",
                                #"RecoALPDecayVertex",
                                #"RecoALPElectron_e",
                                #"RecoALPPositron_e",
                                #"RecoALPElectron_p",
                                #"RecoALPPositron_p",
                                #"RecoALPElectron_pt",
                                #"RecoALPPositron_pt",
                                #"RecoALPElectron_px",
                                #"RecoALPPositron_px",
                                #"RecoALPElectron_py",
                                #"RecoALPPositron_py",
                                #"RecoALPElectron_pz",
                                #"RecoALPPositron_pz",
                                #"RecoALPElectron_eta",
                                #"RecoALPPositron_eta",
                                #"RecoALPElectron_theta",
                                #"RecoALPPositron_theta",
                                #"RecoALPElectron_phi",
                                #"RecoALPPositron_phi",
                                #"RecoALPElectron_charge",
                                #"RecoALPPositron_charge",
                                #"RecoALP_ee_invMass",
                                #"GenMinusRecoALPElectron_e",
                                #"GenMinusRecoALPPositron_e",
                                #"GenMinusRecoALPElectron_p",
                                #"GenMinusRecoALPPositron_p",
                                #"GenMinusRecoALPElectron_pt",
                                #"GenMinusRecoALPPositron_pt",
                                #"GenMinusRecoALPElectron_px",
                                #"GenMinusRecoALPPositron_px",
                                #"GenMinusRecoALPElectron_py",
                                #"GenMinusRecoALPPositron_py",
                                #"GenMinusRecoALPElectron_pz",
                                #"GenMinusRecoALPPositron_pz",
                                #"GenMinusRecoALPElectron_eta",
                                #"GenMinusRecoALPPositron_eta",
                                #"GenMinusRecoALPElectron_theta",
                                #"GenMinusRecoALPPositron_theta",
                                #"GenMinusRecoALPElectron_phi",
                                #"GenMinusRecoALPPositron_phi",
                                #"GenMinusRecoALP_DecayVertex_x",
                                #"GenMinusRecoALP_DecayVertex_y",
                                #"GenMinusRecoALP_DecayVertex_z",
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
				"RecoMET",
				"RecoMET_x",
				"RecoMET_y",
				"RecoMET_phi",

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



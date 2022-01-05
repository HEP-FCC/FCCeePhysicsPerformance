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

#right now, only set up for HNL decays to e e nu
#to do: add ejj channel - will need to define a new function called MCParticle::get_indices_InclusiveDecay in MCParticle.cc within FCCAnalyses
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
                .Define("GenHNL_decay", "MCParticle::list_of_particles_from_decay(0, GenHNL_PID, Particle1)")

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
                .Define("AllGenHNL_genStatus", "MCParticle::get_genStatus(GenHNL_PID)")

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

                # Finding the Lxy of the HNL
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )
                .Define("FSGen_Lxy", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y)")

                # Finding the Lxyz of the HNL
                .Define("FSGen_Lxyz", "return sqrt(FSGenElectron_vertex_x*FSGenElectron_vertex_x + FSGenElectron_vertex_y*FSGenElectron_vertex_y + FSGenElectron_vertex_z*FSGenElectron_vertex_z)")

                # Calculating the lifetime of the HNL
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                .Define("FSGen_lifetime", "return ( FSGen_Lxy.at(0) * AllGenHNL_mass / (AllGenHNL_pt * 3E8 * 1000))" )

                # Calculating the lifetime of the HNL for Lxyz
                .Define("FSGen_lifetimeLxyz", "return ( FSGen_Lxyz.at(0) * AllGenHNL_mass / (AllGenHNL_p * 3E8 * 1000))" )

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
                .Define("FSGen_ee_energy", "return (FSGenElectron_e.at(0) + FSGenPositron_e.at(0))")
                .Define("FSGen_ee_px", "return (FSGenElectron_px.at(0) + FSGenPositron_px.at(0))")
                .Define("FSGen_ee_py", "return (FSGenElectron_py.at(0) + FSGenPositron_py.at(0))")
                .Define("FSGen_ee_pz", "return (FSGenElectron_pz.at(0) + FSGenPositron_pz.at(0))")
                .Define("FSGen_ee_invMass", "return sqrt(FSGen_ee_energy*FSGen_ee_energy - FSGen_ee_px*FSGen_ee_px - FSGen_ee_py*FSGen_ee_py - FSGen_ee_pz*FSGen_ee_pz )")

                # eenu invariant mass
                .Define("FSGen_eenu_energy", "return (FSGenElectron_e.at(0) + FSGenPositron_e.at(0) + FSGenNeutrino_e.at(0))")
                .Define("FSGen_eenu_px", "return (FSGenElectron_px.at(0) + FSGenPositron_px.at(0) + FSGenNeutrino_px.at(0))")
                .Define("FSGen_eenu_py", "return (FSGenElectron_py.at(0) + FSGenPositron_py.at(0) + FSGenNeutrino_py.at(0))")
                .Define("FSGen_eenu_pz", "return (FSGenElectron_pz.at(0) + FSGenPositron_pz.at(0) + FSGenNeutrino_pz.at(0))")
                .Define("FSGen_eenu_invMass", "return sqrt(FSGen_eenu_energy*FSGen_eenu_energy - FSGen_eenu_px*FSGen_eenu_px - FSGen_eenu_py*FSGen_eenu_py - FSGen_eenu_pz*FSGen_eenu_pz )")

                # Defining a vector containing the HNL and its daughters in order written
                # Name of vector is HNL_indices 
                .Define("GenHNL_indices", "MCParticle::get_indices_InclusiveDecay(9900012, {11, -11, 12}, true, false)(Particle, Particle1)")
                #.Define("GenHNL_indices", "MCParticle::get_indices_ExclusiveDecay(9900012, {11, -11, 12}, true, false)(Particle, Particle1)")
                #.Define("GenHNL_indices", "MCParticle::get_indices_ExclusiveDecay(9900012, {11, -11, 12, 22, 22, 22, 22, 22, 22, 22}, true, false)(Particle, Particle1)")
                
                # Defining the individual particles from the vector
                .Define("GenHNL", "selMC_leg(0)(GenHNL_indices, Particle)")
                .Define("GenHNLElectron", "selMC_leg(1)(GenHNL_indices, Particle)")
                .Define("GenHNLPositron", "selMC_leg(2)(GenHNL_indices, Particle)")
                .Define("GenHNLNeutrino", "selMC_leg(3)(GenHNL_indices, Particle)")

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
                .Define("GenHNL_genStatus", "MCParticle::get_genStatus( GenHNL )")

                # Finding the kinematics of each of these daughters
                .Define("GenHNLElectron_mass", "MCParticle::get_mass( GenHNLElectron )")
                .Define("GenHNLElectron_e", "MCParticle::get_e( GenHNLElectron )")
                .Define("GenHNLPositron_e", "MCParticle::get_e( GenHNLPositron )")
                .Define("GenHNLNeutrino_e", "MCParticle::get_e( GenHNLNeutrino )")
                .Define("GenHNLElectron_p", "MCParticle::get_p( GenHNLElectron )")
                .Define("GenHNLPositron_p", "MCParticle::get_p( GenHNLPositron )")
                .Define("GenHNLNeutrino_p", "MCParticle::get_p( GenHNLNeutrino )")
                .Define("GenHNLElectron_pt", "MCParticle::get_pt( GenHNLElectron )")
                .Define("GenHNLPositron_pt", "MCParticle::get_pt( GenHNLPositron )")
                .Define("GenHNLNeutrino_pt", "MCParticle::get_pt( GenHNLNeutrino )")
                .Define("GenHNLElectron_px", "MCParticle::get_px( GenHNLElectron )")
                .Define("GenHNLPositron_px", "MCParticle::get_px( GenHNLPositron )")
                .Define("GenHNLNeutrino_px", "MCParticle::get_px( GenHNLNeutrino )")
                .Define("GenHNLElectron_py", "MCParticle::get_py( GenHNLElectron )")
                .Define("GenHNLPositron_py", "MCParticle::get_py( GenHNLPositron )")
                .Define("GenHNLNeutrino_py", "MCParticle::get_py( GenHNLNeutrino )")
                .Define("GenHNLElectron_pz", "MCParticle::get_pz( GenHNLElectron )")
                .Define("GenHNLPositron_pz", "MCParticle::get_pz( GenHNLPositron )")
                .Define("GenHNLNeutrino_pz", "MCParticle::get_pz( GenHNLNeutrino )")
                .Define("GenHNLElectron_eta", "MCParticle::get_eta( GenHNLElectron )")
                .Define("GenHNLPositron_eta", "MCParticle::get_eta( GenHNLPositron )")
                .Define("GenHNLNeutrino_eta", "MCParticle::get_eta( GenHNLNeutrino )")
                .Define("GenHNLElectron_theta", "MCParticle::get_theta( GenHNLElectron )")
                .Define("GenHNLPositron_theta", "MCParticle::get_theta( GenHNLPositron )")
                .Define("GenHNLNeutrino_theta", "MCParticle::get_theta( GenHNLNeutrino )")
                .Define("GenHNLElectron_phi", "MCParticle::get_phi( GenHNLElectron )")
                .Define("GenHNLPositron_phi", "MCParticle::get_phi( GenHNLPositron )")
                .Define("GenHNLNeutrino_phi", "MCParticle::get_phi( GenHNLNeutrino )")
                .Define("GenHNLElectron_genStatus", "MCParticle::get_genStatus( GenHNLElectron )")
                .Define("GenHNLPositron_genStatus", "MCParticle::get_genStatus( GenHNLPositron )")
                .Define("GenHNLNeutrino_genStatus", "MCParticle::get_genStatus( GenHNLNeutrino )")

                # Finding the production vertex of the daughters (checking GenHNLElectron here)
                .Define("GenHNLElectron_vertex_x", "MCParticle::get_vertex_x( GenHNLElectron )")
                .Define("GenHNLElectron_vertex_y", "MCParticle::get_vertex_y( GenHNLElectron )")
                .Define("GenHNLElectron_vertex_z", "MCParticle::get_vertex_z( GenHNLElectron )")

                # Finding the Lxy of the HNL
                # Definition: Lxy = math.sqrt( (branchGenPtcl.At(daut1).X)**2 + (branchGenPtcl.At(daut1).Y)**2 )  
                .Define("GenHNL_Lxy", "return sqrt(GenHNLElectron_vertex_x*GenHNLElectron_vertex_x + GenHNLElectron_vertex_y*GenHNLElectron_vertex_y)")

                # Finding the Lxyz of the HNL
                .Define("GenHNL_Lxyz", "return sqrt(GenHNLElectron_vertex_x*GenHNLElectron_vertex_x + GenHNLElectron_vertex_y*GenHNLElectron_vertex_y + GenHNLElectron_vertex_z*GenHNLElectron_vertex_z)")
                
                # Calculating the lifetime of the HNL
                # Definition: t = Lxy * branchGenPtcl.At(i).Mass / (branchGenPtcl.At(i).PT * 1000 * 3E8)
                .Define("GenHNL_lifetime", "return ( GenHNL_Lxy * GenHNL_mass / (GenHNL_pt * 3E8 * 1000))" )

                #Calculationg the lifetime of the HNL for Lxyz
                .Define("GenHNL_lifetimeLxyz", "return ( GenHNL_Lxyz * GenHNL_mass / (GenHNL_p * 3E8 * 1000))" )
               
                # Finding the production vertex of the HNL which should be at (0,0,0) 
                .Define("GenHNL_vertex_x", "MCParticle::get_vertex_x(GenHNL_PID)")
                .Define("GenHNL_vertex_y", "MCParticle::get_vertex_y(GenHNL_PID)")
                .Define("GenHNL_vertex_z", "MCParticle::get_vertex_z(GenHNL_PID)")

                # ee invariant mass
                .Define("GenHNL_ee_energy", "return (GenHNLElectron_e + GenHNLPositron_e)")
                .Define("GenHNL_ee_px", "return (GenHNLElectron_px + GenHNLPositron_px)")
                .Define("GenHNL_ee_py", "return (GenHNLElectron_py + GenHNLPositron_py)")
                .Define("GenHNL_ee_pz", "return (GenHNLElectron_pz + GenHNLPositron_pz)")
                .Define("GenHNL_ee_invMass", "return sqrt(GenHNL_ee_energy*GenHNL_ee_energy - GenHNL_ee_px*GenHNL_ee_px - GenHNL_ee_py*GenHNL_ee_py - GenHNL_ee_pz*GenHNL_ee_pz )")

                # eenu invariant mass
                .Define("GenHNL_eenu_energy", "return (GenHNLElectron_e + GenHNLPositron_e + GenHNLNeutrino_e)")
                .Define("GenHNL_eenu_px", "return (GenHNLElectron_px + GenHNLPositron_px + GenHNLNeutrino_px)")
                .Define("GenHNL_eenu_py", "return (GenHNLElectron_py + GenHNLPositron_py + GenHNLNeutrino_py)")
                .Define("GenHNL_eenu_pz", "return (GenHNLElectron_pz + GenHNLPositron_pz + GenHNLNeutrino_pz)")
                .Define("GenHNL_eenu_invMass", "return sqrt(GenHNL_eenu_energy*GenHNL_eenu_energy - GenHNL_eenu_px*GenHNL_eenu_px - GenHNL_eenu_py*GenHNL_eenu_py - GenHNL_eenu_pz*GenHNL_eenu_pz )")

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

                # Now we reconstruct the HNL reco decay vertex using the reco'ed tracks
                # First the full object, of type Vertexing::FCCAnalysesVertex
                .Define("RecoHNLDecayVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, RecoHNLTracks)" )

                # from which we extract the edm4hep::VertexData object, which contains the vertex position in mm
                .Define("RecoHNLDecayVertex",  "VertexingUtils::get_VertexData( RecoHNLDecayVertexObject )")
                
                # We may want to look at the reco'ed HNLs legs: in the RecoHNLParticles vector,
                # the first particle (vector[0]) is the e-, etc :
                .Define("RecoHNLElectron",   "selRP_leg(0)( RecoHNLParticles )")
                .Define("RecoHNLPositron",   "selRP_leg(1)( RecoHNLParticles )")
                
                # reconstruced electron, positron values
                .Define("RecoHNLElectron_e",  "ReconstructedParticle::get_e( RecoHNLElectron )")
                .Define("RecoHNLPositron_e",  "ReconstructedParticle::get_e( RecoHNLPositron )")
                .Define("RecoHNLElectron_p",  "ReconstructedParticle::get_p( RecoHNLElectron )")
                .Define("RecoHNLPositron_p",  "ReconstructedParticle::get_p( RecoHNLPositron )")
                .Define("RecoHNLElectron_pt",  "ReconstructedParticle::get_pt( RecoHNLElectron )")
                .Define("RecoHNLPositron_pt",  "ReconstructedParticle::get_pt( RecoHNLPositron )")
                .Define("RecoHNLElectron_px",  "ReconstructedParticle::get_px( RecoHNLElectron )")
                .Define("RecoHNLPositron_px",  "ReconstructedParticle::get_px( RecoHNLPositron )")
                .Define("RecoHNLElectron_py",  "ReconstructedParticle::get_py( RecoHNLElectron )")
                .Define("RecoHNLPositron_py",  "ReconstructedParticle::get_py( RecoHNLPositron )")
                .Define("RecoHNLElectron_pz",  "ReconstructedParticle::get_pz( RecoHNLElectron )")
                .Define("RecoHNLPositron_pz",  "ReconstructedParticle::get_pz( RecoHNLPositron )")
                .Define("RecoHNLElectron_eta",  "ReconstructedParticle::get_eta( RecoHNLElectron )")
                .Define("RecoHNLPositron_eta",  "ReconstructedParticle::get_eta( RecoHNLPositron )")
                .Define("RecoHNLElectron_theta",  "ReconstructedParticle::get_theta( RecoHNLElectron )")
                .Define("RecoHNLPositron_theta",  "ReconstructedParticle::get_theta( RecoHNLPositron )")
                .Define("RecoHNLElectron_phi",  "ReconstructedParticle::get_phi( RecoHNLElectron )")
                .Define("RecoHNLPositron_phi",  "ReconstructedParticle::get_phi( RecoHNLPositron )")
                .Define("RecoHNLElectron_charge",  "ReconstructedParticle::get_charge( RecoHNLElectron )")
                .Define("RecoHNLPositron_charge",  "ReconstructedParticle::get_charge( RecoHNLPositron )")
                #add dxy, dz, dxyz, and uncertainties

                # ee invariant mass
                .Define("RecoHNL_ee_energy", "return (RecoHNLElectron_e + RecoHNLPositron_e)")
                .Define("RecoHNL_ee_px", "return (RecoHNLElectron_px + RecoHNLPositron_px)")
                .Define("RecoHNL_ee_py", "return (RecoHNLElectron_py + RecoHNLPositron_py)")
                .Define("RecoHNL_ee_pz", "return (RecoHNLElectron_pz + RecoHNLPositron_pz)")
                .Define("RecoHNL_ee_invMass", "return sqrt(RecoHNL_ee_energy*RecoHNL_ee_energy - RecoHNL_ee_px*RecoHNL_ee_px - RecoHNL_ee_py*RecoHNL_ee_py - RecoHNL_ee_pz*RecoHNL_ee_pz )")

                #gen-reco
                .Define("GenMinusRecoHNLElectron_e",   "GenHNLElectron_e-RecoHNLElectron_e")
                .Define("GenMinusRecoHNLPositron_e",   "GenHNLPositron_e-RecoHNLPositron_e")
                .Define("GenMinusRecoHNLElectron_p",   "GenHNLElectron_p-RecoHNLElectron_p")
                .Define("GenMinusRecoHNLPositron_p",   "GenHNLPositron_p-RecoHNLPositron_p")
                .Define("GenMinusRecoHNLElectron_pt",   "GenHNLElectron_pt-RecoHNLElectron_pt")
                .Define("GenMinusRecoHNLPositron_pt",   "GenHNLPositron_pt-RecoHNLPositron_pt")
                .Define("GenMinusRecoHNLElectron_px",   "GenHNLElectron_px-RecoHNLElectron_px")
                .Define("GenMinusRecoHNLPositron_px",   "GenHNLPositron_px-RecoHNLPositron_px")
                .Define("GenMinusRecoHNLElectron_py",   "GenHNLElectron_py-RecoHNLElectron_py")
                .Define("GenMinusRecoHNLPositron_py",   "GenHNLPositron_py-RecoHNLPositron_py")
                .Define("GenMinusRecoHNLElectron_pz",   "GenHNLElectron_pz-RecoHNLElectron_pz")
                .Define("GenMinusRecoHNLPositron_pz",   "GenHNLPositron_pz-RecoHNLPositron_pz")
                .Define("GenMinusRecoHNLElectron_eta",  "GenHNLElectron_eta-RecoHNLElectron_eta")
                .Define("GenMinusRecoHNLPositron_eta",  "GenHNLPositron_eta-RecoHNLPositron_eta")
                .Define("GenMinusRecoHNLElectron_theta",  "GenHNLElectron_theta-RecoHNLElectron_theta")
                .Define("GenMinusRecoHNLPositron_theta",  "GenHNLPositron_theta-RecoHNLPositron_theta")
                .Define("GenMinusRecoHNLElectron_phi",  "GenHNLElectron_phi-RecoHNLElectron_phi")
                .Define("GenMinusRecoHNLPositron_phi",  "GenHNLPositron_phi-RecoHNLPositron_phi")

                .Define("GenMinusRecoHNL_DecayVertex_x",  "GenHNLElectron_vertex_x-RecoHNLDecayVertex.position.x")
                .Define("GenMinusRecoHNL_DecayVertex_y",  "GenHNLElectron_vertex_y-RecoHNLDecayVertex.position.y")
                .Define("GenMinusRecoHNL_DecayVertex_z",  "GenHNLElectron_vertex_z-RecoHNLDecayVertex.position.z")
                
                       
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
                                "FSGen_lifetime",
                                "FSGen_lifetimeLxyz",
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
                                "FSGen_ee_invMass",
                                "FSGen_eenu_invMass",
                                "GenHNL_vertex_x",
                                "GenHNL_vertex_y",
                                "GenHNL_vertex_z",
                                "GenHNL_ee_invMass",
                                "GenHNL_eenu_invMass",
                                "GenHNL_mass",
                                "GenHNL_p",
                                "GenHNL_pt",
                                "GenHNL_pz",
                                "GenHNL_eta",
                                "GenHNL_theta",
                                "GenHNL_phi",
                                "GenHNL_genStatus",
                                "GenHNLElectron_mass",
                                "GenHNLElectron_e",
                                "GenHNLPositron_e",
                                "GenHNLNeutrino_e",
                                "GenHNLElectron_p",
                                "GenHNLPositron_p",
                                "GenHNLNeutrino_p",
                                "GenHNLElectron_pt",
                                "GenHNLPositron_pt",
                                "GenHNLNeutrino_pt",
                                "GenHNLElectron_px",
                                "GenHNLPositron_px",
                                "GenHNLNeutrino_px",
                                "GenHNLElectron_py",
                                "GenHNLPositron_py",
                                "GenHNLNeutrino_py",
                                "GenHNLElectron_pz",
                                "GenHNLPositron_pz",
                                "GenHNLNeutrino_pz",
                                "GenHNLElectron_eta",
                                "GenHNLPositron_eta",
                                "GenHNLNeutrino_eta",
                                "GenHNLElectron_theta",
                                "GenHNLPositron_theta",
                                "GenHNLNeutrino_theta",
                                "GenHNLElectron_phi",
                                "GenHNLPositron_phi",
                                "GenHNLNeutrino_phi",
                                "GenHNLElectron_genStatus",
                                "GenHNLPositron_genStatus",
                                "GenHNLNeutrino_genStatus",
                                "GenHNL_decay",
                                "GenHNLElectron_vertex_x",
                                "GenHNLElectron_vertex_y",
                                "GenHNLElectron_vertex_z",
                                "GenHNL_Lxy",
                                "GenHNL_Lxyz",
                                "GenHNL_lifetime",
                                "GenHNL_lifetimeLxyz",
                                "GenHNLMCDecayVertex",
                                "MC_PrimaryVertex",
                                "n_RecoTracks",
                                ######## Reconstructed particles #######
                                "RecoHNLParticles",
                                "RecoHNLTracks",
                                "n_RecoHNLTracks",
                                "RecoHNLDecayVertexObject",
                                "RecoHNLDecayVertex",
                                "RecoHNLElectron_e",
                                "RecoHNLPositron_e",
                                "RecoHNLElectron_p",
                                "RecoHNLPositron_p",
                                "RecoHNLElectron_pt",
                                "RecoHNLPositron_pt",
                                "RecoHNLElectron_px",
                                "RecoHNLPositron_px",
                                "RecoHNLElectron_py",
                                "RecoHNLPositron_py",
                                "RecoHNLElectron_pz",
                                "RecoHNLPositron_pz",
                                "RecoHNLElectron_eta",
                                "RecoHNLPositron_eta",
                                "RecoHNLElectron_theta",
                                "RecoHNLPositron_theta",
                                "RecoHNLElectron_phi",
                                "RecoHNLPositron_phi",
                                "RecoHNLElectron_charge",
                                "RecoHNLPositron_charge",
                                "RecoHNL_ee_invMass",
                                "GenMinusRecoHNLElectron_e",
                                "GenMinusRecoHNLPositron_e",
                                "GenMinusRecoHNLElectron_p",
                                "GenMinusRecoHNLPositron_p",
                                "GenMinusRecoHNLElectron_pt",
                                "GenMinusRecoHNLPositron_pt",
                                "GenMinusRecoHNLElectron_px",
                                "GenMinusRecoHNLPositron_px",
                                "GenMinusRecoHNLElectron_py",
                                "GenMinusRecoHNLPositron_py",
                                "GenMinusRecoHNLElectron_pz",
                                "GenMinusRecoHNLPositron_pz",
                                "GenMinusRecoHNLElectron_eta",
                                "GenMinusRecoHNLPositron_eta",
                                "GenMinusRecoHNLElectron_theta",
                                "GenMinusRecoHNLPositron_theta",
                                "GenMinusRecoHNLElectron_phi",
                                "GenMinusRecoHNLPositron_phi",
                                "GenMinusRecoHNL_DecayVertex_x",
                                "GenMinusRecoHNL_DecayVertex_y",
                                "GenMinusRecoHNL_DecayVertex_z",
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



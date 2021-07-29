import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gSystem.Load("libFCCAnalysesFlavour")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_bs  = ROOT.dummyLoaderFlavour

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

# Require that there be a Bd (PDG = 511 ) in the event
Filter="MCParticle::filter_pdgID(511, true)(Particle)==true"


#
#	This is used to process a file in which the Bd was forced to decay into K* tau tau,
#       with both taus -> 3 charged pions and K* -> K Pi.
#       We reconstruct the tertiary vertex from tau -> 3 pions, and the Bd decay vertex
#       would only the K and Pi tracks be used in the vertex fit.
#       The example also shows how to retrieve the MC and reco'ed Bd leg,
#       as well as the MC vertices for the Bd decay and the tau decay.
#
#       Example file: 
#       /eos/experiment/fcc/users/e/eperez/vertexing/Bd2KstTauTau_Taus2ThreeChargedPions_evtgen.root
#
#   	To run :
#       python analysis_Bd2Ksttautau.py /eos/experiment/fcc/users/e/eperez/vertexing/Bd2KstTauTau_Taus2ThreeChargedPions_evtgen.root
#	This will create a file (ntuple) Bd2KstTauTau_Taus2ThreeChargedPions_evtgen.root in the local directory.
#       The macro plots_Bd2Ksttautau.x makes plots from this ntuple.   
#

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        #ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        #df2 = (self.df.Range(1000)	# to test over 1000 events only
        df2 = (self.df

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               # Require a Bd in the event:
               .Filter( Filter )


               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks in the event
               .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")


               # MC indices of the decay Bd -> K* tau tau
               # Returns a vector with the indices of : mother Bd, K*, tau-, tau+
               # vector[0] = the mother, and then the daughters in the order specified
               # The first boolean below: when set to true, the dsughters specified in the list are looked
               # for among the final, *stable* particles that come out from the mother, i.e. the decay tree is
               # explored recursively if needed. So, here, we set it to false.
               # The second boolean: when set to true, a decay of the charged conjugate mother, into the
               # *same* final state, is looked for too (i.e. useless for Bd -> { 313, 15, -15} . The use
               # of this second bool may be extended to account for the full charge conjugation, but this
               # requires some care.
               #
               # If the event contains more than one such decays, only the first one is kept.
               # get_indices_ExclusiveDecay looks for an exclusive decay: if a mother is found, that decays 
               # into the particles specified in the list plus other particle(s), this decay is not selected.
               .Define("Bd2KstTauTau_indices",   "MCParticle::get_indices_ExclusiveDecay(  511, { 313, 15, -15}, false, false) ( Particle, Particle1)" )

               # the MC Bd : the Bd is the first particle in the Bd2KstTauTau_indices  vector
               # for practical reasons (because methods in MCParticle consume a vector of MCParticles),
               # selMC_leg returns a vector, whose size is one or zero.
               .Define("Bd",  "selMC_leg(0) ( Bd2KstTauTau_indices , Particle )")

               # by construction, the number of Bd that decay to { 313, 15, -15} is zero or one. It can be zero, despite the filter,
               # when the Bd has oscillated into a Bdbar.  The variable below will be used to select the
               # events of interest (for which FoundBd = 1) :
               .Define("FoundBd",  "MCParticle::get_n( Bd )" )

               # the MC Kstar
               .Define("Kstar",  "selMC_leg(1) ( Bd2KstTauTau_indices , Particle )")
               # the MC taus :
               .Define("taum",  "selMC_leg(2) ( Bd2KstTauTau_indices , Particle )")
               .Define("taup",  "selMC_leg(3) ( Bd2KstTauTau_indices , Particle )")

               .Define("Bd_theta", "MCParticle::get_theta( Bd )")
               .Define("Kstar_theta", "MCParticle::get_theta( Kstar )")
               .Define("taum_theta", "MCParticle::get_theta( taum )")
               .Define("taup_theta", "MCParticle::get_theta( taup )")



               # -------------------------------------------------------------------------------------------------------
               #
               # ----------   the Kstar -> K Pi decay 
               

               # the daughters from the K*:
               # Retrieve first the index of the Kstar in the MC Particle collection. By construction, it is the second
               # element of the vector Bd2KstTauTau_indices :
               .Define("KstarIndex",  " if ( Bd2KstTauTau_indices.size() > 0) return Bd2KstTauTau_indices.at(1); else return -1;")
               # from this index, one gets a vector with the indices of: mother K*, K, Pi, in this order:
               .Define("Kst2KPi_indices",    "MCParticle::get_indices_ExclusiveDecay_MotherByIndex( KstarIndex, { 321, -211 }, true, Particle, Particle1)" )
               # This is the MC Kaon from the Kstar decay :
               .Define("K_from_Kstar", "selMC_leg(1) ( Kst2KPi_indices, Particle)")
               # and the MC pion :
               .Define("Pi_from_Kstar",  "selMC_leg(2) ( Kst2KPi_indices, Particle)")


               # RecoParticles associated with the K+ and Pi- from the Kstar
               # the size of this collection is always 2 provided that Kst2KPi_indices  is not empty.
               # In case one of the Kstar legs did not make a RecoParticle, a "dummy" particle is inserted in the liat.
               # This is done on purpose, to maintain the mapping with the indices.
               .Define("KstRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Kst2KPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("KstTracks",  "ReconstructedParticle2Track::getRP2TRK( KstRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Ds vertex
               .Define("n_KstTracks", "ReconstructedParticle2Track::getTK_n( KstTracks )")

               # Reco'ed vertex of the Kstar  ( = reco'ed decay vertex of the Bd from the K+ and Pi- tracks only)
               .Define("KstVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 2, KstTracks)" )
               .Define("KstVertex",  "VertexingUtils::get_VertexData( KstVertexObject )")

               # MC production vertex of the Kstar ( = MC decay vertex of the Bd, = MC decay vertex of the Kstar)
               .Define("KstMCDecayVertex", " MCParticle::get_vertex( Kstar )")
               # alternatively, one could use this, which returns a Vector3d instead of a vector of Vector3d:
               # .Define("KstMCDecayVertex", " if ( Kstar.size() > 0) return Kstar[0].vertex; else return  edm4hep::Vector3d(1e12, 1e12, 1e12) ; ")

               # -------------------------------------------------------------------------------------------------------



               # -------------------------------------------------------------------------------------------------------
               #
               # ----------   the pions from the tau- decay

               # the daughters from the tau-
               .Define("TauMinusIndex",  " if ( Bd2KstTauTau_indices.size() > 0) return Bd2KstTauTau_indices[2];  else return -1;")
               .Define("Tau2Pions_indices",  " MCParticle::get_indices_ExclusiveDecay_MotherByIndex( TauMinusIndex,  {16, -211, 211, -211  }, true, Particle, Particle1)" )

               # RecoParticles associated with the pions from the tau decau
               .Define("TaumRecoParticles",   " ReconstructedParticle2MC::selRP_matched_to_list( Tau2Pions_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("TaumTracks",   "ReconstructedParticle2Track::getRP2TRK( TaumRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Taum vertex
               .Define("n_TaumTracks", "ReconstructedParticle2Track::getTK_n( TaumTracks )")

               # Reco'ed decay vertex of the Taum
               .Define("TaumVertexObject",  "VertexFitterSimple::VertexFitter_Tk( 3, TaumTracks)" )
               .Define("TaumVertex",  "VertexingUtils::get_VertexData( TaumVertexObject ) ")

               # MC decay vertex of the Taum:
               # first, get one of the pions from the tau decay ( 0 = the mother tau, 1 = the nu, 2 = a pion)
               .Define("PiFromTaum",  "selMC_leg(2) ( Tau2Pions_indices , Particle )")
               # MC production vertex of this pion:
               .Define("TaumMCDecayVertex",  " MCParticle::get_vertex( PiFromTaum )")


               # -------------------------------------------------------------------------------------------------------


        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_PrimaryVertex",
                "ntracks",
                #"Bd2KstTauTau_indices",
                "FoundBd",
                "Bd_theta",
                "Kstar_theta",
                "taum_theta",
                "taup_theta",
                #"K_from_Kstar",
                #"Pi_from_Kstar",
                "KstMCDecayVertex",
                "n_KstTracks",
                "KstVertex",
                "TaumMCDecayVertex",
                "n_TaumTracks",
                "TaumVertex"

                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)



if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    #outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    outDir = './'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()

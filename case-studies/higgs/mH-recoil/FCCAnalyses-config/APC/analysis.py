import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gSystem.Load("libFCCAnalysesHiggs")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_higgs  = ROOT.dummyLoaderHiggs
print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)
print ('higgs   ',_higgs)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = (self.df
               # define an alias for muon index collection
               .Alias("Muon0", "Muon#0.index")
               # define the muon collection
               .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               # define missing momentum
               .Define('missingET_px', 'MissingET.momentum.x')
               .Define('missingET_py', 'MissingET.momentum.y')
               .Define('missingET_pz', 'MissingET.momentum.z')
               .Define('missingET_e', 'MissingET.energy')
               # get cosTheta miss
               .Define('missingET_costheta', 'APCHiggsTools::get_cosTheta_miss(missingET_px,missingET_py,missingET_pz,missingET_e)')
               #select muons on pT
               #.Define("selected_muons", "ReconstructedParticle::sel_pt(10.)(muons)")
							 #muon quality check at least one muon plus and one muon minus
               .Define("selected_muons", "APCHiggsTools::muon_quality_check(muons)")
							 #select muons +
							 .Define("selected_muons_plus", "ReconstructedParticle::sel_charge(1.0,false)(selected_muons)")
							 #select muons -
							 .Define("selected_muons_minus", "ReconstructedParticle::sel_charge(-1.0,false)(selected_muons)")
							 #muons + numbers
							 .Define("selected_muons_plus_n", "ReconstructedParticle::get_n(selected_muons_plus)")
							 #muons - numbers
							 .Define("selected_muons_minus_n", "ReconstructedParticle::get_n(selected_muons_minus)")
							 #muons numbers
							 .Define("selected_muons_n", "ReconstructedParticle::get_n(selected_muons)")
							 # create branch with muon transverse momentum
               .Define("selected_muons_pt", "ReconstructedParticle::get_pt(selected_muons)") 
               # create branch with muon rapidity
               .Define("selected_muons_y",  "ReconstructedParticle::get_y(selected_muons)") 
               # create branch with muon total momentum
               .Define("selected_muons_p",     "ReconstructedParticle::get_p(selected_muons)")
               # create branch with muon energy 
               .Define("selected_muons_e",     "ReconstructedParticle::get_e(selected_muons)")
               # create branch with muon mass
               .Define("selected_muons_m",     "ReconstructedParticle::get_mass(selected_muons)")
               # create branch with muon costheta
               .Define("selected_muons_costheta",  "APCHiggsTools::get_cosTheta(selected_muons)")
               # find zed candidates from  di-muon resonances  
               .Define("zed_leptonic",         "APCHiggsTools::resonanceZBuilder(91)(selected_muons)")      
               # write branch with zed mass
               .Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
							 # write branch with zed number
							 .Define("zed_leptonic_n",       "ReconstructedParticle::get_n(zed_leptonic)")
							 # write branch with zed charge
							 .Define("zed_leptonic_charge",   "ReconstructedParticle::get_charge(zed_leptonic)")
               # write branch with zed transverse momenta
               .Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
               # write branch with zed rapidity
               .Define("zed_leptonic_y",      "ReconstructedParticle::get_y(zed_leptonic)")
               # write branch with zed total momentum
               .Define("zed_leptonic_p",      "ReconstructedParticle::get_p(zed_leptonic)")
               # write branch with zed energy
               .Define("zed_leptonic_e",      "ReconstructedParticle::get_e(zed_leptonic)")
               # write branch with zed costheta
               .Define("zed_leptonic_costheta",  "APCHiggsTools::get_cosTheta(zed_leptonic)")
               # calculate recoil of zed_leptonic
               .Define("zed_leptonic_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
                # write branch with recoil mass
               .Define("zed_leptonic_recoil_m","ReconstructedParticle::get_mass(zed_leptonic_recoil)") 

                # Recoil mass with the MC muons kinematics
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
                .Define("zed_leptonic_MC",   "APCHiggsTools::resonanceZBuilder2(91, true)(selected_muons, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
	        .Define("zed_leptonic_MC_mass",    "ReconstructedParticle::get_mass( zed_leptonic_MC )" )
		.Define("zed_leptonic_recoil_MC",  "ReconstructedParticle::recoilBuilder(240)( zed_leptonic_MC )")
		.Define("zed_leptonic_recoil_MC_mass",   "ReconstructedParticle::get_mass( zed_leptonic_recoil_MC )")

        )

        


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "selected_muons_costheta",
                "selected_muons_pt",
                "selected_muons_y",
                "selected_muons_p",
                "selected_muons_e",
								"selected_muons_m",
                "selected_muons_n",
								"selected_muons_plus_n",
								"selected_muons_minus_n",
                "zed_leptonic_pt",
                "zed_leptonic_y",
                "zed_leptonic_p",
                "zed_leptonic_e",
                "zed_leptonic_m",
								"zed_leptonic_n",
								"zed_leptonic_costheta",
                "zed_leptonic_charge",
                "zed_leptonic_recoil_m",
                "missingET_costheta",

		"zed_leptonic_MC_mass",
		"zed_leptonic_recoil_MC_mass"
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/higgs/mH-recoil/mumu/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_ZH_ecm240/events_058720051.root
if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/FCCee').replace('analysis.py','')+'/'
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

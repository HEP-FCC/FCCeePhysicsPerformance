import sys
import ROOT
import multiprocessing
import os

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

class analysis():
	
	#__________________________________________________________
	def __init__(self, indir, outname, ncpu):
		self.outname = outname
		if ".root" not in outname:
			self.outname+=".root"

		ROOT.ROOT.EnableImplicitMT(ncpu)

		files = [os.path.join(indir, f) for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f))]
	
		names = ROOT.std.vector('string')()
		for n in files: names.push_back(n)
		
		self.df = ROOT.RDataFrame("events", names)
		print (" done")
	#__________________________________________________________
	def run(self):
		df2 = (self.df
				# define an alias for muon index collection
				.Alias("Muon0", "Muon#0.index")
				# define an alias for missingET index collection
				.Alias("MissingET0", "MissingET#0.index")
				#
				#.Alias("missingET_px", "ReconstructedParticles.momentum.x")
				#
				#.Alias("missingET_py", "ReconstructedParticles.momentum.y")
				#
				#.Alias("missingET_pz", "ReconstructedParticles.momentum.z")
				# define the muon collection
				.Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
				# define the MissingET collection
				.Define("missingET",  "ReconstructedParticle::get(MissingET0, ReconstructedParticles)")
				# create branch with missingET polar angle
				.Define("missingET_costheta",  "getRP_costheta(missingET)")
				#.Define("missingET_costheta",  "ReconstructedParticle::get_MET_costheta(missingET_px, missingET_py, missingET_pz)")
				# create branch with missingET number
				#.Define("missingET_n",  "ReconstructedParticle::get_n(missingET)")
				#select muons on pT
				.Define("selected_muons", "ReconstructedParticle::muon_quality_check(muons)")
				#.Define("selected_muons", "selRP_pT(0.)(muons)")
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
				# find zed candidates from  di-muon resonances  
				.Define("selected_muons_tlv",     "ReconstructedParticle::get_tlv(selected_muons)")
				#.Define("zed_leptonic",         "ResonanceBuilder(23, 91)(selected_muons)")
				.Define("zed_leptonic",         "ReconstructedParticle::resonanceZBuilder(91.1876)(selected_muons)")
				# write branch with zed mass
				.Define("zed_leptonic_m",       "ReconstructedParticle::get_mass(zed_leptonic)")
				# write branch with zed number
				.Define("zed_leptonic_n",       "ReconstructedParticle::get_n(zed_leptonic)")
				# write branch with zed charge
				.Define("zed_leptonic_charge",   "ReconstructedParticle::get_charge(zed_leptonic)")
				# write branch with zed transverse momenta
				.Define("zed_leptonic_pt",      "ReconstructedParticle::get_pt(zed_leptonic)")
				# calculate recoil of zed_leptonic
				.Define("zed_leptonic_recoil",  "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
				# write branch with recoil mass
				.Define("zed_leptonic_recoil_m","ReconstructedParticle::get_mass(zed_leptonic_recoil)") 

		)

        


		# select branches for output file
		branchList = ROOT.vector('string')()
		for branchName in [
					"selected_muons_pt",
					"selected_muons_y",
					"selected_muons_p",
					"selected_muons_e",
					"selected_muons_n",
					"selected_muons_plus_n",
					"selected_muons_minus_n",
					"selected_muons_tlv",
					"zed_leptonic_pt",
					"zed_leptonic_m",
					"zed_leptonic_n",
					"zed_leptonic_charge",
					"zed_leptonic_recoil_m"
					#"missingET_px",
					#"missingET_py",
					#"missingET_pz",
					"missingET_costheta",
					#"missingET_n"
					]:
			branchList.push_back(branchName)
		df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python FCCeeAnalyses/ZH_Zmumu/analysis.py root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/p8_ee_ZZ_ecm240/events_058759855.root
if __name__ == "__main__":

	if len(sys.argv)==1:
		print ("usage:")
		print ("python ",sys.argv[0]," file.root")
		sys.exit(3)
	inDir = sys.argv[1]
	#outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
	outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs').replace('analysis_ang.py','')	
	print (outDir)
	#import os
	os.system("mkdir -p {}".format(outDir))
	outfile = outDir+inDir.split('/')[-1]
	print (outfile)
	#import multiprocessing
	ncpus = int(multiprocessing.cpu_count()-2)
	
	#ncpus = 5
	analysis = analysis(inDir, outfile, ncpus)
	analysis.run()

	infiles = [os.path.join(inDir, f) for f in os.listdir(inDir) if os.path.isfile(os.path.join(inDir, f))]
	
	entries = int (0)
	for f in infiles:
		tf = ROOT.TFile(f)
		print (f)
		entries += tf.events.GetEntries()
	
	p = ROOT.TParameter(int)( "eventsProcessed", entries)
	outf=ROOT.TFile(outfile+".root","UPDATE")
	p.Write()

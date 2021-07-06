
#ifndef  APCHiggsTools_ANALYZERS_H
#define  APCHiggsTools_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"

#include "ReconstructedParticle2MC.h"

namespace APCHiggsTools{
	///build the resonance from 2 particles from an arbitrary list of input ReconstructedPartilces. Keep the closest to the mass given as input
	struct resonanceZBuilder {
		float m_resonance_mass;
		resonanceZBuilder(float arg_resonance_mass);
		ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) ;
	};

        // temporary duplication. When arg_use_MC_Kinematics = true, the true kinematics will be used instead of the track momenta
        struct resonanceZBuilder2 {
                float m_resonance_mass;
                bool m_use_MC_Kinematics;
                resonanceZBuilder2(float arg_resonance_mass, bool arg_use_MC_Kinematics);
                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
                                ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) ;
        };


	/// return the costheta of the input ReconstructedParticles
	ROOT::VecOps::RVec<float> get_cosTheta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

	/// return the costheta of the input missing momentum 
  ROOT::VecOps::RVec<float> get_cosTheta_miss(ROOT::VecOps::RVec<Float_t>Px, ROOT::VecOps::RVec<Float_t>Py, ROOT::VecOps::RVec<Float_t>Pz, ROOT::VecOps::RVec<Float_t>E);
  ///return muon_quality_check result (at least one muon plus and one muon minus)
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  muon_quality_check(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
}
#endif

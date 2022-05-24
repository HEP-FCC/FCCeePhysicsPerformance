#include "APCHiggsTools.h"
#include "ReconstructedParticle.h"

#include <algorithm>

using namespace APCHiggsTools;

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  APCHiggsTools::muon_quality_check(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  //at least one muon + and one muon - in each event
  int n_muon_plus = 0;
	int n_muon_minus = 0;
	int n = in.size();
	for (int i = 0; i < n; ++i) {
		if (in[i].charge == 1.0){
			++n_muon_plus;
		}
		else if (in[i].charge == -1.0){
			++n_muon_minus;
		}
	}
	if (n_muon_plus >= 1 && n_muon_minus >= 1){
		result = in;
	}
	return result;
}

ROOT::VecOps::RVec<float> APCHiggsTools::get_cosTheta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
   ROOT::VecOps::RVec<float> result;
	 for (auto & p: in) {
		 TLorentzVector tlv;
		 tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
		 result.push_back(tlv.CosTheta());
	 }
	 return result;
}

ROOT::VecOps::RVec<float> APCHiggsTools::get_cosTheta_miss(ROOT::VecOps::RVec<Float_t>Px, ROOT::VecOps::RVec<Float_t>Py, ROOT::VecOps::RVec<Float_t>Pz, ROOT::VecOps::RVec<Float_t>E) {
  ROOT::VecOps::RVec<float> result;
  for (int i =0; i < Px.size(); ++i) {
		TLorentzVector tlv;
		tlv.SetPxPyPzE(Px.at(i), Py.at(i), Pz.at(i), E.at(i));
    result.push_back(tlv.CosTheta());
  }
  return result;
} 


APCHiggsTools::resonanceZBuilder::resonanceZBuilder(float arg_resonance_mass) {m_resonance_mass = arg_resonance_mass;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> APCHiggsTools::resonanceZBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      //set initial charge == 0
      reso.charge = 0;
      TLorentzVector reso_lv;
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
                                //prevent +2 and -2 charged Z 
            if (reso.charge == legs[i].charge) continue;
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
                std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}



APCHiggsTools::resonanceZBuilder2::resonanceZBuilder2(float arg_resonance_mass, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_use_MC_Kinematics = arg_use_MC_Kinematics;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> APCHiggsTools::resonanceZBuilder2::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc )   {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      //set initial charge == 0
      reso.charge = 0;
      TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
    				//prevent +2 and -2 charged Z 
            if (reso.charge == legs[i].charge) continue;
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;

		// Ideal detector resolution: use the kinematics of the MC particle instead
		if ( m_use_MC_Kinematics) {

		     // ugly: particles_begin is not filled in RecoParticle.
		     // hence: either need to keep trace of the index of the legs into the RecoParticle collection,
		     // or (as done below) use the track index to map the leg to the MC particle :-(

		     int track_index = legs[i].tracks_begin ;   // index in the Track array
		     int mc_index = FCCAnalyses::ReconstructedParticle2MC::getTrack2MC_index( track_index, recind, mcind, reco );
		     if ( mc_index >= 0 && mc_index < mc.size() ) {
			 int pdgID = mc.at( mc_index).PDG;
		         leg_lv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index ).momentum.y, mc.at(mc_index ).momentum.z, mc.at(mc_index ).mass );
		     }
		}

		else {   //use the kinematics of the reco'ed particle
		     leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
		}

            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
		std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  APCHiggsTools::sort_greater(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  //at least one muon + and one muon - in each event
	
  int n = in.size();
  if (n == 0 ){
    return result;
  }
  ROOT::VecOps::RVec<float> pT = FCCAnalyses::ReconstructedParticle::get_pt(in);
  std::vector< std::pair <float, edm4hep::ReconstructedParticleData> > vect;
  for (int i = 0; i<n ; ++i){
    vect.push_back(std::make_pair(pT.at(i),in.at(i)));
  }
  std::stable_sort(vect.begin(), vect.end(),
                 [](const auto& a, const auto& b){return a.first > b.first;});
  //std::sort(vect.begin(), vect.end());
  for (int i = 0; i<n ; ++i){
    result.push_back(vect.at(i).second);
  } 
  return result;
}



float APCHiggsTools::Reweighting_wzp_kkmc(float pT, float m) {
  float scale;
  if (m > 220.){
    if ( pT > 0. && pT <= 1.){scale = 1.0032322;}
    else if ( pT > 1. && pT <= 2.){scale = 0.95560480;}
    else if ( pT > 2. && pT <= 3.){scale = 0.94986398;}
    else if ( pT > 3. && pT <= 4.){scale = 0.95134129;}
    else if ( pT > 4. && pT <= 5.){scale = 0.94456404;}
    else if ( pT > 5. && pT <= 6.){scale = 0.94726464;}
    else if ( pT > 6. && pT <= 7.){scale = 0.94101542;}
    else if ( pT > 7. && pT <= 8.){scale = 0.91753618;}
    else if ( pT > 8. && pT <= 9.){scale = 0.91804730;}
    else if ( pT > 9. && pT <= 10.){scale = 0.92097238;}
    else if ( pT > 10. && pT <= 11.){scale = 0.91521958;}
    else if ( pT > 11. && pT <= 12.){scale = 0.94550474;}
    else if ( pT > 12. && pT <= 13.){scale = 0.91403417;}
    else if ( pT > 13. && pT <= 14.){scale = 0.87701843;}
    else if ( pT > 14. && pT <= 15.){scale = 0.89537075;}
    else if ( pT > 15. && pT <= 16.){scale = 0.90811988;}
    else if ( pT > 16. && pT <= 17.){scale = 0.90657018;}
    else if ( pT > 17. && pT <= 18.){scale = 0.93739754;}
    else if ( pT > 18. && pT <= 19.){scale = 0.98795371;}
    else if ( pT > 19. && pT <= 20.){scale = 2.6656045;}
    else {scale = 1.;}
  }
  else {scale = 1.;}

  return scale;
}

































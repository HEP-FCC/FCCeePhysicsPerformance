#include "APCHiggsTools.h"
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



































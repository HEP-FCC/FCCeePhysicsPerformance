#include "ReconstructedParticle.h"
using namespace ReconstructedParticle;

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  ReconstructedParticle::muon_quality_check(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
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

ROOT::VecOps::RVec<float> ReconstructedParticle::get_costheta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
   ROOT::VecOps::RVec<float> result;
	 for (auto & p: in) {
		 TLorentzVector tlv;
		 tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
		 result.push_back(tlv.CosTheta());
	 }
	 return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_MET_costheta(ROOT::VecOps::RVec<Float_t>Px, ROOT::VecOps::RVec<Float_t>Py, ROOT::VecOps::RVec<Float_t>Pz, ROOT::VecOps::RVec<Float_t>E) {
  ROOT::VecOps::RVec<float> result;
  for (int i =0; i < Px.size(); ++i) {
		TLorentzVector tlv;
		tlv.SetPxPyPzE(Px.at(i), Py.at(i), Pz.at(i), E.at(i));
    //tv3.SetXYZ(Px, Py, Pz);
    result.push_back(tlv.CosTheta());
  }
  return result;
  //return tv3.CosTheta();
} 

ReconstructedParticle::resonanceZBuilder::resonanceZBuilder(float arg_resonance_mass) {m_resonance_mass = arg_resonance_mass;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedParticle::resonanceZBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) { 
	ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      reso.charge = 0;
			TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
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
































ReconstructedParticle::sel_pt::sel_pt(float arg_min_pt) : m_min_pt(arg_min_pt) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  ReconstructedParticle::sel_pt::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}

ReconstructedParticle::sel_p::sel_p(float arg_min_p) : m_min_p(arg_min_p) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  ReconstructedParticle::sel_p::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2) + std::pow(p.momentum.z,2) ) > m_min_p) {
      result.emplace_back(p);
    }
  }
  return result;
}

ReconstructedParticle::sel_charge::sel_charge(int arg_charge, bool arg_abs){m_charge = arg_charge; m_abs = arg_abs;};

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  ReconstructedParticle::sel_charge::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ((m_abs && abs(in[i].charge)==m_charge) || (m_charge==in[i].charge) ) {
      result.emplace_back(p);
    }
  }
  return result;
}



ReconstructedParticle::resonanceBuilder::resonanceBuilder(float arg_resonance_mass) {m_resonance_mass = arg_resonance_mass;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedParticle::resonanceBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      TLorentzVector reso_lv; 
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
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


ReconstructedParticle::recoilBuilder::recoilBuilder(float arg_sqrts) : m_sqrts(arg_sqrts) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  ReconstructedParticle::recoilBuilder::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
  for (auto & v1: in) {
    TLorentzVector tv1;
    tv1.SetXYZM(v1.momentum.x, v1.momentum.y, v1.momentum.z, v1.mass);
    recoil_p4 -= tv1;
  }
  auto recoil_fcc = edm4hep::ReconstructedParticleData();
  recoil_fcc.momentum.x = recoil_p4.Px();
  recoil_fcc.momentum.y = recoil_p4.Py();
  recoil_fcc.momentum.z = recoil_p4.Pz();
  recoil_fcc.mass = recoil_p4.M();
  result.push_back(recoil_fcc);
  return result;
};


ReconstructedParticle::sel_axis::sel_axis(bool arg_pos): m_pos(arg_pos) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedParticle::sel_axis::operator()(ROOT::VecOps::RVec<float> angle, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle.at(i)>0.) result.push_back(in.at(i));
    if (m_pos==0 && angle.at(i)<0.) result.push_back(in.at(i));;
  }
  return result;
}


// Angular separation between the particles of a collection:
//   arg_delta = 0 / 1 / 2 :   return delta_max, delta_min, delta_average

ReconstructedParticle::angular_separationBuilder::angular_separationBuilder( int  arg_delta) : m_delta(arg_delta) {};
float ReconstructedParticle::angular_separationBuilder::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {

 float result = -9999;

 float dmax = -999;
 float dmin = 999;
 float sum = 0;
 float npairs = 0;
 for (int i=0; i < in.size(); i++) {
  if ( in.at(i).energy < 0) continue;    // "dummy" particle - cf selRP_matched_to_list
  TVector3 p1( in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z );
  for (int j=i+1; j < in.size(); j++) {
    if ( in.at(j).energy < 0) continue;   // "dummy" particle
    TVector3 p2( in.at(j).momentum.x, in.at(j).momentum.y, in.at(j).momentum.z );
    float delta_ij = fabs( p1.Angle( p2 ) );
    if ( delta_ij > dmax) dmax = delta_ij;
    if ( delta_ij < dmin) dmin = delta_ij;
    sum = sum + delta_ij;
    npairs ++;
  }
 }
 float delta_max = dmax;
 float delta_min = dmin;
 float delta_ave = sum / npairs;

 if (m_delta == 0 ) result = delta_max;
 if (m_delta == 1 ) result = delta_min;
 if (m_delta == 2 ) result = delta_ave;

 return result;
}


ROOT::VecOps::RVec<float> ReconstructedParticle::get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedParticle::merge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y) {
  //to be keept as ROOT::VecOps::RVec
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ReconstructedParticle::get(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < index.size(); ++i) {
    if (index[i]>-1)
      result.push_back(in.at(index[i]));
    //else
    //  std::cout << "electron index negative " << index[i]<<std::endl;
  }  
  return result;
}


ROOT::VecOps::RVec<float> ReconstructedParticle::get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}


ROOT::VecOps::RVec<float> ReconstructedParticle::get_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

ROOT::VecOps::RVec<float> ReconstructedParticle::get_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector> ReconstructedParticle::get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}


int ReconstructedParticle::get_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x) {
  int result =  x.size();
  return result;
}


ROOT::VecOps::RVec<bool> ReconstructedParticle::getJet_btag(ROOT::VecOps::RVec<int> index, ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid, ROOT::VecOps::RVec<float> values){
  ROOT::VecOps::RVec<bool> result;
  //std::cout << "========================new event=======================" <<std::endl;
  for (size_t i = 0; i < index.size(); ++i) {
    result.push_back(values.at(pid.at(index.at(i)).parameters_begin +1));
    
    //std::cout << pid.at(index.at(i)).parameters_begin << "  ==  " << pid.at(index.at(i)).parameters_end << std::endl;
    //for (unsigned j = pid.at(index.at(i)).parameters_begin; j != pid.at(index.at(i)).parameters_end; ++j) {
    //  std::cout << " values : " << values.at(j) << std::endl;
    //}
  }
  return result;
}

int ReconstructedParticle::getJet_ntags(ROOT::VecOps::RVec<bool> in) {
  int result =  0;
  for (size_t i = 0; i < in.size(); ++i)
    if (in.at(i))result+=1;
  return result;
}

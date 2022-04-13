{

// ---------------------------------------------------------------------------------
//
// Bd -> K* tau tau with both tau -> nu + 3 charged pions
//
// Plots of the tau decay vertex and of the K* -> K Pi decay vertex (chi2, resolution, pulls).
// The resolution plots are fitted either by a gaussian, or by a sum of two gaussians.
//
// ---------------------------------------------------------------------------------


TChain* events = new TChain("events","events");
events->Add("Bd2KstTauTau_Taus2ThreeChargedPions_evtgen.root");


// We've found indeed a Bd -> K* tau tau decay :
TString cut0 = "FoundBd == 1 ";

// Tau -> 3 pions vertex : require that 3 tracks have been reconstructed
TString cut = cut0 + " && n_TaumTracks == 3";

// and require that the K and Pi tracks from K* -> K Pi have been reco'ed too
cut = cut + " &&  n_KstTracks == 2";

// ---------------------------------------------------------------------------------
//
// Tau -> 3 pions vertex
//


	// Chi2 of the Tau- -> 3 pions vertex fit 

TCanvas* chi2 = new TCanvas("chi2","chi2");
TH1F* hchi2 = new TH1F("hchi2",";#chi^{2}/n.d.f.; a.u.",100,0.,10.);
gStyle->SetOptStat(1110);
events->Draw("TaumVertex.chi2 >>hchi2",cut);
TLatex tt;
TString texte="Bd #rightarrow K* #tau #tau, #tau^{#pm} #rightarrow 3p ";
tt.DrawLatexNDC(0.2,0.955,texte);
TString texte2="#tau decay vertex";
tt.DrawLatexNDC(0.2,0.9,texte2);
gPad -> SetLogy(1);

	// ---------------------------------------------------------------------------------
	//
	// Resolution of the tau vertex position 
	//

	// NB: TaumMCDecayVertex is actually a vector, of size zero or one.
	// The cut used below, that demands that one Bd (with the required decay chain) has been found,
        // ensures that TaumMCDecayVertex contains one element.
 	// In the version of ROOT that I use here (6.08/06), one can then use e.g. TaumMCDecayVertex.x
	// w/o having to specify TaumMCDecayVertex[0].x.


	// in x :

TCanvas*  c2 = new TCanvas("TauVertexPosition_x","TauVertexPosition_x");
TH1F* reso_x_tau = new TH1F("reso_x_tau",";x_{vertex} (rec-true) (#mum); Events",100, -70,70);
events->Draw("1e3*(TaumVertex.position.x-TaumMCDecayVertex.x) >>reso_x_tau", cut);
reso_x_tau->Draw();
reso_x_tau->Fit("gaus");
// Fit by the sum of 2 gaussians:
TF1* fx =new TF1("fx","gaus(0)+gaus(3)",-70,70);
fx->SetParameter(0, reso_x_tau->GetFunction("gaus")->GetParameter(0) );
fx->SetParameter(1, reso_x_tau->GetFunction("gaus")->GetParameter(1) );
fx->SetParameter(2, reso_x_tau->GetFunction("gaus")->GetParameter(2) );
fx->SetParameter(3, 0.5*(reso_x_tau->GetFunction("gaus")->GetParameter(0)) );
fx->SetParameter(4,0.) ;
fx->SetParameter(5, 2*(reso_x_tau->GetFunction("gaus")->GetParameter(2)) );
fx->SetParName(0,"Norm 1");
fx->SetParName(1,"Mean 1");
fx->SetParName(2,"Sigma 1");
fx->SetParName(3,"Norm 2");
fx->SetParName(4,"Mean 2");
fx->SetParName(5,"Sigma 2");
reso_x_tau->Fit("fx","l") ;
fx->SetParameter(4,0.) ;
reso_x_tau->Fit("fx","l") ;
tt.DrawLatexNDC(0.2,0.96,texte);
tt.DrawLatexNDC(0.2,0.9,texte2);


	// in z :

TCanvas*  c3 = new TCanvas("TauVertexPosition_z","TauVertexPosition_z");
TH1F* reso_z_tau = new TH1F("reso_z_tau",";z_{vertex} (rec-true) (#mum); Events",100, -70,70);
events->Draw("1e3*(TaumVertex.position.z-TaumMCDecayVertex.z) >>reso_z_tau", cut);
reso_z_tau->Draw();
reso_z_tau->Fit("gaus");
// Fit by the sum of 2 gaussians:
//TF1* fz =new TF1("fz","gaus(0)+gaus(3)",-70,70);
TF1* fz = (TF1*)fx->Clone();
fz->SetName("fz");
fz->SetParameter(0, reso_z_tau->GetFunction("gaus")->GetParameter(0) );
fz->SetParameter(1, reso_z_tau->GetFunction("gaus")->GetParameter(1) );
fz->SetParameter(2, reso_z_tau->GetFunction("gaus")->GetParameter(2) );
fz->SetParameter(3, 0.5*(reso_z_tau->GetFunction("gaus")->GetParameter(0)) );
fz->SetParameter(4,0.) ;
fz->SetParameter(5, 2*(reso_z_tau->GetFunction("gaus")->GetParameter(2)) );
reso_z_tau->Fit("fz","l") ;
fz->SetParameter(4,0.) ;
fz->SetParameter(5,TMath::Abs( fz->GetParameter(5) ) );
reso_z_tau->Fit("fz","l") ;
tt.DrawLatexNDC(0.2,0.96,texte);
tt.DrawLatexNDC(0.2,0.9,texte2);



	// 3d vertex position, resolution and pull

TCanvas*  c4 = new TCanvas("TauVertexPosition_3d","TauVertexPosition_3d");

TString fld = "TMath::Sqrt( pow( 1e3*TaumVertex.position.x, 2) + pow( 1e3*TaumVertex.position.y,2) + pow( 1e3*TaumVertex.position.z,2))";
TString fld_gen = "TMath::Sqrt( pow( 1e3*TaumMCDecayVertex.x[0], 2) + pow( 1e3*TaumMCDecayVertex.y[0],2) + pow( 1e3*TaumMCDecayVertex.z[0],2)   )";
TString fld_res =  fld + " - " + fld_gen;

TH1F* hfld = new TH1F("hfld","; tertiary vtx position (rec-true) (#mum); Events",100,-70,70);
events->Draw(fld_res+ " >> hfld", cut);
hfld->Fit("gaus");
tt.DrawLatexNDC(0.2,0.96,texte);
tt.DrawLatexNDC(0.2,0.9,texte2);

	// Pull of the Tau vertex position

TCanvas* c5 = new TCanvas("pull_TauVertex_3d","pull_TauVertex_3d");
TString fld_mm = "TMath::Sqrt( pow( TaumVertex.position.x, 2) + pow( TaumVertex.position.y,2) + pow( TaumVertex.position.z,2))";
TString fld_gen_mm = "TMath::Sqrt( pow( TaumMCDecayVertex.x[0], 2) + pow( TaumMCDecayVertex.y[0],2) + pow( TaumMCDecayVertex.z[0],2)   )";
TString fld_res_mm =  fld_mm + " - " + fld_gen_mm;
TString term1 = " TaumVertex.position.x * ( TaumVertex.covMatrix[0] * TaumVertex.position.x + TaumVertex.covMatrix[1] * TaumVertex.position.y + TaumVertex.covMatrix[3] * TaumVertex.position.z ) " ;
TString term2 = " TaumVertex.position.y * ( TaumVertex.covMatrix[1] * TaumVertex.position.x + TaumVertex.covMatrix[2] * TaumVertex.position.y + TaumVertex.covMatrix[4] * TaumVertex.position.z ) " ;
TString term3 = " TaumVertex.position.z * ( TaumVertex.covMatrix[3] * TaumVertex.position.x + TaumVertex.covMatrix[4] * TaumVertex.position.y + TaumVertex.covMatrix[5] * TaumVertex.position.z ) ";
TString tsum = term1 + " + " + term2 + " + " + term3;
TString fld_unc = " ( TMath::Sqrt( " + tsum + ") / " + fld_mm +" ) ";
TString fld_pull = "( " + fld_res_mm + " ) / " + fld_unc;
TH1F* h_fld_pull = new TH1F("h_fld_pull","; Pull tertiary vtx position; a.u.",100,-5,5);
events->Draw(fld_pull+" >> h_fld_pull" , cut);
h_fld_pull->Fit("gaus");
tt.DrawLatexNDC(0.2,0.96,texte);
tt.DrawLatexNDC(0.2,0.9,texte2);


// ---------------------------------------------------------------------------------
//
// K* -> K Pi vertex
//


        // Chi2 of the K* -> K Pi vertex fit

TCanvas* Kstchi2 = new TCanvas("Kstchi2","Kstchi2");
TH1F* hchi2_Kst = new TH1F("hchi2_Kst",";#chi^{2}/n.d.f.; a.u.",100,0.,10.);
gStyle->SetOptStat(1110);
events->Draw("KstVertex.chi2 >>hchi2_Kst",cut);
tt.DrawLatexNDC(0.2,0.955,texte);
texte2="K* #rightarrow K #pi decay vertex";
tt.DrawLatexNDC(0.2,0.9,texte2);
gPad -> SetLogy(1);


        // ---------------------------------------------------------------------------------
        //
        // Resolution of the Kstar vertex position 
        //


        // in x :

TCanvas*  c6 = new TCanvas("KstVertexPosition_x","KstVertexPosition_x");
TH1F* reso_x_Kst = new TH1F("reso_x_Kst",";x_{vertex} (rec-true) (#mum); Events",100, -70,70);
events->Draw("1e3*(KstVertex.position.x-KstMCDecayVertex.x) >>reso_x_Kst", cut);
reso_x_Kst->Draw();
reso_x_Kst->Fit("gaus");
// Fit by the sum of 2 gaussians:
TF1* fxKst = (TF1*)fx->Clone();
fxKst->SetName("fxKst");
fxKst->SetParameter(0, reso_x_Kst->GetFunction("gaus")->GetParameter(0) );
fxKst->SetParameter(1, reso_x_Kst->GetFunction("gaus")->GetParameter(1) );
fxKst->SetParameter(2, reso_x_Kst->GetFunction("gaus")->GetParameter(2) );
fxKst->SetParameter(3, 0.5*(reso_x_Kst->GetFunction("gaus")->GetParameter(0)) );
fxKst->SetParameter(4,0.) ;
fxKst->SetParameter(5, 2*(reso_x_Kst->GetFunction("gaus")->GetParameter(2)) );
reso_x_Kst->Fit("fxKst","l") ;
fxKst->SetParameter(4,0.) ;
reso_x_Kst->Fit("fxKst","l") ;
tt.DrawLatexNDC(0.2,0.96,texte);
tt.DrawLatexNDC(0.2,0.9,texte2);





}

{


TChain* events = new TChain("events","events");
events->Add("p8_ecm91GeV_Zbb_EvtGen_Bs2DsK_IDEAtrkCov_p10_v0.root");



// Basic cut & acceptance : demand only one Bs decay to make it safer,
// and that there are 3 reco'ed tracks associated with the Ds :

TString cut0 = "@Bs.size() == 1  && n_DsTracks == 3";

/*
// flight distance of the Bs (MC level) :
events->Draw("TMath::Sqrt( pow( BsMCDecayVertex.x,2) + pow(BsMCDecayVertex.y,2) + pow(BsMCDecayVertex.z,2) )",cut0); 

// flight distance of the Ds, relative to the  Bs (MC level):
events->Draw("TMath::Sqrt( pow( DsMCDecayVertex.x - BsMCDecayVertex.x,2) + pow( DsMCDecayVertex.y - BsMCDecayVertex.y, 2) + pow( DsMCDecayVertex.z - BsMCDecayVertex.z,2) )",cut0);

// flight distance of the Ds (MC level)
events->Draw("TMath::Sqrt( pow(DsMCDecayVertex.x,2) + pow(DsMCDecayVertex.y,2) + pow(DsMCDecayVertex.z,2))",cut0);
*/


// Number of tracks
TH1F* hntr = new TH1F("hntr",";N( Ds tracks ); a.u.",4,-0.5,3.5);
events->Draw("n_DsTracks >>hntr",  "@Bs.size() == 1");
TCanvas* cnt = new TCanvas("cnt","cnt");
gStyle->SetOptStat(10);   // Entries only
hntr->Draw();
gStyle->SetOptStat(10);
TLatex tt;
tt.SetTextSize(0.04);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
gPad -> SetLogy(1);
//cnt->SaveAs("plots/Bs2DsK_nTracks.pdf");


// Chi2 of the Ds vertex fit 
TCanvas* cchi2 = new TCanvas("cchi2","cxhi2");
TH1F* hchi2 = new TH1F("hchi2",";#chi^{2}/n.d.f.; a.u.",100,0.,10.);
gStyle->SetOptStat(1110);
events->Draw("DsVertex.chi2 >>hchi2",cut0+"&& DsVertex.chi2>0");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
gPad -> SetLogy(1);
//cchi2->SaveAs("plots/Bs2DsK_Ds_chi2.pdf");


TCanvas*  c2 = new TCanvas("flight_distance_Ds","flight_distance_Ds");
TString cut = cut0 + " && DsVertex.chi2[0] > 0 && DsVertex.chi2[0] < 10 ";

// "Flight distance" of the Ds - rather the position of the Ds decay vertex

TString fld = "TMath::Sqrt( pow( 1e3*DsVertex.position.x, 2) + pow( 1e3*DsVertex.position.y,2) + pow( 1e3*DsVertex.position.z,2))";
TString fld_gen = "TMath::Sqrt( pow( 1e3*DsMCDecayVertex.x[0], 2) + pow( 1e3*DsMCDecayVertex.y[0],2) + pow( 1e3*DsMCDecayVertex.z[0],2)   )";
TString fld_res =  fld + " - " + fld_gen;

TH1F* hfld = new TH1F("hfld","; tertiary vtx position (rec-true) (#mum); Events",100,-70,70);
events->Draw(fld_res+ " >> hfld", cut);
hfld->Fit("gaus");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
//c2->SaveAs("plots/Ds_vertex_position.pdf");

// Pull of the Ds vertex position

TCanvas* c3 = new TCanvas("pull_flight_distance_Ds","pull_flight_distance_Ds");
TString fld_mm = "TMath::Sqrt( pow( DsVertex.position.x, 2) + pow( DsVertex.position.y,2) + pow( DsVertex.position.z,2))";
TString fld_gen_mm = "TMath::Sqrt( pow( DsMCDecayVertex.x[0], 2) + pow( DsMCDecayVertex.y[0],2) + pow( DsMCDecayVertex.z[0],2)   )";
TString fld_res_mm =  fld_mm + " - " + fld_gen_mm;
TString term1 = " DsVertex.position.x * ( DsVertex.covMatrix[0] * DsVertex.position.x + DsVertex.covMatrix[1] * DsVertex.position.y + DsVertex.covMatrix[3] * DsVertex.position.z ) " ;
TString term2 = " DsVertex.position.y * ( DsVertex.covMatrix[1] * DsVertex.position.x + DsVertex.covMatrix[2] * DsVertex.position.y + DsVertex.covMatrix[4] * DsVertex.position.z ) " ;
TString term3 = " DsVertex.position.z * ( DsVertex.covMatrix[3] * DsVertex.position.x + DsVertex.covMatrix[4] * DsVertex.position.y + DsVertex.covMatrix[5] * DsVertex.position.z ) ";
TString tsum = term1 + " + " + term2 + " + " + term3;
TString fld_unc = " ( TMath::Sqrt( " + tsum + ") / " + fld_mm +" ) ";
TString fld_pull = "( " + fld_res_mm + " ) / " + fld_unc;
TH1F* h_fld_pull = new TH1F("h_fld_pull","; Pull tertiary vtx position; a.u.",100,-5,5);
events->Draw(fld_pull+" >> h_fld_pull" , cut);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
//c3->SaveAs("plots/pull_Ds_vertex_position.pdf");



// -----------------------------------------------------------------------------------------
//
// the propagated tracks at the vertex of the  Ds : show that the corrected Ds
// is better than the non corrected one
//
// -----------------------------------------------------------------------------------------

TCanvas* c4 = new TCanvas("Ds_mass","Ds_mass");
TH1F* h1 = new TH1F("h1","; D_{s} mass (GeV); a.u.",100,1.95,1.99);
events->Draw("RecoDs_mass>>h1",cut0);
TH1F* h2 = new TH1F("h2","; D_{s} mass (GeV); a.u.",100,1.95,1.99);
events->Draw("RecoDs_atVertex_mass>>h2",cut0);
h1->SetLineColor(2);
h2->Draw();
h1->Draw("same");
//h2->Fit("gaus");

gStyle->SetOptStat(0);

TLegend* leg = new TLegend(0.66,0.15,0.94,0.3);
leg -> SetFillColor(0) ;
leg -> SetBorderSize(0);
leg -> SetTextSize(0.04) ;
leg -> AddEntry( h1, "w/o vtx correction","l");
leg -> AddEntry( h2, "with vtx correction","l");
leg -> Draw();
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
//c4->SaveAs("plots/Ds_mass.pdf");



//
// Bs vertex :
//

// chi2 of the Bs vertex

cut = cut + " && n_BsTracks >=2" ;   // remove events for which the bachelor K did not make a reco'ed track

TCanvas* cc = new TCanvas("Bschi2","Bschi2");
TH1F* hbschi2 = new TH1F("hbschi2",";#chi^{2}/n.d.f.;a.u.",100,0.,10.);
//TH1F* hbschi2 = new TH1F("hbschi2",";#chi^{2}/n.d.f.;a.u.",100,0.,5.);
events->Draw("BsVertex_Cov.chi2 >>hbschi2",cut);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex");

// resolution on flight  distance :

TCanvas* c5 = new TCanvas("flight_distance_Bs","flight_distance_Bs");

TString Bfld = "TMath::Sqrt( pow( 1e3*BsVertex.position.x, 2) + pow( 1e3*BsVertex.position.y,2) + pow( 1e3*BsVertex.position.z,2))";
TString Bfld_gen = "TMath::Sqrt( pow( 1e3*BsMCDecayVertex.x, 2) + pow( 1e3*BsMCDecayVertex.y,2) + pow( 1e3*BsMCDecayVertex.z,2)   )";
TString Bfld_res =  Bfld + " - " + Bfld_gen;

TH1F* Bhfld = new TH1F("Bhfld","; flight distance (rec-true) (#mum); Events",100,-70,70);
events->Draw(Bfld_res+ " >> Bhfld", cut);

Bfld = "TMath::Sqrt( pow( 1e3*BsVertex_Cov.position.x, 2) + pow( 1e3*BsVertex_Cov.position.y,2) + pow( 1e3*BsVertex_Cov.position.z,2))";
Bfld_res =  Bfld + " - " + Bfld_gen;

TH1F* Bhfld_Cov = new TH1F("Bhfld_Cov","; flight distance (rec-true) (#mum); Events",100,-70,70);
events->Draw(Bfld_res+ " >> Bhfld_Cov", cut+" && BsVertex_Cov.chi2 < 10");
Bhfld_Cov->Draw();
Bhfld_Cov->Fit("gaus");
gStyle->SetOptStat(1110);
Bhfld_Cov->Draw();
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex");
//c5 -> SaveAs("plots/Bsvertex_flight_distance.pdf");


// pulls
TCanvas* c6 = new TCanvas("pull_Bs_vertex_x","pull_Bs_vertex_x");

TH1F* Bpx = new TH1F("Bpx",";Pull x_{vtx}; a.u.",100,-5,5) ;
TString Bpullx = "(BsVertex_Cov.position.x-BsMCDecayVertex.x)/TMath::Sqrt(BsVertex_Cov.covMatrix[0])>>Bpx";
events->Draw(Bpullx, cut+"&& BsVertex_Cov.chi2 > 0 && BsVertex_Cov.chi2 <10");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
gStyle->SetOptStat(1110);
tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex");
Bpx->Fit("gaus");
//c6 -> SaveAs("plots/Bsvertex_pull_x.pdf");

TH1F* Bpy = new TH1F("Bpy",";Pull y_{vtx}; a.u.",100,-5,5) ;
TString Bpully = "(BsVertex_Cov.position.y-BsMCDecayVertex.y)/TMath::Sqrt(BsVertex_Cov.covMatrix[2])>>Bpy";
events->Draw(Bpully, cut+"&& BsVertex_Cov.chi2 > 0 && BsVertex_Cov.chi2 <10");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
gStyle->SetOptStat(1110);
tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex");
Bpy->Fit("gaus");

TH1F* Bpz = new TH1F("Bpz",";Pull z_{vtx}; a.u.",100,-5,5) ;
TString Bpullz = "(BsVertex_Cov.position.z-BsMCDecayVertex.z)/TMath::Sqrt(BsVertex_Cov.covMatrix[5])>>Bpz";
events->Draw(Bpullz, cut+"&& BsVertex_Cov.chi2 > 0 && BsVertex_Cov.chi2 <10");
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
gStyle->SetOptStat(1110);
tt.DrawLatexNDC(0.2, 0.9, "B_{s} decay vertex");
Bpz->Fit("gaus");



// pulls on the Bs vertex position

TCanvas* c7 = new TCanvas("pull_flight_distance_Bs","pull_flight_distance_Bs");
TString bfld_mm = "TMath::Sqrt( pow( BsVertex_Cov.position.x, 2) + pow( BsVertex_Cov.position.y,2) + pow( BsVertex_Cov.position.z,2))";
TString bfld_gen_mm = "TMath::Sqrt( pow( BsMCDecayVertex.x[0], 2) + pow( BsMCDecayVertex.y[0],2) + pow( BsMCDecayVertex.z[0],2)   )";
TString bfld_res_mm =  bfld_mm + " - " + bfld_gen_mm;
TString bterm1 = " BsVertex_Cov.position.x * ( BsVertex_Cov.covMatrix[0] * BsVertex_Cov.position.x + BsVertex_Cov.covMatrix[1] * BsVertex_Cov.position.y + BsVertex_Cov.covMatrix[3] * BsVertex_Cov.position.z ) " ;
TString bterm2 = " BsVertex_Cov.position.y * ( BsVertex_Cov.covMatrix[1] * BsVertex_Cov.position.x + BsVertex_Cov.covMatrix[2] * BsVertex_Cov.position.y + BsVertex_Cov.covMatrix[4] * BsVertex_Cov.position.z ) " ;
TString bterm3 = " BsVertex_Cov.position.z * ( BsVertex_Cov.covMatrix[3] * BsVertex_Cov.position.x + BsVertex_Cov.covMatrix[4] * BsVertex_Cov.position.y + BsVertex_Cov.covMatrix[5] * BsVertex_Cov.position.z ) ";
TString btsum = bterm1 + " + " + bterm2 + " + " + bterm3;
TString bfld_unc = " ( TMath::Sqrt( " + btsum + ") / " + bfld_mm +" ) ";
TString bfld_pull = "( " + bfld_res_mm + " ) / " + bfld_unc;
TH1F* h_bfld_pull = new TH1F("h_bfld_pull","; Pull Bs flight distance; a.u.",100,-5,5);
events->Draw(bfld_pull+" >> h_bfld_pull" , cut);
tt.DrawLatexNDC(0.2,0.96,"B_{s} #rightarrow D_{s}K  #rightarrow KK#piK");
h_bfld_pull->Fit("gaus");






}

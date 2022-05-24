import ROOT

# global parameters
intLumi					= 5.0e+06 #in pb-1
#inputDir         = '/afs/cern.ch/work/l/lia/private/FCC/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/outputs/FCCee/higgs/mH-recoil/mumu'
inputDir         = '/eos/user/l/lia/FCCee/MVA/trainedNtuples/final'
#outDir            = '/afs/cern.ch/work/l/lia/private/FCC/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/outputs/FCCee/higgs/mH-recoil/mumu/fitresults/'
outDir           = '/eos/home-l/lia/FCCee/MVA/trainedNtuples/plots_fit'
#histoName       = "leptonic_recoil_m_MC_zoom2"
histoName       = "leptonic_recoil_m_zoom3"
# selection name
#sel							= 'MC_sel23'
#sel              = 'sel23'
sel              = 'sel0_MRecoil_Mll_73_120_pTll_05_MVA09'
# fit mode
# true: 	Signal + background fit
# false:  Signal Only fit
SBMode					= False
#SBMode         = True
# activate the new modelled signal method 
NewModelledSignalMode	= False
modelFunction			= 'DCB'

#fitMode:
#0: default
#1: range fit please set fitRange
#2 sideband fit please set sidebandRange
fitMode 				= 0
fitRange				= ['124', '130']
sidebandRange				= ['120', '124', '130', '140']

# fit function
#fitting fucntions, if SBMode = true, please set sgnFunction and bkgFunction
#CBR:     Single Crystal Ball, tail on the right side
#CBL:     Single Crystal Ball. tail on the left side
#BW:      Breit-Wigner
#landau:  Landau distribution
#DCB:     Double-sided Crystal Ball
#Pol1:    1st order Polynomial
#Pol2:    2nd order Polynomial
#Pol3:    3rd order Polynomial
#Pol4:    4th order Polynomial
#Exp:     Exponential
#sgnFunction     = 'CBRG'
#sgnFunction     = 'DCB'
#sgnFunction     = 'DCBA'
#sgnFunction     = 'DCBA_Pol2'
sgnFunction     = 'DCBG'
#sgnFunction     = 'DCBAG'
#sgnFunction     = '2CBG'
#sgnFunction     = '2CBG2'
#sgnFunction     = '2CBG_Pol2'
#sgnFunction     = '2CBG2_Pol2'
#sgnFunction     = 'DCB_Pol2'
#sgnFunction     = 'BW'
#sgnFunction     = 'Pol2'
#sgnFunction     = 'Pol3'
#sgnFunction     = 'Pol4'
#sgnFunction     = 'Bern4'

#sgnFunction     = 'Chebychev3'
#sgnFunction     = 'Bern3'
#Pol1:    1st order Polynomial
#Pol2:    2nd order Polynomial
#Pol3:    3rd order Polynomial
#Pol4:    4th order Polynomial
#Chebychev1:    1st order Chebychev Polynomial
#Chebychev2:    2nd order Chebychev Polynomial
#Chebychev3:    3rd order Chebychev Polynomial
#Chebychev4:    4th order Chebychev Polynomial
bkgFunction      = 'Pol2'
#bkgFunction			= 'Pol3'
#bkgFunction     = 'Bern3'
#sgnProcesses = {'ZH':['p8_ee_ZH_ecm240']}
#sgnProcesses = {'WWmumu':['p8_ee_WW_mumu_ecm240']}
#sgnProcesses = {'ZZ':['p8_ee_ZZ_ecm240']}
#sgnProcesses = {'Zll':['p8_ee_Zll_ecm240']}
sgnProcesses = {'mumuH':['wzp6_ee_mumuH_ecm240']}
#sgnProcesses = {'ZZ':['p8_ee_ZZ_ecm240'],
#                'WWmumu':['p8_ee_WW_mumu_ecm240'],
#                'Zll':['wzp6_ee_mumu_ecm240'],
#                'eeZ':['wzp6_egamma_eZ_Zmumu_ecm240','wzp6_gammae_eZ_Zmumu_ecm240'],
#                }
#sgnProcesses = {'ZZ':['p8_ee_ZZ_ecm240'],
#                'WWmumu':['p8_ee_WW_mumu_ecm240'],
#                'Zll':['p8_ee_Zll_ecm240']}
#bkgProcesses = {'ZZ':['p8_ee_ZZ_ecm240'],
#                  'WWmumu':['p8_ee_WW_mumu_ecm240'],
#                  'Zll':['p8_ee_Zll_ecm240'],
#                  'Zqq':['p8_ee_Zqq_ecm240'],
#                  'eeZ':['wzp6_egamma_eZ_Zmumu_ecm240', 'wzp6_gammae_eZ_Zmumu_ecm240'],
#                  'yymm':['wzp6_gaga_mumu_60_ecm240'],
#                  'yytt':['wzp6_gaga_tautau_60_ecm240']}
bkgProcesses = {'ZZ':['p8_ee_ZZ_ecm240'],
                'WWmumu':['p8_ee_WW_mumu_ecm240'],
                'Zll':['wzp6_ee_mumu_ecm240'],
                'eeZ':['wzp6_egamma_eZ_Zmumu_ecm240','wzp6_gammae_eZ_Zmumu_ecm240'],
                }
# fitting parameters
# if not set, will use tha default value
#please do not change the parameters' name
#customized mean not recommended 

#Gaussian parameters
#mean = ROOT.RooRealVar("mean", "mean", 125.0, 124.0, 126.0)
#sigma = ROOT.RooRealVar("sigma", "width", 0.35, 0.3, 1.5)
#alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.7, 0.1, 10)
#n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 1.0,0.1,200.0)
#n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.0,0.1,200.0)
#DSCB parameters
#alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.637, 1.637, 1.637)
#n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 3.32, 3.32, 3.32)
#alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.925, 0.925, 0.925)
#n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.111, 1.111, 1.111)

#Polynomial bkg parameters
#p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00387, -0.00387)
#p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000158, -0.0000158)
#p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.0000000123, -0.0000000123)




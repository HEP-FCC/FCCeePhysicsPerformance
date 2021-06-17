import ROOT

# global parameters
intLumi					= 5.0e+06 #in pb-1
inputDir         = '/afs/cern.ch/work/l/lia/private/FCC/test/FCCAnalyses_0601/outputs/FCCee/higgs/mH-recoil/mumu'

outDir            = '/afs/cern.ch/work/l/lia/private/FCC/test/FCCAnalyses_0601/outputs/FCCee/higgs/mH-recoil/mumu/fitresults/'
histoName       = "leptonic_recoil_m_zoom2"
# selection name
sel							= 'sel23'
# fit mode
# true: 	Signal + background fit
# false:  Signal Only fit
SBMode					= True

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
sgnFunction     = 'DCB'

#Pol1:    1st order Polynomial
#Pol2:    2nd order Polynomial
#Pol3:    3rd order Polynomial
#Pol4:    4th order Polynomial
#Chebychev1:    1st order Chebychev Polynomial
#Chebychev2:    2nd order Chebychev Polynomial
#Chebychev3:    3rd order Chebychev Polynomial
#Chebychev4:    4th order Chebychev Polynomial
bkgFunction			= 'Pol2'
sgnProcesses = {'ZH':['p8_ee_ZH_ecm240']}

bkgProcesses = {'ZZ':['p8_ee_ZZ_ecm240'],
                  'WWmumu':['p8_ee_WW_mumu_ecm240'],
                  'Zll':['p8_ee_Zll_ecm240'],
                  'Zqq':['p8_ee_Zqq_ecm240'],
                  'egamma':['wzp6_egamma_eZ_Zmumu_ecm240', 'wzp6_gammae_eZ_Zmumu_ecm240'],
                  'gagamumu':['wzp6_gaga_mumu_60_ecm240'],
                  'gagatautau':['wzp6_gaga_tautau_60_ecm240']}
          
# fitting parameters
# if not set, will use tha default value
#please do not change the parameters' name
#customized mean not recommended 

#Gaussian parameters
#mean = ROOT.RooRealVar("mean", "mean", 125.0, 124.0, 126.0)
sigma = ROOT.RooRealVar("sigma", "width", 0.35, 0.3, 1.5)
alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.7, 0.1, 10)
n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 1.0,0.1,200.0)
n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.0,0.1,200.0)
#DSCB parameters
#alpha_L = ROOT.RooRealVar("alphaL", "alpha of Crystal Ball", 1.637, 1.637, 1.637)
#n_L = ROOT.RooRealVar("nL", "n of Crystal Ball", 3.32, 3.32, 3.32)
#alpha_H = ROOT.RooRealVar("alphaH", "alpha of Crystal Ball", 0.925, 0.925, 0.925)
#n_H = ROOT.RooRealVar("nH", "n of Crystal Ball", 1.111, 1.111, 1.111)

#Polynomial bkg parameters
#p0 = ROOT.RooRealVar("p0", "p0 of polynomial", -0.00387, -0.00387)
#p1 = ROOT.RooRealVar("p1", "p1 of polynomial", -0.0000158, -0.0000158)
#p2 = ROOT.RooRealVar("p2", "p2 of polynomial", -0.0000000123, -0.0000000123)




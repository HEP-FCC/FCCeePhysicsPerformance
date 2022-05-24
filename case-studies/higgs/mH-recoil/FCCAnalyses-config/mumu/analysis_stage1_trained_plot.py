import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = '/eos/user/l/lia/FCCee/MVA/trainedNtuples/final/'
#formats        = ['png','pdf']
yaxis          = ['lin','log']
#yaxis          = ['lin']
stacksig       = ['stack','nostack']
#stacksig       = ['stack']
formats        = ['pdf']
#yaxis          = ['lin']
outdir         = '/eos/user/l/lia/FCCee/MVA/trainedNtuples/plots/'

variables = [  #muons
               #"mz",
               #"mz_zoom1",
               #"mz_zoom2",
               #"mz_zoom3",
               #"mz_zoom4",
               #"leptonic_recoil_m",
               #"leptonic_recoil_m_zoom1",
               #"leptonic_recoil_m_zoom2",
               #"leptonic_recoil_m_zoom3",
               #"leptonic_recoil_m_zoom4",
               "BDT_Score",
            ]
###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   =[ 
                     "sel0", 
                     "sel_MVA02",
                     "sel_MVA04", 
                     "sel_MVA06",
                     "sel_MVA08",
                     "sel_MVA09", 
                     "sel_Baseline", 
                     "sel_Baseline_MVA02", 
                     "sel_Baseline_MVA06", 
                     "sel_APC1",
                     "sel_APC1_MVA02", 
                     "sel_APC1_MVA06", 
                     "sel_APC1_MVA02_mll_80_100", 
                     "sel_APC1_MVA02_mll_75_100", 
                     "sel_APC1_MVA02_mll_73_120",
                     "sel_APC1_MVA02_mll_80_100_nopT", 
                     "sel_APC1_MVA02_mll_80_100_pT20", 
                     "sel_APC1_MVA02_mll_80_100_pT10",
                     "sel0_MRecoil",
                     "sel0_MRecoil_MVA02",
                     "sel0_MRecoil_Mll",
                     "sel0_MRecoil_Mll_MVA02",
                     "sel0_MRecoil_pTll",
                     "sel0_MRecoil_pTll_MVA02",
                     "sel0_Mll",
                     "sel0_Mll_MVA02",
                     "sel0_pTll",
                     "sel0_pTll_MVA02",
                     "sel0_MRecoil_Mll_80_100",
                     "sel0_MRecoil_Mll_75_100",
                     "sel0_MRecoil_Mll_73_120",
                     "sel0_MRecoil_pTll_20",
                     "sel0_MRecoil_pTll_15",
                     "sel0_MRecoil_pTll_10",
                     "sel0_MRecoil_pTll_05",
                     "sel0_MRecoil_Mll_73_120_pTll_05",                    
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA02",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA04",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA06",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA08",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA09",
                     "sel_MVA02_costhetamiss",
                     "sel_MVA04_costhetamiss",
                     "sel_MVA06_costhetamiss",
                     "sel_MVA08_costhetamiss",
                     "sel_MVA09_costhetamiss",
                     "sel0_MRecoil_Mll_73_120_pTll_05_costhetamiss",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA02_costhetamiss",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA08_costhetamiss",
                     "sel0_MRecoil_Mll_73_120_pTll_05_MVA09_costhetamiss",
                     "sel_Baseline_no_costhetamiss",
                     ]
extralabel = {}
extralabel['sel0']                            = "Selection: No Selection"
extralabel["sel_MVA02"]                       = "MVA02"
extralabel["sel_MVA04"]                       = "MVA04"
extralabel["sel_MVA06"]                       = "MVA06"
extralabel["sel_MVA08"]                       = "MVA08"
extralabel["sel_MVA09"]                       = "MVA09"
extralabel['sel_Baseline']                    = "Baseline"
extralabel['sel_Baseline_MVA02']              = "Baseline_MVA02"
extralabel['sel_Baseline_MVA06']              = "Baseline_MVA06"
extralabel['sel_APC1']                        = 'APC1'
extralabel['sel_APC1_MVA02']                  = "APC1_MVA02"
extralabel['sel_APC1_MVA06']                  = "APC1_MVA06"
extralabel['sel_APC1_MVA02_mll_80_100']       = "APC1_MVA02_mll_80_100"
extralabel['sel_APC1_MVA02_mll_75_100']       = "APC1_MVA02_mll_75_100"
extralabel['sel_APC1_MVA02_mll_73_120']       = "APC1_MVA02_mll_73_120"
extralabel['sel_APC1_MVA02_mll_80_100_nopT']  = "APC1_MVA02_mll_80_100_nopT"
extralabel['sel_APC1_MVA02_mll_80_100_pT20']  = "APC1_MVA02_mll_80_100_pT20"
extralabel['sel_APC1_MVA02_mll_80_100_pT10']  = "APC1_MVA02_mll_80_100_pT10"
extralabel["sel0_MRecoil"]                    = "sel0_MRecoil"
extralabel["sel0_MRecoil_MVA02"]              = "sel0_MRecoil_MVA02"
extralabel["sel0_MRecoil_Mll"]                = "sel0_MRecoil_Mll"
extralabel["sel0_MRecoil_Mll_MVA02"]          = "sel0_MRecoil_Mll_MVA02"
extralabel["sel0_MRecoil_pTll"]               = "sel0_MRecoil_pTll"
extralabel["sel0_MRecoil_pTll_MVA02"]         = "sel0_MRecoil_pTll_MVA02"
extralabel["sel0_Mll"]                        = "sel0_Mll"
extralabel["sel0_Mll_MVA02"]                  = "sel0_Mll_MVA02"
extralabel["sel0_pTll"]                       = "sel0_pTll"
extralabel["sel0_pTll_MVA02"]                 = "sel0_pTll_MVA02"
extralabel["sel0_MRecoil_Mll_80_100"]         = "sel0_MRecoil_Mll_80_100"
extralabel["sel0_MRecoil_Mll_75_100"]         = "sel0_MRecoil_Mll_75_100"
extralabel["sel0_MRecoil_Mll_73_120"]         = "sel0_MRecoil_Mll_73_120"
extralabel["sel0_MRecoil_pTll_20"]            = "sel0_MRecoil_pTll_20"
extralabel["sel0_MRecoil_pTll_15"]            = "sel0_MRecoil_pTll_15"
extralabel["sel0_MRecoil_pTll_10"]            = "sel0_MRecoil_pTll_10"
extralabel["sel0_MRecoil_pTll_05"]            = "sel0_MRecoil_pTll_05"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05"]       = "sel0_MRecoil_Mll_73_120_pTll_05" 
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA02"] = "sel0_MRecoil_Mll_73_120_pTll_05_MVA02"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA04"] = "sel0_MRecoil_Mll_73_120_pTll_05_MVA04"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA06"] = "sel0_MRecoil_Mll_73_120_pTll_05_MVA06"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA08"] = "sel0_MRecoil_Mll_73_120_pTll_05_MVA08"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA09"] = "sel0_MRecoil_Mll_73_120_pTll_05_MVA09"
extralabel["sel_MVA02_costhetamiss"]            = "sel_MVA02_costhetamiss" 
extralabel["sel_MVA04_costhetamiss"]            = "sel_MVA04_costhetamiss"
extralabel["sel_MVA06_costhetamiss"]            = "sel_MVA06_costhetamiss"
extralabel["sel_MVA08_costhetamiss"]            = "sel_MVA08_costhetamiss"
extralabel["sel_MVA09_costhetamiss"]            = "sel_MVA09_costhetamiss"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_costhetamiss"]        = "sel0_MRecoil_Mll_73_120_pTll_05_costhetamiss" 
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA02_costhetamiss"]  = "sel0_MRecoil_Mll_73_120_pTll_05_MVA02_costhetamiss" 
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss"]  = "sel0_MRecoil_Mll_73_120_pTll_05_MVA04_costhetamiss"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss"]  = "sel0_MRecoil_Mll_73_120_pTll_05_MVA06_costhetamiss"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA08_costhetamiss"]  = "sel0_MRecoil_Mll_73_120_pTll_05_MVA08_costhetamiss"
extralabel["sel0_MRecoil_Mll_73_120_pTll_05_MVA09_costhetamiss"]  = "sel0_MRecoil_Mll_73_120_pTll_05_MVA09_costhetamiss"
extralabel["sel_Baseline_no_costhetamiss"]      = "sel_Baseline_no_costhetamiss"   
                     
colors = {}
colors['mumuH'] = ROOT.kRed
colors['tautauH'] = ROOT.kMagenta
colors['nunuH'] = ROOT.kOrange
colors['eeH'] = ROOT.kYellow
colors['qqH'] = ROOT.kSpring
colors['WWmumu'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['Zqq'] = ROOT.kYellow+2
colors['Zll'] = ROOT.kCyan
colors['eeZ'] = ROOT.kSpring+10
colors['gagatautau'] = ROOT.kViolet+7
colors['gagamumu'] = ROOT.kBlue-8

colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['VV'] = ROOT.kGreen+3

plots = {}
plots['ZH'] = {'signal':{'ZH':['wzp6_ee_mumuH_ecm240']},
               'backgrounds':{'eeZ':["wzp6_egamma_eZ_Zmumu_ecm240",
                                     "wzp6_gammae_eZ_Zmumu_ecm240"],
                                'WW':['p8_ee_WW_mumu_ecm240'],
                                'Zll':['wzp6_ee_mumu_ecm240'],
                                'ZZ':['p8_ee_ZZ_ecm240']}
              }

legend = {}
legend['mumuH'] = 'Z(#mu^{-}#mu^{+})H'
legend['tautauH'] = 'Z(#tau^{-}#tau^{+})H'
legend['qqH'] = 'Z(q#bar{q})H'
legend['eeH'] = 'Z(e^{-}e^{+})H'
legend['nunuH'] = 'Z(#nu#bar{#nu})H'
legend['Zqq'] = 'Z#rightarrow q#bar{q}'
legend['Zll'] = 'Z/#gamma#rightarrow #mu^{+}#mu^{-}'
legend['eeZ'] = 'eeZ'
legend['Wmumu'] = 'W^{+}(#bar{#nu}#mu^{+})W^{-}(#nu#mu^{-})'
legend['gagamumu'] = '#gamma#gamma#mu^{-}#mu^{+}'
legend['gagatautau'] = '#gamma#gamma#tau^{-}#tau^{+}'
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['VV'] = 'VV boson'





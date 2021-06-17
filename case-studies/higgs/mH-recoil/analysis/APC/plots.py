import ROOT

# global parameters
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = 'outputs/FCCee/higgs/mH-recoil/mumu/'
#formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
formats        = ['pdf']
#yaxis          = ['lin']
outdir         = 'outputs/FCCee/higgs/mH-recoil/mumu/plots/'

#variables = ['leptonic_recoil_m_zoom2']
#variables = ['leptonic_recoil_m_zoom9']
#variables = ['Nmu', 'Nmu_plus', 'Nmu_minus', 'Cz', 'Nz', 'mz','mz_zoom1','mz_zoom2', 'mz_zoom3', 'mz_zoom4', 'mz_zoom5', 'mz_zoom6', 'leptonic_recoil_m','leptonic_recoil_m_zoom1', 'leptonic_recoil_m_zoom2', 'leptonic_recoil_m_zoom3', 'leptonic_recoil_m_zoom4', 'leptonic_recoil_m_zoom5', 'leptonic_recoil_m_zoom6', 'leptonic_recoil_m_zoom7', 'leptonic_recoil_m_zoom8', 'leptonic_recoil_m_zoom9', 'leptonic_recoil_m_zoom10', 'muon_y', 'muon_pT', 'muon_E']
#variables = ["Nmu", "Nmu_plus", "Nmu_minus", 'Cz', 'Nz', 'mz','mz_zoom1','mz_zoom2', 'mz_zoom3', 'mz_zoom4', 'mz_zoom5', 'mz_zoom6', 'leptonic_recoil_m','leptonic_recoil_m_zoom1', 'leptonic_recoil_m_zoom2', 'leptonic_recoil_m_zoom3', 'muon_y', 'muon_pT', 'muon_E']
variables = ["MET_costheta", "Nmu_plus", "Nmu_minus", "Nmu", "Cz", "Nz", "mz", "mz_zoom1", 'mz_zoom2', 'mz_zoom3', 'mz_zoom4', 'mz_zoom5', 'mz_zoom6', 'mz_zoom7', "z_pt", "z_y", "z_p", "z_e", 'leptonic_recoil_m','leptonic_recoil_m_zoom1', 'leptonic_recoil_m_zoom2', 'leptonic_recoil_m_zoom3', 'leptonic_recoil_m_zoom4', 'leptonic_recoil_m_zoom5', 'leptonic_recoil_m_zoom6', 'leptonic_recoil_m_zoom7', 'leptonic_recoil_m_zoom8', 'leptonic_recoil_m_zoom9', 'leptonic_recoil_m_zoom10', 'leptonic_recoil_m_zoom11', 'leptonic_recoil_m_zoom12', 'muon_y', 'muon_pT', 'muon_p', "muon_costheta", "muon_e", "muon_m"]
###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
#selections['ZH']   = ["sel0","sel1","sel2"]
#selections['ZH_2'] = ["sel0","sel1","sel2"]
#selections['ZH']   = ["sel1"]
selections['ZH']   = ["sel0", "sel1", "sel2", "sel3", "sel4", "sel5", "sel6", "sel7", "sel8", "sel9", "sel10", "sel11", "sel12", "sel13", "sel14","sel10", "sel11", "sel12", "sel13", "sel14","sel15", "sel16", "sel17", "sel18", "sel19","sel20", "sel21", "sel22", "sel23", "sel24","sel25", "sel26", "sel27", "sel28", "sel29"]
selections['ZH_P']   = ["sel0", "sel1", "sel2", "sel3", "sel4", "sel5", "sel6", "sel7", "sel8", "sel9", "sel10", "sel11", "sel12", "sel13", "sel14","sel10", "sel11", "sel12", "sel13", "sel14","sel15", "sel16", "sel17", "sel18", "sel19","sel20", "sel21", "sel22", "sel23", "sel24","sel25", "sel26", "sel27", "sel28", "sel29"]
#selections['ZH']   = ["sel13"]
extralabel = {}
#extralabel['sel0'] = "Selection: N_{Z} = 1"
#extralabel['sel1'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV"
extralabel['sel0'] = "Selection: No Selection"
extralabel['sel1'] = "Sel.1"
extralabel['sel2'] = "Sel.2"
extralabel['sel3'] = "Sel.3"
extralabel['sel4'] = "Sel.4"
extralabel['sel5'] = "Sel.5"
extralabel['sel6'] = "Sel.6"
extralabel['sel7'] = "Sel.7"
extralabel['sel8'] = "Sel.8"
extralabel['sel9'] = "Sel.9"
extralabel['sel10'] = "Sel.10"
extralabel['sel11'] = "Sel.11"
extralabel['sel12'] = "Sel.12"
extralabel['sel13'] = "Sel.13"
extralabel['sel14'] = "Sel.14"
extralabel['sel15'] = "Sel.15"
extralabel['sel16'] = "Sel.16"
extralabel['sel17'] = "Sel.17"
extralabel['sel18'] = "Sel.18"
extralabel['sel19'] = "Sel.19"
extralabel['sel20'] = "Sel.20"
extralabel['sel21'] = "Sel.21"
extralabel['sel22'] = "Sel.22"
extralabel['sel23'] = "Sel.23"
extralabel['sel24'] = "Sel.24"
extralabel['sel25'] = "Sel.25"
extralabel['sel26'] = "Sel.26"
extralabel['sel27'] = "Sel.27"
extralabel['sel28'] = "Sel.28"
extralabel['sel29'] = "Sel.29"



#extralabel['sel1'] = "Selection: N_{Z} = 1; 73 GeV < m_{Z} < 120 GeV"
#extralabel['sel2'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 110 GeV"
#extralabel['sel3'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV"
#extralabel['sel4'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV; 10 GeV < p_{T}^Z < 70 GeV"
#extralabel['sel6'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV; 10 GeV < p_{T}^Z < 70 GeV; 120 GeV < m_{recoil} < 140 GeV"
#extralabel['sel7'] = "Selection: 8"
#extralabel['sel8'] = "Selection: 9"
#extralabel['sel9'] = "Selection: 10"
#extralabel['sel10'] = "Selection: 11"
#extralabel['sel11'] = "Selection: 12"
#extralabel['sel12'] = "Selection: 13"
#extralabel['sel13'] = "Selection: 14"
#extralabel['sel14'] = "Selection: 15"
#extralabel['sel15'] = "Selection: 16"
#extralabel['sel1'] = "Selection: N_{Z} = 1; 80 GeV < m_{Z} < 100 GeV; p_{T #muon} > 20 GeV; #theta_{#mu^{+}#mu^{-}} < 175^{#degree}"
#extralabel['sel2'] = "Selection: N_{Z} = 1; 86 GeV < m_{Z} < 96 GeV"
#extralabel['sel3'] = "Selection: N_{Z} = 1; new"

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
colors['egamma'] = ROOT.kSpring+10
colors['gagatautau'] = ROOT.kViolet+7
colors['gagamumu'] = ROOT.kBlue-8

colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['VV'] = ROOT.kGreen+3

plots = {}
plots['ZH'] = {'signal':{'nunuH':['wzp6_ee_nunuH_ecm240'],
                          'eeH':['wzp6_ee_eeH_ecm240'],
                          'tautauH':['wzp6_ee_tautauH_ecm240'],
                          'qqH':['wzp6_ee_qqH_ecm240'],
                          'mumuH':['wzp6_ee_mumuH_ecm240']},
                'backgrounds':{'gagatautau':['wzp6_gaga_tautau_60_ecm240'],
                                'gagamumu':['wzp6_gaga_mumu_60_ecm240'],
                                'egamma':['wzp6_gammae_eZ_Zmumu_ecm240', 'wzp6_egamma_eZ_Zmumu_ecm240'],
                                 'Zqq':['p8_ee_Zqq_ecm240'],
                                'WWmumu':['p8_ee_WW_mumu_ecm240'],
                                'Zll':['p8_ee_Zll_ecm240'],
                                'ZZ':['p8_ee_ZZ_ecm240']}
            }

plots['ZH_P'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
                  'backgrounds':{'gagatautau':['wzp6_gaga_tautau_60_ecm240'],
                                  'gagamumu':['wzp6_gaga_mumu_60_ecm240'],
                                  'egamma':['wzp6_gammae_eZ_Zmumu_ecm240', 'wzp6_egamma_eZ_Zmumu_ecm240'],
                                  'Zqq':['p8_ee_Zqq_ecm240'],
                                  'WWmumu':['p8_ee_WW_mumu_ecm240'],
                                  'Zll':['p8_ee_Zll_ecm240'],
                                  'ZZ':['p8_ee_ZZ_ecm240']}
            }
#plots['ZH'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
#               'backgrounds':{'WW':['p8_ee_WW_ecm240'],
#                              'ZZ':['p8_ee_ZZ_ecm240']}
#           }
#plots['ZH'] = {'signal':{'ZH':['p8_noBES_ee_ZH_ecm240']},
#                'backgrounds':{'WW':['p8_noBES_ee_WW_ecm240'],
#                                'ZZ':['p8_noBES_ee_ZZ_ecm240']}
#            }

#plots['ZH'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
#               'backgrounds':{'WW':['p8_ee_WW_mumu_ecm240'],
#                               'ZZ':['p8_ee_ZZ_ecm240']}
#            }

#plots['ZH'] = {'signal':{'ZH':['wzp6_ee_mumuH_ecm240_v2']}
#
#    }
#plots['ZH'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
#                'backgrounds':{'WW':['p8_ee_WW_mumu_ecm240'],
#                                'Zqq':['p8_ee_Zqq_ecm240'],
#                                'Zll':['p8_ee_Zll_ecm240'],
#                                'ZZ':['p8_ee_ZZ_ecm240']}
#            }
#plots['ZH_2'] = {'signal':{'ZH':['p8_ee_ZH_ecm240']},
#                 'backgrounds':{'VV':['p8_ee_WW_ecm240','p8_ee_ZZ_ecm240']}
#             }

legend = {}

legend['mumuH'] = 'Z(#mu^{-}#mu^{+})H'
legend['tautauH'] = 'Z(#tau^{-}#tau^{+})H'
legend['qqH'] = 'Z(q#bar{q})H'
legend['eeH'] = 'Z(e^{-}e^{+})H'
legend['nunuH'] = 'Z(#nu#bar{#nu})H'
legend['Zqq'] = 'Z#rightarrow q#bar{q}'
legend['Zll'] = 'Z#rightarrow l#bar{l}'
legend['egamma'] = 'e#gamma'
legend['WWmumu'] = 'W^{+}(#bar{#nu}#mu^{+})W^{-}(#nu#mu^{-})'
legend['gagamumu'] = '#gamma#gamma#mu^{-}#mu^{+}'
legend['gagatautau'] = '#gamma#gamma#tau^{-}#tau^{+}'


legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
legend['VV'] = 'VV boson'





#python examples/FCCee/higgs/mH-recoil/mumu/preSel.py

from config.common_defaults import deffccdicts
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021/IDEA/"
#basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/fcc_tmp/"

outdir="outputs/FCCee/higgs/mH-recoil/mumu/"

import multiprocessing
NUM_CPUS = int(multiprocessing.cpu_count()-2)

#process_list=['p8_ee_ZH_ecm240']
process_list=['p8_ee_ZH_ecm240','wzp6_gaga_mumu_60_ecm240','wzp6_gaga_tautau_60_ecm240','wzp6_gammae_eZ_Zmumu_ecm240','wzp6_egamma_eZ_Zmumu_ecm240','p8_ee_Zqq_ecm240','p8_ee_Zll_ecm240','p8_ee_ZZ_ecm240','p8_ee_WW_mumu_ecm240','wzp6_ee_mumuH_ecm240','wzp6_ee_tautauH_ecm240','wzp6_ee_qqH_ecm240','wzp6_ee_nunuH_ecm240','wzp6_ee_eeH_ecm240']
fraction=1.0

import config.runDataFrame as rdf
myana=rdf.runDataFrame(basedir,process_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction,outDir=outdir)

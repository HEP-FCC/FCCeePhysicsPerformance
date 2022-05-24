#!/bin/bash
cd /afs/cern.ch/work/l/lia/private/FCC/MVA/FCCAnalyses
source setup.sh
cd /afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/dataframe
source localSetup.sh
cd /afs/cern.ch/work/l/lia/private/FCC/MVA/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/FCCAnalyses-config/mumu

python plot_xgb.py --Vars=normal

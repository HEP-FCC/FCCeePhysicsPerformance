import ROOT
import sys, os, argparse
import uproot
import awkward as ak
import json
import numpy as np
import matplotlib.pyplot as plt
from particle import literals as lp
import pandas as pd
import glob

#Local code
#from userConfig import loc, mode, train_vars, train_vars_vtx, mode_names
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut


#print ("----> Load cxx analyzers from libFCCAnalyses... ",)
#ROOT.gSystem.Load("libedm4hep")
#ROOT.gSystem.Load("libpodio")
#ROOT.gSystem.Load("libFCCAnalyses")
#ROOT.gSystem.Load("libFCCAnalysesHiggs")
#ROOT.gErrorIgnoreLevel = ROOT.kFatal
##Is this still needed?? 01/04/2022 still to be the case
#_edm  = ROOT.edm4hep.ReconstructedParticleData()
#_pod  = ROOT.podio.ObjectID()
#_fcc  = ROOT.dummyLoader
#_higgs  = ROOT.dummyLoaderHiggs
#print ('edm4hep  ',_edm)
#print ('podio    ',_pod)
#print ('fccana   ',_fcc)
#print ('higgs   ',_higgs)

def run(mode):

    #Master dataframe to store to CSV
    df = pd.DataFrame()

    if (mode=="eeZ"):
      path_egamma = f"{loc.TRAIN}/{mode_names['egamma']}"
      path_gammae = f"{loc.TRAIN}/{mode_names['gammae']}"
      files = glob.glob(f"{path_egamma}/*.root") + glob.glob(f"{path_gammae}/*.root")
    else:
      #Location of MC files
      path = f"{loc.TRAIN}/{mode_names[mode]}"  
      #List of all sub-files in the path
      files = glob.glob(f"{path}/*.root")
    df_sub = {}

    #Loop over MC files, and make dataframe, appending them into the master df
        #print(f"Loading ROOT file {f}")
    file = uproot.open(files[0])
    tree = file['events']

        #Load event-level vars
        #print("Converting to awkward array")
    vars_list = train_vars.copy()
    #print(vars_list)
    #df_sub[f] = tree.arrays(library="pd", how="zip", filter_name=train_vars)
    
    df = pd.concat((ut.get_df(f, train_vars.copy()) for f in files), ignore_index=True)
    #df = df.sample(200000)
    #Add to the total file
    #df = df.concat(df_sub[f])

    #Save to pickle
    print("Writing output to pickle file")
    ut.create_dir(loc.PKL)
    print(loc.PKL)
    outfile = f"{loc.PKL}/{mode}.pkl"
    df.to_pickle(outfile)

def main():
    parser = argparse.ArgumentParser(description='Process mumuH, WWmumu, ZZ, Zll,eeZ MC to make reduced files for xgboost training')
    parser.add_argument("--Mode", choices=["mumuH","ZZ","WWmumu","Zll","eeZ"],required=True,help="Decay mode")
    args = parser.parse_args()

    run(args.Mode)

if __name__ == '__main__':
    main()

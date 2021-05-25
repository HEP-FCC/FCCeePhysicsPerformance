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
from userConfig import loc, mode, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut

def run(mode):

    #Master dataframe to store to CSV
    df = pd.DataFrame()

    #Location of MC files
    path = f"{loc.TRAIN}/{mode_names[mode]}"

    #List of all sub-files in the path
    files = glob.glob(f"{path}/*.root")
    if(mode=="uds"):
        #Remove zombie files
        for f in files:
            if "flat_chunk_68" in f:
                files.remove(f)

    df_sub = {}

    #Loop over MC files, and make dataframe, appending them into the master df
    for f in files:

        print(f"Loading ROOT file {f}")
        file_name = f"flat_ee_{mode}"
        file = uproot.open(f)
        tree = file['events']

        #Load event-level vars
        print("Converting to awkward array")
        vars_list = train_vars_vtx.copy()
        vars_list.append("TrueTau23PiBc_vertex")
        vars_list.append("TrueTau23PiBu_vertex")
        df_sub[f] = tree.arrays(library="pd", how="zip", filter_name=train_vars_vtx)

        #Add to the total file
        df = df.append(df_sub[f])

    #Save to pickle
    print("Writing output to pickle file")
    ut.create_dir(loc.PKL)
    outfile = f"{loc.PKL}/{mode}.pkl"
    df.to_pickle(outfile)

def main():
    parser = argparse.ArgumentParser(description='Process inclusive Z -> uds / cc / bb / B -> tau nu MC to make reduced files for xgboost training')
    parser.add_argument("--Mode", choices=["uds","cc","bb","Bu2TauNu","Bc2TauNu"],required=True,help="Decay mode")
    args = parser.parse_args()

    run(args.Mode)

if __name__ == '__main__':
    main()

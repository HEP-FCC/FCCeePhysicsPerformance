import sys, os, argparse
import uproot #uproot4 as uproot
import awkward as ak #awkward1 as ak
import json
import numpy as np
import matplotlib.pyplot as plt
from particle import literals as lp
import pandas as pd
from root_pandas import to_root

#Local code
from userConfig import loc, mode
import kinematics_flat
import plotting
import utils as ut


from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def run(Z_type):

    #Load the MC
    print("Loading ROOT file")
    file_name = f"p8_ee_Z{Z_type}_ecm91"
    file = uproot.open(f"{loc.IN}/{mode}/{file_name}.root")
    tree = file['events']

    #Load event-level vars
    print("Converting to awkward array")
    events = tree.arrays(filter_name="EVT_*")

    #Hemisphere energies
    for hem in ["0","1"]:
        events[f"EVT_thrutshemis{hem}_e"] = events[f"EVT_thrutshemis{hem}_echarged"] + events[f"EVT_thrutshemis{hem}_eneutral"]

    #Total energy (sum of both hemispheres)
    events["EVT_e"] = events["EVT_thrutshemis0_e"] + events["EVT_thrutshemis1_e"]

    #Min and max hemisphere energies per-event
    events["EVT_thrutshemis_e_min"] = np.minimum(events["EVT_thrutshemis0_e"],events["EVT_thrutshemis1_e"])
    events["EVT_thrutshemis_e_max"] = np.maximum(events["EVT_thrutshemis0_e"],events["EVT_thrutshemis1_e"])

    #Difference in energy between hemispheres (max - min so always positive)
    events["EVT_thrutshemis_e_diff"] = events["EVT_thrutshemis_e_max"] - events["EVT_thrutshemis_e_min"]

    '''
    fig, ax = plt.subplots(figsize=(9,9))
    plt.hist(events["EVT_thrutshemis_e_min"],bins=50,range=(0,60),color="crimson",histtype='step',linewidth=2,label="Lower energy hemisphere per-event")
    plt.hist(events["EVT_thrutshemis_e_max"],bins=50,range=(0,60),color="dodgerblue",histtype='step',linewidth=2,label="Higher energy hemisphere per-event")
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(0,60)
    plt.axvline(lp.Z_0.mass/2000., color='k',linestyle='--',label="$m(Z^0)/2$")
    plt.xlabel("Hemisphere energy [GeV]",fontsize=30)
    plt.legend(fontsize=18, loc="upper left")
    ut.create_dir(loc.PLOTS)
    fig.savefig(f"{loc.PLOTS}/inclusive_Z{Z_type}_min_max_hemisphere_E.pdf")

    fig, ax = plt.subplots(figsize=(9,9))
    plt.hist(events["EVT_thrutshemis_e_diff"],bins=30,range=(0,50),color="k",histtype='step',linewidth=2)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(0,50)
    plt.xlabel("Hemisphere energy difference [GeV]",fontsize=30)
    fig.savefig(f"{loc.PLOTS}/inclusive_Z{Z_type}_diff_hemisphere_E.pdf")
    '''

    #Look at charged and neutral multiplicities in the two hemispheres

    #Events where hemisphere 0 is the minimum energy
    events_hem0_min_cut = events["EVT_thrutshemis0_e"] == events["EVT_thrutshemis_e_min"]
    events_hem0_min = events[events_hem0_min_cut]

    #Events where hemisphere 1 is the minimum energy
    events_hem1_min_cut = events["EVT_thrutshemis1_e"] == events["EVT_thrutshemis_e_min"]
    events_hem1_min = events[events_hem1_min_cut]

    #Get the charged and neutral energy and multiplicity
    for ptype in ["charged","neutral"]:
        for var in ["n","e"]:
            events_hem0_min[f"{var}{ptype}_min"] = events_hem0_min[f"EVT_thrutshemis0_{var}{ptype}"]
            events_hem0_min[f"{var}{ptype}_max"] = events_hem0_min[f"EVT_thrutshemis1_{var}{ptype}"]

            events_hem1_min[f"{var}{ptype}_min"] = events_hem1_min[f"EVT_thrutshemis1_{var}{ptype}"]
            events_hem1_min[f"{var}{ptype}_max"] = events_hem1_min[f"EVT_thrutshemis0_{var}{ptype}"]

    #Recombine
    events = ak.concatenate([events_hem0_min,events_hem1_min],axis=0)

    #Axis ranges, titles, and bins
    '''
    plot_config = {"echarged": [0,50,"Charged energy [GeV]",50],
                   "eneutral": [0,40,"Neutral energy [GeV]",50],
                   "ncharged": [0,25,"Charged multiplicity",25],
                   "nneutral": [0,20,"Neutral multiplicity",20]
                   }

    for p in plot_config:

        fig, ax = plt.subplots(figsize=(9,9))
        plt.hist(events[f"{p}_min"],bins=plot_config[p][3],range=(plot_config[p][0],plot_config[p][1]),color="crimson",histtype='step',linewidth=2,label="Lower energy hemisphere per-event")
        plt.hist(events[f"{p}_max"],bins=plot_config[p][3],range=(plot_config[p][0],plot_config[p][1]),color="dodgerblue",histtype='step',linewidth=2,label="Higher energy hemisphere per-event")
        ax.tick_params(axis='both', which='major', labelsize=25)
        plt.xlim(plot_config[p][0],plot_config[p][1])
        plt.xlabel(plot_config[p][2],fontsize=30)
        ymin,ymax = plt.ylim()
        plt.ylim(0,1.15*ymax)
        plt.legend(fontsize=18, loc="upper left")
        fig.savefig(f"{loc.PLOTS}/inclusive_Z{Z_type}_min_max_hemisphere_{p}.pdf")
    '''

    df = pd.DataFrame()
    persist_vars = ["EVT_e", #Total event visible energy
                    "EVT_thrutshemis_e_min", #Lowest energy hemisphere in event
                    "EVT_thrutshemis_e_max", #Highest energy hemisphere in event
                    "EVT_thrutshemis0_e", #costheta < 0 hemisphere energy
                    "EVT_thrutshemis1_e", #costheta > 0 hemisphere energy
                    ]

    for var in ["e","n"]:
        for ptype in ["charged","neutral"]:
            for m in ["min","max"]:
                persist_vars.append(f"{var}{ptype}_{m}")

    for var in persist_vars:
        df[var] = events[var].tolist()

    #Save to CSV
    print("Writing output to CSV")
    ut.create_dir(loc.CSV)
    #df.to_csv(f"{loc.CSV}/inclusive_Z{Z_type}.csv")

    outfile = open(f"{loc.CSV}/inclusive_Z{Z_type}.csv", "wb")
    df.to_csv(outfile)
    outfile.close()

    '''
    #Write to ROOT file too
    print("Writing output to ROOT file")
    ut.create_dir(loc.ROOTFILES)
    root_file_name = f"{loc.ROOTFILES}/inclusive_Z{Z_type}.root"
    if os.path.exists(root_file_name):
        os.remove(root_file_name)
    df.to_root(root_file_name,"events")
    '''


def main():
    parser = argparse.ArgumentParser(description='Process inclusive Z -> uds / cc / bb MC to make reduced ROOT file for further studies')
    parser.add_argument("--Z_type", choices=["uds","cc","bb"],required=True,help="Z decay mode")
    args = parser.parse_args()

    run(args.Z_type)

if __name__ == '__main__':
    main()

## How to simulate electrons with particle gun and evaluate the tracking resolution

## Which code to use

Use the IDEA code in https://github.com/lialavezzi/IDEADetectorSIM.git master branch (I did the pull request for the official repository, not yet accepted). There are some modifications w.r.t. the official repo.
The modifications I made are:
<ul>
<li> in converter/convertHits.cc: added the conversion of MC primary tracks to EDM4Hep. </li>
<li> in install_standalone.sh: changed the wget file location and set the ROME revision to download, to fix installation problems. </li>
<li> in converter/convertTracks.cc fixed bug related to “skipped” vector, added the exception catching </li>
</ul>

## How to prepare the code
<ul>
<li> Download the code from git https://github.com/lialavezzi/IDEADetectorSIM.git </li>

<li> Modify by hand the file: $STANDALONE_INSTALL_DIR/IDEADetectorSIM/simulation/g4GMC/src/GMCG4EventAction.cc adding the line marked with asterisks here:
<code>
for (G4int i=0;i<n_trajectories;i++) {    
      G4VTrajectory *tmpTrk = (*trajectoryContainer)[i];
      *** if(tmpTrk->GetParentID() != 0) continue; ***                 
      cnttracks.push_back( new GMCG4Particle( tmpTrk->GetTrackID(), tmpTrk->GetParentID(), 
      ...
</code>
</li>
  
<li> Perform the usual installation with install_standalone.sh (instructions are in the README) </li>
  
<li> The code for our studies is in: DetectorPerformanceStudies/IDEAPerformanceStudies/electrons/ where there are two directories and a file:
  <ul>
    <li> generate_mac/ </br>
     It contains the bash script generate_mac.sh to generate all the .mac files to shoot each particle we need. 
     If you open it, you find the section SETTINGS where you might need to make changes:
  <code>
      nevts = number of events 
      pdg=’e’ or ‘pi’ for the electrons or negative pions 
      macdir=/path_where_to_put_the_mac_files. 
  </code>
  If you installed the IDEA code, then the SIM_INSTAL_DIR environmental is set and the mac files are put directly in the right position 
  <code>
    ########################## SETTINGS
    nevt=10000
    pdg='e'
    macdir=$SIM_INSTAL_DIR/g4mac/mymac
    ##########################
  </code>
  </li>  
    
  <li> analysis/ </br>
  analysis/ contains the python script analyze.py.
  </li> 
  
  <li> run_production.sh
  It is the bash script that runs the simulation and reconstruction: it needs to be copied in  $SIM_INSTAL_DIR/.     Also here there is a section SETTINGS to set pdg, list of theta and ptot:
  <code>
  #################### SETTINGS
  pdg='e'
  l_theta=(10 30 50 70 89)
  l_ptot=(0.5 1 2 5 10 20 50 100)
  ####################
  </code> 
  </li>
  </ul>
</li>
</ul>

## How to run the simulation 
Just run generate_mac.sh by making it executable and launching it:
<code>
chmod u+x generate_mac.sh
./generate_mac.sh
</code>
Then run the simulation from $SIM_INSTAL_DIR, with run_production.sh, making it executable:
<code>
chmod u+x  run_production.sh
./run_production.sh
</code>
It will create a set of directories in $SIM_OUTPUT_DIR and will fill them. As it is now, to save space, it deletes everything beside: conv/track and conv/mctrack which are what we need to have the plots.

## Hot to run the analysis 
Use the python script analyze.py. </br>
Here check and modify as you need the SETTINGS; basepath should be fine, it is the place where your track/ and mctrack/ directories are; change pdg, l_theta and l_ptot depending on your simulation:
  <code>
  ###################################################
                  SETTINGS 
  basepath = os.environ['SIM_OUTPUT_DIR']+"/conv/"
  pdg='e'
  l_theta = [10, 30, 50, 70, 89]
  l_ptot  = [0.5, 1, 2, 5, 10] 
  ###################################################
  </code>
To run it just use: 
  <code>
  python analyze.py
  </code>
It creates a plot g1.png with the graphs as the ones from CLD and an output.root file with all the residual histograms.

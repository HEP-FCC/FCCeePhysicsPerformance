.# HNL Project

- [HNL Project](#hnl-project)
  * [Welcome](#welcome)
  * [Setup Instructions](#setup-instructions)
  * [Analysis Files](#analysis-files)

## Welcome
This is the code used for the project titled: [Towards Vertexing Studies of Heavy Neutral Leptons with the Future Circular Collider at CERN](http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-444997) by Rohini Sengupta, defended in June 2021.

## Setup Instructions

### setup once, in the beginning:
```
bash
git clone https://github.com/jalimena/FCCAnalyses.git #this is a common FCC analyses repository, but I needed to add one thing there
cd FCCAnalyses
git checkout inclusiveDecay #this git command checks out the specific branch where I made the change in FCCAnalyses
source ./setup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ../..

git clone https://github.com/jalimena/FCCeePhysicsPerformance.git #our main analysis code for HNLs and ALPs lives here
cd FCCeePhysicsPerformance/case-studies/flavour/dataframe
source ./localSetup.sh
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install -DFCCANALYSES_INCLUDE_PATH=<Your_Complete_Path_to>/FCCAnalyses/install/include/FCCAnalyses/
make install
cd ../../../BSM/LLP/DisplacedHNL/
```

### you will need to run these setup commands every time you log in:
```
bash
cd FCCAnalyses
source ./setup.sh
cd ../FCCeePhysicsPerformance/case-studies/flavour/dataframe
source ./localSetup.sh
cd ../../BSM/LLP/DisplacedHNL/
```

In the folder [HNL_sample_creation](HNL_sample_creation) you can find a readme file that explains how to create the samples used in this project. 

## Analysis Files
This concerns the analysis files [gen_distributions_delphes.py](gen_distributions_delphes.py) and [analysis_HNL_read.py](analysis_HNL_read.py) for HNL analysis at the FCC-ee.

To run gen_distributions_delphes.py a standalone setup created by Suchita Kulkarni (suchita.kulkarni@cern.ch) has to be setup first.
The setup requires python 3.7 (or higher), Root (version 6.x), PYTHIA8, DELPHES with FastJet and MadGraph.
The input for the gen_distributions_delphes.py analysis file is the HNL sample created by running the wrapper (mg5 + pythia8 + delphes)
from the standalone framework.

The gen_distributions_delphes.py file is used to validate and analyze the HNL sample produced with standalone delphes (not the edm4hep format). It validates the sample by checking the time
distribution and the transverese displacement of the sample. The analysis provides studies on the kinematics of the HNL and its
daughter particles.

The analysis_HNL_read.py file is an adaptation from the original read_EDM4HEP.py file which provides a basic example showing how to read
different objects from the EDM4HEP files and how to access and store some simple variables in an output ntuple. This is the main script to use with the edm4hep samples. The analysis_HNL_read.py
file is specific for the study of HNLs. It presents a possibility to validate created HNL samples by checking the lifetimes and transverse
displacements of the samples and also presents the starting point for HNL vertex analysis.

To run the analysis_HNL_read.py file the FCC framework has to be setup following the instructions from the official FCCAnalysis page
from GitHub. The repositories of interest are the FCCAnalysis and the FCCeePhysicsPerformance. It is very important to make sure that the
sourcing is correct. For FCCAnalyses, the sourcing should point to the personal FCCAnalyses and not the central version. FCCAnalyses also
needs to be  linked against FCCeePhysicsPerformane, instructions for which can be found on the respective GitHub pages.


### run the analysis:
```
cd FCCeePhysicsPerformance/case-studies/BSM/LLP/DisplacedHNL
python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_50GeV_1p41e-6Ve.root #for one example signal point
./runAnalysis.sh #for all points i've generated so far

python3 finalSel.py #to run the "final selection"
python3 doPlots.py plots.py #to create plots
```
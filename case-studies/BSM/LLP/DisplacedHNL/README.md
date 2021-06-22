# HNL Project

- [HNL Project](#hnl-project)
  * [Welcome](#welcome)
  * [Setup Instructions](#setup-instructions)
  * [Analysis Files](#analysis-files)

## Welcome
This is the code used for the project titled: [Towards Vertexing Studies of Heavy Neutral Leptons with the Future Circular Collider at CERN](http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-444997) by Rohini Sengupta, defended in June 2021.

## Setup Instructions
In the folder [HNL_sample_creation](HNL_sample_creation) you can find a readme file that explains how to create the samples used in this project. 

## Analysis Files
This concerns the analysis files [gen_distributions_delphes.py](gen_distributions_delphes.py) and [analysis_HNL_read.py](analysis_HNL_read.py) for HNL analysis at the FCC-ee.

To run gen_distributions_delphes.py a standalone setup created by Suchita Kulkarni (suchita.kulkarni@cern.ch) has to be setup first.
The setup requires python 3.7 (or higher), Root (version 6.x), PYTHIA8, DELPHES with FastJet and MadGraph.
The input for the gen_distributions_delphes.py analysis file is the HNL sample created by running the wrapper (mg5 + pythia8 + delphes)
from the standalone framework.

The gen_distributions_delphes.py file is used to validate and analyze the HNL sample. It validates the sample by checking the time
distribution and the transverese displacement of the sample. The analysis provides studies on the kinematics of the HNL and its
daughter particles.

The analysis_HNL_read.py file is an adaptation from the original read_EDM4HEP.py file which provides a basic example showing how to read
different objects from the EDM4HEP files and how to access and store some simple variables in an output ntuple. The analysis_HNL_read.py
file is specific for the study of HNLs. It presents a possibility to validate created HNL samples by checking the lifetimes and transverse
displacements of the samples and also presents the starting point for HNL vertex analysis.

To run the analysis_HNL_read.py file the FCC framework has to be setup following the instructions from the official FCCAnalysis page
from GitHub. The repositories of interest are the FCCAnalysis and the FCCeePhysicsPerformance. It is very important to make sure that the
sourcing is correct. For FCCAnalyses, the sourcing should point to the personal FCCAnalyses and not the central version. FCCAnalyses also
needs to be  linked against FCCeePhysicsPerformane, instructions for which can be found on the respective GitHub pages.

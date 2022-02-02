Author: Suchita Kulkarni
Contact: suchita.kulkarni@cern.ch
This folder will allow you to create your own madgraph sample for heavy neutral lepton decaying to e j j final state.

To create a sample where the HNL decays to e e nu final state change the following lines in mg5_proc_card.dat

generate e+ e- > ve n1, (n1 > e j j)
add process e+ e- > ve~ n1, (n1 > e j j)

to

generate e+ e- > ve n1, (n1 > e e nu)
add process e+ e- > ve~ n1, (n1 > e e nu)

First create the LHE file. To do this, you'll need to download the latest version of madgraph (http://madgraph.phys.ucl.ac.be/) and make sure you're using python 3.7 or greater. For the Snowmass study, we're using MadGraph5 v3.2.0. Copy the Madgraph tarball to your local area on lxplus:

```
scp MG5_aMC_v3.2.0.tar.gz username@lxplus7.cern.ch:/afs_path/yadda_yadda/
```

Then ssh to lxplus and unzip the tarball (tar -xf MG5_aMC_v3.2.0.tar.gz). If you're going to generate ALPs, copy the ALP_NLO_UFO/ directory into MG5_aMC_v3_2_0/models.

Then you can do:

```
./bin/mg5_aMC mg5_proc_card.dat
```
to create the LHE file, where mg5_proc_card.dat is the madgraph proc card you are interested in generating.


The resulting events will be stored in  HNL_ljj/Events/run_01/unweighted_events.lhe.gz file.

Unzip it (gunzip unweighted_events.lhe.gz) and give the path to HNL_pythia.cmnd file to generate the delphes root file.

You also need to grab the latest official Delphes card and edm4hep tcl file:
```
#cd to one directory up from FCCeePhysicsPerformance/
git clone https://github.com/HEP-FCC/FCC-config.git
cd FCC-config/
git checkout spring2021
cd ../FCCeePhysicsPerformance/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/
```

To create delphes root file you need to do the following on your command line:

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
DelphesPythia8_EDM4HEP ../../../../../../FCC-config/FCCee/Delphes/card_IDEA.tcl ../../../../../../FCC-config/FCCee/Delphes/edm4hep_IDEA.tcl HNL_eenu_pythia.cmnd HNL_ejj.root
```

the resulting HNL_ejj.root is your EDM sample.

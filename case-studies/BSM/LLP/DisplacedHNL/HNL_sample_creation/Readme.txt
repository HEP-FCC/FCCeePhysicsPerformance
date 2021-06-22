Author: Suchita Kulkarni
Contact: suchita.kulkarni@cern.ch
This folder will allow you to create your own madgraph sample for heavy neutral lepton decaying to e j j final state.

To create a sample where the HNL decays to e e nu final state change the following lines in mg5_proc_card.dat

generate e+ e- > ve n1, (n1 > e j j)
add process e+ e- > ve~ n1, (n1 > e j j)

to

generate e+ e- > ve n1, (n1 > e e nu)
add process e+ e- > ve~ n1, (n1 > e e nu)

The resulting events will be stored in  HNL_ljj/Events/run_01/unweighted_events.lhe.gz file.

Unzip it and give the path to HNL_pythia.cmnd file to generate the delphes root file.

To create delphes root file you need to do the following on your command line:

source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
DelphesPythia8_EDM4HEP $DELPHES_DIR/cards/delphes_card_IDEAtrkCov.tcl edm4hep_output_config.tcl HNL_pythia.cmnd HNL_ejj.root

the resulting HNL_ejj.root is your EDM sample.

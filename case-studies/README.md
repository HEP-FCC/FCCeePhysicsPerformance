Case-Studies
=============

Each case study should eventually use commonly produced events in the common data model EDM4Hep. To run over those common samples, an efficient analysis framework has been developed [FCCAnalyses](https://github.com/HEP-FCC/FCCAnalyses/tree/master/). For each analyses, it is higly recommended to store and maintain the four ```FCCAnalyses``` python configuration files in a directory called ```FCCAnalyses-config``` with a possible directory structure inside in case several configurations are needed for various channels like for example ```case-studies/higgs/mH-recoil/FCCAnalyses-config/ee/``` and ```case-studies/higgs/mH-recoil/FCCAnalyses-config/mumu/```.


To run the case-studies analyses from this repository and using the common installed FCCAnalyses libraries, the following has to be done:

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
export PYTHONPATH=/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/fccanalyses-0.2.0pre02-6kok72w65toi2vvgedijdoqnd4hgg2wu/python:$PYTHONPATH
export PATH=/cvmfs/sw.hsf.org/spackages/linux-centos7-broadwell/gcc-8.3.0/fccanalyses-0.2.0pre02-6kok72w65toi2vvgedijdoqnd4hgg2wu/python/bin:$PATH
```

If custom functions/algorithms have been developed in FCCAnalyses, we need to point to the proper installation

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
export PYTHONPATH=YOURFCCANALYSES:$PYTHONPATH
export LD_LIBRARY_PATH=YOURFCCANALYSES/install/lib:$LD_LIBRARY_PATH
export ROOT_INCLUDE_PATH=YOURFCCANALYSES/install/include:$ROOT_INCLUDE_PATH
```

where ```YOURFCCANALYSES``` is where you have compiled your own FCCAnalyses.
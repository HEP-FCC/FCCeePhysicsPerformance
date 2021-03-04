If not already done, setup the common SW
```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

then source localSetup

```
source ./localSetup.sh
```

and compile


```
mkdir build install
cd build/
cmake .. -DCMAKE_INSTALL_PREFIX=../install -DFCCANALYSES_INCLUDE_PATH=<PATH_FCCANALYSES_INSTALL_INCLUDE_DIR>
make install
cd ..
```

where ```PATH_FCCANALYSES_INSTALL_INCLUDE_DIR``` points to the install include dir of FCCAnalyes. For example ```/afs/cern.ch/user/h/helsens/FCCsoft/HEP-FCC/FCCAnalyses/install/include/FCCAnalyses```.

To find a cvmfs version, use ```spack```:
```
spack find  --paths fccanalyses
```

and choose for example, ```/cvmfs/sw.hsf.org/spackages/linux-centos7-x86_64/gcc-8.3.0/fccanalyses-0.3.0-av3c7xyuiyuxighdswldo6ut7wspgnmr/include/FCCAnalyses```


Then in the ```analysis.py``` you need to add 

```
ROOT.gSystem.Load("libFCCAnalysesHiggs")
_higgs  = ROOT.dummyLoaderHiggs
```

The last line is needed to be able so that we can load all the analysers in the ```.Define```

Setup FCCAnalyses in ```master``` branch (need for ENV VAR LOCALFCCANALYSES)
```
source ./setup.sh
```

then come back in 
```
FCCeePhysicsPerformance/case-studies/flavour/dataframe
```

source localSetup

```
source ./localSetup.sh
```

```
mkdir build install
cd build/
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd ..
```

Then in the ```analysis.py``` you need to add 

```
ROOT.gSystem.Load("libFCCAnalysesFlavour")
_bs  = ROOT.dummyLoaderFlavour
```

The last line is needed to be able so that we can load all the analysers in the ```.Define```

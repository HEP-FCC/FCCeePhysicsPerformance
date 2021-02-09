# Common flavour tools

First thing to always do, if not already done, setup the common:

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

Then first time using the common flavour tools, we need to install some extra packages locally that are not yet available in the common software stack.
To do so, run the install script only once, with ```LOCALPATH``` being written in absolute way, like ```/afs/cern.ch/user/x/xyz/FCCsoft/FCCeePhysicsPerformance/case-studies/flavour/tools/localPythonTools```


```
source ./install.sh LOCALPATH
```


When reconnecting on a fresh shell, you do not need to install the extra packages again, just setup the path correctly (again with ```LOCALPATH``` written as absolute like ```/afs/cern.ch/user/x/xyz/FCCsoft/FCCeePhysicsPerformance/case-studies/flavour/tools/localPythonTools```):

```
source ./localSetup.sh LOCALPATH
```



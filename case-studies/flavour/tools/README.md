# Common flavour tools

First thing to always do, if not already done, setup the common:

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

Then first time using the common flavour tools, we need to install some extra packages locally that are not yet available in the common software stack.
To do so, run the install script only once:

```
source ./install.sh LOCALPATH
```

Then when reconnecting, you do not need to install the extra packages, but just setup the path correctly:

```
source ./localSetup.sh LOCALPATH
```

Then we need to setup the local variables for the tools.


## Example analyzers for vertex resolutions

- Contact and questions : C. Helsens, E. Perez 

- Some details and results: see [our talk at the FCC-ee topical meeting on vertexing, Feb 10, 2021](https://indico.cern.ch/event/1003610/contributions/4214580/attachments/2187832/3696984/2021_02_10_VertexResolutions.pdf)

- Examples considered :
  - Bs to JPsi(mumu) Phi(KK)
    - example file:  /eos/experiment/fcc/ee/examples/lowerTriangle/p8_ecm91GeV_Zbb_EvtGen_Bs2JpsiPhi_IDEAtrkCov.root
    - to produce the ntuple: [`analysis_Bs2JPsiPhi.py`](analysis_Bs2JPsiPhi.py)
    - plotting macro: [`plots_Bs2JsiPhi.x`](plots_Bs2JsiPhi.x)
  - Bc to tau(3pi nu) nu
    - to produce the ntuple: [`analysis_B2TauNu.py`](analysis_B2TauNu.py)
    - plotting script: [`plots_B2TauNu.py`](plots_B2TauNu.py)
  - Bs to Ds(KKPi) K
    - example file:  /eos/experiment/fcc/ee/examples/lowerTriangle/p8_ecm91GeV_Zbb_EvtGen_Bs2DsK_IDEAtrkCov.root
    - to produce the ntuple: [`analysis_Bs2DsK.py`](analysis_Bs2DsK.py)
    - plotting macro: [`plots_Bs2DsK.x`](plots_Bs2DsK.x)

### Setup

Setup: see [case-studies/flavour/dataframe](https://github.com/HEP-FCC/FCCeePhysicsPerformance/tree/master/case-studies/flavour/dataframe) and follow the recipe in the README
- the code needed by the analyzers is in ```case-studies/flavour/dataframe/analyzers```, see [`Bs2JpsiPhi.cc`](../dataframe/Bs2JpsiPhi.cc) and [`Bs2DsK.cc`](../dataframe/Bs2DsK.cc)
- the recipe compiles the code and creates the library libFCCAnalysesFlavour
- come back to case-studies/flavour/VertexExamples and run e.g. :
 ```markdown
python analysis_Bs2JPsiPhi.py  /eos/experiment/fcc/ee/examples/lowerTriangle/p8_ecm91GeV_Zbb_EvtGen_Bs2JpsiPhi_IDEAtrkCov.root
```

### Production of Delphes samples with a customized tracker or beam-pipe

- for example: change the radius of the beam-pipe, the radii of the VXD layers, the thickness of the pipe/layers, the single-hit resolution
- see the [recipe here](https://github.com/HEP-FCC/FCCeePhysicsPerformance/tree/master/General#make-simple-changes-to-the-tracker-or-beam-pipe-description-in-delphes)


### Short description of the configuration files

#### Bs2JpsiPhi, BtoTau 

The two configuration files are very similar. See detailed comments inside [`analysis_Bs2JPsiPhi.py`](analysis_Bs2JPsiPhi.py)

#### Bs2DsK

The first part, that reconstructs the decay vertex of the Ds, is very similar to what is done for Bs2JpsiPhi.
The second part is the reconstruction of the Bs decay vertex. The reconstruction method is explained in the [talk given at the topical meeting on vertexing of Feb 2021](https://indico.cern.ch/event/1003610/contributions/4214580/attachments/2187832/3696984/2021_02_10_VertexResolutions.pdf).








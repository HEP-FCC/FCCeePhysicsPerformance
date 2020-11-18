# General information

Rather random for the while...

### Table of Contents

1. [CLD paper](#cld-paper)
2. [Common event samples](#common-event-samples)
3. [Vertexing and flavour tagging](#vertexing-and-flavour-tagging)
4. [Producing five-parameter tracks with the Delphes interface](#producing-five-parameter-tracks-with-the-delphes-interface)
5. [Jet algorithms in the Delphes interface](#jet-algorithms-in-the-delphes-interface)
6. [Making particle combinations with awkward arrays](#making-particle-combinations-with-awkward-arrays)
7. [Generating events](#generating-events)
8. [Monte-Carlo programs](#monte-carlo-programs)

### CLD paper
The [CLD performance paper on arXiv](https://arxiv.org/abs/1911.12230)

### Common event samples

Some samples (ZH, ZZ and WW, at sqrts = 240 GeV) have been produced (Sep 2020) for the Snowmass Software tutorial.
The events were simulated with Delphes, with the "IDEA\_TrkCov" card.
They are on EOS at CERN, details can be found [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_v02.php).
 

### Vertexing and flavour tagging
- Description of the [LCFIPlus algorithm](https://arxiv.org/pdf/1506.08371.pdf) used for the CLD studies
  - [LCFIPlus in GitHub](https://github.com/lcfiplus/LCFIPlus)
- [Decay Chain Fitting with a Kalman Filter](https://arxiv.org/abs/physics/0503191) W. D. Hulsbergen, Nucl.Instrum.Meth.A 552 (2005) 566
- see also the work done in the context of the [Hcc case study](../case-studies/higgs/hcc)
- [Talk from Clement Helsens, Oct 19, 2020](https://indico.cern.ch/event/965346/contributions/4062989/attachments/2125687/3578824/vertexing.pdf)

### Producing five-parameter tracks with the Delphes interface

- Recent versions of Delphes offer a rather detailed modelling of the tracks via the [TrackCovariance Delphes module](https://github.com/delphes/delphes/blob/master/modules/TrackCovariance.cc), developed from a code by Franco Bedeschi. The module, in the input card, must contain a description of the tracker, see for example [the delphes_card_IDEAtrkCov.tcl](https://github.com/delphes/delphes/blob/master/cards/delphes_card_IDEAtrkCov.tcl).
(Try to give more detail here about the geometry description). This produces five-parameter tracks - i.e., including the transverse and longitudinal impact parameters - with their covariance matrix.

- In FCCSW: in order to save the 5-parameter tracks and their covariance matrix, the [DelphesSaveChargedParticles](https://github.com/HEP-FCC/FCCSW/blob/master/Sim/SimDelphesInterface/src/DelphesSaveChargedParticles.cpp) module should be configured with the flag **saveTrkCov** set to True. Example:
```markdown
chhadSaveTool = DelphesSaveChargedParticles("efcharged")
chhadSaveTool.delphesArrayName = "Calorimeter/eflowTracks"
chhadSaveTool.saveIsolation = False
chhadSaveTool.saveTrkCov = True
chhadSaveTool.particles.Path      = "efcharged"
chhadSaveTool.particles_trkCov.Path      = "efcharged_trkCov"
chhadSaveTool.mcAssociations.Path = "efchargedToMC"
```
See the [tutorial here](https://hep-fcc.github.io/fcc-tutorials/fast-sim-and-analysis/FccFastSimDelphes.html) for a usage example.

- In the FCCEDM output, this will save the track parameters: ( d0, z0, phi, theta, q/p ) with d0 and z0 in mm and q/p in GeV-1 [TBC for q/p]. The covariance matrix is given in this basis. It is saved as 15 floats,  trkCov[0], trkCov[5], trkCov[9], trkCov[12] and trkCov[14] denoting the diagonal elements of the symmetric matrix.




### Jet algorithms in the Delphes interface

- The choice of which jet algorithm is run is made in the Delphes cards, for example :

```markdown
module FastJetFinder GenJetFinder {
  set InputArray NeutrinoFilter/filteredParticles

  set OutputArray jets

  # algorithm: 1 CDFJetClu, 2 MidPoint, 3 SIScone, 4 kt, 5 Cambridge/Aachen, 6 antikt
  set JetAlgorithm 6
  set ParameterR 0.4
  set JetPTMin 1.0
}
```

- In some cases, it may  be desirable to run the algorithm in the "exclusive" mode, forcing the algorithm to produce a fixed number of jets. This can be done by setting the following parameters in the Delphes FastJet finder:

```markdown
module FastJetFinder GenJetFinder {
   set ExclusiveClustering  True
   set NJets  2
.....
}
```

- Algorithms that use the difference in (pseudo-)rapidity between particles in order to define the distance are not well suited for FCC-ee. At FCC, the center-of-mass of the collisions is at rest with respect to the detector, in contrast to what happens at pp colliders. And using Delta( Eta ), instead of Delta(theta) or Delta( cos theta) is harmful, since Delta( Eta ) is not a good measure of the angular separation: for two particles that are emitted close-by and at small angle, their difference in pseudo-rapidity diverges as the log of the polar angle. Hence, using a jet  algorithm thar relies on Eta instead of the polar angle Theta will create too many jets in the forward region. 


- The [VLC algorithm](https://link.springer.com/article/10.1140%2Fepjc%2Fs10052-018-5594-6) was largely used for CLIC studies (where it showed good performance in particular to reject the background from gamma gamma to hadrons, which is severe at CLIC).

- See also the [FastJet user manual](https://arxiv.org/abs/1111.6097) 


### Making particle combinations with awkward arrays

Combinatoric functions provided by the python *awkward array* pckage  are very helpful to make particle combinations - e.g. loop over all Kaons and pions to find D candidates. To use them, the files should be analyzed with *uproot*. Very nice examples of how to use uproot and awkward arrays have been prepared by Donal Hill, see [this repository](https://github.com/donalrinho/fcc_python_tools).
- see also [Donal's talk, Sep 21, 2020](https://indico.cern.ch/event/956147/contributions/4026597/attachments/2106045/3542351/FCC_ee_PP_meeting_21_9_20.pdf)
- the [the scikit-hep software project](https://scikit-hep.org)

### Generating events

#### Beam energy spread

At FCC, the energy of the beams is distributed according to a Gaussian function. The corresponding beam energy spread is given in Table S.1 of the CDR, [see the highlighted line here](parameters_CDR_table.pdf). One should use the second number, the one that corresponds to "BS" (with beamstrahlung). For example, at the Z peak, the beam energy spread amounts to 0.132%. Note that this is the spread of the energy of the beam; to get the relative spread of the centre-of-mass energy √s, these numbers  have to be divided by √2.

It is important to take into account the beam energy spread when generating events. Some Monte-Carlo programs (e.g. Whizard) offer a built-in possibility to convolute the matrix elements with a Gaussian beam energy distribution. 

#### Vertex distribution

- Bunch dimensions: 
  - The bunch length is given by the σ<sub>z</sub> line in the [CDR table](parameters_CDR_table.pdf); one should use the second number, corresponding to the "BS" (with beamstrahlung case). For example, at the Z peak, it amounts to 12.1 mm
  - The bunch dimensions in the transverse plane, at the interaction point,  are given by 
     σ<sub>x,y</sub> = √ ( β*<sub>x,y</sub> ε<sub>x,y</sub>) where the values of the β function at the IP, and the horizontal and vertical emittance ε<sub>x,y</sub>  are given in the [CDR table](parameters_CDR_table.pdf).

- For gaussian bunches, the vertex distribution in (x, y, z) and in time is well approximated by a 4-dimensional gaussian distribution, with (see [here](overlap_gaussian_bunches.pdf) ):
<img src="vertex_formulae.png" alt="drawing" width="480"/>
where α denotes the half-crossing angle, α = 15 mrad.

Summary table:



  √s (GeV)  |  91.2  |  80  |  120  |  175  |  182.5  
------------|--------|------|-------|-------|----------
σ<sub>x</sub> (µm)  |  6.4  |  13.0  |  13.7  |  36.6  |  38.2
σ<sub>y</sub> (nm)  |  28.3  |  41.2  |  36.1  |  65.7  |  68.1
σ<sub>z</sub> (mm)  |  12.1  |  6.0  |  5.3  |  2.62  |  2.54
Vertex σ<sub>x</sub> (µm) | 4.5 | 9.2 | 9.7 | 25.9 | 27.0
Vertex σ<sub>y</sub> (nm) | 20  | 29.2 | 25.5 | 46.5 | 48.2 
Vertex σ<sub>z</sub> (mm) | 0.30 | 0.60 | 0.64 | 1.26 |1.27 
Vertex σ<sub>t</sub> (ps) | 28.6 | 14.1 | 12.5 | 6.2 | 6.0 


#### Transverse boost to account for the crossing angle

Monte-Carlo programs generate events in a frame where the incoming particles collide head-on. The crossing angle in the (x, z) plane results in a transverse boost along the x direction. The parameter of the Lorentz transformation is given by :
γ = √ ( 1 + tan<sup>2</sup> α ), where α denotes the half-crossing angle, α = 15 mrad.
Hence, prior to be sent to the detector simulation, the 4-vectors of the particles in the final state have to be boosted according to :

<img src="transverse_boost_formulae.png" alt="drawing" width="480"/>

where the "star" quantities denote the kinematics in the head-on frame, and the quantities on the leftside of the formulae correspond to the kinematics in the detector frame.

The convention used here is that the incoming bunches have a positive velocity along the x axis. It is this convention that is used in the DD4HEP files that model the interaction region (i.e. the center of the LumiCals is at x > 0).


### Monte-Carlo programs

- [Tutorial for Whizard for e+e-](https://indico.fnal.gov/event/45413/timetable/?view=standard) (Sep 2020)
- KKMC : the state-of-the-art Monte Carlo for e−e+ → ffbar + nγ
  - [KKMC-ee in GitHub](https://github.com/KrakowHEPSoft/KKMCee)
  - [Talk by Martin Chrzaszcz, Oct 19, 2020](https://indico.cern.ch/event/965346/contributions/4062342/attachments/2125634/3578715/mchrzasz.pdf)



# General information

Rather random for the while...

### Table of Contents

1. [CLD paper](#cld-paper)
2. [Common event samples](#common-event-samples)
3. [Vertexing and flavour tagging](#vertexing-and-flavour-tagging)
4. [Producing five-parameter tracks with the Delphes interface](#producing-five-parameter-tracks-with-the-delphes-interface)
5. [Jet algorithms in the Delphes interface](#jet-algorithms-in-the-delphes-interface)

### CLD paper
The [CLD performance paper on arXiv](https://arxiv.org/abs/1911.12230)

### Common event samples

Some samples (ZH, ZZ and WW, at sqrts = 240 GeV) have been produced (Sep 2020) for the Snowmass Software tutorial.
The events were simulated with Delphes, with the "IDEA\_TrkCov" card.
They are on EOS at CERN, details can be found [here](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_v02.php).
 

### Vertexing and flavour tagging
- Description of the [LCFIPlus algorithm](https://arxiv.org/pdf/1506.08371.pdf) used for the CLD studies
- see also the work done in the context of the Hcc case study

### Producing five-parameter tracks with the Delphes interface

- Recent versions of Delphes offer a rather detailed simulation of the tracks via the [TrackCovariance Delphes module](https://github.com/delphes/delphes/blob/master/modules/TrackCovariance.cc), developed from a code by Franco Bedeschi. The module, in the input card, must contain a description of the tracker, see for example [the delphes_card_IDEAtrkCov.tcl](https://github.com/delphes/delphes/blob/master/cards/delphes_card_IDEAtrkCov.tcl).
(Try to give more detail here about the geometry description). This produces five-parameter tracks - i.e., including the transverse and longitudinal impact parameters - with their covariance matrix.

- In FCCSW: in order to save the 5-parameter tracks and their covariance matrix, the [DelphesSaveChargedParticles](https://github.com/HEP-FCC/FCCSW/blob/master/Sim/SimDelphesInterface/src/DelphesSaveChargedParticles.cpp) should be configured with the flag **saveTrkCov** set to True. Example:
```markdown
chhadSaveTool = DelphesSaveChargedParticles("efcharged")
chhadSaveTool.delphesArrayName = "Calorimeter/eflowTracks"
chhadSaveTool.saveIsolation = False
chhadSaveTool.saveTrkCov = True
chhadSaveTool.particles.Path      = "efcharged"
chhadSaveTool.particles_trkCov.Path      = "efcharged_trkCov"
chhadSaveTool.mcAssociations.Path = "efchargedToMC"
```




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



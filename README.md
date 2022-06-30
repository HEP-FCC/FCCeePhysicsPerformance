
## Welcome to the FCC-ee Physics Performance Documentation

### Table of Contents
1. [Organisation](#organisation)
2. [Towards the definition of detector requirements](#towards-the-definition-of-detector-requirements)
3. [List of Active Case studies (evolving)](#case-studies-evolving-list)
4. [General information for FCC-ee analyses](#general-information-for-fcc-ee-analyses)
5. [LOIs submitted to Snowmass](#lois-submitted-to-snowmass)
5. [Software](#software-documentation-&-links)

-----

### Organisation

#### Coordinators
- Patrizia Azzi (INFN Padova) - Patrizia.Azzi@cern.ch
- Emmanuel Perez (CERN) - Emmanuel.Perez@cern.ch

#### Physics Performance meetings

O(monthly) meetings: Mondays, 3pm-5pm, CERN time. Usually the third Monday of each month. 
- [indico category "Physics Performance"](https://indico.cern.ch/category/12894/).
- [indico category for the meetings of the Physics Groups](https://indico.cern.ch/category/15156/)

Next meetings: 
- July 18, 15:00
- no meeting in August
- September 19, t.b.c.

E-group used for announcements: **FCC-PED-FeasibilityStudy**. To subscribe, go [here](https://e-groups.cern.ch/e-groups/EgroupsSearchForm.do).


-----

### Towards the definition of detector requirements

**Goal:** Circular colliders have the advantage of delivering collisions to multiple interaction points, which allow different detector designs to be studied and optimized – up to four for FCC-ee. On the one hand, the detectors must satisfy the constraints imposed by the invasive interaction region layout. On the other hand, the performance of heavy-flavour tagging, of particle identification, of tracking and particle-flow reconstruction, and of lepton, jet, missing energy and angular resolution, need to match the physics programme and the exquisite statistical precision offered by FCC-ee. Benchmark physics processes will be used to determine, via appropriate simulations, the requirements on the detector performance or design that must be satisfied to ensure that the systematic uncertainties of the measurements are commensurate with their statistical precision. The usage of the data themselves, in order to reach the challenging goals on the stability and on the alignment of the detector, in particular for the programme at and around the Z peak, will also be studied. In addition, the potential for discovering very weakly coupled new particles, in decays of Z or Higgs bosons, could motivate dedicated detector designs that would increase the efficiency for reconstructing the unusual signatures of such processes. These studies are crucial input to the further optimization of the two concepts described in the Conceptual Design Report, CLD and IDEA, and to the development of new concepts which might actually prove to be better adapted to (part of) the FCC-ee physics programme.


---------

### Case studies (evolving list) 

1. [Electroweak physics at the Z peak](case-studies/lineshape)
2. [Tau Physics](case-studies/taus)
3. [Flavour physics](case-studies/flavour)
4. [WW threshold](case-studies/ww)
5. [QCD measurements](case-studies/QCD)
6. [Higgs physics](case-studies/higgs)
7. [Top physics](case-studies/top)
8. [Direct searches for new physics](case-studies/BSM)


----------

### General information for FCC-ee analyses

1. [Common event samples](General/README.md#common-event-samples)
2. [Example analyses and how-to's](General/README.md#example-analyses-and-how-to's)
    1. [Basics](General/README.md#Basics)
    2. [How to associate RecoParticles with Monte-Carlo Particles](General/README.md#How-to-associate-RecoParticles-with-Monte-Carlo-Particles)
    3. [How to navigate through the history of the Monte-Carlo particles](General/README.md#How-to-navigate-through-the-history-of-the-Monte-Carlo-particles)
    4. [How to compute event variables (thrust, sphericity, etc)](General/README.md#How-to-compute-event-variables-(thrust,-sphericity,-etc))
    5. [How to fit tracks to a common vertex](General/README.md#How-to-fit-tracks-to-a-common-vertex)
    6. [How to run jet algorithms](General/README.md#How-to-run-jet-algorithms)
    7. [How to run kinematic fits](General/README.md#How-to-run-kinematic-fits)
3. [Code development](General/README.md#code-development)
4. [To produce your own Delphes samples](General/README.md#to-produce-your-own-delphes-samples)
    1. [Quick instructions for producing samples](General/README.md#quick-instructions-for-producing-samples)
    2. [Make simple changes to the tracker or beam-pipe description in Delphes](General/README.md#make-simple-changes-to-the-tracker-or-beam-pipe-description-in-delphes)
    1. [Change the Jet algorithms](General/README.md#change-the-jet-algorithm-in-the-delphes-interface)
5. [The five-parameter tracks produced by the Delphes interface](General/README.md#the-five-parameter-tracks-produced-by-the-delphes-interface)
6. [Vertexing and flavour tagging](General/README.md#vertexing-and-flavour-tagging)
    1. [Vertex-fitter code from Franco Bedeschi](General/README.md#vertex-fitter-code-from-franco-bedeschi)
    2. [Vertexing with the ACTS suite](General/README.md#vertexing-with-the-acts-suite)
    3. [The LCFI+ algorithm](General/README.md#the-LCFIPlus-algorithm)
    4. [The DecayTreeFitter (DTF) algorithm](General/README.md#the-decaytreefitter-(dtf)-algorithm)
    5. [Flavour tagging using machine learning](General/README.md#flavour-tagging-using-machine-learning)
7. [Making particle combinations with awkward arrays](General/README.md#making-particle-combinations-with-awkward-arrays)
8. [Generating events under realistic FCC-ee environment conditions](General/README.md#generating-events-under-realistic-fcc-ee-environment-conditions)
    1. [Beam energy spread](General/README.md#beam-energy-spread)
    2. [Vertex distribution](General/README.md#vertex-distribution)
    3. [Transverse boost to account for the crossing angle](General/README.md#transverse-boost-to-account-for-the-crossing-angle)
9. [Monte-Carlo programs](General/README.md#monte-carlo-programs)
10. [Bibliography](General/README.md#bibliography)



----------

### LOIs submitted to Snowmass

- [Initial list of case studies](https://indico.cern.ch/event/951830/contributions/4000220/attachments/2095812/3522643/SNOWMASS21-EF0-NF0-RF0-TF0-IF0-CompF0-017.pdf)
- "Letters of Interest"  submitted to Snowmass 2021 process (Aug 2020). Collected also here [this repository](https://indico.cern.ch/event/951830/) under "Energy Frontier".
- Other documents submitted to Snowmass 2021:
    - LOIs sent by the [CEPC](https://indico.ihep.ac.cn/event/12410/) collaboration
    - LOIs sent by the [CALICE](https://agenda.linearcollider.org/event/8647/) collaboration
    - Link to the [Snowmass portal](https://snowmass21.org)

----------
 
### Software Documentation & Links

#### Software tutorials

- the [FCCSW tutorials](https://hep-fcc.github.io/fcc-tutorials/)
- the tutorials given for Snowmass (September 2020) have been recorded, see [here](https://indico.cern.ch/event/945608/timetable/#20200922.detailed) and [here](https://indico.cern.ch/event/949950/timetable/?layout=room#20200929.detailed)
- the extremely useful [FCCSW FORUM page](https://fccsw-forum.web.cern.ch/)


#### Useful repositories
- [FCCSW](https://github.com/HEP-FCC/FCCSW)
- [DELPHES]( https://github.com/delphes/delphes)
- [DD4Hep](https://github.com/AIDASoft/DD4hep)
- [key4hep/EDM4hep](https://github.com/key4hep/EDM4hep)
- [FCCAnalyses](https://github.com/HEP-FCC/FCCAnalyses)




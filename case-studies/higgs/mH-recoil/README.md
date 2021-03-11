## The Higgs boson mass and σ(ZH) from the recoil mass with leptonic Z decays

### Abstract

A precision on mH as small as 5 MeV can be achieved from a fit to the distribution of the mass recoiling to 
a leptonically-decaying Z boson (Z → e+e− or μ+μ−) in the e+e− → ZH process at √s = 240 GeV. 
The requirements on the detector design (*electron energy and muon momentum resolution*, in particular) to achieve this statistical precision will be checked with this channel in the FCC-ee context. The feasibility of a calibration of the method – to reduce systematic effects due to, e.g., momentum scale determination and stability – will be ascertained with the e+e− → ZZ → l+l−X process. 
The need for calibration data at the Z pole will also be estimated (frequency, number of events).


See also [the determination of the centre-of-mass energy √s with a precision of O(1 MeV)](../../ww/radiativereturn/README.md) which is a key ingredient
for the determination of the recoil mass.


- The [corresponding Snomass LOI](https://indico.cern.ch/event/951830/contributions/3999001/attachments/2095109/3521327/HiggsParams_SNOWMASS21-EF1_EF0_Patrick_Janot-169.pdf)


### Contributors
- Clement Helsens (CERN)
- Ang Li, Gregorio Bernardi (LPNHE)
- Sylvie Braibant, Valentina Diolaiti, Paolo Giacomelli (Bologna)
- Markus Klute (MIT)
 
### Preliminary analyses 
- Clement Helsens: Developer, Sample production, Preliminary FCCAnalyses design, Preliminary recoil fit analysis

To run the analysis, should use the corresponding [FCCAnalyses](https://github.com/HEP-FCC/FCCAnalyses/tree/master/) configurations located in ```FCCAnalyses-config/mumu``` and ```FCCAnalyses-config/ee```. This preliminary analysis i using the input files produced in the ```edm4hep``` data format, and produced with this [sample production](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_tmp.php). ```FlatNtuples``` and ```histograms``` will be produced and used to fit the recoil mass. ```FCCAnalyses``` output files can also be directly accessed on eos ```/eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/```.

![](images/leptonic_recoil_m_ZH_sel1_stack_lin.png?raw=true)


arguments and examples to run the fitting macro could be seen by running
```python
python utils/massFit.py
usage:   python massFit.py BASEDIR HISTONAME SELECTION BINLOW=120 BINHIGH=140
example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zee/ leptonic_recoil_m_zoom3 sel1
example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zmumu/ leptonic_recoil_m_zoom4 sel0 122 128
```


As an example the fit result of running the following command 
```python
python utils/massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zee/ leptonic_recoil_m_zoom4 sel1 123 127:
```

is shown below (to be re-done with including beam energy spread)

```bash
  EXT PARAMETER                                INTERNAL      INTERNAL  
  NO.   NAME      VALUE            ERROR       STEP SIZE       VALUE   
   1  alpha       -8.67272e-01   4.57686e-02   3.90224e-02   7.11703e-01
   2  cbmean       1.25094e+02   6.79656e-03   3.51532e-03   1.87562e-02
   3  cbsigma      2.81768e-01   6.89490e-03   5.74469e-02  -6.08122e-02
   4  lam         -3.43241e-06   1.01039e-02   3.40174e-01   1.56709e+00
   5  n            1.27209e+00   1.72834e-01   2.30740e-02  -1.34474e+00
   6  nbkg         7.59189e+03   2.15350e+02   1.34305e-03  -1.51568e+00
   7  nsig         9.05996e+03   2.19379e+02   1.28389e-03  -1.51059e+00
```

![](images/fitResult.png?raw=true)


### Bibliography

- [Precision Higgs physics at the CEPC](https://iopscience.iop.org/article/10.1088/1674-1137/43/4/043002) Fenfen An et al 2019 Chinese Phys. C 43 043002


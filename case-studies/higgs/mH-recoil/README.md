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
- Ang Li, Gregorio Bernardi (APC)
- Sylvie Braibant, Valentina Diolaiti, Paolo Giacomelli (Bologna), Giacomo Ortona (Torino)
- Markus Klute, Jan Eysermans, Tianyu Justin Yang (MIT)

### Bibliography

- [Precision Higgs physics at the CEPC](https://iopscience.iop.org/article/10.1088/1674-1137/43/4/043002) Fenfen An et al 2019 Chinese Phys. C 43 043002
- [Measurement of the Higgs boson mass and ee → ZH cross section using Z→μμ and Z→ee at the ILC](https://arxiv.org/abs/1604.07524) J. Yan et al, Phys Rev D94 (2016) 113002

### List of Monte-Carlo samples (spring2021)

See  the compilation from Jan at [this googledoc](https://docs.google.com/spreadsheets/d/1W33UhfJbTILDkeN9ovl2Hcs32DTpSB7v0T0xsQzWPNw/edit#gid=0)

Recommended nominal samples in the [spring2021 campaign](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php) :
  - ZH signal: Use the **Whizard** samples (proper description of the BES), wzp6\_ee\_XXH\_ecm240 with XX = mumu, tautau, ee, nunu, or qq.
  - WW background:
    - mumu analysis: better use p8\_ee\_WW\_mumu\_ecm240, which includes W -> mu and W -> tau -> mu
    - otherwise, the lower statistics inclusive sample p8\_ee\_WW\_ecm240
  - ZZ background : p8\_ee\_ZZ\_ecm240
  - Fermion pair production: 
    - Dileptons: wzp6\_ee\_mumu\_ecm240, wzp6\_ee\_tautau\_ecm240 and wzp6\_ee\_ee\_Mee\_30\_150\_ecm240. The mumu and tautau samples correspond to ee -> Z/gamma\* -> mumu or tautau. The third sample includes the s- and the t-channel (important !), and was generated within 30 < Mee < 150 GeV and 15 deg < theta < 165 deg. The statistics corresponds to O(2x) that expected in 5 ab-1.
    - Hadrons: p8\_ee\_Zqq\_ecm240, corresponds to ee -> Z / gamma\* -> qq , all quark flavors.
  - Other small backgrounds generated in the mumu channel :
    - "single Z", i.e. ee -> e(e)Z with Z -> mumu: use both wzp6\_egamma\_eZ\_Zmumu\_ecm240 and wzp6\_gammae\_eZ\_Zmumu\_ecm240
    - gamma gamma background: wzp6\_gaga\_mumu\_60\_ecm240 and wzp6\_gaga\_tautau\_60\_ecm240, generated within M(mumu) or M(tautau) > 60 GeV

### Results obtained for the FCC week, July 2021

See [Jan's talk](https://indico.cern.ch/event/995850/contributions/4415989/attachments/2272945/3860610/ZHRecoilAnalysis_FCCWeek_29062021.pdf)

 
### Early version of the analysis (December 2020)
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







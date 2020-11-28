## The Higgs boson mass from the recoil mass

### Abstract

A precision on mH as small as 5 MeV can be achieved from a fit to the distribution of the mass recoiling to 
a leptonically-decaying Z boson (Z → e+e− or μ+μ−) in the e+e− → ZH process at √s = 240 GeV. 
The requirements on the detector design (*electron energy and muon momentum resolution*, in particular) to achieve this statistical precision will be checked with this channel in the FCC-ee context. The feasibility of a calibration of the method – to reduce systematic effects due to, e.g., momentum scale determination and stability – will be ascertained with the e+e− → ZZ → l+l−X process. 
The need for calibration data at the Z pole will also be estimated (frequency, number of events).


See also [the determination of the centre-of-mass energy √s with a precision of O(1 MeV)](../../ww/radiativereturn/README.md) which is a key ingredient
for the determination of the recoil mass.


- The [corresponding Snomass LOI](https://indico.cern.ch/event/951830/contributions/3999001/attachments/2095109/3521327/HiggsParams_SNOWMASS21-EF1_EF0_Patrick_Janot-169.pdf)


### Preliminary analyses (Clement Helsens)
Using the corresponding ```FCCAnalyses``` [ZH_Zmumu](https://github.com/HEP-FCC/FCCAnalyses/tree/master/FCCeeAnalyses/ZH_Zmumu) and [ZH_Zee](https://github.com/HEP-FCC/FCCAnalyses/tree/master/FCCeeAnalyses/ZH_Zee) and using the input files in ```edm4hep``` of this [sample production](http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_fccee_tmp.php), produced ```FlatNtuples``` and ```histograms``` used to fit the recoil: ```/eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/```.

arguments and examples to run the fitting macro could be seen by running
```python
python case-studies/higgs/mH-recoil/massFit.py
usage:   python massFit.py BASEDIR HISTONAME SELECTION BINLOW=120 BINHIGH=140
example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zee/ leptonic_recoil_m_zoom3 sel1
example: python massFit.py /eos/experiment/fcc/ee/analyses/case-studies/higgs/mH-recoil/FlatNtuples/ZH_Zmumu/ leptonic_recoil_m_zoom4 sel0 122 128
```

Fit result shown below:
![](fitResult.png?raw=true)

### Bibliography

- [Precision Higgs physics at the CEPC](https://iopscience.iop.org/article/10.1088/1674-1137/43/4/043002) Fenfen An et al 2019 Chinese Phys. C 43 043002


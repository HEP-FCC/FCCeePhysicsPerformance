## Combined search for Bu and Bc to tau + nu decays

### Overview

This analysis is a spin-off of the Bc2TauNu search. \
It inherits the basic steps from Bc2TauNu but aims to consider both Bc2TauNu and Bu2TauNu as separate signals. \
This analysis will also be used as a benchmark to help optimize the generic [FCC analysis workflow](https://github.com/HEP-FCC/FCCAnalyses).

### Contact

Clement Helsens <clement.helsens@cern.ch> \
Xunwu Zuo <xunwu.zuo@cern.ch>


### Scripts

The config files with common variables
- `user_config.py`: paths and common variables.
- `decay_mode_xs.py`: definitions of the branching ratios and cross-sections for the exclusive B-hadron and C-hadron modes considered as background.

The following scripts are used to perform BDT trainings:
- `process_sig_bkg_samples_for_xgb.py`: select a fraction of first stage training ntuples (ROOT) and convert to pickle files (pandas). 
- `train_xgb.py`: train first stage binary BDT. Takes pickle files from previous step as inputs.
- `train_xgb_stage2.py`: train second stage multi-class BDT. Takes second stage training ntuples as inputs.

The following scripts are used to make plots for MVA performance and validations against overtraining:
- `plot_vars_bdt.py`: (OUTDATED) make distributions of BDT variables before and after BDT cuts. To compare signal to background and understand how BDT sculpts the distributions.
- `plot_xgb.py`: make performance plots for first stage BDT. Takes first stage pickles as inputs.
- `plot_xgb_stage2.py`: make performance plots for second stage BDT. Takes second stage training ntuples as inputs.
- `overtrain_test_stage1.py`: validate first stage BDT against overtraining. Takes first stage training and testing ntuples as inputs.
- `overtrain_test_stage2.py`: validate second stage BDT against overtraining. Takes second stage training and testing ntuples as inputs.

The statistical analysis is performed with the following steps:
- `bkg_eff_decide_baseline_sel.py`: Scan different MVA cuts and check the changes in (inclusive) background efficiency and variable shapes. The variable chosen for the final fit needs to be independent from BDT cuts.
- `bkg_eff_compare_incl_and_excl.py`: After baseline selection, compare efficiencies for further cuts between inclusive and exclusive samples, to make sure the exclusive samples give good estimates of background efficiency.
- `bkg_eff_make_tight_sel.py`: Evaluate efficiencies in exclusive samples after tight selection.
- `bkg_eff_MVA_spline.py`: In each category, fit event efficiencies with regard to each of MVA1 and MVA2 (Bu or Bc) cut scans. Output splines.
- `final_sel_pretrim_signal.py`: Process signal samples to skim events. Just to save time of loading samples in the final analysis. No need to pretrim backgrounds as they are quick to load.
- `final_sel_estimate_purity.py`: Read splines and estimate signal and background yields. Scan MVA cuts for optimal signal purity, output to yields.json
- `fit_simultaneous_template.py`: Generate pseudo-data and perform combined fit in two categories. If more than 1 pseudo-data, output to fit_results.json
- `fit_multidim_simultaneous_template.py`: (DEPRECATED) It is a modification of `fit_simultaneous_template.py` to fit multi-dimensional distributions. 
- `toy_study_stats.py`: It takes the fit results from the previous fit step and extract the total uncertainty on the signal strength.
- `toy_plot_summary.py`: It reads the results from the previous toy stats step and make a summary plot for several toy groups.

This is an additional script to study the decay chains in background events after MVA selections, in order to understand what processes need to be generated for exclusive background samples.
- `survey_exclusive_modes.py`: It takes a special sample set (produced by `analysis_extra_bkg_composition.py` in FCCAnalysis) as inputs. It loops through event with high MVA scores and rebuild decay chains that are selected as the signal-like decay. Output is a table in a text file.


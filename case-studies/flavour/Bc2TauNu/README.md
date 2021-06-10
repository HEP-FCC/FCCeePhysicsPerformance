## Search for the decay Bc to tau nu

### Contact

Clement Helsens <Clement.Helsens@cern.ch>  
Donal Hill <Donal.Hill@cern.ch>  


### Pre-print submitted May 28, 2021

- [Prospects for B+c→τ+ντ at FCC-ee](https://arxiv.org/abs/2105.13330)


### Talks

- [First studies of Bc+ → τ+ ντ with EDM4hep and FCCAnalyses](https://indico.cern.ch/event/982690/contributions/4149358/attachments/2162425/3648879/Bc2TauNu_FCC_ee_PP_meeting_14_12_20.pdf) Donal Hill, talk at the Physics Performance meeting, Dec 14, 2020. 
- [Analysis of Bc / B+ to tau nu](https://indico.cern.ch/event/1029041/#25-analysis-of-bc-b-to-tau-nu) Clement Helsens, talk at the Physics Performance meeting, Apr 19, 2021.
- [Updates on the Bc / B+ to tau nu analysis](https://indico.cern.ch/event/1038347/#25-updates-on-the-bc-b-to-tau) Donal Hill, talk at the Physics Performance meeting, May 17, 2021. 
- [Prospects for 𝐵+𝑐→𝜏+𝜈𝜏 at FCC-ee](https://indico.cern.ch/event/1019438/#4-prospects-for-b_cto-tau-nu_t) Clement Helsens, talk at the general FCC-ee physics meeting, May 31, 2021.


### Bibliography

- The CEPC feasibility study in the leptonic  channels: their [Snowmass LOI](https://indico.ihep.ac.cn/event/12410/session/1/contribution/17/material/slides/0.pdf) and the preprint [Analysis of Bc→τντ at CEPC](https://arxiv.org/abs/2007.08234), Taifan Zheng et al, arXiv:2007.08234

### Analysis code summary

The following scripts are used to run the variois steps of the offline analysis:
- `user_config.py`: paths and common variables.
- `decay_mode_xs.py`: definitions of the branching ratios and cross-sections for the exclusive B-hadron modes considered as background.
- `process_sig_bkg_samples_for_xgb.py`: awkward array conversion of ROOT files to pandas data frames used in stage 1 xgboost training. Output stored in pickle files.
- `train_xgb.py`: train first stage BDT.
- `train_xgb_stage2.py`: train second stage BDT.
- `fit_MVA_dists.py`: fit the two MVA distributions above 0.95 in a summed sample of exclusive background. This is used to create cubic splines for accurate cut efficiency determination in the optimisation.
- `estimate_purity.py`: run the 2D cut optimisation procedure to determine best purity for a given set of cuts, and the signal and background yield at those cuts. Persists output to dictionary in JSON.
- `make_selected_samples_for_templates.py`: create files for signal and background passing tight BDT cuts, which are then used to make templates for the fit. Files are written as pandas dataframes in pickle.
- `template_fit.py`: run toy fits to measure the signal yield for a given number of Z’s. Can run with one toy to plot, or with many for toy studies of signal yield precision and bias.
- `analyse_toys.py`: gather toy fit results and look at the distribution of fitted signal yields. Use this to determine the overall signal yield uncertainty expected.
- `calc_BFs.py`: calculate branching ratios and their precisions for different number of Z's. Plot the trends in signal yield, branching fraction ratio, and branching fraction vs. number of Z's.

A few scripts are also used to generate plots and tables for the paper:
- `plot_xgb.py`: plot the BDT distributions from first stage training and the efficiency profiles
- `plot_xgb_stage2.py`: plot the BDT distributions from second stage training and the efficiency profiles
- `exclusive_bkg_summary_table.py`: summarise the exclusive background statistics and efficiencies for the paper in a table.
- `plot_max_hem_E.py`: plot charged vs neutral maximum hemisphere energies in signal and background, which are shown in paper.
- `make_signal_yield_table.py`: make a table for the paper showing signal yields and uncertainties for different number of Z's.
- `make_yield_BF_summary_tables.py`: make summary tables of yield and branching fraction precision as a function of number of Z's.

# ReHo and fALFF processing

This github page stores the code used to process the fMRI data to calcualte ReHo and fALFF values

Broadly: 
* ./CPAC holds the code and settings used to run CPAC
* ./EPI_Registration holds the code for EPI registration of the generated ReHo and fALFF values
* ./ComputeStatsFromDir_zeros.m calcualtes the mean regional values of ReHo and fALFF for each subject
* ./calc_global_and_site_means.py calcualtea the global and site means of the subjects, and the output is used by ./equalize_global_all.py
* ./equalize_global_all.py equalizes the subjects per region using the output of calc_global_and_site_means.py


### Dependencies

You will need python3, Matlab, CPAC and FSL to run this code.

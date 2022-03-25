# ReHo and fALFF processing

This github page stores the code used to process the fMRI data to calcualte ReHo and fALFF values

### Main steps, and corresponding code:
1. Preprocessing and calculation of fALFF and ReHo using CPAC
	* ABIDE_CPAC, especially the CPAC config file (CPAC_config_ABIDEI.yml and CPAC_config_ABIDEII.yml)
2. Registration and segmentation
	* EPI_registraion/ABIDE1_EPI_registration_parallel.sh
	* EPI_registraion/ABIDE1_EPI_registration_parallel.sh
3. Compute regional stats
	* EPI_registraion/compute_stats.py
4. Removal of subjects with poor alignment to MNI
	* notebooks/remove_poor_alignment_and_add_meta.ipynb
5. Removal of subjects with high motion
	* notebooks/motion_based_scan_selection_and_culling.ipynb
6. Site correction
	* /archive/bioinformatics/DLLab/AlexTreacher/src/autism_DCG/github/site_norm/calc_global_and_site_means.py
	* /archive/bioinformatics/DLLab/AlexTreacher/src/autism_DCG/github/site_norm/equalize_global_all.py

### Dependencies

You will need python3, Matlab, CPAC and FSL to run this code.

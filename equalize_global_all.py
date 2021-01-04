import os
import sys
import pandas as pd
import numpy as np

strProjectRoot = '/project/bioinformatics/DLLab/Alex/Projects/Autism'
if not os.path.exists(strProjectRoot):
    strProjectRoot = '//lamella.biohpc.swmed.edu/project/bioinformatics/DLLab/Alex/Projects/Autism'
if not os.path.exists(strProjectRoot):
    raise IOError('Project root can not be found')
strDataRoot = os.path.join(strProjectRoot, 'data/EPI_Registration_mean_functional_EPI_masked/DerivativeMatches/falff')

# get the input file
strCompleteFile = os.path.join(strDataRoot, r'ABIDEIandIIChosenScansBrodmannValues.csv')
strMeanFile = os.path.join(strDataRoot, r'SiteMean.csv')
strOutputFile = strCompleteFile.split('.csv')[0]+'_equalized_global.csv'
strQCFile =  os.path.join(strProjectRoot,'data','ABIDE_meta_Combined_QC_chosen_scan.csv')

dfCompleteData = pd.read_csv(strCompleteFile)
dfMeanData = pd.Series.from_csv(strMeanFile)
dfQC = pd.read_csv(strQCFile)
dfQCRestricted = dfQC[dfQC['QA']>.2][['Scan','QA']]
dfCompleteRestricted = pd.merge(left=dfQCRestricted, right=dfCompleteData, how='inner',left_on=['Scan'],right_on=['ABIDESubjectID'])
dfCompleteRestricted = dfCompleteRestricted[dfCompleteRestricted['SITE_ID'] != 'ABIDEII-KUL_3']
#ABIDEII-KUL_3 did not have enough subjects to use


lBrainRegions = [x for x in dfCompleteRestricted.columns.tolist() if 'MeanRegion' in x]

# calculate the location list
lstLocations = list(set(dfCompleteRestricted['SITE_ID']))

dGlobalAverage = dfMeanData['Global']

# find the difference between the average difference from each location to the global average
dctLocationDiff = {}
for strLocation in lstLocations:
    dctLocationDiff[strLocation] = dfMeanData[strLocation]-dGlobalAverage

dfCompleteRestricted[lBrainRegions] = dfCompleteRestricted.apply(lambda row: row[lBrainRegions]-dctLocationDiff[row['SITE_ID']], axis=1)
dfCompleteRestricted.to_csv(strOutputFile)

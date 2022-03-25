# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 16:37:02 2018

@author: Bioinformatics
"""

import os
import sys
import paths
import pandas as pd
import numpy as np

strDataPath = sys.argv[1]
print(strDataPath)
#strDataPath = '/archive/bioinformatics/DLLab/AlexTreacher/ExperimentOutputs/Autism_DCG/20210914_remove_poor_alignment_and_add_meta/desc-1_alff.csv'
strOutputPath = os.path.join(paths.strExperimentOutputDir,'Autism_DCG','20210914_site_norm')

dfCompleteData = pd.read_csv(strDataPath, index_col=0)

#lBrainRegions = [x for x in dfCompleteData.columns.tolist() if 'MeanRegion' in x]
strCol = 'MeanRegionCombined'

# calculate the location list
lstLocations = list(set(dfCompleteData['SITE_ID']))

#sample the data to make sure there are the same number of CTL and ASD
dfToAverage = pd.DataFrame(columns=dfCompleteData.columns.tolist())
dctSiteAverage = {}
for strLocation in lstLocations:
    if not strLocation in ['ABIDEII-KUL_3','ABIDEII-GU_1']:
        dfLocation = dfCompleteData[dfCompleteData['SITE_ID']==strLocation]
        #if strLocation == 'ABIDEII-NYU_2':
        #    dfLocation = dfCompleteData[(dfCompleteData['SITE_ID']==strLocation) | (dfCompleteData['SITE_ID']== 'ABIDEII-NYU_1')]
        dfASDSubjects = dfLocation[dfLocation['DX_GROUP']==1]
        dfCTLSubjects = dfLocation[dfLocation['DX_GROUP']==2]
        if dfASDSubjects.shape[0] > dfCTLSubjects.shape[0]:
            dfCTLSample=dfCTLSubjects
            dfASDSample=dfASDSubjects.sample(dfCTLSubjects.shape[0], random_state=5)
        elif dfASDSubjects.shape[0] < dfCTLSubjects.shape[0]:
            dfASDSample=dfASDSubjects
            dfCTLSample=dfCTLSubjects.sample(dfASDSubjects.shape[0], random_state=5)
        else:
            dfASDSample=dfASDSubjects
            dfCTLSample=dfCTLSubjects
        #if strLocation != 'ABIDEII-NYU_2':
        dfToAverage = dfToAverage.append(dfASDSample)
        dfToAverage = dfToAverage.append(dfCTLSample)
        dctSiteAverage[strLocation] = np.nanmean(dfASDSample[strCol].values.tolist()+\
                                                dfCTLSample[strCol].values.tolist())

#dfToAverage.to_csv(os.path.join(strDataRoot,'DataForGlobalAverage.csv'))
#calculate the global average
dctSiteAverage['Global'] = np.nanmean(dfToAverage[strCol].values)
strFilePrefix = os.path.basename(strDataPath).split('.')[0]
pd.Series(dctSiteAverage).sort_index().to_csv(os.path.join(strOutputPath, f'{strFilePrefix}_SiteMean.csv'))

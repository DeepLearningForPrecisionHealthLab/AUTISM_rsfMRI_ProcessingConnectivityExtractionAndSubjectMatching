# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 16:37:02 2018

@author: Bioinformatics
"""

import os
import sys
import pandas as pd
import numpy as np

strProjectRoot = '/project/bioinformatics/DLLab/Alex/Projects/Autism'
if not os.path.exists(strProjectRoot):
    strProjectRoot = '//lamella.biohpc.swmed.edu/project/bioinformatics/DLLab/Alex/Projects/Autism'
if not os.path.exists(strProjectRoot):
    raise IOError('Project root can not be found')
strDataRoot = os.path.join(strProjectRoot,
                           'data/EPI_Registration_mean_functional_EPI_masked/DerivativeMatches/falff')

# get the input file
strCompleteFile = os.path.join(strDataRoot, r'ABIDEIandIIChosenScansBrodmannValues.csv')

dfCompleteData = pd.read_csv(strCompleteFile)
#-1 is the nan for this data!
dfCompleteData.replace(-1, np.nan, inplace=True)

lBrainRegions = [x for x in dfCompleteData.columns.tolist() if 'MeanRegion' in x]

# calculate the location list
lstLocations = list(set(dfCompleteData['SITE_ID']))

#sample the data to make sure there are the same number of CTL and ASD
dfToAverage = pd.DataFrame(columns=dfCompleteData.columns.tolist())
dctSiteAverage = {}
for strLocation in lstLocations:
    dfLocation = dfCompleteData[dfCompleteData['SITE_ID']==strLocation]
    if strLocation == 'ABIDEII-NYU_2':
        dfLocation = dfCompleteData[(dfCompleteData['SITE_ID']==strLocation) | (dfCompleteData['SITE_ID']== 'ABIDEII-NYU_1')]
    dfASDSubjects = dfLocation[dfLocation['DX_GROUP']==1]
    dfCTLSubjects = dfLocation[dfLocation['DX_GROUP']==2]
    if dfASDSubjects.shape[0] > dfCTLSubjects.shape[0]:
        dfCTLSample=dfCTLSubjects
        dfASDSample=dfASDSubjects.sample(dfCTLSubjects.shape[0])
    elif dfASDSubjects.shape[0] < dfCTLSubjects.shape[0]:
        dfASDSample=dfASDSubjects
        dfCTLSample=dfCTLSubjects.sample(dfASDSubjects.shape[0])
    else:
        dfASDSample=dfASDSubjects
        dfCTLSample=dfCTLSubjects
    if strLocation != 'ABIDEII-NYU_2':
        dfToAverage = dfToAverage.append(dfASDSample)
        dfToAverage = dfToAverage.append(dfCTLSample)
    dctSiteAverage[strLocation] = np.nanmean(dfASDSample[lBrainRegions].values.tolist()+\
                             dfCTLSample[lBrainRegions].values.tolist())

dfToAverage.to_csv(os.path.join(strDataRoot,'DataForGlobalAverage.csv'))
#calculate the global average
dctSiteAverage['Global'] = np.nanmean(dfToAverage[lBrainRegions].values)
pd.Series(dctSiteAverage).to_csv(os.path.join(strDataRoot, 'SiteMean.csv'))
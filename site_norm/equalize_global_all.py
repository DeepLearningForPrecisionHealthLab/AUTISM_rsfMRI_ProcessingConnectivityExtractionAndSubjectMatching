import os
import sys
import paths
import pandas as pd
import numpy as np

strDataPath = sys.argv[1]
strMeanPath = sys.argv[2]
strOutputFile = strDataPath.split('.csv')[0]+'_equalized_global.csv'

#make sure the data file and mean file match up
strName = os.path.basename(strDataPath).split('.')[0]
assert os.path.basename(strMeanPath).startswith(strName)

#load the data and means
dfCompleteData = pd.read_csv(strDataPath, index_col=0)
dfMeanData = pd.read_csv(strMeanPath, index_col=0, header=None).iloc[:,0]
dfCompleteRestricted = dfCompleteData[(dfCompleteData['SITE_ID'] != 'ABIDEII-KUL_3') & (dfCompleteData['SITE_ID'] != 'ABIDEII-GU_1')]
#ABIDEII-KUL_3 did not have enough subjects to use
#dfCompleteRestricted = dfCompleteData[dfCompleteData['SITE_ID'] != 'ABIDEII-GU_1']

#get the columns that are to be normed
lBrainRegions = [x for x in dfCompleteRestricted.columns.tolist() if 'MeanRegion' in x]

#get the list of locations
lstLocations = list(set(dfCompleteRestricted['SITE_ID']))

#get the global average
dGlobalAverage = dfMeanData['Global']

# find the difference between the average difference from each location to the global average
dctLocationDiff = {}
for strLocation in lstLocations:
    dctLocationDiff[strLocation] = dfMeanData[strLocation]-dGlobalAverage

#subtract the above difference from each subject
dfCompleteRestricted[lBrainRegions] = dfCompleteRestricted.apply(lambda row: row[lBrainRegions]-dctLocationDiff[row['SITE_ID']], axis=1)
dfCompleteRestricted.to_csv(strOutputFile)

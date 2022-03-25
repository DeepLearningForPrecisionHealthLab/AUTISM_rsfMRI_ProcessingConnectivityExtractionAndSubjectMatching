import os
import sys
import numpy as np
import pandas as pd
import nibabel
import re
import glob

strOutputDir = '<path_to>/ExperimentOutputs/Autism_DCG/20210908_derivative_summary'
strPathsFile = '<path_to>/ExperimentOutputs/Autism_DCG/20210908_subject_motion_cull.csv'
dfPaths = pd.read_csv(strPathsFile, index_col=0)

strRegionPath = 'BA_EPI_space.nii'
lMultiRegions=[[3,1,2,5], [4,6], [7], [9], [17], [20,37], [24], [38], [39,40], [41,42,22], [44,45]]
#list with all regions included
lAllRegions = []
_ = [lAllRegions.extend(x) for x in lMultiRegions]

def fRegionsToColName(lRegions):
    return 'MeanRegion'+'_'.join([str(x) for x in lRegions])

def fGetSubject(strPath):
    strSubject = re.findall('sub-([A-Za-z0-9]+)', os.path.basename(strPath))[0]
    if strSubject.startswith('00'):
        strSubject = strSubject[2:]
    return strSubject

def fGetABIDE(strPath):
    #find the ABIDE number (1 or 2)
    #as there is only ABIDE 1 or 2, converting to roman numberals is easy, if ABIDE 4 exists this will fail
    strABIDE = re.findall('ABIDE([I]+)', strPath)[0]
    return strABIDE.__len__()

for intDesc in [1,2,3]:
    for strDerivative in ['alff','falff','reho']:
        print(f'calculating {strDerivative} desc {intDesc}')
        strCol = f'desc-{intDesc}_space-EPI_{strDerivative}.nii.gz'
        dfStats = pd.DataFrame(columns = ['ABIDE']+[fRegionsToColName(x) for x in lMultiRegions])
        for i, row in dfPaths.iterrows():
            strABIDEID = row['subject']
            strABIDE = row['abide']
            strImgPath = row[strCol]
            assert os.path.exists(strImgPath)
            strABIDEID = fGetSubject(strImgPath)
            strABIDE = fGetABIDE(strImgPath)
            dfStats.loc[strABIDEID, 'ABIDE'] = strABIDE

            nibRegions = nibabel.load(strRegionPath)
            arrRegions = np.array(nibRegions.dataobj)

            nibDerivedMap = nibabel.load(strImgPath)
            arrDerivedMap = np.array(nibDerivedMap.dataobj)

            for lRegions in lMultiRegions:
                # create a vectorized function to create a binary mask based on the regions
                fInRegionVector = np.vectorize(lambda x: x in lRegions)
                #create the mask based on the lRegions
                arrMask = fInRegionVector(arrRegions)
                #take the mean of all the values inside the mask
                #dMeanRegionalValue = arrDerivedMap[arrMask==1].mean()
                dMeanRegionalValue = arrDerivedMap[(arrMask==1) & (arrDerivedMap != 0)].mean()
                dfStats.loc[strABIDEID, fRegionsToColName(lRegions)] = dMeanRegionalValue

            #calc the mean value across all of the BA reagions we are using. 
            fInRegionVector = np.vectorize(lambda x: x in lAllRegions)
            arrMask = fInRegionVector(arrRegions)
            dMeanRegionalValue = arrDerivedMap[(arrMask==1) & (arrDerivedMap != 0)].mean()
            dfStats.loc[strABIDEID, 'MeanRegionCombined'] = dMeanRegionalValue
            
            #get the number of zeros that occur across all BA areas.
            lRegions = range(1,52)
            fInRegionVector = np.vectorize(lambda x: x in lRegions)
            arrMask = fInRegionVector(arrRegions)
            #number of zeros in the BA regions (good check for alighnment quality)
            dfStats.loc[strABIDEID, 'zeros in BA'] = arrDerivedMap[(arrMask==1) & (arrDerivedMap==0)].size
            dfStats.loc[strABIDEID, 'fraction of zeros in BA'] = arrDerivedMap[(arrMask==1) & (arrDerivedMap==0)].size/arrMask.sum()

            dfStats.index.name='ABIDE_ID'

        dfStats.to_csv(os.path.join(strOutputDir, f'desc-{intDesc}_{strDerivative}.csv'))

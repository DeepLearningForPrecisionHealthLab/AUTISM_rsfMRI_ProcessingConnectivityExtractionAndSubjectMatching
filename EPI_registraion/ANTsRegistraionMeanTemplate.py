import os
import sys
import re
sys.path.append('/archive/bioinformatics/DLLab/AlexTreacher/src/')
from utilities import nifti_manipulation
strEPITemplate = r'<path_to>EPI_3mm_template.nii'

strMeanFunctional = sys.argv[-1]
print(strMeanFunctional)

#sort out some paths needed for processing
strOutputPath = os.path.dirname(strMeanFunctional)
strScanPrefix = os.path.basename(strMeanFunctional).split('mean_bold')[0]
strEPITransformDir = os.path.join(strOutputPath, f'{strScanPrefix[:-6]}_EPI_Transforms')
strBoldEPITransformPath = os.path.join(strOutputPath, f'{strScanPrefix}mean_bold_space-EPI.nii.gz')
os.makedirs(strEPITransformDir, exist_ok=True)

#don't run if it's already been ran
if os.listdir(strEPITransformDir).__len__() < 3:
    
    #Transform the mean_functional to the template space
    scanMeanFunctional = nifti_manipulation.Scan(strMeanFunctional)
    scanTemplate = nifti_manipulation.Scan(strEPITemplate)
    scanMeanFunctional.fRegisterToTemplate(
        strOutputPath = strBoldEPITransformPath,
        strTemplate = scanTemplate,
        strOutputTransformsPrefix = os.path.join(strEPITransformDir,'EPIxfm'),
        inplace=True
    )

    # Use the transform and apply it to all the derivative maps
    for strDerivative in ['falff','alff','reho']:
        for intDesc in [1,2,3]:
            strDerivativePath = os.path.join(strOutputPath, strScanPrefix+f'{intDesc}_{strDerivative}.nii.gz')
            strDerivativeTransformPath = os.path.join(strDerivativePath.split(f'{strDerivative}.nii.gz')[0]+f'space-EPI_{strDerivative}.nii.gz')
            scanDerivative = nifti_manipulation.Scan(strDerivativePath)
            strOutputDir = os.path.join(strOutputPath, strDerivative)
            scanDerivative.fApplyTransform(
                strOutputPath = strDerivativeTransformPath,
                strTemplate = scanTemplate,
                lTransforms = scanMeanFunctional.lTransformPaths,
            )
else:
    print(f'Previously ran, so skipping {strMeanFunctional}')

import os
import sys
import re
sys.path.append('/project/bioinformatics/DLLab/Alex/Projects')
from utilities import nifti_manipulation

bTesting = False

if bTesting:
    strScanInputName = '0051260_session_1'
    intABIDE = 1
else:
    intABIDE = int(sys.argv[1])
    strScanInputName = str(sys.argv[2]).rstrip()
    print('Running ABIDE%i, %strScanName'%(intABIDE,strScanInputName))
strABIDE = 'ABIDE%i'%intABIDE

#check to see if there is a run in the name (for ABIDE II)
reRunSearch = re.search(r'(_run-)([0-9])', strScanInputName)
if reRunSearch != None:
    strScanName = strScanInputName[:reRunSearch.start()]
    intRun = int(reRunSearch.groups()[1])
else:
    strScanName = strScanInputName
    intRun = 1

strOutputRootPath = '/project/bioinformatics/DLLab/Alex/Projects/Autism/data/EPI_Registration_mean_functional_EPI_masked/'
strABIDE1Path = r'/project/bioinformatics/DLLab/STUDIES/ABIDE1/CPAC/pipeline_1112sub_fal_reho__freq-filter'
strABIDE2Path = r'/project/bioinformatics/DLLab/STUDIES/ABIDE2/CPAC/pipeline_1113sub_fal_reho__freq-filter'
if intABIDE == 1:
    strABIDEPath = strABIDE1Path
else:
    strABIDEPath = strABIDE2Path
strOutputPath = os.path.join(strOutputRootPath, strABIDE)

print(strScanInputName, strScanName)
if not os.path.exists(strABIDEPath):
    raise ValueError('Path does not exit', strABIDEPath)
elif not os.path.exists(os.path.join(strABIDEPath, strScanName)):
    raise ValueError('Path does not exit', os.path.join(strABIDEPath, strScanName))
else:
    print('Path exits: ', os.path.join(strABIDEPath, strScanName))

#Transform the mean_functional to the template space

strMeanFunctional = nifti_manipulation.fGetCPACScan(
    strScanName=strScanName,
    strOutput='mean_functional',
    strCPACOutputPath = strABIDEPath,
    intRun=intRun,
    bGlobalAverage=True
    )

strEPITemplate = r'/project/bioinformatics/DLLab/Alex/Projects/utilities/NeuroTemplates/EPI_3mm_T1_masked.nii'
scanMeanFunctional = nifti_manipulation.Scan(strMeanFunctional)
scanTemplate = nifti_manipulation.Scan(strEPITemplate)
strTransformOutputDir = os.path.join(strOutputPath, 'mean_functional_transforms')
if not os.path.exists(strTransformOutputDir):
    os.makedirs(strTransformOutputDir)
scanMeanFunctional.fRegisterToTemplate(
    strOutputPath = os.path.join(strTransformOutputDir, strScanName+'MeanFunctionalRegisteredToEPI.nii.gz'),
    strTemplate = scanTemplate,
    strOutputTransformsPrefix = os.path.join(strTransformOutputDir,strScanName+'Transform'),
    inplace=True
)

# Use the transform and apply it to all the derivative maps
for strDerivative in ['falff','alff','reho']:
    strDerivativePath = nifti_manipulation.fGetCPACScan(
        strScanName=strScanName,
        strOutput='%s_smooth' % strDerivative,
        strCPACOutputPath=strABIDEPath,
        intRun=intRun,
        bGlobalAverage=True
    )
    scanDerivative = nifti_manipulation.Scan(strDerivativePath)
    strOutputDir = os.path.join(strOutputPath, strDerivative)
    scanDerivative.fApplyTransform(
        strOutputPath = os.path.join(strOutputDir, strScanInputName+'_fALFFTransformed.nii.gz'),
        strTemplate = scanTemplate,
        lTransforms = scanMeanFunctional.lTransformPaths,
    )
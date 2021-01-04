%function [ output_args ] = ComputeStats( input_args )
% Purpose:
% Inputs:
% Outputs:
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

addpath('/project/bioinformatics/DLLab/Alex/software/matlab_add_ons/cell2csv')
addpath('/project/bioinformatics/DLLab/Alex/software/matlab_add_ons/spm8')
strRootDirPreProcessedABIDE='/project/bioinformatics/DLLab/Alex/Projects/Autism/data';

lPreProcessingOptions={'ABIDE1_falff_img_filt0_global0',...
    'ABIDE1_falff_img_filt0_global1',...
    'ABIDE1_falff_img_filt1_global0',...
    'ABIDE1_falff_img_filt1_global1',...
    'ABIDE1_falff_smooth_filt0_global0',...
    'ABIDE1_falff_smooth_filt0_global1',...
    'ABIDE1_falff_smooth_filt1_global0',...
    'ABIDE1_falff_smooth_filt1_global1',...
    'ABIDE1_falff_to_standard_filt0_global0',...
    'ABIDE1_falff_to_standard_filt0_global1',...
    'ABIDE1_falff_to_standard_filt1_global0',...
    'ABIDE1_falff_to_standard_filt1_global1',...
    'ABIDE1_falff_to_standard_smooth_filt0_global0',...
    'ABIDE1_falff_to_standard_smooth_filt0_global1',...
    'ABIDE1_falff_to_standard_smooth_filt1_global0',...
    'ABIDE1_falff_to_standard_smooth_filt1_global1',...
    'ABIDE2_falff_img_filt0_global0',...
    'ABIDE2_falff_img_filt0_global1',...
    'ABIDE2_falff_img_filt1_global0',...
    'ABIDE2_falff_img_filt1_global1',...
    'ABIDE2_falff_smooth_filt0_global0',...
    'ABIDE2_falff_smooth_filt0_global1',...
    'ABIDE2_falff_smooth_filt1_global0',...
    'ABIDE2_falff_smooth_filt1_global1',...
    'ABIDE2_falff_to_standard_filt0_global0',...
    'ABIDE2_falff_to_standard_filt0_global1',...
    'ABIDE2_falff_to_standard_filt1_global0',...
    'ABIDE2_falff_to_standard_filt1_global1',...
    'ABIDE2_falff_to_standard_smooth_filt0_global0',...
    'ABIDE2_falff_to_standard_smooth_filt0_global1',...
    'ABIDE2_falff_to_standard_smooth_filt1_global0',...
    'ABIDE2_falff_to_standard_smooth_filt1_global1'
};
lPreProcessingOptions = {
    'EPI_Registration_mean_functional_EPI_masked/ABIDE1/falff',...
    'EPI_Registration_mean_functional_EPI_masked/ABIDE2/falff',...
    'EPI_Registration_mean_functional_EPI_masked/ABIDE1/alff',...
    'EPI_Registration_mean_functional_EPI_masked/ABIDE2/alff',...
    'EPI_Registration_mean_functional_EPI_masked/ABIDE1/reho',...
    'EPI_Registration_mean_functional_EPI_masked/ABIDE2/reho'
    }
for intC = 1:length(lPreProcessingOptions);
    strProProcessingOptions = lPreProcessingOptions{intC}
    % strLabeledVolSuffix='_falff_labeled.nii';  % for labeled volumes (1 per subject) derived data

    strRootDirPreProcessedABIDEWithOptions=fullfile(strRootDirPreProcessedABIDE,strProProcessingOptions);
    soaNamesOfSubjectPreProcessedDerivativeFiles=dir([strRootDirPreProcessedABIDEWithOptions,'/*.gz']);
    cellarrNamesOfSubjectPreProcessedDerivativeFiles={soaNamesOfSubjectPreProcessedDerivativeFiles.name};
    cellarrAbideSubjects=cellarrNamesOfSubjectPreProcessedDerivativeFiles

    %{
    % load list of subjects
    %   Read in subject list, cellarrAbideSubjects
    strUCLA_ABIDE_MatchingDatabase='Genomics(UCLA)_Subject_metadata_062416_ver2.xlsx';
    % strUCLA_ABIDE_MatchingDatabase='Genomics(UCLA)_Subject_metadata_062416_ver2_edit.xlsx';
    strUCLA_ABIDE_MatchingDatabase=fullfile(strRootDirPreProcessedABIDE,strUCLA_ABIDE_MatchingDatabase);
    [~,~,WorksheetData]=xlsread(strUCLA_ABIDE_MatchingDatabase,1,'A8:G68');
    cellarrAbideSubjects=WorksheetData(2:end,7);
    cellarrUCLASubjects=WorksheetData(2:end,1);
    %}
    strOutputFile=fullfile(strRootDirPreProcessedABIDEWithOptions,['Database_',datestr(now,30),'_zeros_removed.csv']);

    % load list of multiRegions to compute stats for
    % first entry in each multiRegion is the primary Brodmann area
    cellMultiRegions={ [3,1,2,5], [4,6], [7], [9], [17],  [20,37],  [24], [38], [39,40],  [41,42,22], [44,45] };
    % cellMultiRegions={[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],...
    %    [11],[12],[13],[14],[15],[16],[17],[18],[19],[20],...
    %    [21],[22],[23],[24],[25],[26],[27],[28],[29],[30],...
    %    [31],[32],[33],[34],[35],[36],[37],[38],[39],[40],...
    %    [41],[42],[43],[44],[45],[46],[47],[48],[49],[50],...
    %    [51],[52]
    %    }
    nNumMultiRegions=length(cellMultiRegions);
    nNumSubjects=length(cellarrAbideSubjects);

    arr2DSubjStatisticalRegionData=[];
    cellarrAbideSubjectsProcessed={};
    cellarrUCLASubjectsProcessed={};

    for iSubject=1:nNumSubjects  % For each subject in cellarrAbideSubjects
        strAbideSubjID=cellarrAbideSubjects{iSubject};
        % strUCLASubjID=cellarrUCLASubjects{iSubject};
        fprintf(1,'[%d]Processing subject %s\n',iSubject,strAbideSubjID);

        % Construct derivative volume path
        % First extract the ID number
        % strIDNumber = strAbideSubjID(end-4:end)   ; % e.g. '51456' if the input is 'Caltech_51456'

        %     % allow to debug 51344 
        %     if ~strcmpi(strIDNumber,'51344')
        %         continue;  
        %     end

        % now find the filename with that ID number
        IndexC=strfind(cellarrNamesOfSubjectPreProcessedDerivativeFiles,strAbideSubjID);
        Index=find(not(cellfun('isempty',IndexC)));
        if isempty(Index) 
            fprintf(1,'  Error: derivative data for subject, %s, wasnt found in directory %s\n',strAbideSubjID,strRootDirPreProcessedABIDEWithOptions);
            fprintf(1,'  Skipping subject.\n');
            continue;
        elseif length(Index)>1
            fprintf(1,'  Warning: Multiple (%d) matching derivative data files for subject, %s, found in directory %s\n',length(Index),strAbideSubjID,strRootDirPreProcessedABIDEWithOptions);
            fprintf(1,'  Using first file.\n');        
        end
        strSubjectPreProcessedDerivativeFile=cellarrNamesOfSubjectPreProcessedDerivativeFiles{Index(1)};
        fprintf(1,'  Matched to %s\n',strSubjectPreProcessedDerivativeFile);        


        % Load Derivative.nii and labeled.nii
        % Load Derivative 
        strDerivativeVolPath=fullfile(strRootDirPreProcessedABIDE,strProProcessingOptions,strSubjectPreProcessedDerivativeFile);
        strDerivativeVolPath=aam_gunzip(strDerivativeVolPath);
        spmImageInfo_Derivative=spm_vol(strDerivativeVolPath);
        [arr2DImage_Derivative,arr2D_mmXYZCoordsDerivative]=spm_read_vols(spmImageInfo_Derivative);
        % Load labeled volume (atlas fitted to subject derivative data)

        [pathstr,name,ext] = fileparts(strDerivativeVolPath);
        strLabeledVolPath=[pathstr,'/',name,'_labeled.nii'];
        fprintf(1,'  Loading labeled vol %s\n',strLabeledVolPath);
        strLabeledVolPath=aam_gunzip(strLabeledVolPath);
        spmImageInfo_LabeledVol=spm_vol(strLabeledVolPath);
        [arr2DImage_LabeledVol,arr2D_mmXYZCoords_Atlas]=spm_read_vols(spmImageInfo_LabeledVol);

        % compute stats by appending a line of stats to a csv file 

        vecSubjStats=[];
        for idxMultiRegion=1:nNumMultiRegions   % For each multiRegion
            arr1DMultiRegion=cellMultiRegions{idxMultiRegion};

%             fprintf(1,'[%d] MultiRegion contains Brodmann areas', idxMultiRegion);
%             disp(arr1DMultiRegion);

            % defaults (e.g. when MultiRegion not found)
            strucRegStats.min=-1;
            strucRegStats.max=-1;
            strucRegStats.mean=-1;
            strucRegStats.stdev=-1;
            strucRegStats.median=-1;

            %find all the indices where labeledVol is in the current multiRegion
            [idx]=find(ismember(arr2DImage_LabeledVol,arr1DMultiRegion));
            % [i,j,k]=ind2sub(size(arr2DImage_LabeledVol), idx)
            if ~isempty(idx)
                % Compute stats vector: min, max, mean, stdev, median
                arr1DRegionVals=arr2DImage_Derivative(idx);
                %arr1DRegionVals_zeros=arr2DImage_Derivative(idx);
                arr1DRegionVals(arr1DRegionVals==0)=nan;
                strucRegStats.min=min(arr1DRegionVals);
                strucRegStats.max=max(arr1DRegionVals);
                strucRegStats.mean=mean(arr1DRegionVals,'omitnan');
                strucRegStats.stdev=std(arr1DRegionVals,'omitnan');
                strucRegStats.median=median(arr1DRegionVals,'omitnan');
            end
            % arrRegionStats=[strucRegStats.min,strucRegStats.max,strucRegStats.mean,strucRegStats.stdev,strucRegStats.median];
            arrRegionStats=[strucRegStats.mean];
            vecSubjStats=[vecSubjStats, arrRegionStats];
        end

        % fprintf(1,'Computed stats:\n');
        % display(vecSubjStats);

        % Save this row for output to worksheet
        % cellarrUCLASubjectsProcessed=cat(1,cellarrUCLASubjectsProcessed, strUCLASubjID);
        cellarrAbideSubjectsProcessed=cat(1,cellarrAbideSubjectsProcessed,strAbideSubjID);
        arr2DSubjStatisticalRegionData=cat(1,arr2DSubjStatisticalRegionData,vecSubjStats);


    end   % loop over subjects

    % xlswrite(FILE,ARRAY,SHEET,RANGE)
    [rows,cols]=size(arr2DSubjStatisticalRegionData);
    cellDerivedROIStats=cell(rows+1,cols+1);

    % Compute headers for columns
    cellColHeaders={'ABIDESubjectID'};
    cellColHeaderPrefixes={'MeanRegion'};

    nNumColHeaderPrefixes=length(cellColHeaderPrefixes);
    for idxMultiRegion=1:nNumMultiRegions
      for iColHeaderPrefix=1:nNumColHeaderPrefixes
          strThisColHeader=cellColHeaderPrefixes{iColHeaderPrefix};
          arrRegions=cellMultiRegions{idxMultiRegion};
          nNumRegions=length(arrRegions);
          for iRegion=1:nNumRegions
              strThisColHeader=[strThisColHeader, num2str(arrRegions(iRegion))];
              if iRegion~=nNumRegions 
                  strThisColHeader=[strThisColHeader, '_'];
              end
          end
          cellColHeaders={cellColHeaders{:}, strThisColHeader};  % append col heading
      end
    end
    cellDerivedROIStats(1,:)=cellColHeaders;

    % cellDerivedROIStats(2:end,1)=cellarrUCLASubjectsProcessed;
    cellDerivedROIStats(2:end,1)=cellarrAbideSubjectsProcessed;
    cellDerivedROIStats(2:end,2:end)=num2cell(arr2DSubjStatisticalRegionData);


    % xlswrite(strOutputFile,cellDerivedROIStats);  % this wont work on linux since there is no excel server to communicate with. 
    cell2csv(strOutputFile,cellDerivedROIStats);  % this is linux compatible . From Mathworks File Exchange.
end


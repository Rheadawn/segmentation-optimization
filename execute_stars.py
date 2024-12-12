import re
import time
import subprocess
import glob
import os
import json
import uuid

total_execution_time = 0
tsc = "full-TSC"
metric = "simpleMetric"
featureName = "Overtaking"
commandStart = "../distribution/bin/stars-carla-experiments "

def commandEnd(folderName, featureName):
    return f" \"--folderName={folderName}\" \"--featureName={featureName}\" \"--minSegmentTicks=0\" \"--input=../stars-reproduction-source/stars-experiments-data/simulation_runs\" \"--saveResults\""

def by_length(x): # [segmentSize]
    segmentSize = x[0]

    # generate a unique and descriptive folder name
    folderName = f"by_length_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=BY_LENGTH\" \"--segmentationValue={segmentSize}\"" + commandEnd(folderName, featureName)
   
    return segmentation_run(command, folderName)

def static_segment_length_seconds(x): # [windowSize]
    windowSize = x[0]

    # generate a unique and descriptive folder name
    folderName = f"static_segment_length_seconds_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=STATIC_SEGMENT_LENGTH_SECONDS\" \"--segmentationValue={windowSize}\" \"--secondarySegmentationValue=2.0\"" + commandEnd(folderName, featureName)
    
    return segmentation_run(command, folderName)

def static_segment_length_meters(x): # [windowSize]
    windowSize = x[0]

    # generate a unique and descriptive folder name
    folderName = f"static_segment_length_meters_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=STATIC_SEGMENT_LENGTH_METERS\" \"--segmentationValue={windowSize}\" \"--secondarySegmentationValue=2.0\"" + commandEnd(folderName, featureName)
    
    return segmentation_run(command, folderName)

def dynamic_segment_length_meters_speed_acceleration_1(x): # [lookAhead, stepSize]
    lookAhead, stepSize = x

    # generate a unique and descriptive folder name
    folderName = f"dynamic_segment_length_meters_speed_acceleration_1_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1\" \"--segmentationValue={lookAhead}\" \"--secondarySegmentationValue={stepSize}\"" + commandEnd(folderName, featureName)

    return segmentation_run(command, folderName)

def dynamic_segment_length_meters_speed(x): # [lookAhead, scalar, stepSize]
    lookAhead, scalar, stepSize = x

    # generate a unique and descriptive folder name
    folderName = f"dynamic_segment_length_meters_speed_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=DYNAMIC_SEGMENT_LENGTH_METERS_SPEED\" \"--segmentationValue={lookAhead}\" \"--secondarySegmentationValue={scalar}\" \"--tertiarySegmentationValue={stepSize}\"" + commandEnd(folderName, featureName)

    return segmentation_run(command, folderName)

def sliding_window_multistart_meters(x): # [windowSize1, windowSize2, windowSize3]
    windowSize1, windowSize2, windowSize3 = x

    # generate a unique and descriptive folder name
    folderName = f"sliding_window_multistart_meters_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=SLIDING_WINDOW_MULTISTART_METERS\" \"--segmentationValue={windowSize1}\" \"--secondarySegmentationValue={windowSize2}\" \"--tertiarySegmentationValue={windowSize3}\"" + commandEnd(folderName, featureName)

    return segmentation_run(command, folderName)

def sliding_window_multistart_seconds(x): # [windowSize1, windowSize2, windowSize3]
    windowSize1, windowSize2, windowSize3 = x

    # generate a unique and descriptive folder name
    folderName = f"sliding_window_multistart_seconds_{tsc}_{metric}_{str(uuid.uuid4())[:8]}"
    command = commandStart + f"\"--segmentationType=SLIDING_WINDOW_MULTISTART_SECONDS\" \"--segmentationValue={windowSize1}\" \"--secondarySegmentationValue={windowSize2}\" \"--tertiarySegmentationValue={windowSize3}\"" + commandEnd(folderName, featureName)

    return segmentation_run(command, folderName)

def getJson(metric, folderName):
    global tsc

    # Go to serialized-results folder and get metric for tsc out of result folder
    folder_path = os.path.join('serialized-results', folderName, metric, tsc.replace('-',' ') + '.json')
    result_file = glob.glob(folder_path)

    # Load json and return value
    fileContent = open(result_file[0], 'r').read()
    return json.loads(fileContent)

def getSingleMetric(metric, valueName, folderName):
    result = getJson(metric, folderName)
    print(f"{metric} | {valueName}: {result[valueName]}")
    return result[valueName]

def calculateTscCoverage(folderName):
    valid_tsc_instances = getSingleMetric('valid-tsc-instances-per-tsc', 'count', folderName)
    missed_tsc_instances = getSingleMetric('missed-tsc-instances-per-tsc', 'count', folderName)
    return -(valid_tsc_instances / (valid_tsc_instances + missed_tsc_instances))

def calculateFeatureCombinationCoverage(folderName):
    found_predicate_combinations = getSingleMetric('missed-and-found-predicate-combinations', 'found', folderName)
    missed_predicate_combinations = getSingleMetric('missed-and-found-predicate-combinations', 'missed', folderName)
    return -(found_predicate_combinations / (found_predicate_combinations + missed_predicate_combinations))

def calculateFeatureCoverage(folderName):
    global featureName
    found_instances_with_feature = getSingleMetric('valid-tsc-instances-per-tsc', 'featureCount', folderName)
    missed_instances_with_feature = getSingleMetric('missed-tsc-instances-per-tsc', 'featureCount', folderName)
    return -(found_instances_with_feature / (found_instances_with_feature + missed_instances_with_feature))

def tsc_coverage(folderName):
    tsc_coverage = calculateTscCoverage(folderName)
    return tsc_coverage

def tsc_and_feature_combination_coverage(folderName):
    tsc_coverage = calculateTscCoverage(folderName)
    feature_combination_coverage = calculateFeatureCombinationCoverage(folderName)

    total_coverage = (tsc_coverage + feature_combination_coverage) / 2
    return total_coverage

def single_feature_coverage(folderName):
    feature_coverage = calculateFeatureCoverage(folderName)
    return feature_coverage

def segmentation_run(command, folderName):
    global total_execution_time
    global metric

    # Execute stars analysis
    start_time = time.time()
    subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.time()

    # Track execution time
    print(f"Execution time: {(end_time - start_time):.0f} s")
    total_execution_time += (end_time - start_time)

    # Return metric
    metric_function = globals()[metric]
    return metric_function(folderName)

def get_total_execution_time():
    global total_execution_time
    return total_execution_time

def set_TSC(tscName):
    global tsc
    tsc = tscName

def set_metric(metricName):
    global metric
    metric = metricName

def set_featureName(name):
    global featureName
    featureName = name

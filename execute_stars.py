import re
import time
import subprocess
import glob
import os
import json
import uuid

total_execution_time = 0
tsc = "full-TSC"
metric = "metric1"
featureName = "Overtaking"

def by_length(x): # [segmentSize]
    segmentSize = x[0]

    # generate a unique and descriptive folder name
    folderName = f"by_length_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=BY_LENGTH --segmentationValue={segmentSize} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def static_segment_length_seconds(x): # [windowSize, overlapPercentage]
    windowSize, overlapPercentage = x

    # generate a unique and descriptive folder name
    folderName = f"static_segment_length_seconds_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=STATIC_SEGMENT_LENGTH_SECONDS --segmentationValue={windowSize} --secondarySegmentationValue={overlapPercentage} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def static_segment_length_meters(x): # [windowSize, overlapPercentage]
    windowSize, overlapPercentage = x

    # generate a unique and descriptive folder name
    folderName = f"static_segment_length_meters_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=STATIC_SEGMENT_LENGTH_METERS --segmentationValue={windowSize} --secondarySegmentationValue={overlapPercentage} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def dynamic_segment_length_meters_speed_acceleration_1(x): # [lookAhead, stepSize]
    lookAhead, stepSize = x

    # generate a unique and descriptive folder name
    folderName = f"dynamic_segment_length_meters_speed_acceleration_1_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1 --segmentationValue={lookAhead} --secondarySegmentationValue={stepSize} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def dynamic_segment_length_meters_speed(x): # [lookAhead, scalar, stepSize]
    lookAhead, scalar, stepSize = x

    # generate a unique and descriptive folder name
    folderName = f"dynamic_segment_length_meters_speed_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=DYNAMIC_SEGMENT_LENGTH_METERS_SPEED --segmentationValue={lookAhead} --secondarySegmentationValue={scalar} --tertiarySegmentationValue={stepSize} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def sliding_window_multistart_meters(x): # [windowSize1, windowSize2, windowSize3]
    windowSize1, windowSize2, windowSize3 = x

    # generate a unique and descriptive folder name
    folderName = f"sliding_window_multistart_meters_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=SLIDING_WINDOW_MULTISTART_METERS --segmentationValue={windowSize1} --secondarySegmentationValue={windowSize2} --tertiarySegmentationValue={windowSize3} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def sliding_window_multistart_seconds(x): # [windowSize1, windowSize2, windowSize3]
    windowSize1, windowSize2, windowSize3 = x

    # generate a unique and descriptive folder name
    folderName = f"sliding_window_multistart_seconds_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=SLIDING_WINDOW_MULTISTART_SECONDS --segmentationValue={windowSize1} --secondarySegmentationValue={windowSize2} --tertiarySegmentationValue={windowSize3} --saveResults --folderName={folderName} --featureName={featureName}\""
    return segmentation_run(command, folderName)

def getJson(metric, folderName):
    global tsc

    # Go to serialized-results folder and get metric for tsc out of result folder
    folder_path = os.path.join('..', 'stars-carla-experiments', 'serialized-results', folderName, metric, tsc.replace('-',' ') + '.json')
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

def simpleMetric(folderName):
    tsc_coverage = calculateTscCoverage(folderName)
    feature_combination_coverage = calculateFeatureCombinationCoverage(folderName)
    conformity_rate_seconds = getSingleMetric('segment-length-metric', 'conformityRateSeconds', folderName)
    conformity_rate_meters = getSingleMetric('segment-length-metric', 'conformityRateMeters', folderName)

    reward = (tsc_coverage + feature_combination_coverage) / 2
    punishment = -(((1-conformity_rate_seconds)**2 + (1-conformity_rate_meters)**2) / 2)

    return reward - punishment

def specificMetric(folderName):
    tsc_coverage = calculateTscCoverage(folderName)
    feature_combination_coverage = calculateFeatureCombinationCoverage(folderName)
    feature_coverage = calculateFeatureCoverage(folderName)
    conformity_rate_seconds = getSingleMetric('segment-length-metric', 'conformityRateSeconds', folderName)
    conformity_rate_meters = getSingleMetric('segment-length-metric', 'conformityRateMeters', folderName)

    reward = (tsc_coverage + feature_combination_coverage + feature_coverage) / 3
    punishment = -(((1-conformity_rate_seconds)**2 + (1-conformity_rate_meters)**2) / 2)
    
    return reward - punishment

def segmentation_run(command, folderName):
    global total_execution_time
    global metric

    # Execute stars analysis
    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
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
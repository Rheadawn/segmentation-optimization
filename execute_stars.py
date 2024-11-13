import re
import time
import subprocess
import glob
import os
import json
import uuid

total_execution_time = 0

def by_length(x): # [segmentSize]
    segmentSize = x[0]

    # generate a unique and descriptive folder name
    folderName = f"by_length_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=BY_LENGTH --segmentationValue={segmentSize} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def static_segment_length_seconds(x): # [windowSize, overlapPercentage]
    windowSize, overlapPercentage = x

    # generate a unique and descriptive folder name
    folderName = f"static_segment_length_seconds_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=STATIC_SEGMENT_LENGTH_SECONDS --segmentationValue={windowSize} --secondarySegmentationValue={overlapPercentage} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def static_segment_length_meters(x): # [windowSize, overlapPercentage]
    windowSize, overlapPercentage = x

    # generate a unique and descriptive folder name
    folderName = f"static_segment_length_meters_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=STATIC_SEGMENT_LENGTH_METERS --segmentationValue={windowSize} --secondarySegmentationValue={overlapPercentage} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def dynamic_segment_length_meters_speed_acceleration_1(x): # [lookAhead, stepSize]
    lookAhead, stepSize = x

    # generate a unique and descriptive folder name
    folderName = f"dynamic_segment_length_meters_speed_acceleration_1_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1 --segmentationValue={lookAhead} --secondarySegmentationValue={stepSize} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def dynamic_segment_length_meters_speed(x): # [lookAhead, scalar, stepSize]
    lookAhead, scalar, stepSize = x

    # generate a unique and descriptive folder name
    folderName = f"dynamic_segment_length_meters_speed_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=DYNAMIC_SEGMENT_LENGTH_METERS_SPEED --segmentationValue={lookAhead} --secondarySegmentationValue={scalar} --tertiarySegmentationValue={stepSize} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def sliding_window_multistart_meters(x): # [windowSize1, windowSize2, windowSize3]
    windowSize1, windowSize2, windowSize3 = x

    # generate a unique and descriptive folder name
    folderName = f"sliding_window_multistart_meters_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=SLIDING_WINDOW_MULTISTART_METERS --segmentationValue={windowSize1} --secondarySegmentationValue={windowSize2} --tertiarySegmentationValue={windowSize3} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def sliding_window_multistart_seconds(x): # [windowSize1, windowSize2, windowSize3]
    windowSize1, windowSize2, windowSize3 = x

    # generate a unique and descriptive folder name
    folderName = f"sliding_window_multistart_seconds_{tsc}_{metric}_{uuid.uuid4()}"

    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=SLIDING_WINDOW_MULTISTART_SECONDS --segmentationValue={windowSize1} --secondarySegmentationValue={windowSize2} --tertiarySegmentationValue={windowSize3} --saveResults --folderName={folderName}\""
    return segmentation_run(command, folderName)

def segmentation_run(command):
    global total_execution_time

    # Execute stars analysis
    start_time = time.time()
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    end_time = time.time()
    print(f"Execution time: {(end_time - start_time):.0f} s")
    total_execution_time += (end_time - start_time)

    # Go to analysis-result-logs folder
    folders = glob.glob(os.path.join(r"..\stars-carla-experiments\analysis-result-logs", '*'))

    # Get info file of newest analysis
    newest_folder = max(folders, key=os.path.getmtime)
    subfolder_path = os.path.join(newest_folder, r"metrics\valid-tsc-instances-per-projection")
    files = glob.glob(os.path.join(subfolder_path, '*info*'))

    # Get the first number of the info file (number of valid instances for 'all')
    result = 0
    with open(files[0], 'r') as f:
        for word in f.readline().split():
            if re.match(r'^\d+$', word):
                result = int(word)
                break

    return -result

def get_total_execution_time():
    global total_execution_time
    return total_execution_time
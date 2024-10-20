import os
import glob
import subprocess
import re
import time

total_execution_time = 0

def default_run(x):
    global total_execution_time

    # Execute stars analysis
    start_time = time.time()
    command = f"cd ../stars-carla-experiments & gradlew run --args=\"--segmentationType=BY_LENGTH --segmentationValue={x}\""
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

    return result

def get_total_execution_time():
    global total_execution_time
    return total_execution_time
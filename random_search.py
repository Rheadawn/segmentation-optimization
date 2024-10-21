import random
import time
import argparse
from execute_stars import get_total_execution_time
from functionSelector import getBounds, getMethod, getNumberOfDimensions

def random_search_one_dimension():
    maxResult = 0
    print("\n| result | segmentSize |")
    print("\n|---|---|")
    for i in range(0, args.numberOfIterations, 1):
        x = random.uniform(pbounds['x'][0], pbounds['x'][1])
        result = method(x)
        print(f"\n| {result} | {x:.2f} |")
        if result > maxResult:
            maxResult = result
    return maxResult

def random_search_two_dimensions():
    maxResult = 0
    if args.segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        print("\n| result | lookAhead | stepSize |")
    else:
        print("\n| result | windowSize | overlapPercentage |")
    print("\n|---|---|---|")
    for i in range(0, args.numberOfIterations, 1):
        x = random.uniform(pbounds['x'][0], pbounds['x'][1])
        y = random.uniform(pbounds['y'][0], pbounds['y'][1])
        result = method(x, y)
        print(f"\n| {result} | {x:.2f} | {y:.2f} |")
        if result > maxResult:
            maxResult = result
    return maxResult

def random_search_three_dimensions():
    maxResult = 0
    if args.segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        print("\n| result | lookAhead | scalar | stepSize |")
    else:
        print("\n| result | windowSize1 | windowSize2 | windowSize3 |")
    print("\n|---|---|---|---|")
    for i in range(0, args.numberOfIterations, 1):
        x = random.uniform(pbounds['x'][0], pbounds['x'][1])
        y = random.uniform(pbounds['y'][0], pbounds['y'][1])
        z = random.uniform(pbounds['z'][0], pbounds['z'][1])
        result = method(x, y, z)
        print(f"\n| {result} | {x:.2f} | {y:.2f} | {z:.2f} |")
        if result > maxResult:
            maxResult = result
    return maxResult

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Grid Search for optimizing the segmentation used in STARS')
parser.add_argument('--segmentationType', type=str, default="BY_BLOCK", help='Name of the used segmentation method')
parser.add_argument('--numberOfIterations', type=int, default=30, help='Number of iterations for the random search')

args = parser.parse_args()

# Bounded region of parameter space
pbounds = getBounds(args.segmentationType)
method = getMethod(args.segmentationType)
dimCount = getNumberOfDimensions(args.segmentationType)

start_time = time.time()
maxResult = 0
if(dimCount == 1):
    maxResult = random_search_one_dimension()
elif(dimCount == 2):
    maxResult = random_search_two_dimensions()
elif(dimCount == 3):
    maxResult = random_search_three_dimensions()
end_time = time.time()

print(f"\nMAXIMUM: {maxResult}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")
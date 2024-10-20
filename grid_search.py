import time
import argparse
from execute_stars import get_total_execution_time
from functionSelector import getBounds, getMethod, getNumberOfDimensions

def floatRange(start, stop, step):
    while start < stop:
        yield start
        start += step

def grid_search_one_dimension():
    maxResult = 0
    print("\n| result | segmentSize |")
    print("\n|---|---|")
    for i in floatRange(pbounds['x'][0], pbounds['x'][1], args.stepSizeDim1):
        result = method(i)
        print(f"\n| {result} | {i} |")
        if result > maxResult:
            maxResult = result
    return maxResult

def grid_search_two_dimensions():
    maxResult = 0
    if args.segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        print("\n| result | lookAhead | stepSize |")
    else:
        print("\n| result | windowSize | overlapPercentage |")
    print("\n|---|---|---|")
    for i in floatRange(pbounds['x'][0], pbounds['x'][1], args.stepSizeDim1):
        for j in floatRange(pbounds['y'][0], pbounds['y'][1], args.stepSizeDim2):
            result = method(i, j)
            print(f"\n| {result} | {i} | {j} |")
            if result > maxResult:
                maxResult = result
    return maxResult
 
def grid_search_three_dimensions():
    maxResult = 0
    print("\n| result | lookAhead | scalar | stepSize |")
    print("\n|---|---|---|---|")
    for i in floatRange(pbounds['x'][0], pbounds['x'][1], args.stepSizeDim1):
        for j in floatRange(pbounds['y'][0], pbounds['y'][1], args.stepSizeDim2):
            for k in floatRange(pbounds['z'][0], pbounds['z'][1], args.stepSizeDim3):
                result = method(i, j, k)
                print(f"\n| {result} | {i} | {j} | {k} |")
                if result > maxResult:
                    maxResult = result
    return maxResult

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Grid Search for optimizing the segmentation used in STARS')
parser.add_argument('--segmentationType', type=str, default="BY_BLOCK", help='Name of the used segmentation method')
parser.add_argument('--stepSizeDim1', type=float, default=10.0, help='Width of the grid search in the first dimension')
parser.add_argument('--stepSizeDim2', type=float, default=10.0, help='Width of the grid search in the second dimension')
parser.add_argument('--stepSizeDim3', type=float, default=10.0, help='Width of the grid search in the third dimension')

args = parser.parse_args()

# Bounded region of parameter space
pbounds = getBounds(args.segmentationType)
method = getMethod(args.segmentationType)
dimCount = getNumberOfDimensions(args.segmentationType)

start_time = time.time()
maxResult = 0
if(dimCount == 1):
    maxResult = grid_search_one_dimension()
elif(dimCount == 2):
    maxResult = grid_search_two_dimensions()
elif(dimCount == 3):
    maxResult = grid_search_three_dimensions()
end_time = time.time()

print(f"\nMAXIMUM: {maxResult}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")
import time
import argparse
from execute_stars import get_total_execution_time, set_TSC, set_metric, set_featureName
from functionSelector import getBounds, getMethod, getNumberOfDimensions

def floatRange(start, stop, step):
    while start <= stop:
        yield start
        start += step

def grid_search_one_dimension():
    maxResult = 0
    print("| result | segmentSize |")
    print("|---|---|")
    for i in floatRange(pbounds[0][0], pbounds[0][1], args.stepSizeDim1):
        result = method([i])
        print(f"| {result} | {i} |")
        if result > maxResult:
            maxResult = result
    return maxResult

def grid_search_two_dimensions():
    maxResult = 0
    if args.segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1":
        print("| result | lookAhead | stepSize |")
    else:
        print("| result | windowSize | overlapPercentage |")
    print("|---|---|---|")
    for i in floatRange(pbounds[0][0], pbounds[0][1], args.stepSizeDim1):
        for j in floatRange(pbounds[1][0], pbounds[1][1], args.stepSizeDim2):
            result = method([i, j])
            print(f"| {result} | {i} | {j} |")
            if result > maxResult:
                maxResult = result
    return maxResult
 
def grid_search_three_dimensions():
    maxResult = 0
    if args.segmentationType == "DYNAMIC_SEGMENT_LENGTH_METERS_SPEED":
        print("| result | lookAhead | scalar | stepSize |")
    else:
        print("| result | windowSize1 | windowSize2 | windowSize3 |")
    print("|---|---|---|---|")
    for i in floatRange(pbounds[0][0], pbounds[0][1], args.stepSizeDim1):
        for j in floatRange(pbounds[1][0], pbounds[1][1], args.stepSizeDim2):
            for k in floatRange(pbounds[2][0], pbounds[2][1], args.stepSizeDim3):
                result = method([i, j, k])
                print(f"| {result} | {i} | {j} | {k} |")
                if result > maxResult:
                    maxResult = result
    return maxResult

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Grid Search for optimizing the segmentation used in STARS')
parser.add_argument('--segmentationType', type=str, default="BY_BLOCK", help='Name of the used segmentation method')
parser.add_argument('--stepSizeDim1', type=float, default=10.0, help='Width of the grid search in the first dimension')
parser.add_argument('--stepSizeDim2', type=float, default=10.0, help='Width of the grid search in the second dimension')
parser.add_argument('--stepSizeDim3', type=float, default=10.0, help='Width of the grid search in the third dimension')
parser.add_argument('--tsc', type=str, default="full-TSC", help='Name of the used TSC')
parser.add_argument('--metric', type=str, default="simpleMetric", help='Name of the used metric')
parser.add_argument('--featureName', type=str, default="Overtaking", help='Name of the feature to be used in the quality metric')


custom_args = ["--segmentationType","DYNAMIC_SEGMENT_LENGTH_METERS_SPEED_ACCELERATION_1","--stepSizeDim1","5.0","--stepSizeDim2","1.0","--tsc","full-TSC","--metric","simpleMetric"]
args = parser.parse_args(custom_args)

set_TSC(args.tsc)
set_metric(args.metric)
set_featureName(args.featureName)

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

print(f"MAXIMUM: {maxResult}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")





custom_args = ["--segmentationType","STATIC_SEGMENT_LENGTH_SECONDS","--stepSizeDim1","5.0","--stepSizeDim2","1.0","--tsc","full-TSC","--metric","simpleMetric"]
args = parser.parse_args(custom_args)

set_TSC(args.tsc)
set_metric(args.metric)
set_featureName(args.featureName)

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

print(f"MAXIMUM: {maxResult}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")





custom_args = ["--segmentationType","STATIC_SEGMENT_LENGTH_METERS","--stepSizeDim1","10.0","--stepSizeDim2","1.0","--tsc","full-TSC","--metric","simpleMetric"]
args = parser.parse_args(custom_args)

set_TSC(args.tsc)
set_metric(args.metric)
set_featureName(args.featureName)

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

print(f"MAXIMUM: {maxResult}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")











custom_args = ["--segmentationType","DYNAMIC_SEGMENT_LENGTH_METERS_SPEED","--stepSizeDim1","5.0","--stepSizeDim2","100.0","--stepSizeDim3","1.0","--tsc","full-TSC","--metric","simpleMetric"]
args = parser.parse_args(custom_args)

set_TSC(args.tsc)
set_metric(args.metric)
set_featureName(args.featureName)

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

print(f"MAXIMUM: {maxResult}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")
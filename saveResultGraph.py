import argparse
import glob
import json
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Saves a graph for the given segmentationType and metric')
parser.add_argument('--segmentationType', type=str, default="BY_LENGTH", help='Name of the segmentation method to get the data from')
parser.add_argument('--metric', type=str, default="valid-tsc-instances-per-tsc", help='Name of the metric beeing shown in the graph')
parser.add_argument('--metricKey', type=str, default="count", help='Key for the metric json')
parser.add_argument('--tsc', type=str, default="full-TSC", help='Name of the used TSC')
args = parser.parse_args()

# save all folders with the --segmentationType in its name for the path ./serialized-results
json_files = glob.glob(os.path.join('.', 'serialized-results', f"*{args.segmentationType}*", args.metric, args.tsc.replace('-',' ') + '.json'))
numbers = []

for index,json_file in enumerate(json_files):
    fileContent = open(json_files[index], 'r').read()
    metric = json.loads(fileContent)
    numbers.append(metric[args.metrciKey])

# plot the numbers in a graph
plt.plot(numbers)
plt.title(f'{args.segmentationType}-{args.tsc}')
plt.xlabel(args.metric)
plt.ylabel(args.metricKey)
plt.savefig(f'{args.segmentationType}-{args.metric}-{args.metricKey}-{args.tsc}.png')
import time
import argparse
from bayes_opt import BayesianOptimization
from execute_stars import get_total_execution_time
from functionSelector import getBounds, getMethod

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Bayesian Optimization for optimizing the segmentation used in STARS')
parser.add_argument('--segmentationType', type=str, default="BY_BLOCK", help='Name of the used segmentation method')
parser.add_argument('--init_points', type=int, default=10, help='Number of initial points probed by the optimizer')
parser.add_argument('--n_iter', type=int, default=25, help='Number of iterations the optimizer uses after probing')

args = parser.parse_args()

# Bounded region of parameter space
pbounds = getBounds(args.segmentationType)
method = getMethod(args.segmentationType)

optimizer = BayesianOptimization(
    f=method,
    pbounds=pbounds,
    random_state=1,
)

start_time = time.time()
optimizer.maximize(
    init_points=10,
    n_iter=25,
)
end_time = time.time()

print(f"\nMAXIMUM: {optimizer.max}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")
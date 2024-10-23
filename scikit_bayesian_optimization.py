import time
import argparse
import matplotlib.pyplot as plt
from skopt import gp_minimize
from execute_stars import get_total_execution_time
from functionSelector import getBounds, getMethod
from skopt.plots import plot_convergence

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Bayesian Optimization for optimizing the segmentation used in STARS')
parser.add_argument('--segmentationType', type=str, default="BY_LENGTH", help='Name of the used segmentation method')
parser.add_argument('--acq_func', type=str, default="EI", help='Name of the used aquisition function')
parser.add_argument('--n_random_starts', type=int, default=1, help='Number of initial points probed by the optimizer')
parser.add_argument('--n_calls', type=int, default=2, help='Number of iterations the optimizer uses after probing')

args = parser.parse_args()

# Bounded region of parameter space
pbounds = getBounds(args.segmentationType)
method = getMethod(args.segmentationType)

start_time = time.time()
res = gp_minimize(method,                                # the function to minimize
                  pbounds,                               # the bounds on each dimension of x
                  acq_func=args.acq_func,                # the acquisition function
                  n_calls=args.n_calls,                  # the number of evaluations of f
                  n_random_starts=args.n_random_starts,  # the number of random initialization points
                  random_state=1)                        # the random seed
end_time = time.time()

res.fun = -res.fun
res.func_vals = [-val for val in res.func_vals]

for i in range(0, len(res.x_iters)):
    print(f"ITERATION {i+1}: {res.x_iters[i][0]} -> {res.func_vals[i]}")

print(f"\nMAXIMUM: {res.fun}")
print(f"STARS execution time: {get_total_execution_time():.0f} s")
print(f"Total execution time: {(end_time - start_time):.0f} s")

plot_convergence(res)
filename = f"convergence/convergence_plot_init_{args.n_random_starts}_iter_{args.n_calls}_max_{res.fun}"
plt.savefig(filename)
with open(filename + ".txt", "w") as file:
    for key, value in res.items():
        file.write('%s:%s\n' % (key, value))
import time
import argparse
import matplotlib.pyplot as plt
import json
from skopt import gp_minimize
from execute_stars import get_total_execution_time, set_TSC, set_metric, set_featureName
from functionSelector import getBounds, getMethod
from skopt.plots import plot_convergence, plot_gaussian_process



# Parse segmentation parameters
parser = argparse.ArgumentParser(description='Bayesian Optimization for optimizing the segmentation used in STARS')
parser.add_argument('--segmentationType', type=str, default="BY_LENGTH", help='Name of the used segmentation method')
parser.add_argument('--tsc', type=str, default="full-TSC", help='Name of the used TSC')
parser.add_argument('--metric', type=str, default="tsc_coverage", help='Name of the used metric')
parser.add_argument('--featureName', type=str, default="Overtaking", help='Name of the feature to be used in the quality metric')

# Parse Bayesian Optimization parameters
parser.add_argument('--n_random_starts', type=int, default=1, help='Number of initial points probed by the optimizer')
parser.add_argument('--n_calls', type=int, default=2, help='Number of iterations the optimizer uses after probing')

# Parse and store arguments
args = parser.parse_args()
set_TSC(args.tsc)
set_metric(args.metric)
set_featureName(args.featureName)



# Bounded region of parameter space
pbounds = getBounds(args.segmentationType)
method = getMethod(args.segmentationType)

start_time = time.time()
res = gp_minimize(method,                                   # the function to minimize
                  pbounds,                                  # the bounds on each dimension of x
                  acq_func="EI",                            # the acquisition function
                  n_calls=args.n_calls,                     # the number of evaluations of f
                  n_initial_points=args.n_random_starts,    # the number of random initialization points
                  random_state=42,                          # the random seed
                  initial_point_generator="sobol",          # the initial points are generated using a Sobol sequence
                  acq_optimizer="lbfgs"                     # the optimizer used to minimize the acquisition function
                  )                        
end_time = time.time()

# invert the result back, because it was inverted for the optimization
res.fun = -res.fun 
res.func_vals = [-val for val in res.func_vals]



# save metadata
with open(f"optimization_results/metadata_{args.segmentationType}_{args.metric}.json", "w") as file:
    json.dump({"segmentationType": args.segmentationType, "metric": args.metric, "tsc": args.tsc, "featureName": args.featureName, "n_random_starts": args.n_random_starts, "n_calls": args.n_calls, "stars_execution_time": get_total_execution_time(), "total_execution_time": (end_time - start_time)}, file)

# save results for all parameter combiantions analyzed
with open(f"optimization_results/iterations_{args.segmentationType}_{args.metric}.json", "w") as file:
    json.dump([{"parameters": [{"value": res.x_iters[i][j]} for j in range (0, len(res.x_iters[i]))], "result": res.func_vals[i]} for i in range(0, len(res.x_iters))], file)

# save convergence plot
plot_convergence(res)
filename = f"optimization_results/convergence_plot_{args.segmentationType}_{args.metric}.png"
plt.savefig(filename)

# save surrogate model plots
for i in range(0, len(res.x_iters)):
    # Plot surrogate model
    plt.subplot(1, 2, 1)
    ax = plot_gaussian_process(res, 
                               n_calls=i,
                               show_title=False,
                               show_next_point=True
                               )
    ax.set_ylabel("")
    ax.set_xlabel("")

    # Plot EI(x)
    plt.subplot(1, 2, 2)
    ax = plot_gaussian_process(res, 
                               n_calls=i,
                               show_title=False,
                               show_mu=False, 
                               show_acq_func=True,
                               show_observations=False,
                               show_next_point=True
                               )
    ax.set_ylabel("")
    ax.set_xlabel("")

    # Save plot
    filename = f"optimization_results/surrogate_models_plot_{args.segmentationType}_{args.metric}_{i}.png"
    plt.savefig(filename)
import time
from bayes_opt import BayesianOptimization
from execute_stars import default_run
from execute_stars import get_total_execution_time


# Bounded region of parameter space
pbounds = {'x': (100, 200)}

optimizer = BayesianOptimization(
    f=default_run,
    pbounds=pbounds,
    random_state=1,
)

start_time = time.time()
optimizer.maximize(
    init_points=2,
    n_iter=1,
)
end_time = time.time()

print(f"\nMAXIMUM: {optimizer.max}\n")
print(f"STARS execution time: {get_total_execution_time():.0f} s\n")
print(f"Total execution time: {(end_time - start_time):.0f} s\n")
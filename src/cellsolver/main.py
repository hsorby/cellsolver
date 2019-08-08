
import sys
import time

import matplotlib.pyplot as graph
from scipy.integrate import ode

from cellsolver.codesamples import hodgkin_huxley_squid_axon_model_1952 as hh


KNOWN_SOLVERS = ['euler', 'dop853', 'vode']

run_timeit = False

class TimeExecution(object):

    def __init__(self, number=10):
        if number < 1:
            number = 10
        self._number = number

    def __call__(self, f):
        global run_timeit
        def wrapped_f(*args, **kwargs):
            if run_timeit:
                ts = time.time()
                for _ in range(self._number):
                    f(*args, **kwargs)
                te = time.time()
                print('%r  average = %2.2f ms' % \
                      (f.__name__, ((te - ts) * 1000)/self._number))

            return f(*args, **kwargs)

        return wrapped_f

def initialize_system(system):
    rates = system.createRateVector()
    states = system.createStateVector()
    variables = system.createVariableVector()

    system.initializeConstants(states, variables)
    system.computeComputedConstants(variables)

    return states, rates, variables

@TimeExecution(number=10)
def solve_using_euler(system, step_size, interval):
    states, rates, variables = initialize_system(system)

    results = [ [] for _ in range(len(states)) ]
    x = []

    t = interval[0]
    end = interval[-1]
    while t < end:
        hh.computeRates(t, states, rates, variables)
        delta = list(map(lambda var: var * step_size, rates))
        states = [sum(x) for x in zip(states, delta)]

        x.append(t)
        for index, value in enumerate(states):
            results[index].append(value)

        t += step_size

    return x, results

def update(voi, states, rates, variables):
    hh.computeRates(voi, states, rates, variables)
    return rates

@TimeExecution(number=10)
def solve_using_dop853(system, step_size, interval):
    return solve_using_scipy(system, "dop853", step_size, interval)

@TimeExecution(number=10)
def solve_using_vode(system, step_size, interval):
    return solve_using_scipy(system, "vode", step_size, interval)

def solve_using_scipy(system, method, step_size, interval):
    states, rates, variables = initialize_system(system)

    results = [ [] for _ in range(len(states)) ]
    x = []

    solver = ode(update)
    solver.set_integrator(method)
    solver.set_initial_value(states, interval[0])
    solver.set_f_params(rates, variables)

    end = interval[-1]
    while solver.successful() and solver.t < end:
        solver.integrate(solver.t + step_size)

        x.append(solver.t)
        for index, value in enumerate(solver.y):
            results[index].append(value)

    return x, results

def main():
    global run_timeit
    args = sys.argv[:]
    args.pop(0)
    if "timeit" in args:
        args.remove("timeit")
        run_timeit = True
    if len(args):
        solver_type = args.pop(0)
        if solver_type not in KNOWN_SOLVERS:
            print("Unknown solver {0} reverting to Euler instead.".format(solver_type))
            solver_type = "euler"
    else:
        solver_type = "euler"

    step_size = 0.001
    interval = [0.0, 65.35]

    if solver_type == "euler":
        [x, y_n] = solve_using_euler(hh, step_size, interval)
    elif solver_type == "dop853":
        [x, y_n] = solve_using_dop853(hh, step_size, interval)
    elif solver_type == "vode":
        [x, y_n] = solve_using_vode(hh, step_size, interval)
    else:
        x = []
        y_n = []

    graph.xlabel("Time (msecs)")
    graph.ylabel("Y-axis")
    graph.title("A test graph")
    for index, result in enumerate(y_n):
        graph.plot(x, result, label='id {0}'.format(index))
    graph.legend()
    graph.show()


if __name__ == "__main__":
    main()

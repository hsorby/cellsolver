
import os
import time
import argparse
import importlib.util

from scipy.integrate import ode

from cellsolver.codesamples import hodgkin_huxley_squid_axon_model_1952 as hh
from cellsolver.plot import plot_solution


KNOWN_SOLVERS = ['euler', 'dop853', 'vode']


class TimeExecution(object):

    number = 10
    run_timeit = False

    def __init__(self, f):
        self._f = f

    def __call__(self, *args, **kwargs):

        if TimeExecution.run_timeit:
            ts = time.time()
            for _ in range(TimeExecution.number):
                self._f(*args, **kwargs)
            te = time.time()
            print('%r  average = %2.2f ms' %
                  (self._f.__name__, ((te - ts) * 1000)/TimeExecution.number))

        return self._f(*args, **kwargs)


def initialize_system(system):
    rates = system.create_states_array()
    states = system.create_states_array()
    variables = system.create_variables_array()
    resets = system.create_resets_array()

    system.initialize_states_and_constants(states, variables)
    system.compute_computed_constants(variables)

    return states, rates, variables, resets


@TimeExecution
def solve_using_euler(system, step_size, interval):
    states, rates, variables, resets = initialize_system(system)

    if isinstance(step_size, list):
        step_size = step_size[0]

    results = [[] for _ in range(len(states))]
    x = []

    t = interval[0]
    end = interval[-1]

    system.compute_reset_test_value_differences(t, states, variables, resets)
    new_resets = resets[:]

    while (t + step_size) <= end:
        x.append(t)
        for index, value in enumerate(states):
            results[index].append(value)

        system.compute_rates(t, states, rates, variables)

        delta = list(map(lambda var: var * step_size, rates))
        states = [sum(x) for x in zip(states, delta)]

        system.compute_reset_test_value_differences(t, states, variables, resets)
        activated_resets = [(resets[i] * b) <= 0.0 for i, b in enumerate(new_resets)]
        system.apply_resets(t, states, variables, activated_resets)

        resets = new_resets[:]

        t += step_size

    return x, results


def update(voi, states, system, rates, variables):
    system.compute_rates(voi, states, rates, variables)
    return rates


@TimeExecution
def solve_using_dop853(system, step_size, interval):
    return solve_using_scipy(system, "dop853", step_size, interval)


@TimeExecution
def solve_using_vode(system, step_size, interval):
    return solve_using_scipy(system, "vode", step_size, interval)


def solve_using_scipy(system, method, step_size, interval):
    states, rates, variables, resets = initialize_system(system)

    if isinstance(step_size, list):
        step_size = step_size[0]

    results = [[] for _ in range(len(states))]
    x = []

    solver = ode(update)
    solver.set_integrator(method)
    solver.set_initial_value(states, interval[0])
    solver.set_f_params(system, rates, variables)

    system.compute_reset_test_value_differences(solver.t, states, variables, resets)
    new_resets = resets[:]

    x.append(solver.t)
    for index, value in enumerate(solver.y):
        results[index].append(value)

    end = interval[-1]
    while solver.successful() and (solver.t + step_size) <= end:
        solver.integrate(solver.t + step_size)

        system.compute_reset_test_value_differences(solver.t, solver.y, variables, resets)
        activated_resets = [(resets[i] * r) <= 0.0 for i, r in enumerate(new_resets)]
        system.apply_resets(solver.t, solver.y, variables, activated_resets)
        if any(activated_resets):
            solver.set_initial_value(solver.y, solver.t)
            print('activated reset!')

        resets = new_resets[:]

        x.append(solver.t)
        for index, value in enumerate(solver.y):
            results[index].append(value)

    return x, results


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_valid_file(parser, arg):
    expanded_path = os.path.expanduser(arg)
    expanded_path = os.path.expandvars(expanded_path)
    full_path = os.path.abspath(expanded_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        module_name = os.path.splitext(os.path.basename(full_path))[0]
        loaded_module = module_from_file(module_name, full_path)
        return loaded_module  # return the actual loaded module
    else:
        parser.error("The file %s does not exist!" % arg)


def process_arguments():
    parser = argparse.ArgumentParser(description="Solve ODE's described by libCellML generated Python output.")
    parser.add_argument('--solver', default=KNOWN_SOLVERS[0],
                        help='specify the solver: {0} (default: {1})'.format(KNOWN_SOLVERS, KNOWN_SOLVERS[0]))
    parser.add_argument('--timeit', action='store', type=int, nargs='?', const=10, default=0,
                        help='number of iterations for evaluating execution elapsed time (default: 0)')
    parser.add_argument('--interval', action='store', type=float, nargs=2, default=[0.0, 100.0],
                        help='interval to run the simulation for (default: [0.0, 100.0])')
    parser.add_argument('--step-size', action='store', type=float, nargs=1, default=0.001,
                        help='the step size to output results at (default: 0.001)')
    parser.add_argument('module', nargs='?', default=hh, type=lambda file_name: is_valid_file(parser, file_name),
                        help='a module of Python code generated by libCellML')

    return parser


def main():

    parser = process_arguments()
    args = parser.parse_args()

    TimeExecution.run_timeit = args.timeit > 0
    if TimeExecution.run_timeit:
        TimeExecution.number = args.timeit

    valid_solution = True
    if args.solver == "euler":
        [x, y_n] = solve_using_euler(args.module, args.step_size, args.interval)
    elif args.solver == "dop853":
        [x, y_n] = solve_using_dop853(args.module, args.step_size, args.interval)
    elif args.solver == "vode":
        [x, y_n] = solve_using_vode(args.module, args.step_size, args.interval)
    else:
        x = []
        y_n = []
        valid_solution = False
        print("Unknown solver '{0}'.".format(args.solver))
        parser.print_help()

    if valid_solution:
        plot_solution(x, y_n, args.module.VOI_INFO, args.module.STATE_INFO, args.module.__name__)


if __name__ == "__main__":
    main()

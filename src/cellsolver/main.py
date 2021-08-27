import argparse
import importlib
import json
import os
import pickle

from cellsolver.codesamples import hodgkin_huxley_squid_axon_model_1952 as hh
from cellsolver.plot import plot_solution
from cellsolver.utilities import TimeExecution, load_config, info_items_list, not_matching_info_items, matching_info_items

KNOWN_SOLVERS = ['euler', 'dop853', 'vode']


def convert_version_to_module_name(version):
    modified_version = version.replace('.', '_')
    return f'version_{modified_version}'


def system_is_reset_capable(system):
    if hasattr(system, 'create_resets_array') and hasattr(system, 'compute_reset_test_value_differences') and hasattr(system, 'apply_resets'):
        return True

    return False


def system_has_external_variables(system):
    if hasattr(system, 'initialise_states_and_constants') and hasattr(system, 'compute_rates') and hasattr(system, 'compute_variables'):
        def dummy_initial_function(index):
            return 0.0

        def dummy_function(voi, states, rates, variables, index):
            return 1.0

        try:
            system.initialise_states_and_constants(None, None, dummy_initial_function)
            system.compute_rates(None, None, None, None, dummy_function)
            system.compute_variables(None, None, None, None, dummy_function)
        except TypeError as e:
            if f'{e}' == "'NoneType' object does not support item assignment":
                return True

        return False

    return False


def system_solver(system):
    generation_version = convert_version_to_module_name(system.__version__)
    module_name = f'cellsolver.solvers.{generation_version}'
    if system_is_reset_capable(system):
        module_name += '_reset_capable'
    if system_has_external_variables(system):
        module_name += '_external_variables'
    i = importlib.import_module(module_name)
    return i


@TimeExecution
def solve_using_euler(system, step_size, interval, external_module=None):
    solver_module = system_solver(system)
    return solver_module.euler_based_solver(system, step_size, interval, external_module)


@TimeExecution
def solve_using_dop853(system, step_size, interval, external_module=None):
    solver_module = system_solver(system)
    return solver_module.scipy_based_solver(system, "dop853", step_size, interval, external_module)


@TimeExecution
def solve_using_vode(system, step_size, interval, external_module=None):
    solver_module = system_solver(system)
    return solver_module.scipy_based_solver(system, "vode", step_size, interval, external_module)


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def full_path_to_file(arg):
    expanded_path = os.path.expanduser(arg)
    expanded_path = os.path.expandvars(expanded_path)
    return os.path.abspath(expanded_path)


def is_valid_file(arg):
    full_path = full_path_to_file(arg)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return True

    return False


def possible_json_file(parser, arg):
    if is_valid_file(arg):
        full_path = full_path_to_file(arg)
        try:
            with open(full_path) as f:
                content = f.read()

            json.loads(content)
            return full_path
        except json.JSONDecodeError:
            parser.error(f"The config file {arg} is not valid JSON!")
    elif arg is None:
        return ''

    parser.error(f"The config file {arg} does not exist!")


def valid_module(parser, arg):
    if is_valid_file(arg):
        full_path = full_path_to_file(arg)
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
    parser.add_argument('--config', type=lambda file_name: possible_json_file(parser, file_name), nargs='?', default=None,
                        help='a JSON configuration file')
    parser.add_argument('--output-file', default=None,
                        help='specify an output file')
    parser.add_argument('--ext-var', nargs='?', default=None, type=lambda file_name: valid_module(parser, file_name),
                        help='a module of Python code that supplies external variable functions for the module')
    parser.add_argument('module', nargs='?', default=hh, type=lambda file_name: valid_module(parser, file_name),
                        help='a module of Python code generated by libCellML')

    return parser


def apply_config(config, y_n, y_info):
    indices = range(len(y_n))
    if 'plot_excludes' in config:
        info_items = info_items_list(config['plot_excludes'])
        indices = [x for x, z in enumerate(y_info) if not_matching_info_items(z, info_items)]
    if 'plot_includes' in config:
        info_items = info_items_list(config['plot_includes'])
        indices = [x for x, z in enumerate(y_info) if matching_info_items(z, info_items)]

    y_n_out = [y_n[i] for i in indices]
    y_info_out = [y_info[i] for i in indices]
    return y_n_out, y_info_out


def main():
    parser = process_arguments()
    args = parser.parse_args()

    config = {'show_plot': True, 'save_output_to_file': False}

    if args.config is not None:
        config.update(load_config(args.config))

    TimeExecution.run_timeit = args.timeit > 0
    if TimeExecution.run_timeit:
        TimeExecution.number = args.timeit

    external_module = None
    if args.ext_var is not None:
        external_module = args.ext_var

    valid_solution = True
    if args.solver == "euler":
        [x, y_n] = solve_using_euler(args.module, args.step_size, args.interval, external_module)
    elif args.solver == "dop853":
        [x, y_n] = solve_using_dop853(args.module, args.step_size, args.interval, external_module)
    elif args.solver == "vode":
        [x, y_n] = solve_using_vode(args.module, args.step_size, args.interval, external_module)
    else:
        x = []
        y_n = []
        valid_solution = False
        print("Unknown solver '{0}'.".format(args.solver))
        parser.print_help()

    if valid_solution:
        y_n_wanted, state_info_wanted = apply_config(config, y_n, args.module.STATE_INFO)
        plot_title = args.module.__name__

        if config['show_plot']:
            plot_solution(x, y_n_wanted, args.module.VOI_INFO, state_info_wanted, plot_title)

        if args.output_file is not None:
            with open(args.output_file, 'wb') as f:
                pickle.dump({'x': x, 'x_info': args.module.VOI_INFO, 'y_n': y_n_wanted, 'y_n_info': state_info_wanted, 'title': plot_title}, f)


if __name__ == "__main__":
    main()

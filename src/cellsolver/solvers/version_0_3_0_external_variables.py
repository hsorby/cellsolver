
from scipy.integrate import ode

from cellsolver.utilities import apply_config


def initialize_system(system, external_variable_function):
    rates = system.create_states_array()
    states = system.create_states_array()
    variables = system.create_variables_array()

    system.initialise_states_and_constants(states, variables, external_variable_function)
    system.compute_computed_constants(variables)

    return states, rates, variables


def store_result(results, states, state_indices, variables, variable_indices):

    state_indices_size = len(state_indices)
    for index, state_index in enumerate(state_indices):
        results[index].append(states[state_index])

    for index, variable_index in enumerate(variable_indices):
        results[state_indices_size + index].append(variables[variable_index])


def euler_based_solver(system, simulation_parameters, external_module):
    state_indices = apply_config(simulation_parameters['result']['config'], system.STATE_INFO)
    variable_indices = apply_config(simulation_parameters['result']['config'], system.VARIABLE_INFO)
    states, rates, variables = initialize_system(system, external_module.initialise_external_variable)

    step_size = simulation_parameters['integration']['step_size']
    interval = simulation_parameters['integration']['interval']
    output_step_size = simulation_parameters['result']['step_size']

    if isinstance(step_size, list):
        step_size = step_size[0]

    if isinstance(output_step_size, list):
        output_step_size = output_step_size[0]

    results = [[] for _ in range(len(state_indices) + len(variable_indices))]
    x = []

    t = interval[0]
    end = interval[-1]

    result_epoch = interval[0]
    while (t + step_size) < end:
        if (result_epoch == interval[0]) or ((result_epoch + output_step_size) < t):
            result_epoch = t
            # Update computed variables to match current state.
            system.compute_variables(t, states, rates, variables, external_module.update_external_variable)
            # Store current state.
            x.append(t)
            store_result(results, states, state_indices, variables, variable_indices)

        system.compute_rates(t, states, rates, variables, external_module.update_external_variable)

        delta = list(map(lambda var: var * step_size, rates))
        states = [sum(x) for x in zip(states, delta)]

        t += step_size

    # Always have last result in results.
    if abs(x[-1] - end) > 1e-12:
        system.compute_rates(end, states, rates, variables, external_module.update_external_variable)
        system.compute_variables(end, states, rates, variables, external_module.update_external_variable)
        x.append(end)
        store_result(results, states, state_indices, variables, variable_indices)

    return x, results


def update(voi, states, system, rates, variables, update_external_variable):
    system.compute_rates(voi, states, rates, variables, update_external_variable)
    return rates


def scipy_based_solver(system, method, simulation_parameters, external_module):
    state_indices = apply_config(simulation_parameters['result']['config'], system.STATE_INFO)
    variable_indices = apply_config(simulation_parameters['result']['config'], system.VARIABLE_INFO)
    states, rates, variables = initialize_system(system, external_module.initialise_external_variable)

    # step_size = simulation_parameters['integration']['step_size']
    interval = simulation_parameters['integration']['interval']
    output_step_size = simulation_parameters['result']['step_size']

    if isinstance(output_step_size, list):
        output_step_size = output_step_size[0]

    results = [[] for _ in range(len(state_indices) + len(variable_indices))]
    x = []

    solver = ode(update)
    solver.set_integrator(method, max_step=1e-1)
    solver.set_initial_value(states, interval[0])
    solver.set_f_params(system, rates, variables, external_module.update_external_variable)

    system.compute_variables(solver.t, solver.y, solver.f_params, variables, external_module.update_external_variable)
    x.append(solver.t)
    store_result(results, solver.y, state_indices, variables, variable_indices)

    end = interval[-1]
    while solver.successful() and (solver.t + output_step_size) < end:
        solver.integrate(solver.t + output_step_size)

        system.compute_variables(solver.t, solver.y, solver.f_params[1], variables, external_module.update_external_variable)
        x.append(solver.t)
        store_result(results, solver.y, state_indices, variables, variable_indices)

    solver.integrate(end)
    x.append(solver.t)
    store_result(results, solver.y, state_indices, variables, variable_indices)

    return x, results

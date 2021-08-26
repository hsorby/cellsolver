
from scipy.integrate import ode


def initialize_system(system):
    rates = system.create_states_array()
    states = system.create_states_array()
    variables = system.create_variables_array()

    system.initialize_states_and_constants(states, variables)
    system.compute_computed_constants(variables)

    return states, rates, variables


def update(voi, states, system, rates, variables):
    system.compute_rates(voi, states, rates, variables)
    return rates


def euler_based_solver(system, step_size, interval):
    states, rates, variables = initialize_system(system)

    if isinstance(step_size, list):
        step_size = step_size[0]

    results = [[] for _ in range(len(states))]
    x = []

    t = interval[0]
    end = interval[-1]

    while (t + step_size) <= end:
        x.append(t)
        for index, value in enumerate(states):
            results[index].append(value)

        system.compute_rates(t, states, rates, variables)

        delta = list(map(lambda var: var * step_size, rates))
        states = [sum(x) for x in zip(states, delta)]

        t += step_size

    return x, results


def scipy_based_solver(system, method, step_size, interval):
    states, rates, variables = initialize_system(system)

    if isinstance(step_size, list):
        step_size = step_size[0]

    results = [[] for _ in range(len(states))]
    x = []

    solver = ode(update)
    solver.set_integrator(method)
    solver.set_initial_value(states, interval[0])
    solver.set_f_params(system, rates, variables)

    x.append(solver.t)
    for index, value in enumerate(solver.y):
        results[index].append(value)

    end = interval[-1]
    while solver.successful() and (solver.t + step_size) <= end:
        solver.integrate(solver.t + step_size)

        x.append(solver.t)
        for index, value in enumerate(solver.y):
            results[index].append(value)

    return x, results

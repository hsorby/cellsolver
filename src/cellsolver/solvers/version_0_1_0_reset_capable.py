
from scipy.integrate import ode


def initialize_system(system):
    rates = system.create_states_array()
    states = system.create_states_array()
    variables = system.create_variables_array()
    resets = system.create_resets_array()

    system.initialize_states_and_constants(states, variables)
    system.compute_computed_constants(variables)

    return states, rates, variables, resets


def update(voi, states, system, rates, variables):
    system.compute_rates(voi, states, rates, variables)
    return rates


def euler_based_solver(system, step_size, interval):
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


def scipy_based_solver(system, method, step_size, interval):
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

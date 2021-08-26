
from cellsolver.solvers.version_0_1_0 import update, euler_based_solver, scipy_based_solver
import cellsolver.solvers.version_0_1_0


def initialize_system(system):
    rates = system.create_states_array()
    states = system.create_states_array()
    variables = system.create_variables_array()

    system.initialise_states_and_constants(states, variables)
    system.compute_computed_constants(variables)

    return states, rates, variables


cellsolver.solvers.version_0_1_0.initialize_system = initialize_system

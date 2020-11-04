# The content of this file was generated using the Python profile of libCellML 0.2.0.

from enum import Enum
from math import *


__version__ = "0.1.0"
LIBCELLML_VERSION = "0.2.0"

STATE_COUNT = 1
VARIABLE_COUNT = 0
RESETS_COUNT = 1


class VariableType(Enum):
    CONSTANT = 1
    COMPUTED_CONSTANT = 2
    ALGEBRAIC = 3


VOI_INFO = {"name": "time", "units": "second", "component": "single_independent_ode"}

STATE_INFO = [
    {"name": "A", "units": "meter", "component": "single_independent_ode"}
]

VARIABLE_INFO = [
]

RESETS_INFO = [
    {"order": 0, "set": []}
]


def create_states_array():
    return [nan]*STATE_COUNT


def create_variables_array():
    return [nan]*VARIABLE_COUNT


def create_resets_array():
    return [nan]*RESETS_COUNT


def initialize_states_and_constants(states, variables):
    states[0] = 1.0


def compute_computed_constants(variables):
    pass


def compute_rates(voi, states, rates, variables):
    rates[0] = 1.0


def compute_variables(voi, states, rates, variables):
    pass


def compute_reset_test_value_differences(voi, states, variables, test_value_differences):
    test_value_differences[0] = states[0] - 2


def _apply_order_to_active_resets(active_resets):
    pass


def apply_resets(voi, states, variables, active_resets):
    _apply_order_to_active_resets(active_resets)
    if active_resets[0]:
        states[0] = 1

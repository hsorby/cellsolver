# The contents of this file was generated from version 0.2.0 of libCellML.
from math import *


__version__ = "0.2.0"

STATE_VECTOR_SIZE = 4
VARIABLE_VECTOR_SIZE = 18

VOI_INFORMATION = {"component": "membrane", "name": "time", "units": "millisecond"}

STATE_VECTOR_INFORMATION_ARRAY = [
    {"component": "sodium_channel_m_gate", "name": "m", "units": "dimensionless"},
    {"component": "sodium_channel_h_gate", "name": "h", "units": "dimensionless"},
    {"component": "potassium_channel_n_gate", "name": "n", "units": "dimensionless"},
    {"component": "membrane", "name": "V", "units": "millivolt"},
]

VARIABLE_VECTOR_INFORMATION_ARRAY = [
    {"component": "leakage_current", "name": "g_L", "units": "milliS_per_cm2"},
    {"component": "membrane", "name": "Cm", "units": "microF_per_cm2"},
    {"component": "membrane", "name": "E_R", "units": "millivolt"},
    {"component": "potassium_channel", "name": "g_K", "units": "milliS_per_cm2"},
    {"component": "sodium_channel", "name": "g_Na", "units": "milliS_per_cm2"},
    {"component": "leakage_current", "name": "E_L", "units": "millivolt"},
    {"component": "sodium_channel", "name": "E_Na", "units": "millivolt"},
    {"component": "potassium_channel", "name": "E_K", "units": "millivolt"},
    {"component": "membrane", "name": "i_Stim", "units": "microA_per_cm2"},
    {"component": "membrane", "name": "i_L", "units": "microA_per_cm2"},
    {"component": "membrane", "name": "i_Na", "units": "microA_per_cm2"},
    {"component": "sodium_channel_m_gate", "name": "alpha_m", "units": "per_millisecond"},
    {"component": "sodium_channel_m_gate", "name": "beta_m", "units": "per_millisecond"},
    {"component": "sodium_channel_h_gate", "name": "alpha_h", "units": "per_millisecond"},
    {"component": "sodium_channel_h_gate", "name": "beta_h", "units": "per_millisecond"},
    {"component": "membrane", "name": "i_K", "units": "microA_per_cm2"},
    {"component": "potassium_channel_n_gate", "name": "alpha_n", "units": "per_millisecond"},
    {"component": "potassium_channel_n_gate", "name": "beta_n", "units": "per_millisecond"},
]


def leq_func(x, y):
    return 1.0 if x <= y else 0.0


def geq_func(x, y):
    return 1.0 if x >= y else 0.0


def and_func(x, y):
    return 1.0 if bool(x) & bool(y) else 0.0


def create_state_vector():
    return [nan]*4


def create_variable_vector():
    return [nan]*18


def initialize_constants(states, variables):
    states[0] = 0.05
    states[1] = 0.6
    states[2] = 0.325
    states[3] = 0.0
    variables[0] = 0.3
    variables[1] = 1.0
    variables[2] = 0.0
    variables[3] = 36.0
    variables[4] = 120.0


def compute_computed_constants(variables):
    variables[6] = variables[2]-10.613
    variables[8] = variables[2]-115.0
    variables[14] = variables[2]+12.0


def compute_rates(voi, states, rates, variables):
    variables[10] = 0.1*(states[3]+25.0)/(exp((states[3]+25.0)/10.0)-1.0)
    variables[11] = 4.0*exp(states[3]/18.0)
    rates[0] = variables[10]*(1.0-states[0])-variables[11]*states[0]
    variables[12] = 0.07*exp(states[3]/20.0)
    variables[13] = 1.0/(exp((states[3]+30.0)/10.0)+1.0)
    rates[1] = variables[12]*(1.0-states[1])-variables[13]*states[1]
    variables[16] = 0.01*(states[3]+10.0)/(exp((states[3]+10.0)/10.0)-1.0)
    variables[17] = 0.125*exp(states[3]/80.0)
    rates[2] = variables[16]*(1.0-states[2])-variables[17]*states[2]
    variables[5] = -20.0 if and_func(geq_func(voi, 10.0), leq_func(voi, 10.5)) else 0.0
    variables[7] = variables[0]*(states[3]-variables[6])
    variables[15] = variables[3]*pow(states[2], 4.0)*(states[3]-variables[14])
    variables[9] = variables[4]*pow(states[0], 3.0)*states[1]*(states[3]-variables[8])
    rates[3] = -(-variables[5]+variables[9]+variables[15]+variables[7])/variables[1]


def compute_variables(voi, states, rates, variables):
    variables[7] = variables[0]*(states[3]-variables[6])
    variables[9] = variables[4]*pow(states[0], 3.0)*states[1]*(states[3]-variables[8])
    variables[10] = 0.1*(states[3]+25.0)/(exp((states[3]+25.0)/10.0)-1.0)
    variables[11] = 4.0*exp(states[3]/18.0)
    variables[12] = 0.07*exp(states[3]/20.0)
    variables[13] = 1.0/(exp((states[3]+30.0)/10.0)+1.0)
    variables[15] = variables[3]*pow(states[2], 4.0)*(states[3]-variables[14])
    variables[16] = 0.01*(states[3]+10.0)/(exp((states[3]+10.0)/10.0)-1.0)
    variables[17] = 0.125*exp(states[3]/80.0)

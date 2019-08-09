

Cell Solver
===========

A basic codebase for investigating the code generation output from libCellML.

Install
-------

Use 'pip' to install from the repository::

 pip install git+https://github.com/hsorby/cellsolver.git@master

This will install the latest version available on the 'master' branch.

Running
-------

The installation will add a command line tool for running cellsolver.  To run the application type::

 cellsolver

on the command line to execute the default solution which is the Hodgkin Huxley squid axon 1952 model solved using
(forward) Euler method.

There are three solvers currently available: euler, vode, dop853.  To run the application with a particular solver
add one of the known solvers to the command line, for example::

 cellsolver vode

will run the application using the 'vode' solver.

There is also functionality to time the execution of the solver.  To make use of this add the command line parameter
'timeit' to the command.  Using this form of the command will run the solver 10 times and print out the average time
to execute the full simulation.  For example to time the 'dop853' solver use the following command::

cellsolver timeit dop853

Be aware that this may take some time to finish executing.

Note: The default solver is (forward) Euler.  Using a solver unknown to the application will result in this solver being
used.

Additional
----------

It is highly recommended to use a virtual environment to install cellsolver into.

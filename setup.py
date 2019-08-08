from setuptools import setup

setup(
    name='cellsolver',
    version='0.1.0',
    packages=['cellsolver', 'cellsolver.codesamples'],
    package_dir={'': 'src'},
    url='https://github.com/hsorby/cellsolver',
    license='Apache 2.0',
    author='Hugh Sorby',
    author_email='h.sorby@auckland.ac.nz',
    description='A simple test harness for running Python generated code from libCellML.',
    install_requires=['matplotlib', 'scipy'],
    entry_points = {
        'console_scripts': ['cellsolver=cellsolver.main:main'],
    }
)

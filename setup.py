from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='mgns',
    version='0.1',
    py_modules=['mgns'],
    install_requires=[
        'numpy>=1.11.0',
        'scipy>=0.17.0',
        'click>=6.6',
        'biopython>=1.66',
        'joblib>=0.9.4',
        'multiprocess>=0.70.4',
        'Comparable>=1.0',
        'bunch>=1.0.1',
        'genetic>=0.1.dev3',
        'tqdm>=4.7.0',
        'pandas>=0.18.0'
    ],
    include_dirs=[numpy.get_include()],
    entry_points='''
        [console_scripts]
        mgns=mgns:cli
    ''',
    ext_modules=
        cythonize("src/lib/kmerize/rank.pyx"),
        #Extension("mgns.rank", ["lib/kmerize/rank.c"])

)
#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="yanc",
    version="0.2.0",
    description="Yet another NetCDF checker",
    url="https://github.com/metno/yanc",
    author="MET Norway",
    author_email="thomas.nipen@met.no",
    license="GPL-3",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Information Analysis",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GPL License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    # What does your project relate to?
    keywords="meteorology weather prediction",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "*tests*"]),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["numpy>=1.7", "netCDF4", "pyyaml"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        #    'dev': ['check-manifest'],
        "test": ["coverage", "pep8", "flake8"],
        #    'test': ['pytest'],
    },
    test_suite="yanc.tests",
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["yanc=yanc:main"]},
)

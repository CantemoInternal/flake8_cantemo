from setuptools import setup, find_packages
setup(
    name="flake8_cantemo",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'flake8',
    ],
    entry_points={
        'flake8.extension': ['CMO = flake8_cantemo.checker:CantemoChecker'],
    },

)

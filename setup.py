from setuptools import setup, find_packages
setup(
    name="flake8_cantemo",
    version="0.0.1",
    packages=find_packages(),
    keywords='pep8 flake8 python',
    author='Mattias Amnefelt',
    author_email='mattiasa@cantemo.com',
    license='BSD',
    py_modules=['flake8_cantemo'],
    test_suite='run_tests',
    install_requires=[
        'flake8',
    ],
    entry_points={
        'flake8.extension': ['CMO = flake8_cantemo.checker:CantemoChecker'],
    },

)

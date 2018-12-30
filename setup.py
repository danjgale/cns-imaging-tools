from setuptools import setup, find_packages

setup(
    name='cnstools',
    version='0.0.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                    "tests"]),
    license='MIT',
    author='Dan Gale',
    long_description=open('README.md').read(),
    url='https://github.com/danjgale/cns-imaging-tools/',
    install_requires=[
        'numpy>=1.15',
        'scipy>=1.1',
        'nipype>=1.1.1',
        'dcm2bids>=1.1.8'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    setup_requires=['pytest-runner']
)
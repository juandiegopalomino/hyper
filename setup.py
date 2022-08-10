#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['test/']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# Get the version
version_regex = r'__version__ = ["\']([^"\']*)["\']'
with open('hyper/__init__.py', 'r') as f:
    text = f.read()
    match = re.search(version_regex, text)

    if match:
        version = match.group(1)
    else:
        raise RuntimeError("No version number found!")

# Stealing this from Kenneth Reitz
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


packages = [
    'hyper',
    'hyper.http20',
    'hyper.common',
    'hyper.http11',
    'hyper.packages',
    'hyper.packages.rfc3986'
]

setup(
    name='hyperh2v3',
    version=version,
    description='HTTP/2 Client for Python-- Updated to use h2 v3.X.X',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    author='Cory Benfield and JD Palomino did the h2 v3.X.X update',
    author_email='jdpcbs@gmail.com',
    url='http://hyper.rtfd.org',
    packages=packages,
    package_data={'': ['LICENSE', 'README.rst', 'CONTRIBUTORS.rst', 'HISTORY.rst', 'NOTICES']},
    package_dir={'hyper': 'hyper'},
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'h2>=3.0,<4.0,!=2.5.0', 'hyperframe>=5.2,<6.0', 'rfc3986>=1.1.0,<2.0', 'brotlipy>=0.7.0,<1.0'
    ],
    tests_require=['pytest', 'requests', 'mock'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'hyper = hyper.cli:main',
        ],
    },
    extras_require={
        'fast': ['pycohttpparser'],
        # PyPy with bad SSL modules will likely also need the cryptography
        # module at lower than 1.0, because it doesn't support CFFI v1.0 yet.
        ':platform_python_implementation == "PyPy" and python_full_version < "2.7.9"': [
            'cryptography<1.0'
        ],
    }
)

"""
setup.py - Set up script for sample project
"""
import codecs  # To use a consistent encoding
from glob import glob
import os
from setuptools import setup, find_packages, Command
import shutil
from typing import ClassVar, List


class CleanCommand(Command):
    """Command class that will be used by 'setup.py clean'"""
    user_options: ClassVar[List[str]] = []
    cwd: str

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: ' + self.cwd
        for pattern in ['build', 'dist', '*.egg-info', '*.pyc', '*.tgz']:
            for name in glob(pattern):
                if os.path.isdir(name):
                    shutil.rmtree(name)
                else:
                    os.remove(name)


# Get the long description from the README.md file.
# This will be become the contents of the project's home page on PyPI.
# Note that we can't assume that the Python interpreter's working directory is
# this directory, so we can't use a relative path to access README.md
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bootcamp_case_study',
    version='1.0.0',
    description='Case study project for Sutter Python Bootcamp',
    long_description=long_description,
    platforms=['all'],
    install_requires=['pyspark', 'pytest'],  # not used; just an example
    author='Sutter Python Dev',
    author_email='pythondev@sutter.com',
    #  find_packages() function saves you from listing all packages explicitly:
    #  packages=['setup_example', 'setup_example.util']
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    cmdclass={'clean': CleanCommand},  # use CleanCommand class defined above
    license='MIT',
    keywords='setup setuptools'
)

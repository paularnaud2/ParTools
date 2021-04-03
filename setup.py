from shutil import copyfile
from setuptools import find_packages, setup

setup(packages=find_packages())
copyfile('pytools/conf_main_default.py', 'pytools/_conf_main.py')
copyfile('pytools/conf_oracle_default.py', 'pytools/_conf_oracle.py')

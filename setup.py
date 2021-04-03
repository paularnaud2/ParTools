from shutil import copyfile
from setuptools import find_packages, setup

setup(packages=find_packages())
copyfile('conf/conf_main_default.py', 'conf/_conf_main.py')
copyfile('conf/conf_oracle_default.py', 'conf/_conf_oracle.py')

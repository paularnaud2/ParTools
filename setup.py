import os
from pathlib import Path
from shutil import copyfile
from setuptools import setup
from setuptools import find_packages

setup(packages=find_packages())

root = Path(os.path.realpath(__file__)).parent.absolute()
root = str(root).replace("\\", "/") + '/'

src = root + 'conf/conf_mail_gmail.txt'
dst = g.paths['CONF'] + 'conf_main.py'
copyfile(src, dst)

from pytools.common import init_directories
from pytools.common import g

g.init_directories()

copyfile('conf/conf_oracle_default.py', 'conf/conf_oracle.py')

# Check Install
import importlib.util as u
import pytools.conf as cfg
from .g import init_PT

check_list = [
    'flake8',
    'yapf',
    'pytest',
    'cx_Oracle',
    'pandas',
]


def package_is_installed(name):
    return u.find_spec(name)


if cfg.CI:
    for name in check_list:
        if not package_is_installed(name):
            s = (
                "the PyTools package havn't been properly installed."
                " Please run one of the following commands in the root folder:\n"
                "pip install -e .\n"
                "pip install .")
            raise Exception(s)

init_PT()

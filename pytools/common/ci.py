from os.path import exists

if not exists('conf/_conf_main.py'):
    s = ("the PyTools package havn't been properly installed."
         " Please run one of the following commands in the root folder:\n"
         "pip install -e .\n"
         "pip install .")
    raise Exception(s)

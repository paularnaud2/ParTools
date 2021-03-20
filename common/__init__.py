# conf_main and conf_oracle auto-init
from os.path import exists
from shutil import copyfile
if not exists('conf_main.py'):
    copyfile('conf_main_default.py', 'conf_main.py')
if not exists('conf_oracle.py'):
    copyfile('conf_oracle_default.py', 'conf_oracle.py')

# Check if requirements have been installed
try:
    import yapf
    import rope
except Exception:
    s = "Error: required packages have not been installed."
    s += " Please run the following command:\n"
    s += "pip install -r requirements.txt"
    raise Exception(s)

# Imports for package common
from .deco import log_exeptions

from .tools import run_cmd
from .tools import run_sqlplus
from .tools import send_notif
from .tools import init_kwargs
from .tools import list_to_dict

from .log import log
from .log import step_log
from .log import init_log
from .log import log_print
from .log import log_array
from .log import log_input
from .log import check_log
from .log import log_example
from .log import init_sl_time
from .log import gen_sl_detail

from .string import big_number
from .string import replace_from_dict
from .string import get_duration_ms
from .string import get_duration_string

from .file import mkdirs
from .file import load_txt
from .file import save_list
from .file import read_file
from .file import merge_files
from .file import count_lines
from .file import delete_folder
from .file import get_file_list

from .header import get_header
from .header import gen_header
from .header import has_header
from .header import check_header

from .csv import csv_clean
from .csv import load_csv
from .csv import save_csv
from .csv import csv_to_list
from .csv import write_csv_line
from .csv import get_csv_fields_dict

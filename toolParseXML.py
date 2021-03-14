# This script allows you to convert a xml fil into csv

import common as com

from common import g
from time import time

from tools import gl
from tools.finish import finish_xml
from tools.xml import gen_img_dict
from tools.xml import save_img_dict

# Input variables default values
gl.IN_DIR = g.paths['IN'] + "in.xml"
gl.IN_DIR = "test/tools/xml_in.xml"
gl.OUT_DIR = g.paths['OUT'] + "out.csv"

gl.OPEN_OUT_FILE = False

gl.SL_STEP_READ = 1000 * 10**3
gl.SL_STEP_WRITE = 100 * 10**3

# Const
gl.MULTI_TAG_LIST = [
    'libelle',
    'civilite',
    'nom',
    'prenom',
    'telephone1Num',
    'telephone2Num',
    'adresseEmail',
]
gl.RE_EXP_TAG_ELT = '<(.*)>(.*)</(.*)>'
gl.RE_EXP_SUB_TAG = r'<(\w[^<]*\w)>$'

# Global variables
gl.FIRST_TAG = ''
gl.SUB_TAG = ''
gl.N_ROW = 0


def parse_xml(**kwargs):
    com.log("[toolParseXML] parse_xml: start")
    start_time = time()
    com.init_kwargs(gl, kwargs)
    gen_img_dict()
    save_img_dict()
    finish_xml(start_time)


if __name__ == '__main__':
    parse_xml(OPEN_OUT_FILE=True)

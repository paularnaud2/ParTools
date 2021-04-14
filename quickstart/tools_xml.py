# This script allows you to convert a xml file into csv
import pytools.common.g as g
from pytools.tools import xml

# Input variables
in_dir = g.paths['IN'] + "in.xml"
in_dir = "pytools/test/tools/files/xml_in.xml"
out_dir = g.paths['OUT'] + "out.csv"

if __name__ == '__main__':
    xml.parse_xml(in_dir, out_dir)
else:
    xml.parse_xml(in_dir, out_dir, OPEN_OUT_FILE=False)

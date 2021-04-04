# This script allows you to convert a xml fil into csv
import pytools.common.g as g
from pytools.tools import xml

# Input variables
in_dir = g.paths['IN'] + "in.xml"
in_dir = "pytools/test/tools/xml_in.xml"
out_dir = g.paths['OUT'] + "out.csv"

xml.parse_xml(in_dir, out_dir)

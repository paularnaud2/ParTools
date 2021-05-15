# This script allows you to convert a potentially big xml file into csv.

import partools.utils.g as g
from partools.tools import xml
from partools.quickstart import files_dir

# Input variables
# in_path = g.dirs['IN'] + "in.xml"
in_path = f'{files_dir}xml_in.xml'
out_path = g.dirs['OUT'] + "out.csv"

xml.parse_xml(in_path, out_path)

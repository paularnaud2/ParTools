"""
This script extracts all Python doc ('# comments included) present in the
'in_dir' directories (can be useful for spell check)
"""

from pytools.tools.ed import extract_doc

in_dirs = ['pytools', 'quickstart', 'tests']
out_path = 'doc.txt'

extract_doc(in_dirs, out_path)

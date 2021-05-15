"""
This script extracts all Python doc ('# comments included) present in the
'in_dir' directories and subdirectories (recursive search).
This can be useful for spell checking your code.
"""

from pytools.tools.ed import extract_doc
from pytools.quickstart import quickstart_dir

in_dirs = [quickstart_dir]
out_path = 'extract_doc_out.txt'

extract_doc(in_dirs, out_path)

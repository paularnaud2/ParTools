"""
This script extracts all Python doc ('# comments included) present in the
'in_dir' directories and subdirectories (recursive search).
This can be useful for spell checking.
"""

import partools.tools as to
import partools.quickstart as qs

in_dirs = [qs.quickstart_dir]
out_path = 'extract_doc_out.txt'

to.extract_doc(in_dirs, out_path)

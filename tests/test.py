import pytools.common as com
import math

n = 18
NB_MAX_ELT_IN_STATEMENT = 2
n_grp = math.ceil(n / NB_MAX_ELT_IN_STATEMENT)
out = math.floor(math.log10(n_grp)) + 1

print(n_grp, out)

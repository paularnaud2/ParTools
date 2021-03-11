# import common as com
import re

str1 = 'Thread no. * had finished its run'
str2 = 'Thread no. 1 had finished its run'

str1 = re.escape(str1)
str1 = str1.replace(r'\*', '(.*)')
print(str1)

m = re.search(str1, str2)
out = False
if m:
    out = True

print(out)

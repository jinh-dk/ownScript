
# Print the http://..... InternalServerError from the Xunit output file.

import sys
if  len(sys.argv) != 2 :
    exit(1)

import os.path
filename = sys.argv[1]
if not os.path.isfile(filename) :
    exit(1)

f = open(filename, 'r')
content = f.read().replace('\n', '')
f.close()

print(filename)
import re

# http://stackoverflow.com/questions/19750096/python-regex-find-a-substring-that-doesnt-contain-a-substring
# https://regex101.com/r/yY2gG8/1
pattern = r'http(?:(?!http).)*InternalServerError'
errors = re.findall(pattern, content, re.DOTALL)
for error in errors :
    print(error)







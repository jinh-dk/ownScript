
# Print the http://..... ***Error from the Xunit output file. (default is InternalServerError)

# argv[1] : filename
# argv[2] : error code , only 500, 404, 401 supported. Default is 500





import sys

if  len(sys.argv) > 3  or len(sys.argv) < 2:
    exit(1)

if len(sys.argv) == 2 :
    errorcode = '500'
else:
    errorcode = sys.argv[2]

from collections import defaultdict
ErrorDict = defaultdict(lambda : 'InternalServerError')
ErrorDict['500'] = 'InternalServerError'
ErrorDict['404'] = 'NotFound'
ErrorDict['401'] = 'Unauthorized'


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

errorText = ErrorDict[errorcode]

#pattern = r'http(?:(?!http).)*InternalServerError'
pattern = r'http(?:(?!http).)*' + re.escape(errorText)

errors = re.findall(pattern, content, re.DOTALL)
for error in errors :
    print(error)







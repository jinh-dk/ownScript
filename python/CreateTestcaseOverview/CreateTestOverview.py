#
#  Create a test overview in csv file
#  In CSV file, there are 3 columns:    
#  [Endpoint] [Testcase cover the endpoint]  [number of failed testcase]
#
#  Many hardcode 
#


import os, sys
import re

apipattern = r'/*<description>\s*(/api/.*)\s*</description>*'
testcasepattern = r'.*\s(\w+Test).*'
IntegrationTestcaseFolder = r"C:\Users\jinxu\Documents\GitHub\kunaiDev\Kunai\test\Publishing.Api.IntegrationTest"


### Read the API list file  ###
with open(r'C:\Users\jinxu\Documents\GitHub\KunaiTestExecutor\APIs.txt', 'r') as f:
    APIList = f.read().splitlines() 

APITestCaseList = [0] * len(APIList)
APIFailedTestCaseList = [0] * len(APIList)


### Read the testcase files ###
EndPointList = []
isEndPoinstFound = False
Testcase2apiDict = {}
for filename in os.listdir(IntegrationTestcaseFolder):
    ## Testcase file has to be end and 'IntegrationTest.cs' ##
    if (filename.endswith('IntegrationTest.cs')) :
        testfile = open(os.path.join(IntegrationTestcaseFolder, filename), 'r')
        lines = testfile.readlines()
        testfile.close()
        for line in lines :
            ## In each testcase, the covered endpoint has to be inside <description></description> ##
            ## Each endpoint use one line
            if "<description>" in line:                                 
                isEndPoinstFound = True
                m = re.search(apipattern, line)
                ## m need non-empty ##
                if m:                    
                    EndPointList.append(m.group(1))
            elif 'Test()' in line and isEndPoinstFound:
                ## When there is a testcase, summerize, and clear ##
                isEndPoinstFound = False                                
                m = re.search(testcasepattern, line)
                if m:
                    ## remove .cs from filename ##
                    testcasename = filename[:-2] + m.group(1)
                    Testcase2apiDict[testcasename] = EndPointList

                    ## Find the endpoint tested in the testcase, and add the number"
                    for ep in EndPointList :
                        idx = APIList.index(ep)
                        APITestCaseList[idx] = APITestCaseList[idx] + 1
                    EndPointList = []

# read the Test Result files.
import xml.etree.ElementTree as ET
testresult = ET.parse(r'C:\Users\jinxu\Documents\GitHub\KunaiTestExecutor\integrationTest.xml').getroot()
for test in testresult.findall('.//assembly/collection/test'):
    if (test.get('result') == "Fail"):
        ## Where the testcase is failed, read the dictionary to get the list of endpoint that testcase covered.
        _list = Testcase2apiDict[ test.get('name')[len('Unity.Publishing.Api.IntegrationTest.'):] ]
        for ep in _list:            
            idx = APIList.index(ep)
            APIFailedTestCaseList[idx] = APIFailedTestCaseList[idx] + 1        


# Write to CSV file
if (len(APIList) != len(APITestCaseList)):
    print('Wrong!')

import csv
with open(r'C:\Users\jinxu\Documents\GitHub\KunaiTestExecutor\APICoverageOverView.txt', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)                                
    for i in range(0, len(APIList)):                                           
        spamwriter.writerow([ APIList[i], APITestCaseList[i], APIFailedTestCaseList[i]])        
#
#  Create a test overview in csv file
#  In CSV file, there are 3 columns:    
#  [Endpoint] [Testcase cover the endpoint]  [number of failed testcase]
#  
#  Now the script can also update a google spreadsheet.
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



#Update the google spreadsheet
import datetime
import httplib2
#from __future__ import print_function
#import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

spreadsheetId = '1KcpQz3oEj9jQOXc2feI-veEJ-D1PwTrITvhRgNI8bFM'    

rangeName = "A1:C1"
_body = {
        "range" :rangeName,
        "majorDimension": "ROWS" ,
        "values": [
            ["API Name",  "Number of testcase to cover", "Number of failed testcase"]
        ],
    }
request = service.spreadsheets().values().update(
    spreadsheetId=spreadsheetId, valueInputOption="RAW", range=rangeName, body=_body).execute()

## Use len(APIList)+1 to add the last row "Lastupdate:"  ##
for i in range(0, len(APIList)+1):
    rangeName = "A"+str(i+2) + ":C"+str(i+2)
    if i != len(APIList)+1:
        _body = {
            "range" :rangeName,
            "majorDimension":"ROWS",
            "values": [
                [APIList[i], APITestCaseList[i], APIFailedTestCaseList[i]]
            ],
        }
    else:
        now = datetime.datetime.now()
        _body = {
            "range" :rangeName,
            "majorDimension":"ROWS",
            "values": [
                ["Last Update:", "", now]
            ],
        }
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId, valueInputOption="RAW", range=rangeName, body=_body).execute()

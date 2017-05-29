from __future__ import print_function
import datetime
import httplib2
import os

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
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


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
                                   'drive-python-quickstart.json')

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

from googleapiclient.http import MediaFileUpload

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    #file_metadata = { 'name' : 'backend.log',
    #                  'mimeType' : 'text/plain'
    #} 

    file_metadata = {
        'modifiedTime' : datetime.datetime.utcnow().isoformat() + 'Z'
    }

    media = MediaFileUpload(r'C:\Users\jinxu\Documents\GitHub\KunaiLog\Backend.log',
                        mimetype='text/plain',
                        resumable=True)                        
    file_id = "1iecekG5Rlnme9rfJ4PWP1KPUh1Kt8JOLIMcJHIeZmvk"
    results = service.files().update(fileId= file_id,
                                    media_body=media,
                                    body=file_metadata,                                    
                                    fields='id, modifiedTime').execute()
    

    ## Upload Frontend
    media = MediaFileUpload(r'C:\Users\jinxu\Documents\GitHub\KunaiLog\Frontend.log',
                        mimetype='text/plain',
                        resumable=True)  
                         
    file_id = "1CmjkWFjPUQZJmEHqgnFhruFMyfR2Gxm8EDGmUKPaMbY"
    results = service.files().update(fileId= file_id,
                                    media_body=media,
                                    body=file_metadata,                                    
                                    fields='id, modifiedTime').execute()


if __name__ == '__main__':
    main()
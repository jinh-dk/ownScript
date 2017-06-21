from __future__ import print_function
import datetime
import httplib2
import os
import sys

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

    Write the local log file to a google docs file. 
    The id of google docs file are hardcoded.

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    file_metadata = {
        'modifiedTime' : datetime.datetime.utcnow().isoformat() + 'Z'
    }

    # use raw input for path
    # https://stackoverflow.com/questions/17438852/pass-in-string-as-argument-without-it-being-treated-as-raw
    media = MediaFileUpload(sys.argv[1].decode('string_escape'),
                        mimetype='text/plain',
                        resumable=True)                        
    file_id = sys.argv[2]
    results = service.files().update(fileId= file_id,
                                    media_body=media,
                                    body=file_metadata,                                    
                                    fields='id, modifiedTime').execute()

if __name__ == '__main__':
    main()
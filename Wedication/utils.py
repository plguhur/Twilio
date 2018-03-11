import json
import time
import gspread
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from twilio.rest  import Client
import os
import argparse
from twilio.rest import Client

# Parameters from Google API
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES             = ['https://spreadsheets.google.com/feeds']
APPLICATION_NAME   = 'PP-60-ans'
WORKBOOK           = "60ans_PP"

# Parameters from twilio
ACCOUNT_SID        = 'ACc0f384d057e028db7c50c8f5174de10a'
AUTH_TOKEN         = 'ead4d26a2dabc514ea0a78d658cc105a'


def get_credentials(secret_file, scopes, application):
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
    flow = client.flow_from_clientsecrets(secret_file, scopes)
    flow.user_agent = APPLICATION_NAME
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    credentials = tools.run_flow(flow, store, flags)
    return credentials

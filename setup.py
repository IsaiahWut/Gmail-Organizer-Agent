import os.path 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def authenticate():
    creds = None

    # if the token exists, then we can continue on
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    # if the token is not valid or available, we ask the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            # ask the user to log in and verify
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json()) 

    return creds
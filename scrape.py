import os.path
from setup import authenticate

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import base64

# just fetch all the emails and just store them
def fetch_emails():
    
    # call the authenticate function
    # fetch the credentials
    creds = authenticate()

    try:
        # build the service API
        service = build("gmail", "v1", credentials=creds)

        # retrieves the list of messages
        # - limit to just one page of emails
        messages = service.users().messages().list(maxResults=50, userId="me").execute()

        # loop through the messages
        # pull out the actual content
        email_content = {}
        
        # extracting the message list
        messageList = messages.get('messages', [])
            
        for msg in messageList:
            # extracts information about the email
            #   - meta data
            #   - snapshot of the email
            #   - full email content (the body of the email) in base64
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            # we need to grab the ID, Label, and the body
            message_id = txt['id']
            labels = txt.get('labelsIds', [])
            body = None

            # accessing the payload element from the JSON file
            payload_object = txt.get('payload', {})

            # within the payload object, we extract the message part of the JSON file
            message_parts = payload_object.get('parts', [])

            # if we extracted something (ie it is not empty), then we will extract and decode
            if message_parts:
                # if the email has multiple components to it, we need to keep going through each layer
                # until we find the base file that has our data
                for part in message_parts:
                    # our base case that has our email data
                    if part.get("mimeType") == "text/plain":
                        # assign body with the body from the email
                        body = part.get("body", {}).get("data", "")

                        # stop here because we have found our base case
                        break

            # if the email does not have multiple parts, we just skip to this case
            else:
                body = payload_object.get("body", {}).get("data", "")

            # decode the body email from base 64 to plain tesxt
            if body:
                body = base64.urlsafe_b64decode(body).decode("utf-8")

            # appending the email to our dictionary for later use
            email_content[message_id] = {'labels': labels, 'body': body}
        
        # if there is a next page, we should reupdate our 50 messages
        if 'nextPageToken' in messages:
            nextPageToken = messages['nextPageToken']
            messages = service.users().messages().list(userId="me", pageToken=nextPageToken).execute()
        
        return email_content

    except HttpError as error:
        print(f"An error occurred: {error}")
  
# this will turn the dictionary scrape email into a json file
def dictionary_to_json(email_data, filename="emails.json"):
    with open(filename, "w") as json_file:
        json.dump(email_data, json_file, indent=4)
    print(f"Emails saved to {filename}")

email_list = fetch_emails()
dictionary_to_json(email_list)
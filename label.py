import re
import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from setup import authenticate

# parse the text file and return a dictionary of {id: label}
def parse_email_labels(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # only looks for the ID's and labels themselves
    match = re.search(r"START OF OUTPUT\n(.*?)\nEND OF OUTPUT", content, re.DOTALL)

    # if not a match or corrupted file, return an empty dictionary
    if not match:
        print("Data not found in file.")
        return {}
    
    # splits the output data into individual lines 
    # intitializes a dictionary
    email_data = match.group(1).strip().split("\n")
    email_dict = {}

    # loops through each line and extracts the ID and label, and adds that to the dictionary
    for line in email_data:
        if ": " in line:
            email_id, label = line.split(": ")
            email_dict[email_id.strip()] = label.strip()
    
    return email_dict

# check labels on the gmail account, create them if needed
def verify_labels(service, user_id, label_name):
    # scrapes the current existing emails in the Gmail
    labels = service.users().labels().list(userId=user_id).execute().get("labels", [])

    # checks if a label with the same name already exists in Gmail
    for label in labels:
        if label["name"].lower() == label_name.lower():
            return label["id"]
    
    # if does not exist, it will create the label itself and then return the ID
    label_body = {"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
    label = label = service.users().labels().create(userId=user_id, body=label_body).execute()
    return label["id"]

# Apply and make the label changes
def apply_labels(service, email_labels):
    user_id = "me"

    # loop through each ID and its corresponding label
    for email_id, label_name in email_labels.items():
        try:
            # verify if the label exists or not, if we need to create it or not
            label_id = verify_labels(service, user_id, label_name)

            # Gmail API call to add the label to the specific ID
            service.users().messages().modify(
                userId = user_id,
                id = email_id,
                body = {"addLabelIds": [label_id]}
            ).execute()
            print(f"Applied label '{label_name}' to email {email_id}")
        except Exception as e:
            print(f"Failed to label email {email_id}: {e}")


service = build("gmail", "v1", credentials=authenticate())
email_labels = parse_email_labels("labels.txt")
apply_labels(service, email_labels)
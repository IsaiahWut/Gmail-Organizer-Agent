#!/usr/bin/env python
import sys
from crew import EmailorganizerCrew
import agentstack
import agentops
import yaml
import json
from dotenv import load_dotenv

agentops.init(default_tags=agentstack.get_tags())

instance = EmailorganizerCrew().crew()

def run():
    """
    Run the agent.
    """
    original_stdout = sys.stdout
    try: 
        with open("labels.txt", "w") as file:
            sys.stdout = file
            instance.kickoff(inputs=agentstack.get_inputs())
    finally:
        sys.stdout = original_stdout
    
    clean_file("labels.txt")


def replace_info(file_path, json_file_path):
    try:
        # Open the emails.json and verify
        with open(json_file_path, "r") as json_file:
            email_data = json.load(json_file)

        with open(file_path, "r") as file:
            # opens the tasks yaml file and parses that data into yaml_data
            yaml_data = yaml.safe_load(file)

        # updates the variables emails in the tasks.yaml file with the correct path
        yaml_data["variables"]["EMAILS"] = json_file_path

        # write to tasks.yaml in YAML format
        with open(file_path, "w") as file:
            # write the json file to the yaml file so Agent can read
            yaml.dump(email_data, file, default_flow_style=False, sort_keys=False)
        print(f"Successfully wrote email data to {file_path}")

    except Exception as e:
        print(f"Error writing to YAML file: {e}")

# clean the output text file so we are just left with the labels
def clean_file(filename, phrase="START OF OUTPUT"):
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # loop through the file and find the phrase "START OF OUTPUT"
    start_index = next((i for i, line in enumerate(lines) if phrase in line), None)

    if start_index is not None:
        with open(filename, "w") as file:
            # keep the actual agent output
            file.writelines(lines[start_index:]) 

if __name__ == '__main__':
    # authenticate user if necessary
    # fetch emails
    # turn it into a json file
    # email_list = fetch_emails()
    # dictionary_to_json(email_list)

    # dump the json file
    yaml_file = "src/config/tasks.yaml"
    json_file = "emails.json"
    replace_info(yaml_file, json_file)

    run()

# 3/24/25
# need to work on including all of the functions into one file (the fetch_emails and dictionary to json)
# errors with the google oauth lib (python 3.13) but using python 3.12 for agentstack, miscommumincation error
# also issues with the agent, currently it is only organizing one email instead of the entire list
# problem with this might be the firecrawl API key, i might need to get that
# just try and label one email, and then later we can worrry about all of them

'''
3/26/25
might need to make another agent called store, and have that agent store the output, idk if this is even possible

currently it is able to organize 1-8 emails. 

I need to fix the output.json file as it is jumbled and disorganized
    - for parsing, i can either bruce force it and only focus on the actual output
    - or i can fix how it is being stored 
    after this i can loop through the output file and then make the changes ("test if this is actually possible and how it would work separately")

    
    the question is: is the email.json file always 200 lines of code?
    if it is, we can just delete the first 338 lines of code to give us the output we actually want
        we just also need to make sure that we append '}' and " \" " characters so that way we get no errors in the json file *** need to do this
    
    if the email json file is always a set number of lines of code, then we know that we can just delete a fixed number of lines of code
    and it will be okay, instead of us having to delete everything up to a certain point, we can just brute force it
'''
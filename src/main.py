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
    
    # clean the final output txt file
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
    # dump the json file
    yaml_file = "src/config/tasks.yaml"
    json_file = "emails.json"
    replace_info(yaml_file, json_file)

    run()
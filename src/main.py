#!/usr/bin/env python
import sys
from crew import EmailorganizerCrew
import agentstack
import agentops

agentops.init(default_tags=agentstack.get_tags())

instance = EmailorganizerCrew().crew()

def run():
    """
    Run the agent.
    """
    instance.kickoff(inputs=agentstack.get_inputs())

if __name__ == '__main__':
    run()
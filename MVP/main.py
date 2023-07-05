"""
Project:        ENG1013 HVAC
File:           main.py
Purpose:        This file runs the core functionality of the HVAC project. These include,
                1. Control System
                2. System Settings
                3. Graphing
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from controlSystem import controlSystem
from systemSettings import systemSettings
from graphing import graphing
from shared import *

# global vars

"""
Function to display system menu
Params: None
Return: None
"""
def main():
    # get user input
    print("Welcome to ENG1013 Smart Fan System!\n")

    # loop if an incorrect input is entered
    while True:
        print("Please select from the below options: \n1. Control System \n2. System Settings \n3. Graphing\n") 
        try:
            userInput = int(input("Your Choice: "))
            if (userInput not in [1,2,3]):
                print("Invalid selection! Please choose again.\n")
                continue
        except ValueError:
            print("Please enter a value between 1 and 3.\n")
        except KeyboardInterrupt:
            print("\nExiting system...\n")
            exit()

        # call relavent function
        if userInput == 1:
            print("\nTaking you to control system...")
            controlSystem()
        elif userInput == 2:
            print("\nTaking you to system settings...")
            systemSettings()
        elif userInput == 3:
            print("\nTaking you to graphing...")
            graphing()

if __name__ == "__main__":
    main()

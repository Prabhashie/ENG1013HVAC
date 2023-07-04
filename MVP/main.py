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

from controlSystem import controlSystem
from systemSettings import systemSettings
from graphing import graphing

"""
Main function to display system menu
"""
def main():
    # get user input
    print("Welcome to ENG1013 Smart Fan System!\n")
    print("Please select from the below options: \n1. Control System \n2. System Settings \n3. Graphing\n")

    # loop if an incorrect input is entered
    while True: 
        try:
            userInput = int(input("Your Choice: "))
            if (userInput not in [1,2,3]):
                print("Invalid selection! Please choose again.")
                continue
            else:
                break
        except ValueError:
            print("Please enter a value between 1 and 3.")
        except KeyboardInterrupt:
            print("Exiting system...")
            exit()

    # call relavent function
    if userInput == 1:
        controlSystem()
    elif userInput == 2:
        systemSettings()
    elif userInput == 3:
        graphing()

if __name__ == "__main__":
    main()

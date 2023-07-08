"""
Project:        ENG1013 HVAC
File:           systemSettings.py
Purpose:        This file contains the invocation for the system settings menu of the HVAC
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
import shared

# global vars

"""
Function to run the system settings operations such as view and update system parameters
Params: None
Return: None
"""
def systemSettings():
    while True:
        try:
            userInput = int(input("Please enter the PIN to view/ update system parameters: "))
            if userInput == shared.PIN:
                while True:
                    print("\nPlease select from below options: \n1. View system parameters \n2. Update system parameters")
                    try:
                        userInput = int(input("Your choice: "))
                        if (userInput not in [1,2]):
                            print("Invalid selection! Please choose again.\n")
                            continue
                    except ValueError:
                        print("Please enter a value between 1 and 2.\n")
                    except KeyboardInterrupt:
                        print("\nExiting system settings...\n")
                        return
                    # call relavent function
                    if userInput == 1:
                        viewParams()
                    elif userInput == 2:
                        updateParams()
            else:
                print("Incorrect PIN entered! Please try again.\n")     
        except ValueError:
            print("Incorrect PIN entered! Please try again.\n")
        except KeyboardInterrupt:
            print("\nExiting system settings...\n")
            return

"""
Function to view system parameters
Params: None
Return: None
"""   
def viewParams():
    print("Current system parameters are: \n")
    print(f"Ambient temperatue range: {shared.ambientTempLow} - {shared.ambientTempHigh} C\n")

"""
Function to update system parameters
Params: None
Return: None
"""
def updateParams():
    print("Current system parameters are: \n")
    print(f"Ambient temperatue range: {shared.ambientTempLow} - {shared.ambientTempHigh} C\n")

    while True:
        print("Please choose which system parameter to update: \n1. Ambient low threshold \n2. Ambient high threshold")
        try:
            userInput = int(input("Your choice: "))
            if (userInput not in [1,2]):
                print("Invalid selection! Please choose again.\n")
                continue
        except ValueError:
            print("Please enter a value between 1 and 2.\n")
        except KeyboardInterrupt:
            print("\nExiting system settings...\n")
            return
        # update relavent parameters
        if userInput == 1:
            while True:
                try:
                    changeVal = float(input("New value for ambient low threshold: "))
                    shared.ambientTempLow = changeVal
                    print(f"Ambient low threshold successfully updated to {shared.ambientTempLow} C")
                    return
                except ValueError:
                    print("Incorrect value entered! Please enter a float value.")
                    continue
                except KeyboardInterrupt:
                    print("\nAborting update...\n")
                    break
        elif userInput == 2:
            while True:
                try:
                    changeVal = float(input("New value for ambient high threshold: "))
                    shared.ambientTempHigh = changeVal
                    print(f"Ambient high threshold successfully updated to {shared.ambientTempHigh} C")
                    return
                except ValueError:
                    print("Incorrect value entered! Please enter a float value.")
                    continue
                except KeyboardInterrupt:
                    print("\nAborting update...\n")
                    break
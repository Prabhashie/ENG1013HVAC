"""
Project:        ENG1013 HVAC
File:           systemSettings.py
Purpose:        This file contains the invocation for the system settings menu of the HVAC
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
import shared
import time

# global vars

"""
Function to run the system settings operations such as view and update system parameters
Params: None
Return: None
"""
def system_settings():
    pinEntries = 1
    shared.systemSettingsStartTime = time.time()    # importing * and using global doesn't work 
                                                    # global only makes the variable global for the context of the module (file)
                                                    # https://discuss.python.org/t/global-variables-shared-across-modules/16833/2        
    while (pinEntries <= 3): # lock system settings if incorrect PIN entered 3 times 
        try:
            userInput = int(input("Please enter the PIN to view/ update system parameters: "))
            if userInput == shared.PIN:
                while (time.time() - shared.systemSettingsStartTime) <= shared.systemSettingsAccessDuration: # timeout if admin access duration exceeded
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
                        view_params()
                    elif userInput == 2:
                        update_params()
                print("\nAdmin access timeout!")
                return # returns to main menu if timed out
            else:
                if pinEntries < 3:
                    print(f"Incorrect PIN entered! Please try again. You have {3 - pinEntries} attempt(s) left!\n")
                    pinEntries += 1
                else:
                    print("You entered an incorrect PIN 3 times! System settings access denied for 2 minutes.") 
                    shared.invalidPINTimeoutStart = time.time()
                    return  
        except ValueError:
            if pinEntries < 3:
                print(f"Incorrect PIN entered! Please try again. You have {3 - pinEntries} attempt(s) left!\n")
                pinEntries += 1
            else:
                print("You entered an incorrect PIN 3 times! System settings access denied for 2 minutes.")
                shared.invalidPINTimeoutStart = time.time()
                return
        except KeyboardInterrupt:
            print("\nExiting system settings...\n")
            return

"""
Function to view system parameters
Params: None
Return: None
"""   
def view_params():
    if (time.time() - shared.systemSettingsStartTime) <= shared.systemSettingsAccessDuration: # timeout if admin access duration exceeded
        print("Current system parameters are: \n")
        print(f"Ambient temperatue range: {shared.ambientTempLow} - {shared.ambientTempHigh} C\n")
        if (shared.closedDoorDistance == 0):
            distance = "Not calibrated yet"
        else:
            distance = f"{shared.closedDoorDistance} cm"
        print(f"Average distance between the door and ultra-sonic sensor: {distance}\n")

"""
Function to update system parameters
Params: None
Return: None
"""
def update_params():
    print("Current system parameters are: \n")
    print(f"Ambient temperatue range: {shared.ambientTempLow} - {shared.ambientTempHigh} C\n")

    while (time.time() - shared.systemSettingsStartTime) <= shared.systemSettingsAccessDuration: # timeout if admin access duration exceeded
        print("Please choose which system parameter to update: \n1. Ambient low threshold \n2. Ambient high threshold \n3. Settings access duration ")
        try:
            userInput = int(input("Your choice: "))
            if (userInput not in [1, 2, 3]):
                print("Invalid selection! Please choose again.\n")
                continue
        except ValueError:
            print("Please enter a value between 1 and 2.\n")
        except KeyboardInterrupt:
            print("\nExiting update parameters...\n")
            return
        # update relavent parameters
        # TODO: check input values against acceptable range
        if userInput == 1:
            while (time.time() - shared.systemSettingsStartTime) <= shared.systemSettingsAccessDuration: # timeout if admin access duration exceeded
                try:
                    changeVal = float(input("New value for ambient low threshold (Celcius): "))
                    if ((shared.minLowTemp - shared.temperatureTolerence) <= changeVal <= (shared.minLowTemp + shared.temperatureTolerence)):
                        shared.ambientTempLow = changeVal
                        print(f"Ambient low threshold successfully updated to {shared.ambientTempLow} C")
                        return
                    else:
                        print(f"Ambient low threshold should be between {(shared.minLowTemp - shared.temperatureTolerence)} and {(shared.minLowTemp + shared.temperatureTolerence)} C")
                        continue
                except ValueError:
                    print("Incorrect value entered! Please enter a float value.")
                    continue
                except KeyboardInterrupt:
                    print("\nAborting update...\n")
                    break
        elif userInput == 2:
            while (time.time() - shared.systemSettingsStartTime) <= shared.systemSettingsAccessDuration: # timeout if admin access duration exceeded
                try:
                    changeVal = float(input("New value for ambient low threshold (Celcius): "))
                    if ((shared.maxHighTemp - shared.temperatureTolerence) <= changeVal <= (shared.maxHighTemp + shared.temperatureTolerence)):
                        shared.ambientTempHigh = changeVal
                        print(f"Ambient high threshold successfully updated to {shared.ambientTempHigh} C")
                        return
                    else:
                        print(f"Ambient high threshold should be between {(shared.maxHighTemp - shared.temperatureTolerence)} and {(shared.maxHighTemp + shared.temperatureTolerence)} C")
                        continue
                except ValueError:
                    print("Incorrect value entered! Please enter a float value.")
                    continue
                except KeyboardInterrupt:
                    print("\nAborting update...\n")
                    break
        elif userInput == 3:
            while (time.time() - shared.systemSettingsStartTime) <= shared.systemSettingsAccessDuration: # timeout if admin access duration exceeded
                try:
                    changeVal = float(input("New value for settings access duration (seconds): "))
                    if ((shared.desiredTimeoutDuration - shared.accessDurationTolerence) <= changeVal <= (shared.desiredTimeoutDuration + shared.accessDurationTolerence)):
                        shared.systemSettingsAccessDuration = changeVal
                        print(f"System settings access duration successfully updated to {shared.systemSettingsAccessDuration} s")
                        print("Return to main menu and come back to system settings for new admin timeout to get activated!")
                        return
                    else:
                        print(f"System settings access duration should be between {(shared.desiredTimeoutDuration - shared.accessDurationTolerence)} and {(shared.desiredTimeoutDuration + shared.accessDurationTolerence)} C")
                        continue
                except ValueError:
                    print("Incorrect value entered! Please enter a float value.")
                    continue
                except KeyboardInterrupt:
                    print("\nAborting update...\n")
                    break

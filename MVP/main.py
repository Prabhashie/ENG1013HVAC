print("Welcome to ENG1013 Smart Fan System")
print("Please select from the below options:\nControl System: 1\nSystem Settings: 2\nGraphing: 3 \n")
while True:
    user_Input = input("Input:")
    if user_Input != 1 or 2 or 3:
        print("Invalid selection! Please choose again.")
        continue
    else:
        break

def main():
    if user_Input == 1:
        #call the relevant function
    elif user_Input == 2:
        #call the relevant function
    elif user_Input == 3:
        #call the relevant function

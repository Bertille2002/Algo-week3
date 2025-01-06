import pandas as pd 
from user_functions import * 

def main():
    users = 'users_hashed.csv'
    while True :
        input = display_menu()
        if input == "1" :
            login()
        elif input == "2" :
            new_user()
        elif input == "3" :
            print("Closing program.")
            break
        else :
            print("Invalid input.")

if __name__ == "__main__" :
    main()
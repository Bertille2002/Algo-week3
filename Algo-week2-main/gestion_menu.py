import pandas as pd 
from login_menu import *
from user_functions import *
from menu_products import *
from gestion_account import *
from prod_function_pandas import *

def user_main(username) :
    print(f"Welcome {username}!")
    while True : 
        input = user_menu()
        if input == "1" :
            open_prod_menu(username)
        elif input == "2" : 
            check_password()
        elif input == "3" : 
            change_data(username)
        elif input == "4" :
            delete_user(username)
        elif input == "5" :
            print("Logging out...")
            break
        else : 
            print("Invalid input.")

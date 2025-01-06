import pandas as pd 
from datetime import date 
import os
from menu_products import *
import hashlib
from gestion_menu import *

# Menu display options
def display_menu() : 
    print("\n Interactive menu : ")
    print("1. Sign in")
    print("2. Sign up")
    option = input("Enter your choice : ")
    return option

# read data in df
def load_hashed_user_data():
    user_data = {}
    df = pd.read_csv('users_hashed.csv')
    for _, row in df.iterrows() :
        user_data[row['username']] = {
            'password': row['password']
        }
    return user_data

# Option 1 : login function
def login() : 
    hashed_user_data = load_hashed_user_data()
    input_username = input("Enter your username : ").strip()
    if input_username in hashed_user_data :
        input_password = input("Enter password : ").strip()
        hashed_password = hashed_user_data[input_username]['password']
        input_password_hash = hashlib.sha256(input_password.encode()).hexdigest()
        if input_password_hash == hashed_password :
            print("Login successful !")
            # redirect to 'products_function.py' 
            user_main(input_username)
        else :
            print("Incorrect password.")
    else :
        print("Username not found. Try again or create an account.")

# Option 2 : sign up function 

# find last id for unique IDs
def get_last_ID() : 
    df = pd.read_csv('users_hashed.csv')
    if not df.empty :
        last_id = df['ID'].iloc[-1]
        return last_id
    else :
        print("CSV file is empty")
        return 0

# add user function
def new_user() :
    last_id = get_last_ID()
    # read existing user data
    try :
        users_df = pd.read_csv('users_hashed.csv')
    except :
        users_df = pd.DataFrame(columns=["ID", "first_name", "last_name", "username", "password", "order_date"])
    # ask for sign up details 
    new_name = input("Enter your first name : ")
    new_lname = input("Enter your last name : ")
    new_username = input("Enter your username : ")
    new_password = input("Enter your password : ")
    new_date = 'NA'
    new_id = last_id + 1
    # Define the folder path for products csv file creation 
    folder_path = 'csv_files'
    if not os.path.exists(folder_path) :
        os.makedirs(folder_path)
    # check if username already exists 
    if new_username in users_df['username'].values :
        print("Username already exists.")
        return
    # Genertate salt and hash for password 
    hashed_password = hashlib.sha256(new_password.encode())
    # Define new row
    new_user_data = {
        'ID': [new_id],
        'first_name': [new_name],
        'last_name': [new_lname],
        'username': [new_username],
        'password': [hashed_password],
        'order_date': [new_date]
    }
    new_df = pd.DataFrame(new_user_data)
    # add new user info to csv file
    if not users_df.empty :
        new_df.to_csv('users_hashed.csv', mode='a',index=False, header=False)
    else :
        new_df.to_csv('users_hashed.csv', mode='w',index=False, header=True)
    print("New user added successfully!")
    # Create new csv products file
    orders_file = os.path.join(folder_path,f'orders_{new_username}.csv')
    if not os.path.exists(orders_file) :
        orders_df = pd.DataFrame(columns=["ID", "first_name", "last_name", "username", "password", "order_date"])
        orders_df.to_csv(orders_file, index=False)
    print(f"Orders file '{orders_file}' created in '{folder_path}' folder.")


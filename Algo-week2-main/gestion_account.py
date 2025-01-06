import pandas as pd 
import hashlib 
from pip._vendor import requests
from menu_products import products_main

def user_menu() : 
    print("\n Interactive menu : ")
    print("1. Go to products menu")
    print("2. Check password strength")
    print("3. Change user info")
    print("4. Delete account")
    print("5. Log out")
    option = input("Enter your choice : ")
    return option

def open_prod_menu(username) :
    print("Opening products menu ...")
    products_main(username)

def check_password_pwned(password) :
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5 = sha1_hash[:5]
    remaining_hash = sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{first5}"
    response = requests.get(url)
    if response.status_code == 200 :
        hashes = response.text.splitlines()
        for hash_entry in hashes : 
            hash_part, count = hash_entry.split(':')
            if hash_part == remaining_hash : 
                return True
    else : 
        print("Error connecting to Have I been Pwned API.")
    return False 

def check_password() : 
    password_to_check = input("Enter your password to check if it has been pawned : ")
    if check_password_pwned(password_to_check):
        print("This password has been pwned. It is not safe to use.")
    else:
        print("This password has not been pwned. It is safe to use.")

# Option 3 : Change user data
def change_data(username) : 
    try : 
        df = pd.read_csv('users_hashed.csv')
        row_index = df[df['username'] == username].index
        if row_index.empty : 
            print(f"No user with username : {username} found.")
            return
        value_to_change = input("Enter the data  you wish to change (username, password) : ")
        if value_to_change not in ['username', 'password']:
            print("Invalid input.")
            return
        if value_to_change == 'username' :
            new_username = input("Enter your new username : ")
            if new_username != username : 
                df.loc[row_index,'username'] = new_username
            else :
                print("New username cannot be old username")
        elif value_to_change == 'password' : 
            new_password = input("Enter your new password : ")
            hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
            print("New password successfully updated!")
        df.to_csv('users_hashed.csv', index=False)
    except FileNotFoundError :
        print("File users not found.")


# Option 4 : delete user 
def delete_user(username):
    print("You can only delete your own account.")
    try : 
        df = pd.read_csv('users_hashed.csv')
        row_index = df[df['username'] == username].index
        if row_index.empty:
            print(f"No user with username '{username}' found.")
            return
        input_username = input("Enter your username : ").strip()
        hashed_password = df.loc[row_index, 'password'].values[0]
        if hashlib.sha256(input_password.encode()).hexdigest() == hashed_password:
            print("Successful login, you can now delete your account.")
            df = df[df['username'] != username]  # Delete the user from the DataFrame
            df.to_csv('users_hashed.csv', index=False)  # Save back to CSV
            print(f"The account '{username}' has been deleted.")
        else :
            print("Incorrect password.")
    except FileNotFoundError :
        print("Error : User data file not found.")
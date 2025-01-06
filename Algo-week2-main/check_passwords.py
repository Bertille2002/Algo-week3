import hashlib
import requests
import pandas as pd

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

def check_passwords_users(df, password_column) :
    df['Compromised'] = df[password_column].apply(lambda x: check_password_pwned(x))
    return df 

if __name__ == "__main__" : 
    df = pd.read_csv('users.csv')
    result_df = check_passwords_users(df, 'password')
    print(result_df)
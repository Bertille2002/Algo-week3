import pandas as pd 
import csv
import hashlib 
import os 

user_data = [
    [1,"Alice","Beaumont","ngarcia.mit@gmail.com", "alice12","abcd1234","12-05-24"],
    [2,"Jean","Dubois","ngarcia.mit@gmail.com", "JD_3","sigma13!","27-12-23"],
    [3,"Simon","Schmitt","simonschmitt@gmail.com", "Simsum","T4ylor_$wift","18-10-21"],
    [4,"Chloe", "Lukasiak", "chloelukasiak@yahoo.fr", "chlobird","C4itlyn_Cl4rk","01-08-15"],
    [5,"Maddie", "Ziegler", "maddieziegler@gmail.com", "madz","0ui0uiBag3tte","15-02-14"],
    [6,"Aaron", "Colin", "aaroncolin@gmail.com", "aaroncol","Sl4yYy_","30-11-22"]
]

df = pd.DataFrame(user_data, columns= ['ID', 'first_name', 'last_name', 'email', 'username', 'password', 'order_date'])

print(df)

with open('users.csv', 'w', newline='') as file :
    writer = csv.writer(file)
    field = ['ID', 'first_name', 'last_name', 'email', 'username', 'password', 'order_date']
    writer.writerow(field)
    writer.writerows(user_data)

# Hash passwords

def hash_passwords() :
    df = pd.read_csv('users.csv')
    def generate_salt(length=16) : 
        return os.urandom(length).hex()
    def hash_value(password) : 
        salt = generate_salt()
        salted_password = salt + password
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        return salted_password, salt
    # Apply the hash_value function to each password
    df[['password','salt']] = df['password'].apply(lambda x: pd.Series(hash_value(x)))
    df.to_csv('users_hashed_salted.csv',index=False)
    return df

hashed_df = hash_passwords()
print(hashed_df)
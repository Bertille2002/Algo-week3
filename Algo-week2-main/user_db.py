import pandas as pd 
import csv
import hashlib 

user_data = [
    [1,"Alice","Beaumont","alice12","abcd1234","12-05-24"],
    [2,"Jean","Dubois","JD_3","sigma13!","27-12-23"],
    [3,"Simon","Schmitt","Simsum","T4ylor_$wift","18-10-21"],
    [4,"Chloe", "Lukasiak", "chlobird","C4itlyn_Cl4rk","01-08-15"],
    [5,"Maddie", "Ziegler", "madz","0ui0uiBag3tte","15-02-14"],
    [6,"Aaron", "Colin", "aaroncol","Sl4yYy_","30-11-22"]
]

df = pd.DataFrame(user_data, columns= ['ID', 'first_name', 'last_name', 'username', 'password', 'order_date'])

print(df)

with open('users.csv', 'w', newline='') as file :
    writer = csv.writer(file)
    field = ['ID', 'first_name', 'last_name', 'username', 'password', 'order_date']
    writer.writerow(field)
    writer.writerows(user_data)

# Hash passwords

def hash_passwords() :
    df = pd.read_csv('users.csv')
    def hash_value(password) : 
        return hashlib.sha256(password.encode()).hexdigest()
    df['password'] = df['password'].apply(hash_value)
    df.to_csv('users_hashed.csv',index=False)
    return df

hashed_df = hash_passwords()
print(hashed_df)
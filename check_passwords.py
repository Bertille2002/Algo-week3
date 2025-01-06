import hashlib
import requests
import pandas as pd
import smtplib 
import uuid
from datetime import datetime, timedelta
from email.message import EmailMessage

def gen_resetLink() :
    token = str(uuid.uuid4())
    expiration_date = datetime.now() + timedelta(hours=1)
    link = f"https://reset-password.local/{token}"
    print(f"The reset link generated is : {link}")
    print(f"This link expires at : {expiration_date}")
    return link 

def compPWD_email(user_email, reset_link) :
    msg = EmailMessage()
    msg['Subject'] = "Important : Reset your TheAmazone password."
    msg['From'] = "ngarcia.mit@gmail.com"
    msg['To'] = user_email
    msg.set_content(f"""
Hello,
                
We have noticed that your password might have been compromised. For safety reasons we recommend you change your current password.
                
Please use this link in order to reset your password {reset_link}
                
This link will expire in an hour
                
If you are not the source of this request or if you have any question, please contact our security team. 
                
Best regards,
TheAmazone security team <3.
                """)
    try : 
        with smtplib.SMTP("smtp.gmail.com", 587) as server :
            server.starttls()
            server.login("ngarcia.mit@gmail.com","fflwnhelkhpyhuon")
            server.send_message(msg)
        print("Email sent successfully !")
    except Exception as e : 
        print(f"Error during sending {e}")


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
                reset_link = gen_resetLink()
                user_email = 'ngarcia.mit@gmail.com'
                compPWD_email(user_email, reset_link)
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

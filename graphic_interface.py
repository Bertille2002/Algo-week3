from tkinter import Tk, Label, Entry, messagebox, Toplevel, Button
import pandas as pd
import hashlib
import csv_files
import os  

# Load user data from a CSV file
def load_hashed_user_data():
    user_data = {}
    df = pd.read_csv('users_hashed_salted.csv')
    for _, row in df.iterrows():
        user_data[row['username']] = {
            'salt': row['salt'],
            'password': row['password']
        }
    return user_data

def login(username, password):
    hashed_user_data = load_hashed_user_data()
    if username in hashed_user_data:
        hashed_password = hashed_user_data[username]['password']
        input_password_hash = hashlib.sha256(password.encode()).hexdigest()
        if input_password_hash == hashed_password:
            messagebox.showinfo("Success", "Login successful!")
            user_main(username)  # Redirect to the main menu
        else:
            messagebox.showerror("Error", "Incorrect password.")
    else:
        messagebox.showerror("Error", "Username not found. Try again or create an account.")

# Placeholder for redirection function
def user_main(username):
    # Simulate redirection to another menu
    messagebox.showinfo("Welcome", f"Welcome, {username}! Redirecting to the main menu...")
    # Implement actual redirection logic here

# Helper function: Get last ID
def get_last_ID():
    try:
        df = pd.read_csv('users_hashed_salted.csv')
        if not df.empty:
            return df['ID'].iloc[-1]
        else:
            return 0
    except FileNotFoundError:
        return 0

# Helper function: Save new user to CSV
def save_new_user(new_user_data):
    try:
        users_df = pd.read_csv('users_hashed_salted.csv')
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=["ID", "first_name", "last_name", "email", "username", "password", "order_date"])
    
    # Add the new user to the DataFrame
    new_df = pd.DataFrame(new_user_data)
    if not users_df.empty:
        new_df.to_csv('users_hashed_salted.csv', mode='a', index=False, header=False)
    else:
        new_df.to_csv('users_hashed_salted.csv', mode='w', index=False, header=True)

    # Create new orders CSV file
    folder_path = 'csv_files'
    os.makedirs(folder_path, exist_ok=True)
    orders_file = os.path.join(folder_path, f'orders_{new_user_data["username"][0]}.csv')
    if not os.path.exists(orders_file):
        orders_df = pd.DataFrame(columns=["ID", "first_name", "last_name", "email", "username", "password", "order_date"])
        orders_df.to_csv(orders_file, index=False)
    return True

#
#
#
# LOGIN PAGE FUNCTION START
#
# 
#

class AppWindow(Tk) : 
    def __init__(self) :
        super().__init__()

        label1 = Label(self, text = "Welcome to TheAmazone !", fg="black")
        label1.place(x=70,y=10)

        username_label = Label(self, text="Username:")
        username_label.place(x=50, y=55)
        self.username_entry = Entry(self)
        self.username_entry.place(x=120, y=55)

        password_label = Label(self, text="Password:")
        password_label.place(x=50, y=85)
        self.password_entry = Entry(self, show="*")
        self.password_entry.place(x=120, y=85)

        button1 = Button(self, text = "Sign in", fg="black", width = 15, command = self.handle_login)
        button1.place(x=90,y=120)

        no_acc_label = Label(self, text="No account ?")
        no_acc_label.place(x=50,y=150)
        
        button_newacc = Button(self, text= 'Sign up', fg='black', width = 15, command = self.open_signup_window)
        button_newacc.place(x=90,y=180)

        self.geometry("300x230")
        self.title("TheAmazone")

    def handle_login(self) :
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username and password :
            hashed_user_data = load_hashed_user_data()
            if username in hashed_user_data :
                user_data = hashed_user_data[username]
                stored_salt = user_data['salt']
                stored_hashed_password = user_data['password']
                salted_input_password = stored_salt + password 
                hashed_input_password = hashlib.sha256(salted_input_password.encode()).hexdigest()
                if hashed_input_password == stored_hashed_password :
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    self.open_user_menu(username)
                else : 
                    messagebox.showerror("Error", "Incorrect password.")
            else : 
                messagebox.showerror("Error","Username not found.")
        else : 
            messagebox.showerror("Error","Please enter both username and password.")
        
    def open_user_menu(self, username) : 
        self.destroy()
        menu_window = Toplevel()
        menu_window.title("MyAmazone account")
        menu_window.geometry("700x500")
        Label(menu_window, text=f"Welcome, {username}", font = ("Arial",12)).pack(pady=10)

        top_bar = Label(menu_window, text="",bg="VioletRed3")
        top_bar.pack(side="top",fill='x')
        top_bar2 = Label(menu_window, text="",bg="VioletRed3")
        top_bar2.pack(side="top",fill='x')
        
        logout_button = Button(menu_window, text= "Log out", width=6, bg='white',fg='black')
        logout_button.place(x=10,y=52)

        check_pwd_button = Button(menu_window, text= "Check password strength", width=19, bg='white')
        check_pwd_button.place(x=95,y=52)

        change_user_info_button = Button(menu_window, text= "Change user info", width=14, bg='white')
        change_user_info_button.place(x=285,y=52)

        del_button = Button(menu_window, text= "Delete account", width=12, bg='white')
        del_button.place(x=440,y=51)

        view_prods_button = Button(menu_window, text= "View my product", width=30)
        view_prods_button.pack(pady=10)

        add_prod_button = Button(menu_window, text= "Order new product", width=30)
        add_prod_button.pack(pady=10)

        del_prod_button = Button(menu_window, text= "Delete product order", width=30)
        del_prod_button.pack(pady=10)

        search_prod_button = Button(menu_window, text= "Search for product", width=30)
        search_prod_button.pack(pady=10)

        sort_prod_button = Button(menu_window, text= "View products sorted", width=30)
        sort_prod_button.pack(pady=10)

    def open_signup_window(self) : 
        signup_window = Toplevel(self)
        signup_window.title("Create an Account")
        signup_window.geometry("400x400")

        Label(signup_window, text = "First Name : ").place(x=50,y=50)
        first_name_entry = Entry(signup_window)
        first_name_entry.place(x=150,y=50)

        Label(signup_window, text = "Last Name : ").place(x=50,y=90)
        last_name_entry = Entry(signup_window)
        last_name_entry.place(x=150,y=90)

        Label(signup_window, text = "Email : ").place(x=50,y=130)
        email_entry = Entry(signup_window)
        email_entry.place(x=150,y=130)

        Label(signup_window, text = "Username : ").place(x=50,y=170)
        username_entry = Entry(signup_window)
        username_entry.place(x=150,y=170)

        Label(signup_window, text = "Password : ").place(x=50,y=210)
        password_entry = Entry(signup_window, show="*")
        password_entry.place(x=150,y=210)

        Label(signup_window, text = "Verify password : ").place(x=50,y=250)
        verify_password_entry = Entry(signup_window, show="*")
        verify_password_entry.place(x=150,y=250)

        def submit_signup() : 
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            email= email_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            verified_password = verify_password_entry.get().strip()

            if not all([first_name, last_name, email, username, password]) :
                messagebox.showerror("Error","All fields are required")
                return
            
            if password != verified_password :
                messagebox.showerror("Error","Passwords do not correspond")

            try :
                users_df = pd.read_csv('users_hashed_salted.csv')
                if username in users_df['username'].values :
                    messagebox.showerror("Error", "Username already exists")
                    return 
            except FileNotFoundError :
                pass 
            
            def generate_salt(length=16) : 
                return os.urandom(length).hex()
            
            salt = generate_salt()
            salted_password = salt + password
            hashed_salted_password = hashlib.sha256(salted_password.encode()).hexdigest()
            
            new_id = get_last_ID() + 1
            new_user_data = {
                'ID': [new_id],
                'first_name': [first_name],
                'last_name': [last_name],
                'email': [email],
                'username': [username],
                'password': [hashed_salted_password],
                'order_date': ['NA'],
                'salt': [salt]
            }

            save_new_user(new_user_data)
            messagebox.showinfo("Success","Account created successfully.")
            signup_window.destroy()
        
        Button(signup_window, text = "Create account", fg="black", width = 15, command = submit_signup).place(x=130,y=295)


window = AppWindow()
window.mainloop()


from tkinter import Tk, Label, Entry, messagebox, Toplevel, Button, Frame, Text, END, StringVar, OptionMenu, Listbox
from tkinter.ttk import Combobox
import pandas as pd
import hashlib
import csv_files
import os  
import requests
import smtplib 
import uuid
from datetime import datetime, timedelta
from email.message import EmailMessage

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

def log_login_attempt(username, success):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "SUCCESS" if success else "FAILURE"
    log_entry = f"{timestamp} | Username: {username} | Status: {status}\n"
    with open("login_attempts.csv", "a") as log_file:
        log_file.write(log_entry)


# Placeholder for redirection function
def user_main(username):
    # Simulate redirection to another menu
    messagebox.showinfo("Welcome", f"Welcome, {username}! Redirecting to the main menu...")

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
        self.frame = Frame(self)
        self.frame.pack()

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
                    if self.check_password_pwned(password) : 
                        log_login_attempt(username, True)
                        messagebox.showinfo("Success", f"Welcome, {username}! Unfortunately, Our systems have detected that your password may be compromised. Please change it on our plateform or use the link we have sent you via e-mail.")
                        self.open_user_menu(username)
                    else :
                        log_login_attempt(username, True)
                        messagebox.showinfo("Success", f"Welcome, {username}!")
                        self.open_user_menu(username)
                else : 
                    log_login_attempt(username, False)
                    messagebox.showerror("Error", "Incorrect password.")
            else : 
                log_login_attempt(username, False)
                messagebox.showerror("Error","Username not found.")
        else : 
            messagebox.showerror("Error","Please enter both username and password.")

    def gen_resetLink(self) :
        token = str(uuid.uuid4())
        expiration_date = datetime.now() + timedelta(hours=1)
        link = f"https://localhost/change_data/{token}"
        print(f"The reset link generated is : {link}")
        print(f"This link expires at : {expiration_date}")
        return link 

    def compPWD_email(self, user_email, reset_link) :
        msg = EmailMessage()
        msg['Subject'] = "Important : Reset your TheAmazone password."
        msg['From'] = "ngarcia.mit@gmail.com"
        msg['To'] = user_email
        msg.set_content(f"""
    Hello,
                    
    We have noticed that your password might have been compromised. For safety reasons we recommend you change your current password.
                    
    Please use this link in order to reset your password {reset_link}
                    
    This link will expire in an hour.

    Or you can directly change your user's data on our plateform.
                    
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
    
    def check_password_pwned(self, password) :
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
                    reset_link = self.gen_resetLink()
                    user_email = 'ngarcia.mit@gmail.com'
                    self.compPWD_email(user_email, reset_link)
                    return True
        else : 
            print("Error connecting to Have I been Pwned API.")
        return False 
        
    def open_user_menu(self, username) : 
        self.withdraw()
        menu_window = Toplevel()
        menu_window.title("MyAmazone account")
        menu_window.geometry("700x500")
        Label(menu_window, text=f"Welcome, {username} !", font = ("Arial",12)).pack(pady=10)

        top_bar = Label(menu_window, text="",bg="VioletRed3")
        top_bar.pack(side="top",fill='x')
        top_bar2 = Label(menu_window, text="",bg="VioletRed3")
        top_bar2.pack(side="top",fill='x')

        button_frame = Frame(menu_window, width=200)
        button_frame.pack(side="left",fill="y")
        button_frame.pack_propagate(False) # Prevent resizing of the frame
        
        result_area = Text(menu_window, wrap="word",width=100, height=25)
        result_area.pack(side="right", fill="both", expand=True)
        
        logout_button = Button(menu_window, text= "Log out", width=6, bg='white',fg='black',command=lambda: self.logout(menu_window))
        logout_button.place(x=10,y=52)

        change_user_info_button = Button(menu_window, text= "Change user info", width=14, bg='white', command=lambda: self.open_change_user_info_window(username))
        change_user_info_button.place(x=100,y=52)

        del_button = Button(menu_window, text= "Delete account", width=12, bg='white', command=lambda: self.open_delete_account_window(username))
        del_button.place(x=270,y=52)

        view_prods_button = Button(button_frame, text= "View my products", width=30, command=lambda: self.view_myprod(result_area, username))
        view_prods_button.pack(pady=10)

        add_prod_button = Button(button_frame, text= "Order new product", width=30, command=lambda: self.open_add_product_form(result_area))
        add_prod_button.pack(pady=10)

        del_prod_button = Button(button_frame, text= "Delete product in order file", width=30, command=lambda: self.open_delete_product_form(result_area, username))
        del_prod_button.pack(pady=10)

        search_prod_button = Button(button_frame, text= "Search for product in file", width=30, command=lambda: self.open_search_prod_form(result_area, username))
        search_prod_button.pack(pady=10)

        sort_prod_button = Button(button_frame, text= "View ordered products sorted", width=30, command=lambda: self.open_sort_orders_form(result_area, username))
        sort_prod_button.pack(pady=10)

    def logout(self, menu_window) :
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            menu_window.destroy()
            self.deiconify()

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

    def open_change_user_info_window(self, username) :
        change_info_window = Toplevel(self)
        change_info_window.title("Change User Info")
        change_info_window.geometry("400x300")

        Label(change_info_window, text="New Username :").grid(row=0, column=0, padx=5, pady=10)
        new_username_entry = Entry(change_info_window)
        new_username_entry.grid(row=0, column=1, padx=5, pady=10)

        Label(change_info_window, text="New Password :").grid(row=1, column=0, padx=5, pady=10)
        new_password_entry = Entry(change_info_window, show="*")
        new_password_entry.grid(row=1, column=1, padx=5, pady=10)

        Label(change_info_window, text="Confirm Password :").grid(row=2, column=0, padx=5, pady=10)
        confirm_password_entry = Entry(change_info_window, show="*")
        confirm_password_entry.grid(row=2, column=1, padx=5, pady=10)

        def save_changes() :
            new_username = new_username_entry.get().strip()
            new_password = new_password_entry.get().strip()
            confirm_password = confirm_password_entry.get().strip()

            if not new_username or not new_password or not confirm_password :
                messagebox.showwarning("Input error", "All fields are required!")
                return
            
            if new_password != confirm_password :
                messagebox.showwarning("Password error", "Passwords do not match!")
                return
            
            try:
                users_df = pd.read_csv('users_hashed_salted.csv')
                user_row = users_df[users_df['username'] == username]
                if user_row.empty:
                    messagebox.showerror("Error", "User not found!")
                    return
                salt = user_row['salt'].values[0]
                new_password_hashed = hashlib.sha256(f"{new_password}{salt}".encode()).hexdigest()
                users_df.loc[users_df['username'] == username, 'username'] = new_username
                users_df.loc[users_df['username'] == new_username, 'password'] = new_password_hashed
                users_df.to_csv('users_hashed_salted.csv', index=False)
                messagebox.showinfo("Success", "User info updated successfully!")
                change_info_window.destroy()
            except FileNotFoundError:
                messagebox.showerror("Error", "User data file not found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        
        save_button = Button(change_info_window, text="Save Changes", command=save_changes)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)


    def open_delete_account_window(self, username) :
        delete_account_window = Toplevel(self)
        delete_account_window.title("Delete Account")
        delete_account_window.geometry("400x300")

        Label(delete_account_window, text="Re-enter your password to delete your account:").grid(row=0, column=0, padx=5, pady=10)
        password_entry = Entry(delete_account_window, show="*")
        password_entry.grid(row=0, column=1, padx=5, pady=10)

        def delete_account() :
            entered_password = password_entry.get().strip()
            if not entered_password :
                messagebox.showwarning("Input error", "Please enter your password to confirm.")
                return
            try : 
                users_df = pd.read_csv('users_hashed_salted.csv')
                user_row = users_df[users_df['username'] == username]
                if user_row.empty :
                    messagebox.showerror("Error", "User not found.")
                    return
                salt = user_row['salt'].values[0]
                stored_password_hash = user_row['password'].values[0]
                entered_password_hash = hashlib.sha256(f"{entered_password}{salt}".encode()).hexdigest()
                if entered_password_hash == stored_password_hash :
                    users_df = users_df[users_df['username'] != username]
                    users_df.to_csv('users_hashed_salted.csv', index=False)
                    messagebox.showinfo("Success", "Your account has been deleted successfully.")
                    delete_account_window.destroy()
                else : 
                    messagebox.showerror("Password error", "Incorrect password. Account not deleted.")
            except FileNotFoundError :
                messagebox.showerror("Error", "User data file not found.")
            except Exception as e :
                messagebox.showerror("Error", f"An error occurred: {e}")
        
        delete_button = Button(delete_account_window, text="Delete Account", command=delete_account)
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)
        cancel_button = Button(delete_account_window, text="Cancel", command=delete_account_window.destroy)
        cancel_button.grid(row=2, column=0, columnspan=2, pady=10)

    def view_myprod(self, result_area, username) :
        try :
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            result_area.delete(1.0, END)
            result_area.insert(END, "List of products : \n")
            for index, row in df.iterrows():
                result_area.insert(END, f"{row['P_name']}\n")
        except FileNotFoundError:
            messagebox.showerror("Error", "File was not found")

    def next_prodid(self): 
        try:
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            last_id = df['ID'].max()
            return int(last_id) + 1  
        except FileNotFoundError:
            return 1 
            
    def open_add_product_form(self, result_area) :
        result_area.delete(1.0, END)

        try :
            products_df = pd.read_csv('csv_files/products.csv')
        except FileNotFoundError :
            messagebox.showerror("Error", "Product file was not found")

        form_frame = Frame(result_area)
        result_area.window_create("insert", window=form_frame)

        product_var = StringVar()
        quantity_var = StringVar()
        price_var = StringVar()

        Label(form_frame, text="Select Product :").grid(row=0, column=0, padx=5, pady=5)
        product_dropdown = OptionMenu(form_frame, product_var, *products_df['P_name'].tolist())
        product_dropdown.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Quantity :").grid(row=1, column=0, padx=5, pady=5)
        quantity_entry = Entry(form_frame, textvariable=quantity_var)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Total price :").grid(row=2, column=0, padx=5, pady=5)
        total_price_label = Label(form_frame, textvariable=price_var)
        total_price_label.grid(row=2, column=1, padx=5, pady=5)

        def update_total_price(*args) :
            try :
                product_name = product_var.get()
                quantity = int(quantity_entry.get())
                product_row = products_df[products_df['P_name'] == product_name]
                if not product_row.empty :
                    price = product_row['P_price (in $/Kg)'].values[0]
                    total_price = price * quantity 
                    price_var.set(f"${total_price:.2f}")
                else : 
                    price_var.set("Invalid product")
            except ValueError : 
                price_var.set("Enter valid quantity")

        quantity_var.trace("w", update_total_price)
        product_var.trace("w", update_total_price)
        
        def place_order() :
            product_name = product_var.get()
            try :
                quantity = int(quantity_var.get().strip())
                if quantity <= 0 :
                    raise ValueError("Quantity must be greater than 0.")
                product_row = products_df[products_df['P_name'] == product_name]
                if product_row.empty :
                    messagebox.showerror("Error", "Invalid product selected.")
                    return 
                price = product_row['P_price (in $/Kg)'].values[0]
                total_price = price * quantity
                order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

                user_order_file = f'csv_files/orders_{self.username_entry.get().strip()}.csv'
                try : 
                    orders_df = pd.read_csv(user_order_file)
                    new_id = orders_df['ID'].max() + 1 if not orders_df.empty else 1
                except FileNotFoundError : 
                    orders_df = pd.DataFrame(columns=["ID", "P_name", "P_quantity", "P_price (in $/Kg)", "order_date"])
                    new_id = 1 

                order_data = pd.DataFrame([{
                    'ID': new_id,
                    'P_name': product_name,
                    'P_quantity': quantity,
                    'P_price (in $/Kg)': total_price,
                    'order_date': order_date
                }])
                
                orders_df = pd.concat([orders_df, order_data], ignore_index=True)
                orders_df.to_csv(user_order_file, index=False)

                messagebox.showinfo("Success","Order placed successfully!")
                result_area.delete(1.0, END)
            except ValueError : 
                messagebox.showerror("Error", "Please enter a valid quantity.")
            except Exception as e :
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        
        order_button = Button(form_frame, text="Order", command=place_order)
        order_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def open_delete_product_form(self, result_area, username) :
        result_area.delete(1.0, END)
        form_frame = Frame(result_area)
        result_area.window_create("insert", window=form_frame)

        Label(form_frame, text="Select Product to Delete :").grid(row=0,column=0, padx=5, pady=5)

        listbox = Listbox(form_frame)
        listbox.grid(row=1, column=0, pady=5, columnspan=2)

        user_order_file = f'csv_files/orders_{username}.csv'

        try : 
            orders_df = pd.read_csv(user_order_file)
            for index, row in orders_df.iterrows() :
                listbox.insert(END, f"{row['P_name']} (Qty: {row['P_quantity']})")
        except FileNotFoundError :
            messagebox.showerror("Error", "No orders found for this user.")
            return 
        
        def delete_selected_product() :
            selected_index = listbox.curselection()
            if not selected_index :
                messagebox.showerror("Error", "Please select a product to delete.")
                return 
            
            selected_product = listbox.get(selected_index)
            product_name = selected_product.split(" (Qty: ")[0]
            nonlocal orders_df 
            orders_df = orders_df[orders_df['P_name'] != product_name]
            orders_df.to_csv(user_order_file, index=False)
            listbox.delete(selected_index)
            messagebox.showinfo("Success", f"Deleted product: {product_name}")

        delete_button = Button(form_frame, text="Delete", command=delete_selected_product)
        delete_button.grid(row=2, column=0, columnspan=2, pady=10)

    def open_search_prod_form(self, result_area, username) :
        result_area.delete(1.0, END)
        form_frame = Frame(result_area)
        result_area.window_create("insert", window=form_frame)

        Label(form_frame, text="Please Enter a Product Name to Search :").grid(row=0,column=0, padx=5, pady=5)

        product_entry = Entry(form_frame)
        product_entry.grid(row=0, column=1, padx=5, pady=5)

        def search_product() :
            prod_to_search = product_entry.get().strip()
            if not prod_to_search:
                messagebox.showwarning("Input error", "Please enter a product's name to search")
                return 

            try : 
                df = pd.read_csv(f'csv_files/orders_{username}.csv')
                result = df[df['P_name'] == prod_to_search]
                if not result.empty :
                    result = result.iloc[0]
                    result_area.delete(1.0, END)
                    result_area.insert(END,f"Product found :\n"
                                            f"{result['P_name']}\n" 
                                            f"ID: {result['ID']}\n" 
                                            f"Quantity : {result['P_quantity']}\n" 
                                            f"Price : {result['P_price (in $/Kg)']}\n" 
                                            f"Date : {result['order_date']}\n")
                else : 
                    result_area.delete(1.0, END)
                    result_area.insert(END, f"Product '{prod_to_search}' not found.")
            except FileNotFoundError :
                messagebox.showerror("Error","The csv file was not found.")

        search_button = Button(form_frame, text="Search", command=search_product)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

    def open_sort_orders_form(self, result_area, username) : 
        result_area.delete(1.0, END)

        form_frame = Frame(result_area)
        result_area.window_create("insert", window=form_frame)

        Label(form_frame, text="View your orders sorted by :", font=("Arial", 12)).grid(row=0, column=0, columnspan=3, padx=5, pady=10)

        def display_sorted_orders(sort_column) :
            try :
                orders_df = pd.read_csv(f'csv_files/orders_{username}.csv')
                if not orders_df.empty :
                    sorted_df = orders_df.sort_values(by=sort_column)

                    result_area.delete(1.0, END)
                    result_area.insert(END, f"Orders sorted by {sort_column}:\n\n")

                    for index, row in sorted_df.iterrows() :
                        result_area.insert(END, f"{row['P_name']} | "
                                                f"Quantity: {row['P_quantity']} | Price: {row['P_price (in $/Kg)']} | "
                                                f"Order Date: {row['order_date']}\n")
                else :
                    result_area.insert(END, "No orders found.")
            except FileNotFoundError :
                messagebox.showerror("Error", "The csv file was not found.")

        sort_by_name_button = Button(form_frame, text="Sort by Product Name", command=lambda: display_sorted_orders('P_name'))
        sort_by_name_button.grid(row=1, column=0, padx=5, pady=5)

        sort_by_quantity_button = Button(form_frame, text="Sort by Quantity", command=lambda: display_sorted_orders('P_quantity'))
        sort_by_quantity_button.grid(row=1, column=1, padx=5, pady=5)

        sort_by_price_button = Button(form_frame, text="Sort by Price", command=lambda: display_sorted_orders('P_price (in $/Kg)'))
        sort_by_price_button.grid(row=1, column=2, padx=5, pady=5)

        
window = AppWindow()
window.mainloop()


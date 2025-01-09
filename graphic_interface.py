from tkinter import Tk, Label, Entry, messagebox, Toplevel, Button, Frame, Text, END
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
                        messagebox.showinfo("Success", f"Welcome, {username}! Unfortunately, Our systems have detected that your password may be compromised. Please change it on our plateform or use the link we have sent you via e-mail.")
                        self.open_user_menu(username)
                    else :
                        messagebox.showinfo("Success", f"Welcome, {username}!")
                        self.open_user_menu(username)
                else : 
                    messagebox.showerror("Error", "Incorrect password.")
            else : 
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
        Label(menu_window, text=f"Welcome, {username}", font = ("Arial",12)).pack(pady=10)

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

        change_user_info_button = Button(menu_window, text= "Change user info", width=14, bg='white')
        change_user_info_button.place(x=100,y=52)

        del_button = Button(menu_window, text= "Delete account", width=12, bg='white')
        del_button.place(x=270,y=52)

        view_prods_button = Button(button_frame, text= "View my products", width=30, command=lambda: self.view_myprod(result_area, username))
        view_prods_button.pack(pady=10)

        add_prod_button = Button(button_frame, text= "Order new product", width=30, command=lambda: self.open_add_product_form(result_area))
        add_prod_button.pack(pady=10)

        del_prod_button = Button(button_frame, text= "Delete product order", width=30, command=lambda: self.delete_prod(result_area, username))
        del_prod_button.pack(pady=10)

        search_prod_button = Button(button_frame, text= "Search for product", width=30, command=lambda: self.search_prod(result_area, username))
        search_prod_button.pack(pady=10)

        sort_prod_button = Button(button_frame, text= "View products sorted", width=30)
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

    def view_myprod(self, result_area, username):
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

        self.product_list = self.load_product_list()
        self.selected_product_label = Label(self.frame, text="Product : ")
        self.selected_product_label.grid(row=2, column=0)
        self.selected_product = Combobox(self.frame, values=self.product_list)
        self.selected_product.grid(row=2, column=1)
        
        self.quantity_label = Label(self.frame, text="Quantity:")
        self.quantity_label.grid(row=3, column=0)
        self.quantity_entry = Entry(self.frame)
        self.quantity_entry.grid(row=3, column=1)

        self.price_label = Label(self.frame, text="Price: $0")
        self.price_label.grid(row=4, column=1)

        self.quantity_entry.bind("<KeyRelease>", self.update_price)

        self.add_button = Button(self.frame, text="Add Product", command=self.add_prod)
        self.add_button.grid(row=5, columnspan=2, pady=10)
        
    def load_product_list(self) :
        df = pd.read_csv('csv_files/products.csv')
        return df['P_name'].tolist()

    def update_price(self, event=None) :
        selected_product = self.selected_product.get()
        df = pd.read_csv('csv_files/products.csv')
        product_row = df[df['P_name'] == selected_product]
        unit_price = product_row['Price per unit'].values[0]
        try : 
            quantity = int(quantity_entry.get())
            total_price = unit_price * quantity
            price_label.config(text=f"Price: ${total_price:.2f}")
        except ValueError :
            price_label.config(text="Price: $0")

    def add_prod(self, result_area, username):
        selected_product = self.selected_product.get()
        quantity = self.quantity_entry.get()
        if not selected_product or not quantity :
            messagebox.showwarning("Input error", "Please fill all fields")
            return 
        try : 
            quantity = int(quantity)
            if quantity <= 0 :
                messagebox.showerror("Error", "Quantity must be greater than zero.")
                return 
        except ValueError :
            messagebox.showerror("Error", "Please enter a valid number for quantity.")
            return 
        
        product_row = df[df['Product Name'] == selected_product]
        price_per_unit = product_row['Price per unit'].values[0]
        total_price = price_per_unit * quantity
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_id = next_prodid()
        new_row = {'ID': new_id, 'P_name' : selected_product, 'P_quantity': [quantity], 'P_price (in $/Kg)' : total_price, 'order_date' : order_date}

        try : 
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            df = df.append(new_row, ignore_index=True)
            df.to_csv(f'csv_files/orders_{username}.csv', index=False)
            messagebox.showinfo("New product added successfully !")
            clear.entries()
            view_myprod(result_area, username)
        except FileNotFoundError:
            df = pd.DataFrame([new_row])
            df.to_csv(f'csv_files/orders_{username}.csv', index=False)
            messagebox.showinfo("New product added successully !")
            clear.entries()
            view_myprod(result_area, username)

    def delete_prod():
        row_to_delete= delete_name_entry.get()

        if not row_to_delete :
            messagebox.showwarning("Input error", "Please enter the product's name you wish to delete")
            return

        try:
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            df = df[df['P_name'] != row_to_delete]
            df.to_csv(f'csv_files/orders_{username}.csv', index = False)
            messagebox.showinfo(f"Product '{row_to_delete}' deleted successully !")
            delete_name_entry.delete(0, END)
            view_myprod()
        except FileNotFoundError :
            messagebox.showerror("Error", "The file was not found")

    def search_prod():
        prod_to_search = search_name_entry.get()

        if not prod_to_search:
            messagebox.showwarning("Input error", "Please enter the product's name you wish to search : ")
            return 

        try : 
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            if prod_to_search in df['P_name'].values:
                result = df[df['P_name'] == prod_to_search]
                prod_list.delete(1.0, END)
                prod_list.insert[END, f"Product found : {result.iloc[0]['P_name']} | ID: {result.iloc[0]['ID']} | Quantity : {result.iloc[0]['P_quantity']} | Price : {result.iloc[0] ['P_price (in $/Kg)]']} | Date : {result.iloc[0]['order_date']}\n"]
            else : 
                messagebox.showinfo("Search result", f"Product '{prod_to_search}' not found")
        except FileNotFoundError :
            messagebox.showerror("Error","The csv file was not found.")


    def sort_quantity():
        try :
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            df_sorted = df.sort_values(by='P_quantity',ascending=False)
            display_sorted_data(df_sorted)
        except FileNotFoundError :
            messagebox.showerror("Error", "The csv file was not found.")

    def sort_by_price():
        try :
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            df_sorted = df.sort_values(by= 'P_price (in $/Kg)', ascending=False)
            display_sorted_data(df_sorted)
        except FileNotFoundError :
            messagebox.showerror("Error", "The csv file was not found.")

    def sort_by_name():
        try :
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            df_sorted = df.sort_values(by= 'P_name', ascending=True)
            display_sorted_data(df_sorted)
        except FileNotFoundError :
            messagebox.showerror("Error", "The csv file was not found.")


    def apply_sorting():
        sort_criteria = []

        if sort_quantity_ver.get():
           sort_criteria.append('P_quantity')
        if sort_price_var.get():
           sort_criteria.append('P_price (in $/Kg)')
        if sort_name_var.get():
           sort_criteria.append('P_name')

        if not sort_criteria:
           messagebox.showwarning("Input error", "Please select at least one sorting criterion : ")
           return

        try : 
            df = pd.read_csv(f'csv_files/orders_{username}.csv')
            df_sorted = df.sort_values(by=sort_criteria, ascending=False)
            display_sorted_data(df_sorted)
        except FileNotFoundError : 
            messagebox.showerror("Error", "The csv file was not found")

    def display_sorted_data():
        prod_list.delete(1.0, tk.END)
        prod_list.insert(tk.END, "Sorted Products : \n")
        for index, row in df_sorted.iterrows():
            prod_list.insert(tk.END, f"ID : {row['ID']} | Name : {row['P_name']} | Quantity : {row['P_quantity']} | Price : {row['P_price (in $/Kg)']} | Date : {row['order_date']}\n")

        
window = AppWindow()
window.mainloop()


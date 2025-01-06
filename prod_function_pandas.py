# Options du menu interactif
import pandas as pd
from os.path import isfile

# Options du menu interactif
def display_menu():
    print("\nInteractive Menu:")
    print("1. View products only")
    print("2. Add a new product")
    print("3. Delete a product")
    print("4. Search for a specific product")
    print("5. Sort table")
    print("6. Close file")
    option = input("Enter your choice (1-6): ")
    return option

# Options du menu interactif de tri
def sort_menu():
    print("Choose sorting method : ")
    print("1. Sort by Quantity (QuickSort)")
    print("2. Sort by Price (MergeSort)")
    print("3. Sort by Product in alphabetical order (Bubble sort)")
    sort_choice = input("Choose a method (1-3): ")  # Inviter l'utilisateur a choisir une methode de tri en saissant un chiffre (1, 2 ou 3)
    return sort_choice

# Option 1 : Afficher la liste de produits
def view_names(chemin):
    try:
        df = pd.read_csv(chemin)
        print("List of products : ")
        for index, row in df.iterrows():
            print(row['P_name'])
    except FileNotFoundError:
        print("The csv_files file was not found")

# Option 2 : Ajouter un nouveau produit

# Defintion de l'ID du nouveau produit, Permet d'avoir un ID unique pour chaque produit
def next_id(chemin):
    try:
        df = pd.read_csv(chemin)
        last_id = df['ID'].max()
        return int(last_id) + 1
    except FileNotFoundError:
        return 1  # Start with ID 1 if file doesn't exist

# Ajout du nouveau produit dans la liste
def new_product(chemin):
    # Demande des détails du produit à l'utilisateur
    new_prod = input("Enter the name of a new product : ")
    new_quant = input("Enter its quantity : ")
    new_price = input("Enter its price (/kg) : ")
    new_expdate = input("Enter the expiration date (dd-mm-yy) : ")
    new_id = next_id()  # Defintion de l'ID du nouveau produit grace a la fonction next_id()
    new_row = [new_id, new_prod, new_quant, new_price, new_expdate]
    #The below line was incorrectly indented causing the error.
    prod_df = pd.DataFrame(columns=["ID", "P_name", "P_quantity", "P_price (in $/Kg)", "order_date"])  # Ouvre notre liste de produit avec le mode read
    prod_df.to_csv('csv_files', index=False, mode='a', header=not isfile('csv_files'))  # Lecture du fichier csv et convertion en dictionnaire Python
    # writer.writerow(new_row)
    print("New product added successfully.")
    prod_df = pd.read_csv(columns=["ID", "P_name", "P_quantity", "P_price (in $/Kg)", "order_date"])  # Ouvre notre liste de produit avec le mode read
    prod_df.to_csv(products.csv, index=False)  # Lecture du contenu du fichier

# Option 3 : delete product row
def delete_product(chemin):
    row_to_delete = input("Enter the row you wish to delete.")
    try:  # Utilisation de try en cas d'erreurs du fichier
        df = pd.read_csv(chemin)  # Changed from 'products_functions.py' to 'products.csv'
        reader = pd.DataFrame(open(chemin))  # Added open function to read the csv
        rows = [row for row in reader if row["P_name"] != row_to_delete]  # Définir les lignes qui ne correspondent pas à celle indiqué pour deletion
        #Fixed indentation of next line
        total_rows = len(df) # Calcul du nombre total de lignes
        if len(rows) == 0 or len(rows) == total_rows:
            print(f"No row with Name = '{row_to_delete}' was found.") # Indique si la ligne n'existe pas
            return
        #Fixed indentation and removed pd.DataFrame call on a string
        df = pd.read_csv(chemin)
        df.drop(df[df['P_name'] == row_to_delete].index, inplace=True)
        print(f"The product : {row_to_delete} has been deleted.")
    except FileNotFoundError:
        print(f"Error: The file '{produits}' does not exist.") #'produits' variable is not defined. You should use products.csv or the defined filename
    except KeyError:
        print(f"Error: The column 'P_name' does not exist in the file.")

def search_prod() :
    df = pd.read_csv(chemin)
    prod_to_search = input("Enter the product you wish to search : ")
    if prod_to_search in df["P_name"] :
        location = df["P_name"].index(prod_to_search)
        return f"Product {prod_to_search} found at index {location}"
    else : 
        return f"Product {prod_to_search} not found "



# sorting table by quantity
def sort_quantity(chemin) :
    df = pd.read_csv(chemin)
    df_sorted_quantity = df.sort_values(by='P_quantity',ascending=False)
    print("Table sorted by quantity : ")
    print(df_sorted_quantity)

# sorting table by price
def sort_price(chemin) :
    df = pd.read_csv(chemin)
    df_sorted_price = df.sort_values(by='P_price (in $/Kg)',ascending=False)
    print("Table sorted by price : ")
    print(df_sorted_price)

# sort table by name
def sort_name(chemin) :
    df = pd.read_csv(chemin)
    df_sorted_name = df.sort_values(by='P_name',ascending=False)
    print("Table sorted by product name : ")
    print(df_sorted_name)
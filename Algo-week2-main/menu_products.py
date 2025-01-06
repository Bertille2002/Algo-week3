### Menu interactif ###
from prod_function_pandas import *
from user_functions import *
from login_menu import *
import pandas as pd  

# fonctions options du menu 
def products_main(username):
  produits = f'csv_files/orders_{username}.csv' # definir le fichier individuel 
  print(f"Welcome, {username} ! You're now managing : {produits}.")
  while True :
    input = display_menu()
    if input == "1" :
      view_names(produits) # Voir la liste des produits, noms uniquement
    elif input == "2" :
      new_product(produits) # Ajouter un produit a la bdd (base de donnees)
    elif input == "3" :
      delete_product(produits) # Supprimer un produit de la bdd
    elif input == "4" :
      search_value_in_df(produits) # Recherche d'un produit, algorithme recherche binaire
    elif input == "5" : 
      sort_choice = sort_menu()
      if sort_choice == "1" : # Tri de la bdd par quantité avec QuickSort 
        sort_quantity(produits)
      elif sort_choice == "2" : # Tri par prix avec MergeSort
        sort_price(produits)
      elif sort_choice == "3" : # Tri par produit ordre alphabetique 
        sort_name(produits)
      else : # Echec de la requete si la valeur saisie ne correspond pas a une option de tri défini
        print("Invalid option.")
    elif input == "6" : # Fermer le menu interactif 
      print("Closing program.")
      break
    else : # Echec de la requete si la valeur saisie ne correspond pas a une option défini
      print("Invalid input.")

if __name__ == "__products_main__" :
  products_main()
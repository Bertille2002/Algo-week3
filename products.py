import pandas as pd 

products_available = [
    [1,"pesto","5.55"],
    [2,"morbier","14.75"],
    [3,"linguine","1.15"],
    [4, "saumon","25.30"],
    [5, "clémentines", "6.99"],
    [6, "poulet", "15.25"],
    [7,"poires","15.5"],
    [8,"lardons","5.45"],
    [9,"Mozzarella","1.05"],
    [10, "huîtres", "45.99"],
    [11, "salades", "2.50"],
    [12, "thym", "7.5"],
    [13, "pomme", "18.2"],
    [14, "oeuf", "43.1"],
    [15, "pasta", "1.05"],
    [16, "riz", "2.3"],
    [17, "lait", "0.99"],
    [18, "fromage", "5.5"],
    [19, "Ananas", "6.99"],
    [20, "Chocolat", "1.05"],
    [21, "Whisky", "89.99"],
    [22, "Chips","1.65"],
    [23, "olives", "5.5"],
    [24,"Café","8.15"],
    [25,"Poivrons","4.50"],
    [26,"Huile d'olive","15.69"],
    [27, "Crevettes",  "34.99"],
    [28, "Litchi", "9.99"],
    [29, "Frites","7.5"],
    [30,"Raisins","10.15"],
    [31,"Entrecote","14.99"],
    [32,"Parmesan","5.99"],
    [33, "Carottes", "4.95"],
    [34, "Dessert", "3.84"],
    [35, "Crème Fraiche","6.15"]
]

df = pd.DataFrame(products_available, columns=["ID", "P_name", "P_price (in $/Kg)"])
df.to_csv('products.csv', index=False)
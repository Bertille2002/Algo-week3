import csv

with open('login_attempts.csv', 'w', newline='') as file :
    writer = csv.writer(file)
    field = ['timestamp', 'username', 'password', 'status']
    writer.writerow(field)
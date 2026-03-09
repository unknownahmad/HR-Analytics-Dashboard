import csv
import os

FILE_NAME = "employees.csv"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_data(employees):
    if not employees:
        return

    headers = employees[0].keys()
    
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(employees)
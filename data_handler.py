import csv
import os

FILE_NAME = "employees.csv"

def load_data():
    file_exists = os.path.exists(FILE_NAME)
    
    if file_exists == False:
        empty_list = []
        return empty_list
    
    with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file_object:
        reader = csv.DictReader(file_object)
        
        data_list = []
        
        for row in reader:
            data_list.append(row)
            
        return data_list

def save_data(employees):
    length_of_data = len(employees)
    
    if length_of_data == 0:
        return
    
    first_employee = employees[0]
    headers = first_employee.keys()
    
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file_object:
        writer = csv.DictWriter(file_object, fieldnames=headers)
        
        writer.writeheader()
        
        for emp in employees:
            writer.writerow(emp)

def export_report(report_text):
    with open("department_report.txt", mode='w', encoding='utf-8') as file_object:
        file_object.write(report_text)
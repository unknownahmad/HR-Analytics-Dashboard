import data_handler
import analytics
from tabulate import tabulate

def get_valid_salary():
    while True:
        salary_input = input("Enter salary: ")
        
        is_digit = salary_input.isdigit()
        
        if is_digit == True:
            return salary_input
            
        print("Invalid input. Please enter a whole number.")

def view_employees(employees):
    number_of_employees = len(employees)
    
    if number_of_employees == 0:
        print("No employees found in the system.")
        return
    
    table_data = []
    
    for emp in employees:
        name = emp['name']
        department = emp['department']
        salary_string = emp['salary']
        salary_float = float(salary_string)
        formatted_salary = f"${salary_float:,.0f}"
        
        row = [name, department, formatted_salary]
        table_data.append(row)
        
    headers = ["Name", "Department", "Salary"]
    print("\n")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def delete_employee(employees):
    name_to_remove = input("Enter the full name of the employee to delete: ")
    
    count_before = len(employees)
    
    updated_list = analytics.remove_employee_by_name(employees, name_to_remove)
    
    count_after = len(updated_list)
    
    if count_after < count_before:
        data_handler.save_data(updated_list)
        print("Employee removed successfully.")
        return updated_list
    else:
        print("Employee name not found.")
        return employees

def edit_employee_salary(employees):
    name_to_find = input("Enter the full name of the employee to edit: ")
    
    employee_exists = False
    
    for emp in employees:
        current_name = emp['name']
        current_name_lower = current_name.lower()
        search_name_lower = name_to_find.lower()
        
        if current_name_lower == search_name_lower:
            employee_exists = True
            
    if employee_exists == False:
        print("Employee not found.")
        return employees
        
    new_salary_value = get_valid_salary()
    
    updated_list = analytics.update_employee_salary(employees, name_to_find, new_salary_value)
    
    data_handler.save_data(updated_list)
    
    print("Salary updated and saved to file.")
    return updated_list

def display_menu():
    print("\n--- HR Analytics Dashboard ---")
    print("1. View All Employees")
    print("2. Add New Employee")
    print("3. View Detailed Statistics")
    print("4. Filter by Department")
    print("5. Export Analysis Report")
    print("6. Delete Employee")
    print("7. Edit Employee Salary")
    print("8. Exit")

def main():
    employees = data_handler.load_data()
    
    while True:
        display_menu()
        choice = input("Select an option (1-8): ")
        
        if choice == "1":
            view_employees(employees)
            
        elif choice == "2":
            name = input("Enter name: ")
            dept = input("Enter department: ")
            sal = get_valid_salary()
            
            new_emp = {}
            new_emp["name"] = name
            new_emp["department"] = dept
            new_emp["salary"] = sal
            
            employees.append(new_emp)
            data_handler.save_data(employees)
            print("Employee added.")
            
        elif choice == "3":
            stats = analytics.calculate_global_stats(employees)
            print("\n--- Salary Stats ---")
            print(f"Average: ${stats['avg']:,.2f}")
            print(f"Median:  ${stats['median']:,.2f}")
            print(f"Range:   ${stats['min']:,.0f} - ${stats['max']:,.0f}")
            
        elif choice == "4":
            target = input("Department name: ")
            filtered = analytics.filter_by_dept(employees, target)
            view_employees(filtered)
            
        elif choice == "5":
            analysis = analytics.get_department_analysis(employees)
            report_text = "HR SUMMARY REPORT\n"
            report_text = report_text + "=================\n"
            for d, data in analysis.items():
                line = f"{d}: {data['count']} staff | Avg: ${data['avg']:,.2f}\n"
                report_text = report_text + line
            data_handler.export_report(report_text)
            print("Report saved.")
            
        elif choice == "6":
            employees = delete_employee(employees)
            
        elif choice == "7":
            employees = edit_employee_salary(employees)
            
        elif choice == "8":
            print("Shutting down...")
            break
            
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
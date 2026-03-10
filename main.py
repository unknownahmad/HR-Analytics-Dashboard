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
        if emp['name'].lower() == name_to_find.lower():
            employee_exists = True
            
    if employee_exists == False:
        print("Employee not found.")
        return employees
        
    new_salary_value = get_valid_salary()
    updated_list = analytics.update_employee_salary(employees, name_to_find, new_salary_value)
    data_handler.save_data(updated_list)
    print("Salary updated and saved to file.")
    return updated_list

def run_raise_simulation(employees):
    percent_input = input("Enter the percentage increase (e.g., 5 for 5%): ")
    
    is_valid = percent_input.replace('.', '', 1).isdigit()
    
    if is_valid == False:
        print("Please enter a valid number.")
        return
        
    percent_float = float(percent_input)
    new_total, new_avg = analytics.simulate_raise(employees, percent_float)
    
    stats = analytics.calculate_global_stats(employees)
    old_total = stats["total"]
    difference = new_total - old_total
    
    print(f"\n--- Raise Simulation ({percent_input}%) ---")
    print(f"Current Total Payroll: ${old_total:,.2f}")
    print(f"New Total Payroll:     ${new_total:,.2f}")
    print(f"Total Budget Increase: ${difference:,.2f}")
    print(f"New Average Salary:    ${new_avg:,.2f}")

def display_menu():
    print("\n--- HR Analytics Dashboard ---")
    print("1. View All Employees")
    print("2. Add New Employee")
    print("3. View Detailed Statistics")
    print("4. Filter by Department")
    print("5. Export Analysis Report")
    print("6. Delete Employee")
    print("7. Edit Employee Salary")
    print("8. Simulate Company-Wide Raise")
    print("9. Exit")

def main():
    employees = data_handler.load_data()
    
    while True:
        display_menu()
        choice = input("Select an option (1-9): ")
        
        if choice == "1":
            view_employees(employees)
        elif choice == "2":
            name = input("Enter name: ")
            dept = input("Enter department: ")
            sal = get_valid_salary()
            new_emp = {"name": name, "department": dept, "salary": sal}
            employees.append(new_emp)
            data_handler.save_data(employees)
        elif choice == "3":
            stats = analytics.calculate_global_stats(employees)
            print(f"\nAvg: ${stats['avg']:,.2f} | Median: ${stats['median']:,.2f}")
            print(f"Range: ${stats['min']:,.0f} - ${stats['max']:,.0f}")
        elif choice == "4":
            target = input("Department: ")
            filtered = analytics.filter_by_dept(employees, target)
            view_employees(filtered)
        elif choice == "5":
            analysis = analytics.get_department_analysis(employees)
            report = "HR REPORT\n=========\n"
            for d, data in analysis.items():
                report += f"{d}: {data['count']} staff | Avg: ${data['avg']:,.2f}\n"
            data_handler.export_report(report)
            print("Report saved.")
        elif choice == "6":
            employees = delete_employee(employees)
        elif choice == "7":
            employees = edit_employee_salary(employees)
        elif choice == "8":
            run_raise_simulation(employees)
        elif choice == "9":
            print("Shutting down...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
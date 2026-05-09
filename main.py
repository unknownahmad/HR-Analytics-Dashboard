import data_handler
import analytics
from tabulate import tabulate

def get_valid_number(prompt: str) -> float:
    """Robust input validation using try/except."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid numerical value.")

def view_employees(employees: list[dict]) -> None:
    if not employees:
        print("No employees found in the system.")
        return
    
    table_data = [
        [emp['name'], emp['department'], f"${float(emp['salary']):,.0f}"]
        for emp in employees
    ]
    
    print("\n" + tabulate(table_data, headers=["Name", "Department", "Salary"], tablefmt="grid"))

def run_raise_simulation(employees: list[dict]) -> None:
    percent_float = get_valid_number("Enter the percentage increase (e.g., 5 for 5%): ")
    new_total, new_avg = analytics.simulate_raise(employees, percent_float)
    
    stats = analytics.calculate_global_stats(employees)
    difference = new_total - stats["total"]
    
    print(f"\n--- Raise Simulation ({percent_float}%) ---")
    print(f"Current Total Payroll: ${stats['total']:,.2f}")
    print(f"New Total Payroll:     ${new_total:,.2f}")
    print(f"Total Budget Increase: ${difference:,.2f}")
    print(f"New Average Salary:    ${new_avg:,.2f}")

def display_menu() -> None:
    print("\n--- HR Analytics Dashboard ---")
    print("1. View All Employees\n2. Add New Employee\n3. View Detailed Statistics")
    print("4. Filter by Department\n5. Export Analysis Report\n6. Delete Employee")
    print("7. Edit Employee Salary\n8. Simulate Company-Wide Raise\n9. Exit")

def main() -> None:
    employees = data_handler.load_data()
    
    while True:
        display_menu()
        choice = input("\nSelect an option (1-9): ")
        
        if choice == "1":
            view_employees(employees)
        elif choice == "2":
            name = input("Enter name: ")
            dept = input("Enter department: ")
            sal = get_valid_number("Enter salary: ")
            employees.append({"name": name, "department": dept, "salary": sal})
            data_handler.save_data(employees)
            print("✅ Employee added successfully.")
        elif choice == "3":
            stats = analytics.calculate_global_stats(employees)
            print(f"\nAvg: ${stats['avg']:,.2f} | Median: ${stats['median']:,.2f}")
            print(f"Range: ${stats['min']:,.0f} - ${stats['max']:,.0f}")
        elif choice == "4":
            target = input("Department: ")
            view_employees(analytics.filter_by_dept(employees, target))
        elif choice == "5":
            analysis = analytics.get_department_analysis(employees)
            report = "HR REPORT\n=========\n"
            for d, data in analysis.items():
                report += f"{d}: {data['count']} staff | Avg: ${data['avg']:,.2f}\n"
            data_handler.export_report(report)
            print("✅ Report saved.")
        elif choice == "6":
            name_to_remove = input("Enter the exact name of the employee to delete: ")
            employees = analytics.remove_employee_by_name(employees, name_to_remove)
            data_handler.save_data(employees)
            print("✅ Update complete.")
        elif choice == "7":
            name_to_edit = input("Enter the exact name of the employee to edit: ")
            new_sal = str(get_valid_number("Enter new salary: "))
            employees = analytics.update_employee_salary(employees, name_to_edit, new_sal)
            data_handler.save_data(employees)
            print("✅ Salary updated.")
        elif choice == "8":
            run_raise_simulation(employees)
        elif choice == "9":
            print("Shutting down...")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-9.")

if __name__ == "__main__":
    main()
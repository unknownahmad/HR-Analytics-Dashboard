employees = [
    {"name": "John", "department": "Sales", "salary": 50000},
    {"name": "Alice", "department": "IT", "salary": 60000},
    {"name": "Bob", "department": "HR", "salary": 45000},
    {"name": "Sarah", "department": "IT", "salary": 75000}
]

while True:
    print("\n" + "="*32)
    print("      HR ANALYTICS DASHBOARD")
    print("="*32)
    print("1. View All Employees")
    print("2. Add New Employee")
    print("3. Remove Employee")
    print("4. Department Statistics (Avg Salary)")
    print("5. Exit")
        
    choice=input("\n"+"Select an option (1-5): ")
    
    if choice=="1":
        print("\nAll Employees:")
        for emp in employees:
            print(f"- {emp['name']} ({emp['department']}): ${emp['salary']}")
    
    elif choice=="2":
        n=input("Name: ")
        d=input("Department: ")
        s=int(input("Salary (numbers only): "))
        new_emp={"name": n,"department": d,"salary": s}
        employees.append(new_emp)
        print("Employee added!")
    
    break
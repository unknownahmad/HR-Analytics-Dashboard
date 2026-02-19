#list of employees dictionaries
#each employee is represented as a dictionary with name, department and salary
employees = [
    {"name": "John", "department": "Sales", "salary": 50000},
    {"name": "Alice", "department": "IT", "salary": 60000},
    {"name": "Bob", "department": "HR", "salary": 45000},
    {"name": "Sarah", "department": "IT", "salary": 75000}
]
#main programe loop
while True:
    # display the menu header and options
    print("\n" + "="*32)
    print("      HR ANALYTICS DASHBOARD")
    print("="*32)
    print("1. View All Employees")
    print("2. Add New Employee")
    print("3. Remove Employee")
    print("4. Company Average")
    print("5. Exit")
    #input :)
    choice=input("\n"+"Select an option (1-5): ")
    
    if choice=="1":
        print("\nAll Employees:")
        #loop thru the employees and print their info
        for emp in employees:
            print(f"- {emp['name']} ({emp['department']}): ${emp['salary']}")
    
    elif choice=="2":
        #get new details
        n=input("Name: ")
        d=input("Department: ")
        s=int(input("Salary (numbers only): "))
        #create new dict
        new_emp={"name": n,"department": d,"salary": s}
        #add it the the list and voilaaaa
        employees.append(new_emp)
        print("Employee added!")
        
    elif choice=="3":
        name_to_remove=input("Enter name to remove: ")
        #set a boolian so we can track if the employee was found and deleted
        found=False
        for i in range(len(employees)):
            if employees[i]["name"].lower()==name_to_remove.lower():
                employees.pop(i)
                print("Removed successfully.")
                found=True
                break
        if not found:
            print("Name not found.")
    
    elif choice == "4":
        total = 0
        #sum of all saleries
        for emp in employees:
            total =total+ emp["salary"]
        #check to avoide division by 0 so it dont crash
        if len(employees)>0:
            avg=total/len(employees)
            print(f"Total Employees: {len(employees)}")
            print(f"Average Salary: ${avg}")
    #bye bye        
    elif choice == "5":
        print("Goodbye!")
        break
    #for invalid input
    else:
        print("Invalid choice.")

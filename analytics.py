def calculate_global_stats(employees):
    total_employees = len(employees)
    
    if total_employees == 0:
        empty_stats = {}
        empty_stats["count"] = 0
        empty_stats["total"] = 0
        empty_stats["avg"] = 0
        return empty_stats
    
    total_salary = 0.0
    
    for emp in employees:
        salary_string = emp['salary']
        salary_float = float(salary_string)
        total_salary = total_salary + salary_float
        
    average_salary = total_salary / total_employees
    
    stats = {}
    stats["count"] = total_employees
    stats["total"] = total_salary
    stats["avg"] = average_salary
    
    return stats

def get_department_analysis(employees):
    dept_data = {}
    
    for emp in employees:
        department_name = emp['department']
        salary_string = emp['salary']
        salary_float = float(salary_string)
        
        is_department_present = department_name in dept_data
        
        if is_department_present == False:
            empty_salary_list = []
            dept_data[department_name] = empty_salary_list
            
        dept_data[department_name].append(salary_float)
    
    analysis = {}
    
    for dept, salaries in dept_data.items():
        total_department_salary = 0.0
        
        for sal in salaries:
            total_department_salary = total_department_salary + sal
            
        headcount = len(salaries)
        average_department_salary = total_department_salary / headcount
        
        department_stats = {}
        department_stats["avg"] = average_department_salary
        department_stats["count"] = headcount
        
        analysis[dept] = department_stats
        
    return analysis
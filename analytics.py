def calculate_global_stats(employees):
    total_employees = len(employees)
    
    if total_employees == 0:
        empty_stats = {}
        empty_stats["count"] = 0
        empty_stats["total"] = 0
        empty_stats["avg"] = 0
        empty_stats["min"] = 0
        empty_stats["max"] = 0
        empty_stats["median"] = 0
        return empty_stats
    
    salaries_list = []
    total_salary_sum = 0.0
    
    for emp in employees:
        salary_string = emp['salary']
        salary_float = float(salary_string)
        salaries_list.append(salary_float)
        total_salary_sum = total_salary_sum + salary_float
        
    salaries_list.sort()
    
    minimum_salary = salaries_list[0]
    maximum_salary = salaries_list[-1]
    
    average_salary = total_salary_sum / total_employees
    
    is_even = total_employees % 2 == 0
    middle_index = total_employees // 2
    
    if is_even == True:
        right_middle_value = salaries_list[middle_index]
        left_middle_index = middle_index - 1
        left_middle_value = salaries_list[left_middle_index]
        median_salary = (left_middle_value + right_middle_value) / 2
    else:
        median_salary = salaries_list[middle_index]

    stats = {}
    stats["count"] = total_employees
    stats["total"] = total_salary_sum
    stats["avg"] = average_salary
    stats["min"] = minimum_salary
    stats["max"] = maximum_salary
    stats["median"] = median_salary
    
    return stats

def get_department_analysis(employees):
    dept_groups = {}
    
    for emp in employees:
        department_name = emp['department']
        salary_string = emp['salary']
        salary_float = float(salary_string)
        
        present_in_map = department_name in dept_groups
        
        if present_in_map == False:
            new_list = []
            dept_groups[department_name] = new_list
            
        dept_groups[department_name].append(salary_float)
    
    analysis_results = {}
    
    for dept, salaries in dept_groups.items():
        sum_of_dept_salaries = 0.0
        
        for s in salaries:
            sum_of_dept_salaries = sum_of_dept_salaries + s
            
        number_of_dept_staff = len(salaries)
        dept_average = sum_of_dept_salaries / number_of_dept_staff
        
        single_dept_stats = {}
        single_dept_stats["avg"] = dept_average
        single_dept_stats["count"] = number_of_dept_staff
        
        analysis_results[dept] = single_dept_stats
        
    return analysis_results

def filter_by_dept(employees, target_department):
    filtered_list = []
    
    standard_target = target_department.lower()
    
    for emp in employees:
        current_dept = emp['department']
        standard_current = current_dept.lower()
        
        if standard_current == standard_target:
            filtered_list.append(emp)
            
    return filtered_list

def remove_employee_by_name(employees, name_to_delete):
    updated_list = []
    
    name_to_delete_lower = name_to_delete.lower()
    
    for emp in employees:
        current_name = emp['name']
        current_name_lower = current_name.lower()
        
        is_match = current_name_lower == name_to_delete_lower
        
        if is_match == False:
            updated_list.append(emp)
            
    return updated_list
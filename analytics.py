def calculate_average_salary(employees):
    if not employees:
        return 0
    total = sum(float(emp['salary']) for emp in employees)
    return total / len(employees)

def get_department_stats(employees):
    stats = {}
    
    for emp in employees:
        dept = emp['department']
        sal = float(emp['salary'])
        
        if dept not in stats:
            stats[dept] = []
        stats[dept].append(sal)
    
    averages = {}
    for dept, salaries in stats.items():
        averages[dept] = sum(salaries) / len(salaries)
        
    return averages

def find_top_earners(employees, threshold=60000):
    return [emp for emp in employees if float(emp['salary']) >= threshold]
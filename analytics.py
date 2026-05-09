import statistics
from collections import defaultdict

def calculate_global_stats(employees: list[dict]) -> dict:
    """Calculates min, max, average, and median salaries."""
    if not employees:
        return {"count": 0, "total": 0, "avg": 0, "min": 0, "max": 0, "median": 0}
    
    # Extract salaries into a clean list of floats using a list comprehension
    salaries = [float(emp['salary']) for emp in employees]
    
    return {
        "count": len(salaries),
        "total": sum(salaries),
        "avg": sum(salaries) / len(salaries),
        "min": min(salaries),
        "max": max(salaries),
        "median": statistics.median(salaries)
    }

def get_department_analysis(employees: list[dict]) -> dict:
    """Calculates average salary and headcount per department."""
    dept_salaries = defaultdict(list)
    
    for emp in employees:
        dept_salaries[emp['department']].append(float(emp['salary']))
        
    return {
        dept: {
            "avg": sum(salaries) / len(salaries),
            "count": len(salaries)
        }
        for dept, salaries in dept_salaries.items()
    }

def filter_by_dept(employees: list[dict], target_department: str) -> list[dict]:
    """Returns a list of employees matching the target department."""
    target = target_department.lower()
    return [emp for emp in employees if emp['department'].lower() == target]

def remove_employee_by_name(employees: list[dict], name_to_delete: str) -> list[dict]:
    """Returns a new list excluding the specified employee."""
    target = name_to_delete.lower()
    return [emp for emp in employees if emp['name'].lower() != target]

def update_employee_salary(employees: list[dict], target_name: str, new_salary: str) -> list[dict]:
    """Updates an employee's salary and returns the updated list."""
    target = target_name.lower()
    for emp in employees:
        if emp['name'].lower() == target:
            emp['salary'] = new_salary
            break # Efficiency: stop looping once we find the exact person
    return employees

def simulate_raise(employees: list[dict], percentage_increase: float) -> tuple[float, float]:
    """Calculates the new total payroll and average salary after a company-wide raise."""
    if not employees:
        return 0.0, 0.0
        
    multiplier = 1 + (percentage_increase / 100)
    
    new_total = sum(float(emp['salary']) * multiplier for emp in employees)
    new_avg = new_total / len(employees)
    
    return new_total, new_avg
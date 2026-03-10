import customtkinter as ctk
import data_handler
import analytics

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("HR Analytics Dashboard")
        self.geometry("1100x750")
        
        self.employees = data_handler.load_data()
        self.display_list = self.employees
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="HR DATA PRO", font=("Helvetica", 20, "bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=20)

        self.btn_view = ctk.CTkButton(self.sidebar, text="1. View All Employees", command=self.view_all)
        self.btn_view.grid(row=1, column=0, padx=20, pady=10)

        self.btn_add = ctk.CTkButton(self.sidebar, text="2. Add Employee", command=self.open_add)
        self.btn_add.grid(row=2, column=0, padx=20, pady=10)

        self.btn_stats = ctk.CTkButton(self.sidebar, text="3. Detailed Stats", command=self.open_stats)
        self.btn_stats.grid(row=3, column=0, padx=20, pady=10)

        self.filter_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Department Name")
        self.filter_entry.grid(row=4, column=0, padx=20, pady=(15, 5))
        
        self.btn_filter = ctk.CTkButton(self.sidebar, text="4. Filter List", command=self.apply_filter)
        self.btn_filter.grid(row=5, column=0, padx=20, pady=(0, 10))

        self.btn_export = ctk.CTkButton(self.sidebar, text="5. Export Report", command=self.export_data)
        self.btn_export.grid(row=6, column=0, padx=20, pady=10)

        self.btn_del = ctk.CTkButton(self.sidebar, text="6. Delete Employee", command=self.open_delete)
        self.btn_del.grid(row=7, column=0, padx=20, pady=10)

        self.btn_edit = ctk.CTkButton(self.sidebar, text="7. Edit Salary", command=self.open_edit)
        self.btn_edit.grid(row=8, column=0, padx=20, pady=10)

        self.btn_sim = ctk.CTkButton(self.sidebar, text="8. Simulate Raise", command=self.open_simulate)
        self.btn_sim.grid(row=9, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.sidebar, text="", text_color="green", font=("Helvetica", 12))
        self.status_label.grid(row=10, column=0, padx=20, pady=20)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        self.stats_frame = ctk.CTkFrame(self.main_container, height=80)
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.avg_label = ctk.CTkLabel(self.stats_frame, text="Avg: $0", font=("Helvetica", 16, "bold"))
        self.avg_label.pack(side="left", padx=30, pady=20)
        
        self.med_label = ctk.CTkLabel(self.stats_frame, text="Median: $0", font=("Helvetica", 16, "bold"))
        self.med_label.pack(side="left", padx=30, pady=20)

        self.count_label = ctk.CTkLabel(self.stats_frame, text="Staff: 0", font=("Helvetica", 16, "bold"))
        self.count_label.pack(side="right", padx=30, pady=20)

        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, label_text="Data View")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.active_window = None

        self.refresh_ui()

    def set_status(self, message):
        self.status_label.configure(text=message)

    def view_all(self):
        self.display_list = self.employees
        self.refresh_ui()
        self.set_status("Viewing all records.")

    def apply_filter(self):
        target = self.filter_entry.get()
        target_is_empty = target == ""
        
        if target_is_empty == True:
            self.set_status("Enter dept to filter.")
            return
            
        filtered_data = analytics.filter_by_dept(self.employees, target)
        self.display_list = filtered_data
        self.refresh_ui()
        self.set_status(f"Filtered: {target}")

    def export_data(self):
        analysis_data = analytics.get_department_analysis(self.employees)
        report_string = "HR SUMMARY REPORT\n=================\n"
        
        for dept, data in analysis_data.items():
            count_val = data['count']
            avg_val = data['avg']
            line = f"{dept}: {count_val} staff | Avg: ${avg_val:,.2f}\n"
            report_string = report_string + line
            
        data_handler.export_report(report_string)
        self.set_status("Report Exported.")

    def refresh_ui(self):
        children = self.scroll_frame.winfo_children()
        
        for widget in children:
            widget.destroy()

        stats = analytics.calculate_global_stats(self.display_list)
        
        avg_value = stats['avg']
        med_value = stats['median']
        count_value = stats['count']
        
        self.avg_label.configure(text=f"Avg: ${avg_value:,.2f}")
        self.med_label.configure(text=f"Median: ${med_value:,.2f}")
        self.count_label.configure(text=f"Staff: {count_value}")

        for emp in self.display_list:
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(fill="x", pady=5, padx=5)
            
            name_label = ctk.CTkLabel(row, text=emp['name'], width=200, anchor="w")
            name_label.pack(side="left", padx=10)
            
            dept_label = ctk.CTkLabel(row, text=emp['department'], width=150)
            dept_label.pack(side="left", padx=10)
            
            sal_string = emp['salary']
            sal_float = float(sal_string)
            sal_label = ctk.CTkLabel(row, text=f"${sal_float:,.0f}", width=100)
            sal_label.pack(side="left", padx=10)

    def check_active_window(self):
        is_open = self.active_window is not None
        
        if is_open == True:
            window_exists = self.active_window.winfo_exists()
            if window_exists == True:
                self.active_window.focus()
                return True
        return False

    def open_add(self):
        is_open = self.check_active_window()
        if is_open == True:
            return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Add Employee")
        self.active_window.geometry("350x400")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Name:").pack(pady=(20, 5))
        self.add_name = ctk.CTkEntry(self.active_window, width=200)
        self.add_name.pack()

        ctk.CTkLabel(self.active_window, text="Department:").pack(pady=(10, 5))
        self.add_dept = ctk.CTkEntry(self.active_window, width=200)
        self.add_dept.pack()

        ctk.CTkLabel(self.active_window, text="Salary:").pack(pady=(10, 5))
        self.add_sal = ctk.CTkEntry(self.active_window, width=200)
        self.add_sal.pack()

        self.add_err = ctk.CTkLabel(self.active_window, text="", text_color="red")
        self.add_err.pack(pady=10)

        ctk.CTkButton(self.active_window, text="Save", command=self.execute_add).pack(pady=10)

    def execute_add(self):
        n = self.add_name.get()
        d = self.add_dept.get()
        s = self.add_sal.get()

        if n == "" or d == "" or s == "":
            self.add_err.configure(text="All fields required.")
            return
            
        if s.isdigit() == False:
            self.add_err.configure(text="Salary must be numbers.")
            return

        new_emp = {}
        new_emp["name"] = n
        new_emp["department"] = d
        new_emp["salary"] = s

        self.employees.append(new_emp)
        data_handler.save_data(self.employees)
        self.display_list = self.employees
        self.refresh_ui()
        self.set_status("Employee Added.")
        self.active_window.destroy()

    def open_stats(self):
        is_open = self.check_active_window()
        if is_open == True:
            return

        stats = analytics.calculate_global_stats(self.employees)
        
        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Detailed Stats")
        self.active_window.geometry("300x250")
        self.active_window.attributes('-topmost', True)

        min_val = stats['min']
        max_val = stats['max']
        total_val = stats['total']

        ctk.CTkLabel(self.active_window, text="Global Statistics", font=("Helvetica", 16, "bold")).pack(pady=20)
        ctk.CTkLabel(self.active_window, text=f"Minimum Salary: ${min_val:,.0f}").pack(pady=5)
        ctk.CTkLabel(self.active_window, text=f"Maximum Salary: ${max_val:,.0f}").pack(pady=5)
        ctk.CTkLabel(self.active_window, text=f"Total Payroll: ${total_val:,.0f}").pack(pady=5)

    def open_delete(self):
        is_open = self.check_active_window()
        if is_open == True:
            return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Delete Employee")
        self.active_window.geometry("300x200")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Exact Name to Delete:").pack(pady=(20, 5))
        self.del_name = ctk.CTkEntry(self.active_window, width=200)
        self.del_name.pack()

        self.del_err = ctk.CTkLabel(self.active_window, text="", text_color="red")
        self.del_err.pack(pady=5)

        ctk.CTkButton(self.active_window, text="Confirm Delete", fg_color="red", command=self.execute_delete).pack(pady=10)

    def execute_delete(self):
        target = self.del_name.get()
        count_before = len(self.employees)
        
        updated = analytics.remove_employee_by_name(self.employees, target)
        count_after = len(updated)
        
        if count_after < count_before:
            self.employees = updated
            data_handler.save_data(self.employees)
            self.display_list = self.employees
            self.refresh_ui()
            self.set_status("Employee Deleted.")
            self.active_window.destroy()
        else:
            self.del_err.configure(text="Name not found.")

    def open_edit(self):
        is_open = self.check_active_window()
        if is_open == True:
            return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Edit Salary")
        self.active_window.geometry("300x250")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Exact Name:").pack(pady=(20, 5))
        self.edit_name = ctk.CTkEntry(self.active_window, width=200)
        self.edit_name.pack()

        ctk.CTkLabel(self.active_window, text="New Salary:").pack(pady=(10, 5))
        self.edit_sal = ctk.CTkEntry(self.active_window, width=200)
        self.edit_sal.pack()

        self.edit_err = ctk.CTkLabel(self.active_window, text="", text_color="red")
        self.edit_err.pack(pady=5)

        ctk.CTkButton(self.active_window, text="Update Salary", command=self.execute_edit).pack(pady=10)

    def execute_edit(self):
        target = self.edit_name.get()
        new_s = self.edit_sal.get()
        
        if new_s.isdigit() == False:
            self.edit_err.configure(text="Salary must be numbers.")
            return

        found = False
        for emp in self.employees:
            if emp['name'].lower() == target.lower():
                found = True

        if found == False:
            self.edit_err.configure(text="Name not found.")
            return

        self.employees = analytics.update_employee_salary(self.employees, target, new_s)
        data_handler.save_data(self.employees)
        self.display_list = self.employees
        self.refresh_ui()
        self.set_status("Salary Updated.")
        self.active_window.destroy()

    def open_simulate(self):
        is_open = self.check_active_window()
        if is_open == True:
            return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Raise Simulator")
        self.active_window.geometry("350x300")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Percentage Increase (e.g., 5):").pack(pady=(20, 5))
        self.sim_entry = ctk.CTkEntry(self.active_window, width=100)
        self.sim_entry.pack()

        self.sim_err = ctk.CTkLabel(self.active_window, text="", text_color="red")
        self.sim_err.pack(pady=5)

        ctk.CTkButton(self.active_window, text="Run Simulation", command=self.execute_simulate).pack(pady=10)

        self.sim_result_1 = ctk.CTkLabel(self.active_window, text="", font=("Helvetica", 14, "bold"))
        self.sim_result_1.pack(pady=5)
        self.sim_result_2 = ctk.CTkLabel(self.active_window, text="", font=("Helvetica", 14, "bold"))
        self.sim_result_2.pack(pady=5)

    def execute_simulate(self):
        val = self.sim_entry.get()
        is_valid = val.replace('.', '', 1).isdigit()
        
        if is_valid == False:
            self.sim_err.configure(text="Enter a valid number.")
            return
            
        percent_float = float(val)
        new_total, new_avg = analytics.simulate_raise(self.employees, percent_float)
        
        stats = analytics.calculate_global_stats(self.employees)
        old_total = stats["total"]
        diff = new_total - old_total

        self.sim_err.configure(text="")
        self.sim_result_1.configure(text=f"New Budget: ${new_total:,.0f} (+${diff:,.0f})")
        self.sim_result_2.configure(text=f"New Average: ${new_avg:,.0f}")

if __name__ == "__main__":
    app = HRApp()
    app.mainloop()
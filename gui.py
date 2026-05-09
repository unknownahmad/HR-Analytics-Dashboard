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
        
        # Data State
        self.employees = data_handler.load_data()
        self.display_list = self.employees
        self.active_window = None
        
        # Grid Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_content()
        self.refresh_ui()

    def _build_sidebar(self):
        """Constructs the navigation sidebar."""
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#1e1e21")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Branding
        self.logo = ctk.CTkLabel(self.sidebar, text="HR DATA PRO", font=("Helvetica", 22, "bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Core Navigation (Removed clunky numbers)
        btn_style = {"width": 220, "height": 40, "font": ("Helvetica", 14), "anchor": "w"}
        
        ctk.CTkButton(self.sidebar, text="  📊 View All Employees", command=self.view_all, **btn_style).grid(row=1, column=0, padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="  ➕ Add Employee", command=self.open_add, **btn_style).grid(row=2, column=0, padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="  📈 Detailed Stats", command=self.open_stats, **btn_style).grid(row=3, column=0, padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="  💾 Export Report", command=self.export_data, **btn_style).grid(row=4, column=0, padx=20, pady=5)

        # Filtering Section
        ctk.CTkLabel(self.sidebar, text="Data Filters", font=("Helvetica", 12, "bold"), text_color="gray").grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")
        self.filter_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Department Name", width=220, height=35)
        self.filter_entry.grid(row=6, column=0, padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="Apply Filter", command=self.apply_filter, width=220, fg_color="#4a4a4a", hover_color="#3a3a3a").grid(row=7, column=0, padx=20, pady=5)

        # Action Section
        ctk.CTkLabel(self.sidebar, text="Operations", font=("Helvetica", 12, "bold"), text_color="gray").grid(row=8, column=0, padx=20, pady=(20, 5), sticky="w")
        ctk.CTkButton(self.sidebar, text="  ✏️ Edit Salary", command=self.open_edit, **btn_style).grid(row=9, column=0, padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="  🚀 Simulate Raise", command=self.open_simulate, fg_color="#2b7a4b", hover_color="#1e5c36", **btn_style).grid(row=10, column=0, padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="  🗑️ Delete Employee", command=self.open_delete, fg_color="#8a2e2e", hover_color="#632121", **btn_style).grid(row=11, column=0, padx=20, pady=5)

        # Status Tracker
        self.status_label = ctk.CTkLabel(self.sidebar, text="System Ready", text_color="#5cc776", font=("Helvetica", 12))
        self.status_label.grid(row=12, column=0, padx=20, pady=(30, 10), sticky="s")

    def _build_main_content(self):
        """Constructs the data visualization area."""
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Top KPI Frame (Card Design)
        self.stats_frame = ctk.CTkFrame(self.main_container, height=100, fg_color="#242428", corner_radius=10)
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.avg_label = ctk.CTkLabel(self.stats_frame, text="Avg Salary\n$0", font=("Helvetica", 18, "bold"), justify="center")
        self.avg_label.pack(side="left", expand=True, pady=20)
        
        self.med_label = ctk.CTkLabel(self.stats_frame, text="Median Salary\n$0", font=("Helvetica", 18, "bold"), justify="center")
        self.med_label.pack(side="left", expand=True, pady=20)

        self.count_label = ctk.CTkLabel(self.stats_frame, text="Total Headcount\n0", font=("Helvetica", 18, "bold"), justify="center")
        self.count_label.pack(side="left", expand=True, pady=20)

        # Data Grid
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, label_text="Employee Database", label_font=("Helvetica", 16, "bold"), fg_color="#242428", corner_radius=10)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

    def set_status(self, message: str):
        self.status_label.configure(text=message)

    def view_all(self):
        self.display_list = self.employees
        self.refresh_ui()
        self.set_status("Viewing all records.")

    def apply_filter(self):
        target = self.filter_entry.get().strip()
        if not target:
            self.set_status("⚠️ Enter dept to filter.")
            return
            
        self.display_list = analytics.filter_by_dept(self.employees, target)
        self.refresh_ui()
        self.set_status(f"Filtered by: {target}")

    def export_data(self):
        analysis_data = analytics.get_department_analysis(self.employees)
        report_lines = ["HR SUMMARY REPORT", "=" * 20]
        
        for dept, data in analysis_data.items():
            report_lines.append(f"{dept}: {data['count']} staff | Avg: ${data['avg']:,.2f}")
            
        data_handler.export_report("\n".join(report_lines))
        self.set_status("✅ Report Exported.")

    def refresh_ui(self):
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        stats = analytics.calculate_global_stats(self.display_list)
        
        self.avg_label.configure(text=f"Avg Salary\n${stats['avg']:,.0f}")
        self.med_label.configure(text=f"Median Salary\n${stats['median']:,.0f}")
        self.count_label.configure(text=f"Total Headcount\n{stats['count']}")

        # Header Row
        header = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        header.pack(fill="x", pady=(5, 10), padx=10)
        ctk.CTkLabel(header, text="NAME", font=("Helvetica", 12, "bold"), width=250, anchor="w", text_color="gray").pack(side="left")
        ctk.CTkLabel(header, text="DEPARTMENT", font=("Helvetica", 12, "bold"), width=200, anchor="w", text_color="gray").pack(side="left")
        ctk.CTkLabel(header, text="SALARY", font=("Helvetica", 12, "bold"), width=150, anchor="e", text_color="gray").pack(side="right", padx=10)

        # Data Rows
        for emp in self.display_list:
            row = ctk.CTkFrame(self.scroll_frame, fg_color="#2f2f35", corner_radius=6)
            row.pack(fill="x", pady=2, padx=5)
            
            ctk.CTkLabel(row, text=emp['name'], width=250, anchor="w", font=("Helvetica", 14)).pack(side="left", padx=10, pady=8)
            ctk.CTkLabel(row, text=emp['department'], width=200, anchor="w", font=("Helvetica", 14)).pack(side="left", padx=10, pady=8)
            ctk.CTkLabel(row, text=f"${float(emp['salary']):,.0f}", width=150, anchor="e", font=("Helvetica", 14, "bold")).pack(side="right", padx=20, pady=8)

    def is_window_active(self) -> bool:
        if self.active_window and self.active_window.winfo_exists():
            self.active_window.focus()
            return True
        return False

    def open_add(self):
        if self.is_window_active(): return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Add Employee")
        self.active_window.geometry("400x450")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="New Employee Registration", font=("Helvetica", 18, "bold")).pack(pady=(20, 20))
        
        self.add_name = ctk.CTkEntry(self.active_window, placeholder_text="Full Name", width=250, height=40)
        self.add_name.pack(pady=10)

        self.add_dept = ctk.CTkEntry(self.active_window, placeholder_text="Department", width=250, height=40)
        self.add_dept.pack(pady=10)

        self.add_sal = ctk.CTkEntry(self.active_window, placeholder_text="Salary (Numbers only)", width=250, height=40)
        self.add_sal.pack(pady=10)

        self.add_err = ctk.CTkLabel(self.active_window, text="", text_color="#ff6b6b")
        self.add_err.pack(pady=5)

        ctk.CTkButton(self.active_window, text="Save Record", command=self.execute_add, width=250, height=40).pack(pady=10)

    def execute_add(self):
        n, d, s = self.add_name.get().strip(), self.add_dept.get().strip(), self.add_sal.get().strip()

        if not n or not d or not s:
            self.add_err.configure(text="⚠️ All fields are required.")
            return
            
        try:
            float(s)
        except ValueError:
            self.add_err.configure(text="⚠️ Salary must be a valid number.")
            return

        self.employees.append({"name": n, "department": d, "salary": s})
        data_handler.save_data(self.employees)
        self.display_list = self.employees
        self.refresh_ui()
        self.set_status("✅ Employee Added.")
        self.active_window.destroy()

    def open_stats(self):
        if self.is_window_active(): return

        stats = analytics.calculate_global_stats(self.employees)
        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Detailed Analytics")
        self.active_window.geometry("350x300")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Global Statistics", font=("Helvetica", 18, "bold")).pack(pady=20)
        
        frame = ctk.CTkFrame(self.active_window, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=40)
        
        ctk.CTkLabel(frame, text="Minimum Salary:").grid(row=0, column=0, sticky="w", pady=10)
        ctk.CTkLabel(frame, text=f"${stats['min']:,.0f}", font=("Helvetica", 14, "bold")).grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(frame, text="Maximum Salary:").grid(row=1, column=0, sticky="w", pady=10)
        ctk.CTkLabel(frame, text=f"${stats['max']:,.0f}", font=("Helvetica", 14, "bold")).grid(row=1, column=1, sticky="e")
        
        ctk.CTkLabel(frame, text="Total Payroll:").grid(row=2, column=0, sticky="w", pady=10)
        ctk.CTkLabel(frame, text=f"${stats['total']:,.0f}", font=("Helvetica", 14, "bold")).grid(row=2, column=1, sticky="e")

    def open_delete(self):
        if self.is_window_active(): return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Delete Record")
        self.active_window.geometry("350x250")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Remove Employee", font=("Helvetica", 18, "bold")).pack(pady=(20, 10))
        self.del_name = ctk.CTkEntry(self.active_window, placeholder_text="Exact Full Name", width=250, height=40)
        self.del_name.pack(pady=10)

        self.del_err = ctk.CTkLabel(self.active_window, text="", text_color="#ff6b6b")
        self.del_err.pack(pady=5)

        ctk.CTkButton(self.active_window, text="Confirm Deletion", fg_color="#8a2e2e", hover_color="#632121", width=250, height=40, command=self.execute_delete).pack(pady=10)

    def execute_delete(self):
        target = self.del_name.get().strip()
        updated = analytics.remove_employee_by_name(self.employees, target)
        
        if len(updated) < len(self.employees):
            self.employees = updated
            data_handler.save_data(self.employees)
            self.display_list = self.employees
            self.refresh_ui()
            self.set_status("✅ Employee Deleted.")
            self.active_window.destroy()
        else:
            self.del_err.configure(text="⚠️ Name not found in database.")

    def open_edit(self):
        if self.is_window_active(): return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Edit Salary")
        self.active_window.geometry("350x300")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Adjust Compensation", font=("Helvetica", 18, "bold")).pack(pady=(20, 10))
        self.edit_name = ctk.CTkEntry(self.active_window, placeholder_text="Exact Full Name", width=250, height=40)
        self.edit_name.pack(pady=10)

        self.edit_sal = ctk.CTkEntry(self.active_window, placeholder_text="New Salary", width=250, height=40)
        self.edit_sal.pack(pady=10)

        self.edit_err = ctk.CTkLabel(self.active_window, text="", text_color="#ff6b6b")
        self.edit_err.pack(pady=5)

        ctk.CTkButton(self.active_window, text="Update Record", width=250, height=40, command=self.execute_edit).pack(pady=10)

    def execute_edit(self):
        target, new_s = self.edit_name.get().strip(), self.edit_sal.get().strip()
        
        try:
            float(new_s)
        except ValueError:
            self.edit_err.configure(text="⚠️ Salary must be a valid number.")
            return

        if not any(emp['name'].lower() == target.lower() for emp in self.employees):
            self.edit_err.configure(text="⚠️ Name not found in database.")
            return

        self.employees = analytics.update_employee_salary(self.employees, target, new_s)
        data_handler.save_data(self.employees)
        self.display_list = self.employees
        self.refresh_ui()
        self.set_status("✅ Salary Updated.")
        self.active_window.destroy()

    def open_simulate(self):
        if self.is_window_active(): return

        self.active_window = ctk.CTkToplevel(self)
        self.active_window.title("Budget Simulator")
        self.active_window.geometry("400x350")
        self.active_window.attributes('-topmost', True)

        ctk.CTkLabel(self.active_window, text="Raise Projection Models", font=("Helvetica", 18, "bold")).pack(pady=(20, 10))
        self.sim_entry = ctk.CTkEntry(self.active_window, placeholder_text="Percentage Increase (e.g., 5)", width=250, height=40)
        self.sim_entry.pack(pady=10)

        self.sim_err = ctk.CTkLabel(self.active_window, text="", text_color="#ff6b6b")
        self.sim_err.pack()

        ctk.CTkButton(self.active_window, text="Run Simulation", width=250, height=40, fg_color="#2b7a4b", hover_color="#1e5c36", command=self.execute_simulate).pack(pady=10)

        self.sim_result_1 = ctk.CTkLabel(self.active_window, text="", font=("Helvetica", 16, "bold"))
        self.sim_result_1.pack(pady=(15, 5))
        self.sim_result_2 = ctk.CTkLabel(self.active_window, text="", font=("Helvetica", 16, "bold"), text_color="gray")
        self.sim_result_2.pack()

    def execute_simulate(self):
        try:
            percent_float = float(self.sim_entry.get().strip())
        except ValueError:
            self.sim_err.configure(text="⚠️ Enter a valid numerical percentage.")
            return
            
        new_total, new_avg = analytics.simulate_raise(self.employees, percent_float)
        old_total = analytics.calculate_global_stats(self.employees)["total"]
        diff = new_total - old_total

        self.sim_err.configure(text="")
        self.sim_result_1.configure(text=f"New Budget: ${new_total:,.0f} (+${diff:,.0f})")
        self.sim_result_2.configure(text=f"New Avg Salary: ${new_avg:,.0f}")

if __name__ == "__main__":
    app = HRApp()
    app.mainloop()
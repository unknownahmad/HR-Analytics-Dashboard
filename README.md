# HR Analytics Dashboard & Data Pipeline

A professional-grade "People Analytics" and employee management system. This project demonstrates foundational data science programming by implementing a fully decoupled architecture for data storage, mathematical aggregation, and user interfaces.

## 🏗️ Architecture

The system replaces a monolithic script with a modular pipeline:
* **`data_handler.py`**: Manages persistent file I/O operations with CSV formatting.
* **`analytics.py`**: The mathematical engine handling Pandas-style grouping, filtering, and predictive budget simulations.
* **`gui.py`**: A modern desktop dashboard built with `CustomTkinter` for real-time statistical tracking.
* **`main.py`**: A robust command-line interface utilizing `tabulate` for structured data visualization.

## 🛠️ Features

* **Complete CRUD Operations**: Create, read, update, and delete employee records with strict data validation.
* **Statistical Aggregation**: Automatically calculates global and department-specific statistics, including Minimum, Maximum, Average, and Median salaries.
* **Predictive Modeling**: Simulates company-wide percentage raises to project total budget impacts.
* **Automated Reporting**: Exports actionable text-based HR summaries.
* **Dual Interfaces**: Operate the pipeline through a lightweight terminal CLI or a dark-mode graphical desktop application.


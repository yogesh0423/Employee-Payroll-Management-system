import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Database Setup ----------
conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL
)
""")
conn.commit()

# ---------- Functions ----------
def add_employee():
    name = entry_name.get()
    department = entry_dept.get()
    position = entry_position.get()
    salary = entry_salary.get()

    if not (name and department and position and salary):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        salary = float(salary)
        cursor.execute("INSERT INTO employees (name, department, position, salary) VALUES (?, ?, ?, ?)",
                       (name, department, position, salary))
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully!")
        clear_fields()
        show_employees()
    except ValueError:
        messagebox.showerror("Error", "Salary must be a number!")

def show_employees():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM employees")
    for emp in cursor.fetchall():
        tree.insert("", tk.END, values=emp)

def delete_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Select Record", "Please select an employee to delete.")
        return
    emp_id = tree.item(selected_item)["values"][0]
    cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
    conn.commit()
    show_employees()
    messagebox.showinfo("Deleted", "Employee record deleted successfully!")

def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Select Record", "Please select an employee to update.")
        return
    emp_id = tree.item(selected_item)["values"][0]
    name = entry_name.get()
    department = entry_dept.get()
    position = entry_position.get()
    salary = entry_salary.get()

    if not (name and department and position and salary):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        salary = float(salary)
        cursor.execute("""
            UPDATE employees 
            SET name = ?, department = ?, position = ?, salary = ?
            WHERE emp_id = ?
        """, (name, department, position, salary, emp_id))
        conn.commit()
        show_employees()
        clear_fields()
        messagebox.showinfo("Success", "Employee updated successfully!")
    except ValueError:
        messagebox.showerror("Error", "Salary must be a number!")

def select_record(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, 'values')
    entry_name.delete(0, tk.END)
    entry_dept.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_salary.delete(0, tk.END)

    entry_name.insert(0, values[1])
    entry_dept.insert(0, values[2])
    entry_position.insert(0, values[3])
    entry_salary.insert(0, values[4])

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_dept.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_salary.delete(0, tk.END)

# ---------- UI Setup ----------
root = tk.Tk()
root.title("Employee Payroll Management System")
root.geometry("800x500")
root.configure(bg="#f2f2f2")

# Labels and Entries
tk.Label(root, text="Employee Payroll Management", font=("Arial", 18, "bold"), bg="#f2f2f2").pack(pady=10)

frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

tk.Label(frame, text="Name:", bg="#f2f2f2").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Department:", bg="#f2f2f2").grid(row=1, column=0, padx=5, pady=5)
entry_dept = tk.Entry(frame)
entry_dept.grid(row=1, column=1)

tk.Label(frame, text="Position:", bg="#f2f2f2").grid(row=2, column=0, padx=5, pady=5)
entry_position = tk.Entry(frame)
entry_position.grid(row=2, column=1)

tk.Label(frame, text="Salary:", bg="#f2f2f2").grid(row=3, column=0, padx=5, pady=5)
entry_salary = tk.Entry(frame)
entry_salary.grid(row=3, column=1)

# Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Employee", command=add_employee, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Employee", command=update_employee, width=15, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Employee", command=delete_employee, width=15, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear Fields", command=clear_fields, width=15, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)

# Table
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Dept", "Position", "Salary"), show="headings", height=8)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Dept", text="Department")
tree.heading("Position", text="Position")
tree.heading("Salary", text="Salary")

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Dept", width=150)
tree.column("Position", width=150)
tree.column("Salary", width=100)

tree.bind("<ButtonRelease-1>", select_record)
tree.pack()

show_employees()
root.mainloop()

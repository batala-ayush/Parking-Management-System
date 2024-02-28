import tkinter as tk
from tkinter import ttk

def on_tree_select(event):
    # Retrieve selected item from the tree
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')
    print("Selected Item:", values)

report_window = tk.Tk()
report_window.title("Parking Management System")
screen_width = report_window.winfo_screenwidth()
screen_height = report_window.winfo_screenheight()
report_window.geometry(f"{screen_width}x{screen_height}")
report_window.resizable(False, False)

label = tk.Label(report_window, text="Transaction Report", font=('calibri', 30, 'bold'))
label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

frame_for_slots = tk.Frame(report_window, width=800, height=600)
frame_for_slots.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a scrollable table using Treeview
table_columns = ("Vehicle Id", "College ID", "Name", "Vehicle Type", "Entry Time", "Exit Time", "Total Charge")
tree = ttk.Treeview(frame_for_slots, columns=table_columns, show="headings", height=20)

# Set column headings
for col in table_columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor=tk.CENTER, stretch=tk.NO)  # Disable column stretching

# Add sample data (replace this with your actual data)
sample_data = [
    ("1", "ABC123", "John Doe", "Car", "12:00 PM", "2:00 PM", "$5.00"),
    ("2", "XYZ789", "Jane Doe", "Motorcycle", "1:30 PM", "4:00 PM", "$8.00"),
    # Add more rows as needed
]

for data in sample_data:
    tree.insert("", "end", values=data)

# Add a scrollbar to the table
scrollbar = ttk.Scrollbar(frame_for_slots, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Bind the tree selection event to the on_tree_select function
tree.bind("<ButtonRelease-1>", on_tree_select)

# Set borders for table rows and columns
style = ttk.Style()
style.configure("Treeview.Heading", font=('calibri', 12, 'bold'))
style.configure("Treeview", rowheight=25, font=('calibri', 12))
style.map("Treeview", background=[('selected', '#d9d9d9')])  # Use the default background color

# Pack the table and scrollbar
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

report_window.mainloop()

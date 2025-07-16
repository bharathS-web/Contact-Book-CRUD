import tkinter as tk
from tkinter import ttk, messagebox
from db_config import get_connection


def fetch_contacts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_contact(name, phone, email, group):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email, group_name) VALUES (%s, %s, %s, %s)",
                       (name, phone, email, group))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def update_contact(id, name, phone, email, group):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET name=%s, phone=%s, email=%s, group_name=%s WHERE id=%s",
                   (name, phone, email, group, id))
    conn.commit()
    conn.close()

def delete_contact(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=%s", (id,))
    conn.commit()
    conn.close()

# ------------ GUI ------------

def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for contact in fetch_contacts():
        tree.insert("", "end", values=contact)

def add_contact():
    if name_var.get() and phone_var.get():
        success = insert_contact(name_var.get(), phone_var.get(), email_var.get(), group_var.get())
        if success:
            messagebox.showinfo("Success", "Contact added.")
            populate_table()
            clear_fields()
        else:
            messagebox.showerror("Error", "Failed to add contact. Phone number might be duplicate.")
    else:
        messagebox.showwarning("Required", "Name and Phone are required.")

def update_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a contact to update.")
        return
    contact_id = tree.item(selected[0])['values'][0]
    update_contact(contact_id, name_var.get(), phone_var.get(), email_var.get(), group_var.get())
    messagebox.showinfo("Updated", "Contact updated.")
    populate_table()
    clear_fields()

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Select a contact to delete.")
        return
    contact_id = tree.item(selected[0])['values'][0]
    delete_contact(contact_id)
    messagebox.showinfo("Deleted", "Contact deleted.")
    populate_table()
    clear_fields()

def on_row_select(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        name_var.set(values[1])
        phone_var.set(values[2])
        email_var.set(values[3])
        group_var.set(values[4])

def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    group_var.set("")
    tree.selection_remove(tree.selection())

# ------------ Window Setup ------------

root = tk.Tk()
root.title("Contact Book")
root.geometry("750x500")
root.configure(bg="#f7f7f7")

# Entry Fields
name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
group_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10, bg="#f7f7f7")
frame.pack()

tk.Label(frame, text="Name:", bg="#f7f7f7").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=name_var, width=30).grid(row=0, column=1)

tk.Label(frame, text="Phone:", bg="#f7f7f7").grid(row=1, column=0, sticky="w")
tk.Entry(frame, textvariable=phone_var, width=30).grid(row=1, column=1)

tk.Label(frame, text="Email:", bg="#f7f7f7").grid(row=2, column=0, sticky="w")
tk.Entry(frame, textvariable=email_var, width=30).grid(row=2, column=1)

tk.Label(frame, text="Group:", bg="#f7f7f7").grid(row=3, column=0, sticky="w")
tk.Entry(frame, textvariable=group_var, width=30).grid(row=3, column=1)

# Buttons
button_frame = tk.Frame(root, pady=10, bg="#f7f7f7")
button_frame.pack()

tk.Button(button_frame, text="Add Contact", command=add_contact, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Contact", command=update_selected, bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Contact", command=delete_selected, bg="#f44336", fg="white", width=15).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear Fields", command=clear_fields, bg="#9E9E9E", fg="white", width=15).grid(row=0, column=3, padx=5)

# Table
tree = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Email", "Group"), show="headings", height=10)
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.heading("Group", text="Group")

tree.column("ID", width=40, anchor="center")
tree.column("Name", width=150)
tree.column("Phone", width=120)
tree.column("Email", width=180)
tree.column("Group", width=100)

tree.bind("<<TreeviewSelect>>", on_row_select)
tree.pack(pady=10)

populate_table()
root.mainloop()

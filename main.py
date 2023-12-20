import tkinter as tk
from tkinter import messagebox
from tkinter import font
import sqlite3


class AuthorizationWindow:
    def __init__(self, master, app):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x300")
        self.app = app

        # Create a table for users if not exists
        self.app.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                role TEXT
            )
        ''')
        self.app.connection.commit()

        self.insert_sample_users()

        # Insert sample user account
        # self.app.cursor.execute('''
        #     INSERT OR IGNORE INTO users (username, password) VALUES
        #     ('admin', 'adminpass')
        # ''')
        # self.app.connection.commit()

        # Create login elements
        self.label_username = tk.Label(master, text="Username:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        self.label_username.pack(side=tk.TOP, pady=10)

        self.entry_username = tk.Entry(master, justify='center')
        self.entry_username.pack(side=tk.TOP, pady=5)

        self.label_password = tk.Label(master, text="Password:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        self.label_password.pack(side=tk.TOP, pady=5)

        self.entry_password = tk.Entry(master, show="*", justify='center')
        self.entry_password.pack(side=tk.TOP, pady=5)

        self.button_login = tk.Button(
            master, text="Login", command=self.login, bg='green', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        self.button_login.pack(side=tk.TOP, pady=10)

    def insert_sample_users(self):
        # Insert sample user accounts if not already present
        sample_users = [
            ('admin', 'adminpass', 'administrator'),
            ('moderator', 'modpass', 'moderator'),
            ('storekeeper', 'storepass', 'storekeeper'),
            ('logistician', 'logpass', 'logistician')
        ]
        self.app.cursor.executemany('''
            INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)
        ''', sample_users)
        self.app.connection.commit()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            query = "SELECT * FROM users WHERE username=? AND password=?"
            self.app.cursor.execute(query, (username, password))
            user = self.app.cursor.fetchone()

            if user:
                self.app.user_role = user[3]  # Set user role
                self.master.destroy()  # Close the login window
                self.app.show_main_window()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Error during login: {str(e)}")


class WarehouseApp:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        self.master.title("Warehouse App")

        # Create and connect to a SQLite database
        self.connection = sqlite3.connect("warehouse.db")
        self.cursor = self.connection.cursor()

        # Initialize user role
        self.user_role = None

        # Show the authorization window
        self.show_authorization_window()

    def show_authorization_window(self):
        authorization_window = tk.Toplevel(self.master)
        AuthorizationWindow(authorization_window, self)

    def show_main_window(self):
        self.master.deiconify()  # Show the main window

        # Create a table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                vendor_code TEXT,
                location TEXT,
                quantity INTEGER,
                weight REAL,
                shelf_life TEXT,
                shipper TEXT
            )
        ''')
        self.connection.commit()

        # Create GUI elements
        self.label_id = tk.Label(self.master, text="ID:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.entry_id = tk.Entry(self.master)
        # self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_name = tk.Label(self.master, text="Name:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_name = tk.Entry(self.master)
        # self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_vendor_code = tk.Label(self.master, text="Vendor Code:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_vendor_code.grid(
        # row=2, column=0, padx=5, pady=5, sticky="e")

        self.entry_vendor_code = tk.Entry(self.master)
        # self.entry_vendor_code.grid(row=2, column=1, padx=5, pady=5)

        self.label_location = tk.Label(self.master, text="Location:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_location.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.entry_location = tk.Entry(self.master)
        # self.entry_location.grid(row=3, column=1, padx=5, pady=5)

        self.label_quantity = tk.Label(self.master, text="Quantity:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_quantity.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.entry_quantity = tk.Entry(self.master)
        # self.entry_quantity.grid(row=4, column=1, padx=5, pady=5)

        self.label_weight = tk.Label(self.master, text="Weight:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_weight.grid(row=5, column=0, padx=5, pady=5, sticky="e")

        self.entry_weight = tk.Entry(self.master)
        # self.entry_weight.grid(row=5, column=1, padx=5, pady=5)

        self.label_shelf_life = tk.Label(self.master, text="Shelf Life:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_shelf_life.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        self.entry_shelf_life = tk.Entry(self.master)
        # self.entry_shelf_life.grid(row=6, column=1, padx=5, pady=5)

        self.label_shipper = tk.Label(self.master, text="Shipper:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_shipper.grid(row=7, column=0, padx=5, pady=5, sticky="e")

        self.entry_shipper = tk.Entry(self.master)
        # self.entry_shipper.grid(row=7, column=1, padx=5, pady=5)

        self.label_search_property = tk.Label(
            self.master, text="Search by:", font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.label_search_property.grid(
        # row=8, column=0, padx=5, pady=5, sticky="e")

        self.search_property_options = [
            "ID", "Name", "Vendor Code", "Location", "Quantity", "Weight", "Shelf Life", "Shipper"]
        self.selected_search_property = tk.StringVar(self.master)
        self.selected_search_property.set(self.search_property_options[0])

        self.dropdown_search_property = tk.OptionMenu(
            self.master, self.selected_search_property, *self.search_property_options)
        # self.dropdown_search_property.grid(row=8, column=1, padx=5, pady=5)
        self.dropdown_search_property.config(
            bg='green', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))

        self.label_search_term = tk.Label(self.master, text="Search Term:", font=font.Font(
            family='Verdana', size=9, weight='bold'))
        # self.label_search_term.grid(
        # row=9, column=0, padx=5, pady=5, sticky="e")

        self.entry_search_term = tk.Entry(self.master)
        # self.entry_search_term.grid(row=9, column=1, padx=5, pady=5)

        self.button_insert = tk.Button(
            self.master, text="Insert", command=self.insert_item, bg='blue', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.button_insert.grid(row=10, column=0, columnspan=2, pady=10)

        self.button_update = tk.Button(
            self.master, text="Update", command=self.update_item, bg='blue', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.button_update.grid(row=11, column=0, columnspan=2, pady=10)

        self.button_delete = tk.Button(
            self.master, text="Delete", command=self.delete_item, bg='red', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.button_delete.grid(row=12, column=0, columnspan=2, pady=10)

        self.button_search = tk.Button(
            self.master, text="Search", command=self.search_items, bg='green', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.button_search.grid(row=13, column=0, columnspan=2, pady=10)

        self.button_display = tk.Button(
            self.master, text="Display all", command=self.display_items, bg='green', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.button_display.grid(row=14, column=0, columnspan=2, pady=10)

        # Create a larger text widget to display items like a table
        self.text_area = tk.Text(self.master, height=20, width=80)
        # self.text_area.grid(row=15, column=0, columnspan=2, padx=5, pady=5)

        self.logout_button = tk.Button(
            self.master, text="Logout", command=self.logout, bg='red', fg='white', font=font.Font(family='Verdana', size=9, weight='bold'))
        # self.logout_button.grid(row=0, column=2, sticky="ne", pady=10)

        # Create GUI elements with improved layout
        self.label_id.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_id.grid(row=2, column=1, padx=5, pady=5)

        self.label_name.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_name.grid(row=3, column=1, padx=5, pady=5)

        self.label_vendor_code.grid(
            row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_vendor_code.grid(row=4, column=1, padx=5, pady=5)

        self.label_location.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.entry_location.grid(row=5, column=1, padx=5, pady=5)

        self.label_quantity.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantity.grid(row=6, column=1, padx=5, pady=5)

        self.label_weight.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.entry_weight.grid(row=7, column=1, padx=5, pady=5)

        self.label_shelf_life.grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.entry_shelf_life.grid(row=8, column=1, padx=5, pady=5)

        self.label_shipper.grid(row=9, column=0, padx=5, pady=5, sticky="e")
        self.entry_shipper.grid(row=9, column=1, padx=5, pady=5)

        # Search elements in a single row at the top
        self.label_search_property.grid(
            row=1, column=13, padx=5, pady=5)
        self.dropdown_search_property.grid(
            row=1, column=14, padx=5, pady=5)
        self.label_search_term.grid(
            row=1, column=15, padx=5, pady=5)
        self.entry_search_term.grid(
            row=1, column=16, padx=5, pady=5)

        # Buttons and text area closer to labels and entries
        self.button_insert.grid(row=4, column=2, padx=5, ipadx=5)
        self.button_update.grid(row=5, column=2, padx=5, ipadx=5)
        self.button_delete.grid(row=6, column=2, padx=5, ipadx=5)
        self.button_search.grid(row=1, column=17, padx=5,
                                pady=10, sticky='e', ipadx=5)
        self.button_display.grid(row=1, column=3, padx=5, pady=10, ipadx=5)

        self.text_area.grid(row=2, column=3, rowspan=7,
                            columnspan=15, padx=5, pady=5)

        # Logout button placed at the top right corner
        self.logout_button.grid(
            row=0, column=17, pady=10, ipadx=5)

    def logout(self):
        self.user_role = None
        self.master.destroy()

    def insert_item(self):
        if self.user_role == 'administrator':
            name = self.entry_name.get()
            vendor_code = self.entry_vendor_code.get()
            location = self.entry_location.get()
            quantity = self.entry_quantity.get()
            weight = self.entry_weight.get()
            shelf_life = self.entry_shelf_life.get()
            shipper = self.entry_shipper.get()

            if name and vendor_code and location and quantity and weight and shelf_life and shipper:
                try:
                    self.cursor.execute('''
                        INSERT INTO items (name, vendor_code, location, quantity, weight, shelf_life, shipper)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (name, vendor_code, location, quantity, weight, shelf_life, shipper))
                    self.connection.commit()
                    messagebox.showinfo(
                        "Success", "Item inserted successfully.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Error inserting item: {str(e)}")
            else:
                messagebox.showwarning("Warning", "All fields are required.")
        else:
            messagebox.showwarning(
                "Warning", "You do not have permission to add items.")

    def update_item(self):
        if self.user_role == 'administrator' or self.user_role == 'manager' or self.user_role == 'storekeeper':
            item_id = self.entry_id.get()
            name = self.entry_name.get()
            vendor_code = self.entry_vendor_code.get()
            location = self.entry_location.get()
            quantity = self.entry_quantity.get()
            weight = self.entry_weight.get()
            shelf_life = self.entry_shelf_life.get()
            shipper = self.entry_shipper.get()

            if item_id and location:
                try:
                    update_query = '''
                        UPDATE items
                        SET name = ?, vendor_code = ?, location = ?, quantity = ?,
                            weight = ?, shelf_life = ?, shipper = ?
                        WHERE id = ?
                    '''
                    self.cursor.execute(update_query, (name, vendor_code, location,
                                                       quantity, weight, shelf_life, shipper, item_id))
                    self.connection.commit()
                    messagebox.showinfo(
                        "Success", "Item updated successfully.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Error updating item: {str(e)}")
            else:
                messagebox.showwarning(
                    "Warning", "Item ID and location are required.")
        elif self.user_role == 'logistician':
            # Logisticians are only allowed to update the location
            item_id = self.entry_id.get()
            location = self.entry_location.get()

            if item_id and location:
                try:
                    update_query = "UPDATE items SET location = ? WHERE id = ?"
                    self.cursor.execute(update_query, (location, item_id))
                    self.connection.commit()
                    messagebox.showinfo(
                        "Success", "Item location updated successfully.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Error updating item location: {str(e)}")
            else:
                messagebox.showwarning(
                    "Warning", "You do not have permission to update items.")
        else:
            messagebox.showwarning(
                "Warning", "Not authorized")

    def delete_item(self):
        if self.user_role == 'administrator' or self.user_role == 'manager' or self.user_role == 'storekeeper':
            item_id = self.entry_id.get()

            if item_id:
                try:
                    self.cursor.execute(
                        "DELETE FROM items WHERE id = ?", (item_id,))
                    self.connection.commit()
                    messagebox.showinfo(
                        "Success", "Item deleted successfully.")
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Error deleting item: {str(e)}")
            else:
                messagebox.showwarning("Warning", "Item ID is required.")
        elif self.user_role == 'logistician':
            messagebox.showwarning(
                "Warning", "Logisticians are not allowed to delete items.")
        else:
            messagebox.showwarning(
                "Warning", "Unauthorized")

    def search_items(self):
        search_property = self.selected_search_property.get()
        search_term = self.entry_search_term.get()

        if search_property and search_term:
            try:
                query = f"SELECT * FROM items WHERE {
                    search_property.lower()} LIKE ?"
                self.cursor.execute(query, ('%' + search_term + '%',))
                items = self.cursor.fetchall()

                if items:
                    # Clear previous content in the text area
                    self.text_area.delete(1.0, tk.END)

                    # Display items in the text area like a table
                    header = "ID\tName\tVendor Code\tLocation\tQuantity\tWeight\tShelf Life\tShipper\n"
                    self.text_area.insert(tk.END, header)

                    for item in items:
                        row_str = f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{
                            item[4]}\t{item[5]}\t{item[6]}\t{item[7]}\n"
                        self.text_area.insert(tk.END, row_str)
                else:
                    messagebox.showinfo("Items", "No items found.")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error searching items: {str(e)}")
        else:
            messagebox.showwarning(
                "Warning", "Search property and search term are required.")

    def display_items(self):
        self.cursor.execute("SELECT * FROM items")
        items = self.cursor.fetchall()

        if items:
            # Clear previous content in the text area
            self.text_area.delete(1.0, tk.END)

            # Display items in the text area like a table
            header = "ID\tName\tVendor Code\tLocation\tQuantity\tWeight\tShelf Life\tShipper\n"
            self.text_area.insert(tk.END, header)

            for item in items:
                row_str = f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{
                    item[4]}\t{item[5]}\t{item[6]}\t{item[7]}\n"
                self.text_area.insert(tk.END, row_str)
        else:
            messagebox.showinfo("Items", "No items found.")


if __name__ == "__main__":
    while True:
        root = tk.Tk()
        app = WarehouseApp(root)
        root.mainloop()

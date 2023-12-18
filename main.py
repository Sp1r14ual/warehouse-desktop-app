import tkinter as tk
from tkinter import messagebox
import sqlite3


class WarehouseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Warehouse App")

        # Create and connect to a SQLite database
        self.connection = sqlite3.connect("warehouse.db")
        self.cursor = self.connection.cursor()

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
        self.label_id = tk.Label(master, text="ID:")
        self.label_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.entry_id = tk.Entry(master)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_name = tk.Label(master, text="Name:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_vendor_code = tk.Label(master, text="Vendor Code:")
        self.label_vendor_code.grid(
            row=2, column=0, padx=5, pady=5, sticky="e")

        self.entry_vendor_code = tk.Entry(master)
        self.entry_vendor_code.grid(row=2, column=1, padx=5, pady=5)

        self.label_location = tk.Label(master, text="Location:")
        self.label_location.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.entry_location = tk.Entry(master)
        self.entry_location.grid(row=3, column=1, padx=5, pady=5)

        self.label_quantity = tk.Label(master, text="Quantity:")
        self.label_quantity.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.entry_quantity = tk.Entry(master)
        self.entry_quantity.grid(row=4, column=1, padx=5, pady=5)

        self.label_weight = tk.Label(master, text="Weight:")
        self.label_weight.grid(row=5, column=0, padx=5, pady=5, sticky="e")

        self.entry_weight = tk.Entry(master)
        self.entry_weight.grid(row=5, column=1, padx=5, pady=5)

        self.label_shelf_life = tk.Label(master, text="Shelf Life:")
        self.label_shelf_life.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        self.entry_shelf_life = tk.Entry(master)
        self.entry_shelf_life.grid(row=6, column=1, padx=5, pady=5)

        self.label_shipper = tk.Label(master, text="Shipper:")
        self.label_shipper.grid(row=7, column=0, padx=5, pady=5, sticky="e")

        self.entry_shipper = tk.Entry(master)
        self.entry_shipper.grid(row=7, column=1, padx=5, pady=5)

        self.label_search_property = tk.Label(
            master, text="Search by Property:")
        self.label_search_property.grid(
            row=8, column=0, padx=5, pady=5, sticky="e")

        self.search_property_options = [
            "ID", "Name", "Vendor Code", "Location", "Quantity", "Weight", "Shelf Life", "Shipper"]
        self.selected_search_property = tk.StringVar(master)
        self.selected_search_property.set(self.search_property_options[0])

        self.dropdown_search_property = tk.OptionMenu(
            master, self.selected_search_property, *self.search_property_options)
        self.dropdown_search_property.grid(row=8, column=1, padx=5, pady=5)

        self.label_search_term = tk.Label(master, text="Search Term:")
        self.label_search_term.grid(
            row=9, column=0, padx=5, pady=5, sticky="e")

        self.entry_search_term = tk.Entry(master)
        self.entry_search_term.grid(row=9, column=1, padx=5, pady=5)

        self.button_insert = tk.Button(
            master, text="Insert Item", command=self.insert_item)
        self.button_insert.grid(row=10, column=0, columnspan=2, pady=10)

        self.button_update = tk.Button(
            master, text="Update Item", command=self.update_item)
        self.button_update.grid(row=11, column=0, columnspan=2, pady=10)

        self.button_delete = tk.Button(
            master, text="Delete Item", command=self.delete_item)
        self.button_delete.grid(row=12, column=0, columnspan=2, pady=10)

        self.button_search = tk.Button(
            master, text="Search Items", command=self.search_items)
        self.button_search.grid(row=13, column=0, columnspan=2, pady=10)

        self.button_display = tk.Button(
            master, text="Display Items", command=self.display_items)
        self.button_display.grid(row=14, column=0, columnspan=2, pady=10)

        # Create a larger text widget to display items like a table
        self.text_area = tk.Text(master, height=20, width=80)
        self.text_area.grid(row=15, column=0, columnspan=2, padx=5, pady=5)

    def insert_item(self):
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
                messagebox.showinfo("Success", "Item inserted successfully.")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error inserting item: {str(e)}")
        else:
            messagebox.showwarning("Warning", "All fields are required.")

    def update_item(self):
        item_id = self.entry_id.get()
        name = self.entry_name.get()
        vendor_code = self.entry_vendor_code.get()
        location = self.entry_location.get()
        quantity = self.entry_quantity.get()
        weight = self.entry_weight.get()
        shelf_life = self.entry_shelf_life.get()
        shipper = self.entry_shipper.get()

        if item_id and (name or vendor_code or location or quantity or weight or shelf_life or shipper):
            try:
                update_query = "UPDATE items SET "
                update_values = []

                if name:
                    update_query += "name = ?, "
                    update_values.append(name)

                if vendor_code:
                    update_query += "vendor_code = ?, "
                    update_values.append(vendor_code)

                if location:
                    update_query += "location = ?, "
                    update_values.append(location)

                if quantity:
                    update_query += "quantity = ?, "
                    update_values.append(quantity)

                if weight:
                    update_query += "weight = ?, "
                    update_values.append(weight)

                if shelf_life:
                    update_query += "shelf_life = ?, "
                    update_values.append(shelf_life)

                if shipper:
                    update_query += "shipper = ?, "
                    update_values.append(shipper)

                update_query = update_query.rstrip(", ") + " WHERE id = ?"
                update_values.append(item_id)

                self.cursor.execute(update_query, tuple(update_values))
                self.connection.commit()
                messagebox.showinfo("Success", "Item updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating item: {str(e)}")
        else:
            messagebox.showwarning(
                "Warning", "Item ID and at least one field to update are required.")

    def delete_item(self):
        item_id = self.entry_id.get()

        if item_id:
            try:
                self.cursor.execute(
                    "DELETE FROM items WHERE id = ?", (item_id,))
                self.connection.commit()
                messagebox.showinfo("Success", "Item deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting item: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Item ID is required.")

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
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()

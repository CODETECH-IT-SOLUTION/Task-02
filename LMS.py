import tkinter as tk
from tkinter import messagebox
import datetime

class LibraryItem:
    def __init__(self, title, author, category):
        self.title = title
        self.author = author
        self.category = category
        self.is_checked_out = False
        self.due_date = None

class Library:
    def __init__(self):
        self.items = []
        self.checked_out_items = {}

    def add_item(self, item):
        self.items.append(item)

    def check_out_item(self, item, borrower, days=14):
        if item.is_checked_out:
            return False
        item.is_checked_out = True
        item.due_date = datetime.datetime.now() + datetime.timedelta(days=days)
        self.checked_out_items[borrower] = item
        return True

    def return_item(self, borrower):
        item = self.checked_out_items.pop(borrower, None)
        if item:
            item.is_checked_out = False
            item.due_date = None
            return True
        return False

    def calculate_fine(self, item):
        if item.is_checked_out and datetime.datetime.now() > item.due_date:
            overdue_days = (datetime.datetime.now() - item.due_date).days
            return overdue_days * 1  # Assuming $1 fine per day
        return 0

    def search_items(self, keyword):
        return [item for item in self.items if keyword.lower() in item.title.lower() or
                keyword.lower() in item.author.lower() or
                keyword.lower() in item.category.lower()]

library = Library()

def add_item_window():
    def add_item():
        title = title_entry.get()
        author = author_entry.get()
        category = category_entry.get()
        item = LibraryItem(title, author, category)
        library.add_item(item)
        messagebox.showinfo("Success", "Item added successfully")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Item")

    tk.Label(add_window, text="Title:").grid(row=0, column=0)
    title_entry = tk.Entry(add_window)
    title_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Author:").grid(row=1, column=0)
    author_entry = tk.Entry(add_window)
    author_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Category:").grid(row=2, column=0)
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=2, column=1)

    tk.Button(add_window, text="Add Item", command=add_item).grid(row=3, columnspan=2)

def check_out_item_window():
    def check_out_item():
        title = title_entry.get()
        borrower = borrower_entry.get()
        items = library.search_items(title)
        if items:
            item = items[0]  # Assuming the first match
            if library.check_out_item(item, borrower):
                messagebox.showinfo("Success", "Item checked out successfully")
            else:
                messagebox.showerror("Error", "Item is already checked out")
        else:
            messagebox.showerror("Error", "Item not found")
        check_out_window.destroy()

    check_out_window = tk.Toplevel(root)
    check_out_window.title("Check Out Item")

    tk.Label(check_out_window, text="Title:").grid(row=0, column=0)
    title_entry = tk.Entry(check_out_window)
    title_entry.grid(row=0, column=1)

    tk.Label(check_out_window, text="Borrower:").grid(row=1, column=0)
    borrower_entry = tk.Entry(check_out_window)
    borrower_entry.grid(row=1, column=1)

    tk.Button(check_out_window, text="Check Out Item", command=check_out_item).grid(row=2, columnspan=2)

def return_item_window():
    def return_item():
        borrower = borrower_entry.get()
        if library.return_item(borrower):
            messagebox.showinfo("Success", "Item returned successfully")
        else:
            messagebox.showerror("Error", "Item not found or already returned")
        return_window.destroy()

    return_window = tk.Toplevel(root)
    return_window.title("Return Item")

    tk.Label(return_window, text="Borrower:").grid(row=0, column=0)
    borrower_entry = tk.Entry(return_window)
    borrower_entry.grid(row=0, column=1)

    tk.Button(return_window, text="Return Item", command=return_item).grid(row=1, columnspan=2)

def search_items_window():
    def search_items():
        keyword = keyword_entry.get()
        results = library.search_items(keyword)
        result_text.delete(1.0, tk.END)
        for item in results:
            result_text.insert(tk.END, f"Title: {item.title}, Author: {item.author}, Category: {item.category}\n")
    search_window = tk.Toplevel(root)
    search_window.title("Search Items")

    tk.Label(search_window, text="Keyword:").grid(row=0, column=0)
    keyword_entry = tk.Entry(search_window)
    keyword_entry.grid(row=0, column=1)

    tk.Button(search_window, text="Search", command=search_items).grid(row=1, columnspan=2)

    result_text = tk.Text(search_window, height=10, width=50)
    result_text.grid(row=2, columnspan=2)

root = tk.Tk()
root.title("Library Management System")

tk.Button(root, text="Add Item", command=add_item_window).pack()
tk.Button(root, text="Check Out Item", command=check_out_item_window).pack()
tk.Button(root, text="Return Item", command=return_item_window).pack()
tk.Button(root, text="Search Items", command=search_items_window).pack()

root.mainloop()

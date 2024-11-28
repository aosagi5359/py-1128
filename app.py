import tkinter
from tkinter import ttk
from tkinter import messagebox
import database

class CoffeeBeanApp:
    def __init__(self, root):
        self.connection = database.connect()
        database.create_tables(self.connection)
        
        self.root = root
        self.root.title("Coffee Bean App")
        
        # Frame for Menu Options
        self.frame = tkinter.Frame(root)
        self.frame.pack(padx=20, pady=20)
        
        self.create_menu()

    def create_menu(self):
        # Menu Frame
        menu_frame = tkinter.LabelFrame(self.frame, text="Select an Option")
        menu_frame.pack(padx=10, pady=10)

        # Buttons for different actions
        button1 = tkinter.Button(menu_frame, text="Add a new bean", command=self.prompt_add_new_bean)
        button1.grid(row=0, column=0, padx=10, pady=5)

        button2 = tkinter.Button(menu_frame, text="See all beans", command=self.prompt_see_all_beans)
        button2.grid(row=1, column=0, padx=10, pady=5)

        button3 = tkinter.Button(menu_frame, text="Find a bean by name", command=self.prompt_find_bean)
        button3.grid(row=2, column=0, padx=10, pady=5)

        button4 = tkinter.Button(menu_frame, text="Best preparation method", command=self.prompt_find_best_method)
        button4.grid(row=3, column=0, padx=10, pady=5)

        button5 = tkinter.Button(menu_frame, text="Exit", command=self.root.quit)
        button5.grid(row=4, column=0, padx=10, pady=5)

    def prompt_add_new_bean(self):
        # Add Bean Popup
        add_bean_window = tkinter.Toplevel(self.root)
        add_bean_window.title("Add a New Bean")

        # Input fields
        name_label = tkinter.Label(add_bean_window, text="Enter bean name: ")
        name_label.pack(padx=10, pady=5)
        name_entry = tkinter.Entry(add_bean_window)
        name_entry.pack(padx=10, pady=5)

        method_label = tkinter.Label(add_bean_window, text="Enter preparation method: ")
        method_label.pack(padx=10, pady=5)
        method_entry = tkinter.Entry(add_bean_window)
        method_entry.pack(padx=10, pady=5)

        rating_label = tkinter.Label(add_bean_window, text="Enter rating (0-100): ")
        rating_label.pack(padx=10, pady=5)
        rating_entry = tkinter.Entry(add_bean_window)
        rating_entry.pack(padx=10, pady=5)

        def save_bean():
            name = name_entry.get()
            method = method_entry.get()
            try:
                rating = int(rating_entry.get())
                if 0 <= rating <= 100:
                    database.add_bean(self.connection, name, method, rating)
                    messagebox.showinfo("Success", f"Bean '{name}' added successfully!")
                    add_bean_window.destroy()
                else:
                    messagebox.showerror("Error", "Rating must be between 0 and 100.")
            except ValueError:
                messagebox.showerror("Error", "Rating must be a number between 0 and 100.")
        
        save_button = tkinter.Button(add_bean_window, text="Save Bean", command=save_bean)
        save_button.pack(padx=10, pady=5)

    def prompt_see_all_beans(self):
        # Display all beans
        all_beans_window = tkinter.Toplevel(self.root)
        all_beans_window.title("All Beans")

        beans = database.get_all_beans(self.connection)
        for bean in beans:
            label = tkinter.Label(all_beans_window, text=f"{bean[1]} ({bean[2]}) - {bean[3]}/100")
            label.pack(padx=10, pady=5)

    def prompt_find_bean(self):
        # Search for a bean by name
        find_bean_window = tkinter.Toplevel(self.root)
        find_bean_window.title("Find a Bean by Name")

        name_label = tkinter.Label(find_bean_window, text="Enter bean name to find: ")
        name_label.pack(padx=10, pady=5)
        name_entry = tkinter.Entry(find_bean_window)
        name_entry.pack(padx=10, pady=5)

        def search_bean():
            name = name_entry.get()
            beans = database.get_beans_by_name(self.connection, name)
            result_window = tkinter.Toplevel(self.root)
            result_window.title("Search Results")

            if beans:
                for bean in beans:
                    label = tkinter.Label(result_window, text=f"{bean[1]} ({bean[2]}) - {bean[3]}/100")
                    label.pack(padx=10, pady=5)
            else:
                messagebox.showinfo("No Results", f"No beans found with name '{name}'.")

        search_button = tkinter.Button(find_bean_window, text="Search", command=search_bean)
        search_button.pack(padx=10, pady=5)

    def prompt_find_best_method(self):
        # Find the best preparation method for a specific bean
        find_method_window = tkinter.Toplevel(self.root)
        find_method_window.title("Best Preparation Method")

        name_label = tkinter.Label(find_method_window, text="Enter bean name to find: ")
        name_label.pack(padx=10, pady=5)
        name_entry = tkinter.Entry(find_method_window)
        name_entry.pack(padx=10, pady=5)

        def search_best_method():
            name = name_entry.get()
            best_method = database.get_best_preparation_for_bean(self.connection, name)
            if best_method:
                messagebox.showinfo("Best Preparation Method", f"The best preparation method for {name} is {best_method[0][2]}.")
            else:
                messagebox.showinfo("No Results", f"No preparation methods found for bean '{name}'.")

        search_button = tkinter.Button(find_method_window, text="Search", command=search_best_method)
        search_button.pack(padx=10, pady=5)

# Create the main window
root = tkinter.Tk()
app = CoffeeBeanApp(root)
root.mainloop()

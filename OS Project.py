import os
import platform
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, PhotoImage
import psutil  # For system details like CPU and memory usage.

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Management System")
        self.root.geometry("1000x600")
        self.root.config(bg="#f0f4fa")  # Light background for the app
        self.create_widgets()
        self.show_system_info()

    def create_widgets(self):
        # Header for the application
        header_label = tk.Label(self.root, text="File Management System", font=("Arial", 18, "bold"), 
                                bg="#2a75db", fg="white", pady=10)
        header_label.pack(fill=tk.X)

        # Frame for OS Information Display
        os_info_frame = tk.Frame(self.root, bg="#f0f4fa")
        os_info_frame.pack(pady=5)
        self.os_info_label = tk.Label(os_info_frame, text="", font=("Arial", 10), bg="#f0f4fa", fg="#333333")
        self.os_info_label.pack()

        # Frame for File Operations with icons and labels
        file_frame = tk.Frame(self.root, bg="#f0f4fa")
        file_frame.pack(pady=10)

        # Load and resize images
        self.icons = {
            "create": PhotoImage(file="create.png").subsample(3, 3),
            "delete": PhotoImage(file="delete.png").subsample(3, 3),
            "rename": PhotoImage(file="rename.png").subsample(3, 3),
            "list": PhotoImage(file="list.png").subsample(3, 3),
            "read": PhotoImage(file="read.png").subsample(3, 3),
            "write": PhotoImage(file="write.png").subsample(3, 3),
        }

        # Define a common style for the buttons
        button_bg = "#e1ecf4"
        button_fg = "#333333"

        # Button setup with icons and labels
        self.create_button = tk.Button(file_frame, image=self.icons["create"], command=self.create_file,
                                       bg=button_bg, activebackground="#d0e6f0", borderwidth=0)
        self.create_button.grid(row=0, column=0, padx=10)
        tk.Label(file_frame, text="Create", bg="#f0f4fa", fg=button_fg).grid(row=1, column=0)

        self.delete_button = tk.Button(file_frame, image=self.icons["delete"], command=self.delete_file,
                                       bg=button_bg, activebackground="#d0e6f0", borderwidth=0)
        self.delete_button.grid(row=0, column=1, padx=10)
        tk.Label(file_frame, text="Delete", bg="#f0f4fa", fg=button_fg).grid(row=1, column=1)

        self.rename_button = tk.Button(file_frame, image=self.icons["rename"], command=self.rename_file,
                                       bg=button_bg, activebackground="#d0e6f0", borderwidth=0)
        self.rename_button.grid(row=0, column=2, padx=10)
        tk.Label(file_frame, text="Rename", bg="#f0f4fa", fg=button_fg).grid(row=1, column=2)

        self.list_button = tk.Button(file_frame, image=self.icons["list"], command=self.list_files,
                                     bg=button_bg, activebackground="#d0e6f0", borderwidth=0)
        self.list_button.grid(row=0, column=3, padx=10)
        tk.Label(file_frame, text="List", bg="#f0f4fa", fg=button_fg).grid(row=1, column=3)

        self.read_button = tk.Button(file_frame, image=self.icons["read"], command=self.read_file,
                                     bg=button_bg, activebackground="#d0e6f0", borderwidth=0)
        self.read_button.grid(row=0, column=4, padx=10)
        tk.Label(file_frame, text="Read", bg="#f0f4fa", fg=button_fg).grid(row=1, column=4)

        self.write_button = tk.Button(file_frame, image=self.icons["write"], command=self.write_file,
                                      bg=button_bg, activebackground="#d0e6f0", borderwidth=0)
        self.write_button.grid(row=0, column=5, padx=10)
        tk.Label(file_frame, text="Write", bg="#f0f4fa", fg=button_fg).grid(row=1, column=5)

        # ScrolledText for displaying messages and file contents
        self.text_area = scrolledtext.ScrolledText(self.root, width=95, height=25, bg="#ffffff", fg="#333333", wrap=tk.WORD)
        self.text_area.pack(pady=10)

    def show_system_info(self):
        # Display basic system information
        system_info = f"OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})\n"
        system_info += f"Processor: {platform.processor()}\n"
        system_info += f"User: {os.getlogin()}\n"
        system_info += f"Disk Usage: {shutil.disk_usage('/').free // (1024 ** 3)} GB free of {shutil.disk_usage('/').total // (1024 ** 3)} GB\n"
        system_info += f"CPU Usage: {psutil.cpu_percent()}% | Memory Usage: {psutil.virtual_memory().percent}%"
        self.os_info_label.config(text=system_info)

    def create_file(self):
        # Check the current working directory
        print("Current Working Directory:", os.getcwd())
        
        filename = filedialog.asksaveasfilename(title="Select file to create", defaultextension=".txt",
                                                filetypes=[("Text files", ".txt"), ("All files", ".*")],
                                                initialdir="/home/farhan/OS")  # Change to your desired directory
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write("")  # Create an empty file
                self.text_area.insert(tk.END, f"File '{filename}' created successfully.\n")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating file: {e}\n{e}")

    def delete_file(self):
        filename = filedialog.askopenfilename(title="Select file to delete", filetypes=[("All files", ".*")])
        if filename:
            try:
                os.remove(filename)
                self.text_area.insert(tk.END, f"File '{filename}' deleted successfully.\n")
            except FileNotFoundError:
                messagebox.showerror("Error", f"Error: File '{filename}' not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting file: {e}")

    def rename_file(self):
        old_name = filedialog.askopenfilename(title="Select file to rename", filetypes=[("All files", ".*")])
        if old_name:
            new_name = filedialog.asksaveasfilename(title="Select new name for file", defaultextension=".txt",
                                                    filetypes=[("Text files", ".txt"), ("All files", ".*")])
            if new_name:
                try:
                    os.rename(old_name, new_name)
                    self.text_area.insert(tk.END, f"File '{old_name}' renamed to '{new_name}' successfully.\n")
                except Exception as e:
                    messagebox.showerror("Error", f"Error renaming file: {e}")

    def list_files(self):
        files = os.listdir(os.getcwd())
        self.text_area.insert(tk.END, "Files in current directory:\n")
        for file in files:
            self.text_area.insert(tk.END, f" - {file}\n")

    def read_file(self):
        filename = filedialog.askopenfilename(title="Select file to read", filetypes=[("All files", ".*")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                self.text_area.insert(tk.END, f"Content of '{filename}':\n{content}\n")
            except FileNotFoundError:
                messagebox.showerror("Error", f"Error: File '{filename}' not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {e}")

    def write_file(self):
        filename = filedialog.askopenfilename(title="Select file to write to", filetypes=[("All files", ".*")])
        if filename:
            self.show_write_window(filename)

    def show_write_window(self, filename):
        # New window for writing content with a resizable text area
        write_window = tk.Toplevel(self.root)
        write_window.title("Write Content")
        write_window.geometry("600x400")
        
        # Text box that can be resized
        write_text = scrolledtext.ScrolledText(write_window, width=70, height=20, wrap=tk.WORD)
        write_text.pack(expand=True, fill=tk.BOTH)

        def save_content():
            content = write_text.get("1.0", tk.END)
            try:
                with open(filename, 'a') as file:
                    file.write(content)
                messagebox.showinfo("Success", f"Content written to '{filename}' successfully.")
                write_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error writing to file: {e}")

        save_button = tk.Button(write_window, text="Save", command=save_content)
        save_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

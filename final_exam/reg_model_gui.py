import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from reg_models import *

class RegressionModelsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Regression Models GUI")

        self.left_frame = tk.Frame(master)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = tk.Label(self.left_frame, text="Select CSV File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_entry = tk.Entry(self.left_frame, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self.left_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.load_button = tk.Button(self.left_frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=1, column=1, padx=10, pady=10)

        self.x_label = tk.Label(self.left_frame, text="Select X Variable(s):")
        self.x_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.x_listbox = tk.Listbox(self.left_frame, selectmode="multiple", width=40)
        self.x_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.y_label = tk.Label(self.left_frame, text="Select Y Variable:")
        self.y_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.y_var = tk.StringVar()
        self.y_dropdown = tk.OptionMenu(self.left_frame, self.y_var, "")
        self.y_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.model_label = tk.Label(self.left_frame, text="Select Model:")
        self.model_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.model_var = tk.StringVar()
        self.model_var.set("Linear Regression")
        self.model_dropdown = tk.OptionMenu(self.left_frame, self.model_var, "Linear Regression", "Logistic Regression", "KNN Regression")
        self.model_dropdown.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.accuracy_button = tk.Button(self.left_frame, text="Calculate", command=self.calculate_accuracy)
        self.accuracy_button.grid(row=5, column=0, padx=10, pady=10)

        self.plot_button = tk.Button(self.left_frame, text="Plot Data", command=self.plot_data)
        self.plot_button.grid(row=5, column=1, padx=10, pady=10)

        self.df = None

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

    def load_data(self):
        file_path = self.file_path_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a CSV file.")
            return

        try:
            self.df = pd.read_csv(file_path)
            self.x_listbox.delete(0, tk.END)
            for column in self.df.columns:
                self.x_listbox.insert(tk.END, column)
            self.y_dropdown['menu'].delete(0, 'end')  # Clear previous items
            for column in self.df.columns:
                self.y_dropdown['menu'].add_command(label=column, command=tk._setit(self.y_var, column))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def calculate_accuracy(self):
        if self.df is None:
            messagebox.showerror("Error", "Please load data first.")
            return

        x_indices = self.x_listbox.curselection()

        if not x_indices:
            messagebox.showwarning("Warning", "Please select X variable(s).")
            return

        x_columns = [self.x_listbox.get(i) for i in x_indices]
        y_column = self.y_var.get()

        x = x_select(self.df, columns=x_columns)
        y = y_select(self.df, columns=(y_column,))

        model = self.model_var.get()
        if model == "Linear Regression":
            score = lr_score(x, y)
        elif model == "Logistic Regression":
            score = logr_score(x, y)
        elif model == "KNN Regression":
            score = knnr_score(x, y)

        messagebox.showinfo("Accuracy", f"The r2 of {model} is: {score}")

    def plot_data(self):
        if self.df is None:
            messagebox.showerror("Error", "Please load data first.")
            return

        x_indices = self.x_listbox.curselection()

        if not x_indices:
            messagebox.showwarning("Warning", "Please select X variable(s).")
            return

        x_columns = [self.x_listbox.get(i) for i in x_indices]
        y_column = self.y_var.get()

        x = x_select(self.df, columns=x_columns)
        y = y_select(self.df, columns=(y_column,))

        model = self.model_var.get()
        if model == "Linear Regression":
            lr_plot(self.df, x, y)
        elif model == "Logistic Regression":
            logr_plot(self.df, x, y)
        elif model == "KNN Regression":
            knnr_plot(x, y)
            
def main():
    root = tk.Tk()
    app = RegressionModelsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

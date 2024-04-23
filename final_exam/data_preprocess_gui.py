import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from data_preprocess import auto_clean, category_convert, remove_columns, float_convert, int_convert

class DataPreprocessApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Preprocessing GUI")

        self.left_frame = tk.Frame(master)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.right_frame = tk.Frame(master)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        self.file_label = tk.Label(self.left_frame, text="Select CSV File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_entry = tk.Entry(self.left_frame, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_button = tk.Button(self.left_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.load_button = tk.Button(self.left_frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=1, column=1, padx=10, pady=10)

        self.variables_label = tk.Label(self.left_frame, text="Variables:")
        self.variables_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.variables_listbox = tk.Listbox(self.left_frame, selectmode="multiple", width=40)
        self.variables_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.dtype_listbox = tk.Listbox(self.left_frame, width=15)
        self.dtype_listbox.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.int_button = tk.Button(self.left_frame, text="Convert to Integer", command=self.convert_to_int)
        self.int_button.grid(row=3, column=0, padx=10, pady=10)

        self.float_button = tk.Button(self.left_frame, text="Convert to Float", command=self.convert_to_float)
        self.float_button.grid(row=3, column=1, padx=10, pady=10)

        self.remove_button = tk.Button(self.left_frame, text="Remove Variable", command=self.remove_variable)
        self.remove_button.grid(row=3, column=2, padx=10, pady=10)

        self.category_button = tk.Button(self.left_frame, text="Convert to Category", command=self.convert_to_category)
        self.category_button.grid(row=4, column=0, padx=10, pady=10)

        self.remove_columns_button = tk.Button(self.left_frame, text="Remove Columns", command=self.remove_columns)
        self.remove_columns_button.grid(row=4, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self.left_frame, text="Save Preprocessed Data", command=self.save_preprocessed_data)
        self.save_button.grid(row=4, column=2, padx=10, pady=10)

        self.preprocess_button = tk.Button(self.left_frame, text="Auto clean ", command=self.preprocess_data)
        self.preprocess_button.grid(row=5, column=1, padx=10, pady=10)

        self.text_widget = tk.Text(self.right_frame, height=20, width=60)
        self.text_widget.grid(row=0, column=0, padx=10, pady=10)

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
            self.variables_listbox.delete(0, tk.END)
            self.dtype_listbox.delete(0, tk.END)
            for column in self.df.columns:
                column_info = self.get_column_info(column)
                self.variables_listbox.insert(tk.END, column_info[0])
                self.dtype_listbox.insert(tk.END, column_info[1])
            self.display_csv_data()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_column_info(self, column_name):
        dtype_str = str(self.df[column_name].dtype)
        return (column_name, dtype_str)

    def display_csv_data(self):
       self.text_widget.delete("1.0", tk.END)
       self.text_widget.insert(tk.END, self.df.to_string(index=False, line_width=2048))

    def convert_to_int(self):
        selected_indices = self.variables_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one variable.")
            return
        for index in selected_indices:
            column_name = self.variables_listbox.get(index)
            int_convert(self.df, columns=(column_name,))
        messagebox.showinfo("Success", "Variables converted to integers.")
        self.display_csv_data()

    def convert_to_float(self):
        selected_indices = self.variables_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one variable.")
            return
        for index in selected_indices:
            column_name = self.variables_listbox.get(index)
            float_convert(self.df, columns=(column_name,))
        messagebox.showinfo("Success", "Variables converted to floats.")
        self.display_csv_data()

    def remove_variable(self):
        selected_indices = self.variables_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one variable.")
            return
        for index in selected_indices:
            column_name = self.variables_listbox.get(index)
            del self.df[column_name]
        self.variables_listbox.delete(0, tk.END)
        for column in self.df.columns:
            self.variables_listbox.insert(tk.END, column)
        messagebox.showinfo("Success", "Variables removed.")
        self.display_csv_data()

    def convert_to_category(self):
        selected_indices = self.variables_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one variable.")
            return
        for index in selected_indices:
            column_name = self.variables_listbox.get(index)
            category_convert(self.df, columns=(column_name,))
        messagebox.showinfo("Success", "Variables converted to category.")
        self.display_csv_data()

    def remove_columns(self):
        selected_indices = self.variables_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one variable.")
            return
        columns_to_remove = []
        for index in selected_indices:
            column_name = self.variables_listbox.get(index)
            columns_to_remove.append(column_name)
        remove_columns(self.df, columns=columns_to_remove)
        self.variables_listbox.delete(0, tk.END)
        for column in self.df.columns:
            self.variables_listbox.insert(tk.END, column)
        messagebox.showinfo("Success", "Columns removed.")
        self.display_csv_data()

    def save_preprocessed_data(self):
        if self.df is None:
            messagebox.showerror("Error", "No data to save.")
            return
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Preprocessed data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")

    def preprocess_data(self):
        if self.df is None:
            messagebox.showerror("Error", "Please load data first.")
            return
        try:
            df_cleaned = auto_clean(self.df)
            messagebox.showinfo("Success", "Data preprocessing completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = DataPreprocessApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

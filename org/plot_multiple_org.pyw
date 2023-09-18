# -*- coding: utf-8 -*-
"""
Created by Vincenzo Sammartano
@author:  v.sammartano@gmail.com
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Define a function to analyze the selected data file with given parameters
def analyze_data():
    try:
        # Get user inputs
        file_path = file_path_var.get()
        time_filter = float(time_filter_entry.get())
        variable_name = variable_name_entry.get()
        units = units_entry.get()
        header_lines = int(header_lines_entry.get())

        # Check if a file was selected
        if not file_path:
            messagebox.showwarning("Warning", "Please select a data file.")
            return

        # Specify the delimiter used in your .dat file
        delimiter = '\t'  # Change this to the actual delimiter used in your file

        # Load the selected .dat file into a DataFrame, skipping the specified number of header lines
        df = pd.read_csv(file_path, delimiter=delimiter, header=None, skiprows=header_lines)
        
        # Convert the 'time' column to float, assuming it's in the first column (change as needed)
        df[0] = df[0].astype(float)

        # Filter the data to include only rows where the time column is less than or equal to the provided time filter
        filtered_df = df[df[0] <= time_filter]

        # Check if any data is left after filtering
        if filtered_df.empty:
            messagebox.showwarning("Warning", "No data points left after applying the time filter.")
            return

        # Plot the filtered data with custom labels
        plt.plot(filtered_df[0], filtered_df[1], label=f'{variable_name} ({units})')
        plt.xlabel('Time (seconds)')
        plt.ylabel(f'{variable_name} ({units})')
        plt.legend()
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Invalid input values. Please enter valid numbers.")

# Function to open the file dialog and get the selected file path
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Data Files", "*.dat")])
    file_path_var.set(file_path)

def delete():
    root.destroy()
    
# Create the main application window
root = tk.Tk()
root.title("Data Analysis App")

# Variable to store the selected file path
file_path_var = tk.StringVar()

# Create a button to select the data file
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=20)

# Create an Entry widget for the time filter
time_filter_label = tk.Label(root, text="Time Filter (seconds):")
time_filter_label.pack()
time_filter_entry = tk.Entry(root)
time_filter_entry.pack()

# Create an Entry widget for the variable name
variable_name_label = tk.Label(root, text="Variable Name:")
variable_name_label.pack()
variable_name_entry = tk.Entry(root)
variable_name_entry.pack()

# Create an Entry widget for the units
units_label = tk.Label(root, text="Units:")
units_label.pack()
units_entry = tk.Entry(root)
units_entry.pack()

# Create an Entry widget for the number of header lines to skip
header_lines_label = tk.Label(root, text="Number of Header Lines to Skip:")
header_lines_label.pack()
header_lines_entry = tk.Entry(root)
header_lines_entry.pack()

# Create a button to trigger the data analysis and plotting
plot_button = tk.Button(root, text="Plot", command=analyze_data)
plot_button.pack(pady = 10)

# Create athe exit button
exit_button = tk.Button(root, text="Exit", command=delete)
exit_button.pack(pady = 10)

# Start the main application loop
root.mainloop()

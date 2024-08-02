# -*- coding: utf-8 -*-
"""
Created by Vincenzo Sammartano
@author: v.sammartano@gmail.com
"""
##Libraries to be used
import re
import os
import tkinter as tk
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import ttk, filedialog, messagebox, StringVar, Entry, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

###############
# Global variables to store data, delimiter, and header lines
loaded_data = None
selected_delimiter = ','  # Default delimiter
selected_header_lines = 0  # Default header lines
selected_x_column = None
selected_y_columns = []
use_x_as_y = False
# Checkboxes for column selection
column_checkboxes = []
variable_name_entries = []

###Function block
# Function to load data from a file
def load_data():
    global loaded_data, selected_delimiter, selected_header_lines
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_delimiter = delimiter_combobox.get()
        if selected_delimiter:
            header_lines = header_lines_entry.get()
            try:
                selected_header_lines = int(header_lines)
            except ValueError:
                selected_header_lines = 0
            try:
                if selected_delimiter == 'Space':
                    selected_delimiter = ' '
                elif selected_delimiter == 'Tab':
                    selected_delimiter = '\t'
                loaded_data = pd.read_csv(file_path, delimiter=selected_delimiter, header=selected_header_lines)
                print(f"Loaded data from {file_path} with delimiter: {selected_delimiter} and {selected_header_lines} header lines")
                populate_column_checkboxes()
            except pd.errors.EmptyDataError:
                print("The loaded file is empty.")
            except pd.errors.ParserError:
                print(f"Error: Unable to load data from {file_path} with delimiter: {selected_delimiter} and {selected_header_lines} header lines")

# Function to populate the column selection checkboxes with variable names
def populate_column_checkboxes():
    global column_checkboxes, variable_name_entries
    if loaded_data is not None:
        num_columns = loaded_data.shape[1]
        for idx in range(num_columns):
            col_name = str(idx)
            var_x = tk.BooleanVar()
            var_y = tk.BooleanVar()
            var_name = tk.StringVar()
            checkbox_x = tk.Checkbutton(column_variable_frame, variable=var_x)
            checkbox_y = tk.Checkbutton(column_variable_frame, variable=var_y)
            entry = tk.Entry(column_variable_frame, textvariable=var_name, width=10)
            checkbox_x.grid(row=idx+1, column=0, sticky='w', padx=10,pady=1)
            checkbox_y.grid(row=idx+1, column=1, sticky='w')
            entry.grid(row=idx+1, column=3, sticky='w')
            column_checkboxes.append((idx, var_x, var_y, entry))
            variable_name_entries.append((idx, var_name))
            column_name = tk.Label(column_variable_frame, text=col_name)
            column_name.grid(row=idx+1, column=2, sticky='w',padx=10,pady=1)

# Function to plot the data
def plot_data():
    global selected_x_column, selected_y_columns, use_x_as_y, canvas
    selected_x_column = None
    selected_y_columns = []
    use_x_as_y = False
    for idx, var_x, var_y, _ in column_checkboxes:
        if var_x.get():
            selected_x_column = idx
        if var_y.get():
            selected_y_columns.append(idx)
            if use_x_as_y:
                use_x_as_y = False

    if loaded_data is not None and selected_x_column is not None and selected_y_columns:
        ax.clear()
        x = loaded_data.iloc[:, selected_x_column]
        for y_col in selected_y_columns:
            y = loaded_data.iloc[:, y_col]
            ax.plot(x, y, label=f"{variable_name_entries[selected_x_column][1].get()} vs {variable_name_entries[y_col][1].get()}")
        ax.set_xlabel(f"X-axis: {variable_name_entries[selected_x_column][1].get()}")
        ax.set_ylabel("Y-axis")
        ax.set_title("Line Plot")
        ax.legend()
        if canvas:
            canvas.get_tk_widget().pack_forget()  # Clear the previous canvas
        canvas = FigureCanvasTkAgg(fig, master=frame_fig)
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=4)


# Function to save the plot
def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png'),('JPG Files', '*.jpg')])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Info", f"Plot saved as {save_filename}")

###End of Function

###Main Program
if __name__ == "__main__":
    
    # Create the main application window
    root = tk.Tk()
    root.title("Data Analysis App")
    root.geometry("900x510+200+150")  # Adjusted the window size
    root.resizable(width=False, height=False)
    
    ##Global block vars
    # Delimiter dictionary
    delimiter_mapping = {
        "Comma": ",",
        "Semicolon": ";",
        "Tab": "\t",
        "Space": r'\s+'
        }
    
    #Fonts
    f_H12B = font.Font(family='Helvetica', size=12, weight='bold')
    f_H12 = font.Font(family='Helvetica', size=12, weight='normal')
    f_H11B = font.Font(family='Helvetica', size=11, weight='bold')
    f_H10 = font.Font(family='Helvetica', size=10, weight='normal')
    f_H08 = font.Font(family='Helvetica', size=8, weight='normal')
    font.families()

    #####################
    
    # My notebook
    my_notebook = ttk.Notebook(root)
    my_notebook.pack()

    # Main frames
    top_frame_1 = tk.Frame(my_notebook)
    top_frame_1.grid(row=0, column=0, sticky="w")
    statistics_frame = tk.Frame(my_notebook)   

    # Window tabs
    my_notebook.add(top_frame_1, text="Data Chart")
    my_notebook.add(statistics_frame, text="Data Statistics")

    # Data Selection frame
    data_selection_frame = tk.LabelFrame(top_frame_1, text="Data Selection")
    data_selection_frame.grid(row=0, column=0, padx=25, sticky="w")

    # Entry widget for the number of header lines to skip
    header_lines_label = tk.Label(data_selection_frame, text="Number of Header Lines to Skip:", font=f_H10)
    header_lines_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    header_lines_entry = tk.Entry(data_selection_frame, width= 11, font=f_H10)
    header_lines_entry.insert(0, str(selected_header_lines))
    header_lines_entry.grid(row=0, column=1, sticky='w', padx=5, pady=10)

    # Delimiter frame
    delimiter_label = tk.Label(data_selection_frame, text="Select Delimiter:",font=f_H10)
    delimiter_label.grid(row = 1, column = 0, sticky='w', padx=5, pady=10)
    delimiter_options = [',', ';', 'Tab', 'Space']
    delimiter_combobox = ttk.Combobox(data_selection_frame, values = delimiter_options,
                                      width=9,font=f_H10)
    delimiter_combobox.set(selected_delimiter)
    delimiter_combobox.grid(row=1, column=1, sticky='w', padx=5,pady=10)
    
    # Data Configuration frame
    column_variable_frame = tk.LabelFrame(top_frame_1, text="Data Configuration")
    column_variable_frame.grid(row=1, column=0, padx=18, sticky="nw")
    column_x_lab = tk.Label(column_variable_frame, text="Use as X", font=f_H10) 
    column_y_lab = tk.Label(column_variable_frame, text="Use as Y", font=f_H10) 
    column_x_lab.grid(row=0, column=0, padx=6, pady=10, sticky="w")
    column_y_lab.grid(row=0, column=1, padx=6, pady=10, sticky="w")
    column_number_lab = tk.Label(column_variable_frame, text="Column #", font=f_H10) 
    column_number_lab.grid(row=0, column=2, padx=6, pady=10, sticky="w")
    var_name_lab = tk.Label(column_variable_frame, text="Variable name", font=f_H10) 
    var_name_lab.grid(row=0, column= 3, padx=6, pady=10, sticky="w", columnspan = 2)

    # Figure frame
    frame_fig = tk.LabelFrame(top_frame_1, text="", width=495, height=458, font=f_H10)
    frame_fig.grid(row=0, column=1, padx = 10, pady = 5,rowspan=5, sticky="nesw")
    frame_fig.config(borderwidth=0.5, bg="white")
    # Figure initialization
    # the inches have to be equale to the dimension of the labelframe at a specific dpi
    fig = Figure(figsize=(7.07,6.542857), dpi=70)
    ax = fig.add_subplot()
    canvas = None
    current_chart_index = 0
    toolbar = None
    
    # Buttons block
    # Buttons Frame for plot
    button_frame = tk.LabelFrame(top_frame_1, text="Actions",width=50)
    button_frame.grid(row=4, column=0, padx=20,pady = 4,  sticky="s")

    # Button to select the data file
    select_button = tk.Button(data_selection_frame, text="Select Data File", command=load_data, font=f_H10)
    select_button.grid(row=2, column=0, padx=10, pady=5, sticky="nesw", columnspan=2)
    
    # Button to plot data
    plot_button = tk.Button(button_frame, text="Plot Data", command=plot_data,width= 8)
    plot_button.grid(row=0, column=0, padx=15, pady=8, sticky="w")

    # button to save the current plot
    save_plot_button = tk.Button(button_frame, text="Save Plot", command=save_plot, width=10)
    save_plot_button.grid(row=0, column=1, padx=15, pady=8, sticky="w")

    # Exit button
    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy,width= 10)
    exit_button.grid(row=0, column=2, padx=15,pady=8) #columnspan=0)

 
    statistics_text = None  # Define the global variable
    
##    create_statistics_tab()
    
    # Start the main application loop
    root.mainloop()

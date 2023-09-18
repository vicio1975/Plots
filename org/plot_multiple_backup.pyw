# -*- coding: utf-8 -*-
"""
Created by Vincenzo Sammartano
@author: v.sammartano@gmail.com
"""
##Libraried to be used
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, StringVar, Entry, font
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import re
import os
from matplotlib import style
import seaborn as sns

delimiter_mapping = {
    "Comma": ",",
    "Semicolon": ";",
    "Tab": "\t",
    "Space": r'\s+'
    }

###Function block
def update_statistics():
    """
    This is the statistics module
    """

    if filtered_df is not None:
        statistics_text.delete(1.0, tk.END)  # Clear the previous text
        # Create a dictionary to map the original column names to the variable names
        column_mapping = {filtered_df.columns[i+1]: variable_names[i] for i in range(len(variable_names))}
        filtered_df_stat = pd.DataFrame.copy(filtered_df)
        # Rename the columns of the filtered DataFrame using the dictionary
        filtered_df_stat.rename(columns=column_mapping, inplace=True)
        L= len(variable_names)
        statistics = filtered_df_stat.iloc[:, 1:L+1].describe()
        statistics_text.insert(tk.END, statistics)
        
            
def select_file():
    """
    Open a file dialog to select a data file.
    """
    file_dialog = filedialog.askopenfile(filetypes=[("Data Files", "*.dat;*.csv;*.txt;*.out")])
    if file_dialog:
        file_path = file_dialog.name
        file_name = os.path.basename(file_path)
        file_path_var.set(file_path)
        file_dialog.close()
        selected_file_label.config(text=f"Selected File: {file_name}")

def analyze_data():
    """
    Function to analyze the selected data file with given parameters
    """
    try:
        global df, variable_names, current_chart_index, toolbar, filtered_df

        file_path = file_path_var.get()
        time_filter_min = float(time_filter_min_entry.get())
        time_filter_max = float(time_filter_max_entry.get())
        header_lines = int(header_lines_entry.get())
        column_separator = column_separator_combobox.get()
        variable_names = re.split(r'\s*,\s*', variable_names_var.get())

        if not file_path:
            messagebox.showwarning("Warning", "Please select a data file.")
            return

        delimiter = delimiter_mapping[column_separator]
        df = pd.read_csv(file_path, delimiter=delimiter, header=None, skiprows=header_lines)
        df[0] = df[0].astype(float)
        min_time_data = df[0].min()

        if time_filter_min < min_time_data:
            messagebox.showwarning("Warning", f"The minimum time filter must be greater than or equal to {min_time_data}.")
            return

        filtered_df = df[(df[0] >= time_filter_min) & (df[0] <= time_filter_max)]

        if filtered_df.empty:
            messagebox.showwarning("Warning", "No data points left after applying the time filter.")
            return

        # Check if the number of named variables is valid
        if len(variable_names) > len(filtered_df.columns) - 1:
            messagebox.showwarning("Warning", "The number of named variables exceeds the number of available columns.")
            return

        clean_plot()  # Clear the previous plot
        plot_chart(current_chart_index)  # Plot the first chart

        # Show the Next button
        next_button.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        # Show the Previous button
        prev_button.grid(row=0, column=2, padx=5, pady=8, sticky="w")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def clean_plot():
    """
    Function to clear the current plot
    """
    global canvas, toolbar
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None
    if toolbar:
        toolbar.destroy()
        toolbar = None

def plot_chart(index):
    """
    Function to plot the chart for the given variable index
    """
    global ax, canvas, current_chart_index

    ax.clear()  # Clear the previous plot
    # Use the selected variable name as the label
    variable_name = variable_names[index]
    ax.plot(filtered_df[0], filtered_df[index + 1], label=variable_name)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel(variable_name)
    ax.ticklabel_format(axis= 'y', style='plain')
    ax.legend()
    
    if canvas:
        canvas.get_tk_widget().pack_forget()  # Clear the previous canvas
    canvas = FigureCanvasTkAgg(fig, master=frame_fig)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=4)
    current_chart_index = index
    
def save_plot():
    """
    Save the current plot to an image file.
    """
    if canvas:
        file_path = file_path_var.get()
        # Get the selected variable name
        variable_name = variable_names[current_chart_index]
        # Define the filename for saving
        save_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{variable_name}.png"
        # Use savefig to save the current plot
        fig.savefig(save_filename)
        messagebox.showinfo("Info", f"Plot saved as {save_filename}")
        
def show_next_chart():
    """
    Function to show the next chart
    """
    global current_chart_index
    if current_chart_index < len(variable_names) - 1:
        current_chart_index += 1
        clean_plot()
        plot_chart(current_chart_index)

def show_previous_chart():
    """
    Function to show the previous chart
    """
    global current_chart_index
    if current_chart_index > 0:
        current_chart_index -= 1
        clean_plot()
        plot_chart(current_chart_index)
        
def create_statistics_tab():
    """
    Statistics part
    """
    global statistics_text  # Declare statistics_text as a global variable
    statistics_frame = ttk.Frame(my_notebook)
    my_notebook.add(statistics_frame, text="Data Statistics")
    
    ##Statistics
    statistics_label = tk.Label(statistics_frame, text="Descriptive Statistics", font=f_H12B)
    statistics_label.pack(padx=10, pady=10)
    
    # Displaying statistics
    statistics_text = tk.Text(statistics_frame, height=20, width=80, wrap=tk.WORD)
    statistics_text.pack(padx=10, pady=10)

    # Vertical scrollbar for the statistics text widget
    statistics_scrollbar = tk.Scrollbar(statistics_frame, orient=tk.VERTICAL, command=statistics_text.yview)
    statistics_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    statistics_text.config(yscrollcommand=statistics_scrollbar.set)

    statistics_scrollbar_H = tk.Scrollbar(statistics_frame, orient=tk.HORIZONTAL, command=statistics_text.xview)
    statistics_scrollbar_H.pack(side=tk.RIGHT, fill=tk.X)
    statistics_text.config(xscrollcommand=statistics_scrollbar_H.set)

    # Button to calculate statistics
    calculate_stats_button = tk.Button(statistics_frame, text="Calculate Statistics", command=update_statistics, font=f_H10B)
    calculate_stats_button.pack(pady=10)
    
###End of Function

###Main Program
if __name__ == "__main__":

    # Create the main application window
    root = tk.Tk()
    root.title("Data Analysis App")
    root.geometry("1000x510+200+150")  # Adjusted the window size
    root.resizable(width=False, height=False)

    # My notebook
    my_notebook = ttk.Notebook(root)
    my_notebook.pack()

    # Fonts
    f_H12 = tk.font.Font(family='Helvetica', size=12, weight='normal')
    f_H12B = tk.font.Font(family='Helvetica', size=12, weight='bold')
    f_H10 = tk.font.Font(family='Helvetica', size=10, weight='normal')
    f_H10B = tk.font.Font(family='Helvetica', size=10, weight='bold')
    font.families()

    # Variable to store the selected file path
    file_path_var = StringVar()

    # Main frames
    top_frame_1 = tk.Frame(my_notebook, width=10)
    top_frame_1.grid(row=0, column=0, sticky="w")
    
    # Window tabs
    my_notebook.add(top_frame_1, text="Data Chart")

    # Data Selection frame
    data_selection_frame = tk.LabelFrame(top_frame_1, text="Data Selection", width=10)
    data_selection_frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Button to select the data file
    select_button = tk.Button(data_selection_frame, text="Select Data File", command=select_file, font=f_H10)
    select_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    selected_file_label = tk.Label(data_selection_frame, text=" ", font=f_H10, width= 20)
    selected_file_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Entry widget for the number of header lines to skip
    header_lines_label = tk.Label(data_selection_frame, text="Number of Header Lines to Skip:", font=f_H10)
    header_lines_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")
    header_lines_entry = tk.Entry(data_selection_frame, width= 18, font=f_H10)
    header_lines_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Data Configuration frame
    data_config_frame = tk.LabelFrame(top_frame_1, text="Data Configuration", width=10)
    data_config_frame.grid(row=1, column=0, padx=5, pady=10, sticky="w")

    # Time Frame Selection frame
    time_frame_frame = tk.LabelFrame(top_frame_1, text="Time Frame Selection", width=10)
    time_frame_frame.grid(row=2, column=0, padx = 5, pady=5, sticky="w")

    # Entry widget for the minimum time filter
    time_filter_min_label = tk.Label(time_frame_frame, text="Minimum Time (seconds):", font=f_H10)
    time_filter_min_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    time_filter_min_entry = tk.Entry(time_frame_frame, width = 20)
    time_filter_min_entry.grid(row=0, column=1, padx = 10, pady=5, sticky="w")

    # Entry widget for the maximum time filter
    time_filter_max_label = tk.Label(time_frame_frame, text="Maximum Time (seconds):", font=f_H10)
    time_filter_max_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    time_filter_max_entry = tk.Entry(time_frame_frame, width = 20)
    time_filter_max_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Combobox for selecting the column separator
    column_separator_label = tk.Label(data_config_frame, text="Data Delimiter:", font=f_H10)
    column_separator_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    delimiter_options = ["Comma", "Semicolon", "Tab", "Space"]
    column_separator_combobox = ttk.Combobox(data_config_frame, values=delimiter_options)
    column_separator_combobox.set(delimiter_options[0])
    column_separator_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Entry widget for the variable names
    variable_names_label = tk.Label(data_config_frame, text="Variable Names (comma-separated):", font=f_H10)
    variable_names_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    variable_names_var = StringVar()
    variable_names_entry = tk.Entry(data_config_frame, textvariable=variable_names_var)
    variable_names_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Figure frame
    frame_fig = tk.LabelFrame(top_frame_1, text="", width=495, height=458, font=f_H10)
    frame_fig.grid(row=0, column=1, padx = 10, pady = 5,rowspan=5, sticky="w")
    frame_fig.config(borderwidth=0, bg="white")

    #Buttons
    button_frame = tk.LabelFrame(top_frame_1, text="Actions",width=50)
    button_frame.grid(row=3, column=0, padx=2,  sticky="w")

    # Button to plot data
    plot_button = tk.Button(button_frame, text="Plot Data", command=analyze_data,
                            width= 8)
    plot_button.grid(row=0, column=0, padx=5, pady=8, sticky="w")

    # Button to show the next chart
    next_button = tk.Button(button_frame, text="Next", command=show_next_chart,
                            width= 8)
    next_button.grid(row=0, column=1, padx=5, pady=8, sticky="w")

    # Button to show the previous chart
    prev_button = tk.Button(button_frame, text="Previous", command=show_previous_chart,
                            width= 8)
    prev_button.grid(row=0, column=2, padx=5, pady=8, sticky="w")

    # Button to clear the current plot
    clean_button = tk.Button(button_frame, text="Clean Plot", command=clean_plot,
                             width= 8)
    clean_button.grid(row=0, column=3, padx=5, pady=8, sticky="w")

    # button to save the current plot
    save_plot_button = tk.Button(button_frame, text="Save Plot", command=save_plot, width=10)
    save_plot_button.grid(row=0, column=4, padx=5, pady=8, sticky="w")

    # Exit button
    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy,
                            width= 10)
    exit_button.grid(row=1, column=0, padx=5,pady=8, columnspan=5)
    
    # Figure initialization
    #the inches have to be equale to the dimension of the labelframe at a specific dpi
    fig = Figure(figsize=(7.07,6.542857), dpi=70)
    ax = fig.add_subplot()
    canvas = None
    current_chart_index = 0
    toolbar = None
  
    statistics_text = None  # Define the global variable
    
    create_statistics_tab()
    
    # Start the main application loop
    root.mainloop()

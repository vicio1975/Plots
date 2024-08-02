import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Global variables to store data, delimiter, and header lines
loaded_data = None
selected_delimiter = ','  # Default delimiter
selected_header_lines = 0  # Default header lines
selected_x_column = None
selected_y_columns = []

# Function to load data from a file
def load_data():
    global loaded_data
    file_path = filedialog.askopenfilename()
    if file_path:
        # Ask user to select a delimiter using a Combobox
        selected_delimiter = delimiter_combobox.get()
        if selected_delimiter:
            # Ask user to specify the number of header lines using an Entry
            header_lines = header_lines_entry.get()
            try:
                selected_header_lines = int(header_lines)
            except ValueError:
                selected_header_lines = 0

            # Load data using Pandas with the selected delimiter and header lines
            try:
                if selected_delimiter == 'Space':
                    selected_delimiter = ' '
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
            var = tk.BooleanVar()
            var_name = tk.StringVar()
            checkbox = tk.Checkbutton(column_variable_frame, text=f"Column {idx + 1}:", variable=var)
            entry = tk.Entry(column_variable_frame, textvariable=var_name)
            checkbox.grid(row=idx, column=0, sticky='w')
            entry.grid(row=idx, column=1, sticky='w')
            column_checkboxes.append((idx, var, entry))
            variable_name_entries.append((idx, var_name))

# Function to plot the data
def plot_data():
    global selected_x_column, selected_y_columns
    selected_x_column = None
    selected_y_columns = []
    for idx, var, _ in column_checkboxes:
        if var.get():
            if selected_x_column is None:
                selected_x_column = idx
            else:
                selected_y_columns.append(idx)

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
        canvas.draw()

# Create the main application window
root = tk.Tk()
root.title("Plot Data App")

# Create a Notebook widget for different tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create the "Load and Plot Data" tab
load_plot_tab = ttk.Frame(notebook)
notebook.add(load_plot_tab, text='Load and Plot Data')

# Create a Figure and a canvas for Matplotlib plot
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=load_plot_tab)
canvas.get_tk_widget().pack()

# Delimiter and Header Lines frame
delimiter_frame = tk.Frame(load_plot_tab)
delimiter_frame.pack(pady=10)

delimiter_label = tk.Label(delimiter_frame, text="Select Delimiter:")
delimiter_label.grid(row=0, column=0, sticky='e')

delimiter_options = [',', ';', '\t', 'Space']  # Add more delimiter options if needed
delimiter_combobox = ttk.Combobox(delimiter_frame, values=delimiter_options)
delimiter_combobox.set(selected_delimiter)
delimiter_combobox.grid(row=0, column=1, sticky='w')

header_lines_label = tk.Label(delimiter_frame, text="Header Lines:")
header_lines_label.grid(row=0, column=2, sticky='e')

header_lines_entry = tk.Entry(delimiter_frame)
header_lines_entry.insert(0, str(selected_header_lines))
header_lines_entry.grid(row=0, column=3, sticky='w')

# Column selection frame with variable names
column_variable_frame = tk.Frame(load_plot_tab)
column_variable_frame.pack()

# Checkboxes for column selection
column_checkboxes = []
variable_name_entries = []

# Button for loading data
load_button = tk.Button(load_plot_tab, text="Load Data", command=load_data)
load_button.pack(pady=10)

# Button for plotting data
plot_button = tk.Button(load_plot_tab, text="Plot Data", command=plot_data)
plot_button.pack(pady=10)

root.mainloop()

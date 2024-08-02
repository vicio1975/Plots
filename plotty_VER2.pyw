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
use_x_as_y = False

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
            col_name = "Column" + str(idx)
            var_x = tk.BooleanVar()
            var_y = tk.BooleanVar()
            var_name = tk.StringVar()
            checkbox_x = tk.Checkbutton(column_variable_frame, text="Use as X", variable=var_x)
            checkbox_y = tk.Checkbutton(column_variable_frame, text="Use as Y", variable=var_y)
            entry = tk.Entry(column_variable_frame, textvariable=var_name)
            checkbox_x.grid(row=idx, column=0, sticky='w')
            checkbox_y.grid(row=idx, column=1, sticky='w')
            entry.grid(row=idx, column=3, sticky='w')
            column_checkboxes.append((idx, var_x, var_y, entry))
            variable_name_entries.append((idx, var_name))
            column_name = tk.Label(column_variable_frame, text=col_name)
            column_name.grid(row=idx, column=2, sticky='w')

# Function to plot the data
def plot_data():
    global selected_x_column, selected_y_columns, use_x_as_y
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
        canvas.draw()

# Function to save the plot
def save_plot():
    
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png')])
    if file_path:
        fig.savefig(file_path)
        print(f"Saved plot to {file_path}")

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
canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)

# Delimiter frame
delimiter_frame = tk.Frame(load_plot_tab)
delimiter_frame.grid(row=1, column=0, columnspan=3, pady=10)

delimiter_label = tk.Label(delimiter_frame, text="Select Delimiter:")
delimiter_label.grid(row=0, column=0, sticky='e', padx=10)

delimiter_options = [',', ';', '\t', 'Space']  # Add more delimiter options if needed
delimiter_combobox = ttk.Combobox(delimiter_frame, values=delimiter_options)
delimiter_combobox.set(selected_delimiter)
delimiter_combobox.grid(row=0, column=1, sticky='w', padx=10)

# Header lines frame
header_lines_frame = tk.Frame(load_plot_tab)
header_lines_frame.grid(row=2, column=0, columnspan=3, pady=10)

header_lines_label = tk.Label(header_lines_frame, text="Header Lines:")
header_lines_label.grid(row=0, column=0, sticky='e', padx=10)

header_lines_entry = tk.Entry(header_lines_frame)
header_lines_entry.insert(0, str(selected_header_lines))
header_lines_entry.grid(row=0, column=1, sticky='w', padx=10)

# Column selection frame with variable names
column_variable_frame = tk.Frame(load_plot_tab)
column_variable_frame.grid(row=3, column=0, columnspan=3, pady=10)

# Checkboxes for column selection
column_checkboxes = []
variable_name_entries = []

# Button for loading data
load_button = tk.Button(load_plot_tab, text="Load Data", command=load_data)
load_button.grid(row=4, column=0, padx=10, pady=10, sticky='w')

# Button for plotting data
plot_button = tk.Button(load_plot_tab, text="Plot Data", command=plot_data)
plot_button.grid(row=4, column=1, padx=10, pady=10, sticky='w')

# Button for saving the chart
save_button = tk.Button(load_plot_tab, text="Save Chart", command=save_plot)
save_button.grid(row=4, column=2, padx=10, pady=10, sticky='w')

# Start the main application loop
root.mainloop()

import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox, font, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
loaded_data = None
selected_delimiter = ','
selected_header_lines = 0
selected_x_column = None
selected_y_columns = []


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
                populate_column_checkboxes()
            except pd.errors.EmptyDataError:
                print("The loaded file is empty.")
            except pd.errors.ParserError:
                print(f"Error: Unable to load data from {file_path} with delimiter: {selected_delimiter} and {selected_header_lines} header lines")

# Function to populate the column selection checkboxes with variable names
def populate_column_checkboxes():
    global column_checkboxes, variable_name_entries

    # Clear the old labels
    for widget in checkboxes_frame.winfo_children():
        widget.destroy()

    column_checkboxes.clear()
    variable_name_entries.clear()

    if loaded_data is not None:
        num_columns = loaded_data.shape[1]

        for idx in range(num_columns):
            var_x = tk.BooleanVar()
            var_y = tk.BooleanVar()
            var_name = tk.StringVar()
            checkbox_x = tk.Checkbutton(checkboxes_frame, variable=var_x)
            checkbox_y = tk.Checkbutton(checkboxes_frame, variable=var_y)
            entry = tk.Entry(checkboxes_frame, textvariable=var_name, width=10)
            checkbox_x.grid(row=idx, column=0, sticky='w', padx=30, pady=2)
            checkbox_y.grid(row=idx, column=1, sticky='w', padx=30, pady=2)
            entry.grid(row=idx, column=3, sticky='w', padx=30, pady=2)
            column_checkboxes.append((checkbox_x, var_x, checkbox_y, var_y, entry))
            variable_name_entries.append((idx, var_name))
            column_name = tk.Label(checkboxes_frame, text=f"{idx}")
            column_name.grid(row=idx, column=2, sticky='w', padx=32, pady=2)


# Function to plot the data
def plot_data():
    global selected_x_column, selected_y_columns, canvas
    selected_x_column = None
    selected_y_columns = []
    legend_labels = []

    for idx, (_, var_x, _, var_y, var_name) in enumerate(column_checkboxes):
        if var_x.get():
            selected_x_column = idx
        if var_y.get():
            selected_y_columns.append(idx)
            legend_labels.append(var_name.get())

    if loaded_data is not None and selected_x_column is not None and selected_y_columns:
        ax.clear()
        x = loaded_data.iloc[:, selected_x_column]
        for y_col in selected_y_columns:
            y = loaded_data.iloc[:, y_col]
            ax.plot(x, y)
        ax.set_xlabel(f"X-axis: {variable_name_entries[selected_x_column][1].get()}")
        ax.set_ylabel("Y-axis")
        ax.legend(legend_labels)

    if canvas:
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(fig, master=frame_fig)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=4)


# Function to save the plot
def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png'), ('JPG Files', '*.jpg')])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Info", f"Plot saved as {file_path}")

def tune_plot():
    """
tune the chart
"""
    root2 = tk.Tk()
    root2.title("Tune chart")
    root2.geometry("300x100+800+150")
    root2.resizable(width=False, height=False)
    f_H10 = font.Font(family='Helvetica', size=2, weight='normal')

    def go(): 
        ax.set_title(title_entry.get())
        ax.set_xlabel(x_entry.get())
        ax.set_ylabel(y_entry.get())
       
        canvas.draw_idle()
    
    set_button  = tk.Button(root2, text="Format chart",command=go, font=f_H10)
    set_button.grid(row= 3, column=1, sticky="ew")

    # Main frames    
    title_label = tk.Label(root2, text="Title:", font=f_H10)
    title_label.grid(row=0, column=0, padx=5, pady=6, sticky="w")
    title_entry=tk.Entry(root2, width=20, font=f_H10)
    title_entry.grid(row=0, column=1, padx=5, pady=6, sticky="w")

    x_label = tk.Label(root2, text="X label:", font=f_H10)
    x_label.grid(row=1, column=0, padx=5, pady=6, sticky="w")
    x_entry=tk.Entry(root2, width=20, font=f_H10)
    x_entry.grid(row=1, column=1, padx=5, pady=6, sticky="w")

    y_label = tk.Label(root2, text="Y label:", font=f_H10)
    y_label.grid(row=2, column=0, padx=5, pady=6, sticky="w")
    y_entry=tk.Entry(root2, width=20, font=f_H10)
    y_entry.grid(row=2, column=1, padx=5, pady=6, sticky="w")
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Data Analysis App")
    root.geometry("950x510+200+150")
    root.resizable(width=False, height=False)
    #Fonts
    f_H12B = font.Font(family='Helvetica', size=12, weight='bold')
    f_H12 = font.Font(family='Helvetica', size=12, weight='normal')
    f_H11B = font.Font(family='Helvetica', size=11, weight='bold')
    f_H10 = font.Font(family='Helvetica', size=10, weight='normal')
    f_H08 = font.Font(family='Helvetica', size=8, weight='normal')
    font.families()# Function to load data from a file
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
    data_selection_frame.grid(row=0, column=0, padx=70, pady=6, sticky="w")

    # Entry widget for the number of header lines to skip
    header_lines_label = tk.Label(data_selection_frame, text="Number of Header Lines to Skip:", font=f_H10)
    header_lines_label.grid(row=0, column=0, padx=5, pady=6, sticky="w")
    header_lines_entry = tk.Entry(data_selection_frame, width=11, font=f_H10)
    header_lines_entry.insert(0, str(selected_header_lines))
    header_lines_entry.grid(row=0, column=1, sticky='w', padx=5, pady=6)

    # Delimiter frame
    delimiter_label = tk.Label(data_selection_frame, text="Select Delimiter:", font=f_H10)
    delimiter_label.grid(row=1, column=0, sticky='w', padx=5, pady=10)
    delimiter_options = [',', ';', 'Tab', 'Space']
    delimiter_combobox = ttk.Combobox(data_selection_frame, values=delimiter_options, width=9, font=f_H10)
    delimiter_combobox.set(selected_delimiter)
    delimiter_combobox.grid(row=1, column=1, sticky='w', padx=5, pady=10)

    # Data Configuration frame
    column_variable_frame = tk.LabelFrame(top_frame_1, text="Data Configuration")
    column_variable_frame.grid(row=1, column=0, padx=18, sticky="nw")

    column_x_lab = tk.Label(column_variable_frame, text="Use as X", font=f_H10)
    column_y_lab = tk.Label(column_variable_frame, text="Use as Y", font=f_H10)
    column_x_lab.grid(row=0, column=0, padx=1, pady=10, sticky="ew")
    column_y_lab.grid(row=0, column=1, padx=1, pady=10, sticky="ew")
    column_number_lab = tk.Label(column_variable_frame, text="Column #", font=f_H10)
    column_number_lab.grid(row=0, column=2, padx=1, pady=10, sticky="ew")
    var_name_lab = tk.Label(column_variable_frame, text="Variable name", font=f_H10)
    var_name_lab.grid(row=0, column=3, padx=1, pady=10, sticky="ew")

    # Create a canvas to contain the checkboxes and a scrollbar
    checkbox_canvas = tk.Canvas(column_variable_frame, height=200)
    checkbox_canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

    checkbox_scrollbar = Scrollbar(column_variable_frame, orient="vertical", command=checkbox_canvas.yview)
    checkbox_scrollbar.grid(row=1, column=4, sticky="ns")
    checkbox_canvas.config(yscrollcommand=checkbox_scrollbar.set)

    # Create a frame within the canvas to contain the checkboxes
    checkboxes_frame = tk.Frame(checkbox_canvas)
    checkbox_canvas.create_window((0, 0), window=checkboxes_frame, anchor="nw")

    # List to store checkbox references
    column_checkboxes = []
    variable_name_entries = []
    
    # Figure frame
    frame_fig = tk.LabelFrame(top_frame_1, text="", width=490, height=458, font=f_H10)
    frame_fig.grid(row=0, column=1, padx=5, pady=5, rowspan=5, sticky="nesw")
    frame_fig.config(borderwidth=0.5, bg="white")

    # Figure initialization
    fig = Figure(figsize=(7.07, 6.542857), dpi=70)
    ax = fig.add_subplot()
    canvas = None

    # Buttons block
    # Buttons Frame for plot
    button_frame = tk.LabelFrame(top_frame_1, text="Actions", width=50)
    button_frame.grid(row=4, column=0, padx=20, pady=4, sticky="s")

    # Button to select the data file
    select_button = tk.Button(data_selection_frame, text="Select Data File", command=load_data, font=f_H10)
    select_button.grid(row=2, column=0, padx=15, pady=5, sticky="nesw", columnspan=2)

    # Button to plot data
    plot_button = tk.Button(button_frame, text="Plot Data", command=plot_data, width=8)
    plot_button.grid(row=0, column=0, padx=15, pady=8, sticky="w")

    # Button to save the current plot
    save_plot_button = tk.Button(button_frame, text="Save Plot", command=save_plot, width=10)
    save_plot_button.grid(row=0, column=1, padx=15, pady=8, sticky="w")

    # Button to modify Axes
    set_plot_button = tk.Button(button_frame, text="Chart Tune", command=tune_plot, width=10)
    set_plot_button.grid(row=0, column=2, padx=15, pady=8, sticky="w")


    # Exit button
    exit_button = tk.Button(button_frame, text="Exit", command=root.destroy, width=10)
    exit_button.grid(row=0, column=4, padx=15, pady=8)



    # Start the main application loop
    root.mainloop()

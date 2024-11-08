import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from matplotlib.figure import Figure
from tkinter import filedialog, messagebox, font, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
datasets = []
selected_delimiter = ','
selected_header_lines = 0
selected_x_column = None
selected_y_columns = []
loaded_data = None
column_checkboxes = []
variable_name_entries = []
last_plotted_data = {
    "x_column": None,
    "y_columns": [],
    "variable_names": []
}
current_plotted_x = None
current_plotted_y = []

# Variables to store plot formatting
plot_title = ""
x_axis_label = ""
y_axis_label = ""

def load_data():
    global datasets, selected_delimiter, selected_header_lines, loaded_data

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
                datasets.append(loaded_data)
                populate_column_checkboxes()
            except pd.errors.EmptyDataError:
                print("The loaded file is empty.")
            except pd.errors.ParserError:
                print(f"Error: Unable to load data from {file_path} with delimiter: {selected_delimiter} and {selected_header_lines} header lines")

def populate_column_checkboxes():
    global column_checkboxes, variable_name_entries

    for widget in checkboxes_frame.winfo_children():
        widget.destroy()

    column_checkboxes.clear()
    variable_name_entries.clear()

    if datasets:
        latest_data = datasets[-1]
        num_columns = latest_data.shape[1]

        for idx in range(num_columns):
            var_x = tk.BooleanVar()
            var_y = tk.BooleanVar()
            var_name = tk.StringVar()

            checkbox_x = tk.Checkbutton(checkboxes_frame, variable=var_x)
            checkbox_y = tk.Checkbutton(checkboxes_frame, variable=var_y)
            entry = tk.Entry(checkboxes_frame, textvariable=var_name, width=10)
            column_checkboxes.append((checkbox_x, var_x, checkbox_y, var_y, entry))
            variable_name_entries.append((idx, var_name))
            column_name = tk.Label(checkboxes_frame, text=f"{idx}")

            checkbox_x.grid(row=idx, column=0, sticky='w', padx=30, pady=2)
            checkbox_y.grid(row=idx, column=1, sticky='w', padx=30, pady=2)
            column_name.grid(row=idx, column=2, sticky='w', padx=32, pady=2)
            entry.grid(row=idx, column=3, sticky='w', padx=30, pady=2)

def plot_data():
    global selected_x_column, selected_y_columns, canvas
    global plot_title, x_axis_label, y_axis_label
    global current_plotted_x, current_plotted_y  # Track current plotted data

    if loaded_data is None:
        messagebox.showwarning("Warning", "No data loaded.")
        return
    
    selected_x_column = None
    selected_y_columns = []
    legend_labels = []
    variable_names = []

    for idx, (_, var_x, _, var_y, var_name) in enumerate(column_checkboxes):
        if var_x.get():
            selected_x_column = idx
        if var_y.get():
            selected_y_columns.append(idx)
            legend_labels.append(var_name.get())
            variable_names.append(var_name.get())

    if selected_x_column is None or not selected_y_columns:
        messagebox.showwarning("Warning", "Please select both X and Y columns for plotting.")
        return

    current_plotted_x = selected_x_column
    current_plotted_y = selected_y_columns

    ax.clear()
    x = loaded_data.iloc[:, selected_x_column]
    for y_col in selected_y_columns:
        y = loaded_data.iloc[:, y_col]
        ax.plot(x, y, label=variable_name_entries[y_col][1].get())
    
    # Set default plot title if not provided
    if not plot_title:
        plot_title = "Data Plot"
    
    # Default axis labels
    x_axis_label = "X-axis"
    y_axis_label = "Y-axis"

    # Override X-axis label if a user-provided name exists
    user_provided_x_name = variable_name_entries[selected_x_column][1].get().strip()
    if user_provided_x_name:
        x_axis_label = f"X-axis: {user_provided_x_name}"

    ax.set_title(plot_title)
    ax.set_xlabel(x_axis_label)
    ax.set_ylabel(y_axis_label)

    try:
        if any(variable_names):
            ax.legend().remove()
            ax.legend()
        else:
            messagebox.showwarning("Warning", "Variable names added...legend is empty!")
    except (IndexError, AttributeError):
        messagebox.showwarning("Warning", "Error updating legend. Check variable names and indices.")

    if canvas:
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(fig, master=frame_fig)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=4)


def clear_plot():
    global datasets, column_checkboxes, variable_name_entries

    ax.clear()
    if canvas:
        canvas.draw_idle()

    datasets = []
    column_checkboxes.clear()
    variable_name_entries.clear()

    for widget in checkboxes_frame.winfo_children():
        widget.destroy()

def save_plot():
    def open_save_dialog():
        save_window = tk.Toplevel(root)
        save_window.title("Save Plot Options")
        save_window.geometry("260x145")
        save_window.resizable(width=False, height=False)
        f_H10 = font.Font(family='Helvetica', size=12)

        # Resolution (DPI) setting
        dpi_label = tk.Label(save_window, text="Resolution (DPI):", font=f_H10)
        dpi_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        dpi_entry = tk.Entry(save_window, width=10, font=f_H12)
        dpi_entry.insert(0, "100")  # Default DPI value
        dpi_entry.grid(row=0, column=1, padx=10, pady=12)

        # File format setting
        format_label = tk.Label(save_window, text="File Format:", font=f_H10)
        format_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        format_options = ["png", "jpg", "pdf", "svg"]
        format_combobox = ttk.Combobox(save_window, values=format_options, font=f_H10, width=8)
        format_combobox.set("png")  # Default format
        format_combobox.grid(row=1, column=1, padx=10, pady=10)

        def save_with_options():
            file_path = filedialog.asksaveasfilename(defaultextension=f'.{format_combobox.get()}',
                                                     filetypes=[(f"{format_combobox.get().upper()} Files", f'*.{format_combobox.get()}')])
            if file_path:
                try:
                    dpi = int(dpi_entry.get())
                except ValueError:
                    dpi = 100  # Fallback to default DPI if invalid input

                fig.savefig(file_path, dpi=dpi, format=format_combobox.get())
                messagebox.showinfo("Info", f"Plot saved as {file_path}")
            save_window.destroy()

        save_button = tk.Button(save_window, text="Save", command=save_with_options, font=f_H12)
        save_button.grid(row=2, column=0, columnspan=2, padx = 10, pady=10,sticky="ew")

    open_save_dialog()

def tune_plot():
    global plot_title, x_axis_label, y_axis_label  # Use global instead of nonlocal

    root2 = tk.Toplevel(root)
    root2.title("Format chart")
    root2.geometry("300x158+800+150")
    root2.resizable(width=False, height=False)
    f_H08 = font.Font(family='Helvetica', size=12, weight='normal')

    def go(): 
        global plot_title, x_axis_label, y_axis_label  # Ensure access to global variables
        plot_title = title_entry.get()
        x_axis_label = x_entry.get()
        y_axis_label = y_entry.get()

        ax.set_title(plot_title)
        ax.set_xlabel(x_axis_label)
        ax.set_ylabel(y_axis_label)
        if canvas:
            canvas.draw_idle()

    set_button = tk.Button(root2, text="Format chart", command=go, font=f_H08)
    set_button.grid(row=3, column=1, sticky="ew")

    title_label = tk.Label(root2, text="Title:", font=f_H08)
    title_label.grid(row=0, column=0, padx=5, pady=6, sticky="ew")
    title_entry = tk.Entry(root2, width=20, font=f_H08)
    title_entry.insert(0, plot_title)
    title_entry.grid(row=0, column=1, padx=5, pady=6, sticky="ew")

    x_label = tk.Label(root2, text="X label:", font=f_H08)
    x_label.grid(row=1, column=0, padx=5, pady=6, sticky="ew")
    x_entry = tk.Entry(root2, width=20, font=f_H08)
    x_entry.insert(0, x_axis_label)
    x_entry.grid(row=1, column=1, padx=5, pady=6, sticky="ew")

    y_label = tk.Label(root2, text="Y label:", font=f_H08)
    y_label.grid(row=2, column=0, padx=5, pady=6, sticky="ew")
    y_entry = tk.Entry(root2, width=20, font=f_H08)
    y_entry.insert(0, y_axis_label)
    y_entry.grid(row=2, column=1, padx=5, pady=6, sticky="ew")


def show_statistics():
    global current_plotted_x, current_plotted_y

    if loaded_data is not None and current_plotted_x is not None and current_plotted_y:
        stats_window = tk.Toplevel(root)
        stats_window.title("Data Statistics")
        stats_window.geometry("300x650+1170+150")
        stats_window.resizable(width=False, height=True)
        
        header = tk.Label(stats_window, text="Statistics for Plotted Data", font=f_H12B)
        header.pack(pady=10)

        for y_col in current_plotted_y:
            y_data = loaded_data.iloc[:, y_col]
            mean = y_data.mean()
            median = y_data.median()
            std_dev = y_data.std()
            min_val = y_data.min()
            max_val = y_data.max()

            stats_text = (
                f"Column {y_col} - {variable_name_entries[y_col][1].get()}:\n"
                f"  Mean: {mean:.2f}\n"
                f"  Median: {median:.2f}\n"
                f"  Standard Deviation: {std_dev:.2f}\n"
                f"  Min: {min_val:.2f}\n"
                f"  Max: {max_val:.2f}\n"
            )
            stats_label = tk.Label(stats_window, text=stats_text, justify="left", font=f_H10)
            stats_label.pack(anchor='w', padx=10, pady=5)
    else:
        messagebox.showwarning("Warning", "No data is currently plotted for statistics.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Data Analysis App")
    root.geometry("970x650+200+150")
    root.resizable(width=False, height=False)
    
    f_H12B = font.Font(family='Helvetica', size=12, weight='bold')
    f_H12 = font.Font(family='Helvetica', size=12, weight='normal')
    f_H11B = font.Font(family='Helvetica', size=11, weight='bold')
    f_H10 = font.Font(family='Helvetica', size=10, weight='normal')
    f_H08 = font.Font(family='Helvetica', size=8, weight='normal')
    
    font.families()

    my_notebook = ttk.Notebook(root)
    my_notebook.pack()

    top_frame_1 = tk.Frame(my_notebook)
    top_frame_1.grid(row=0, column=0, sticky="w")
    statistics_frame = tk.Frame(my_notebook)
    my_notebook.add(top_frame_1, text="Data Chart")

    data_selection_frame = tk.LabelFrame(top_frame_1, text="Data Selection")
    data_selection_frame.grid(row=0, column=0, padx=70, pady=6, sticky="w")

    header_lines_label = tk.Label(data_selection_frame, text="Number of Header Lines to Skip:", font=f_H10)
    header_lines_label.grid(row=0, column=0, padx=5, pady=6, sticky="w")
    header_lines_entry = tk.Entry(data_selection_frame, width=11, font=f_H10)
    header_lines_entry.insert(0, str(selected_header_lines))
    header_lines_entry.grid(row=0, column=1, sticky='w', padx=5, pady=6)

    delimiter_label = tk.Label(data_selection_frame, text="Select Delimiter:", font=f_H10)
    delimiter_label.grid(row=1, column=0, sticky='w', padx=5, pady=10)
    delimiter_options = [',', ';', 'Tab', 'Space']
    delimiter_combobox = ttk.Combobox(data_selection_frame, values=delimiter_options, width=9, font=f_H10)
    delimiter_combobox.set(selected_delimiter)
    delimiter_combobox.grid(row=1, column=1, sticky='w', padx=5, pady=10)

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

    checkbox_canvas = tk.Canvas(column_variable_frame, height=200)
    checkbox_canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

    checkbox_scrollbar = Scrollbar(column_variable_frame, orient="vertical", command=checkbox_canvas.yview)
    checkbox_scrollbar.grid(row=1, column=4, sticky="ns")
    checkbox_canvas.config(yscrollcommand=checkbox_scrollbar.set)

    checkboxes_frame = tk.Frame(checkbox_canvas)
    checkbox_canvas.create_window((0, 0), window=checkboxes_frame, anchor="nw")

    frame_fig = tk.LabelFrame(top_frame_1, text="", width=490, height=458, font=f_H10)
    frame_fig.grid(row=0, column=1, padx=5, pady=5, rowspan=5, sticky="nesw")
    frame_fig.config(borderwidth=0.5, bg="white")

    fig = Figure(figsize=(7.07, 6.542857), dpi=70)
    ax = fig.add_subplot()
    canvas = None

    load_data_button = tk.Button(top_frame_1, text="Load Data", command=load_data, font=f_H10)
    load_data_button.grid(row=2, column=0, padx=40, pady=6, sticky="ew")

    plot_button = tk.Button(top_frame_1, text="Plot", command=plot_data, font=f_H10)
    plot_button.grid(row=3, column=0, padx=40, pady=6, sticky="ew")

    clear_plot_button = tk.Button(top_frame_1, text="Clear Plot", command=clear_plot, font=f_H10)
    clear_plot_button.grid(row=4, column=0, padx=40, pady=6, sticky="ew")

    tune_plot_button = tk.Button(top_frame_1, text="Format Chart", command=tune_plot, font=f_H10)
    tune_plot_button.grid(row=5, column=0, padx=40, pady=6, sticky="ew")

    save_plot_button = tk.Button(top_frame_1, text="Save Plot", command=save_plot, font=f_H10)
    save_plot_button.grid(row=6, column=0, padx=40, pady=6, sticky="ew")

    exit_button = tk.Button(top_frame_1, text="Exit", command=root.destroy, font=f_H10)
    exit_button.grid(row=7, column=0, padx=40, pady=6, sticky="ew")

    show_stats_button = tk.Button(top_frame_1, text="Show Statistics", command=show_statistics, font=f_H10)
    show_stats_button.grid(row=6, column=1, padx=40, pady=6, sticky="ew")

    root.mainloop()

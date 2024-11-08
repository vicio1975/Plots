# Plotty app
This is a Tkinter-based Python application designed for visualizing and analyzing data using Pandas and Matplotlib. It provides a graphical user interface (GUI) for loading datasets, selecting columns for plotting, customizing plot appearance, and displaying statistical summaries of plotted data.

Features
Load Data from CSV Files: Import datasets with user-defined delimiters and header lines.
Data Plotting: Select columns to use as X and Y axes for plotting data.
Customize Plots: Set and update plot titles, X-axis, and Y-axis labels through a user-friendly interface.
Plot Persistence: Ensures that plot customization is retained when additional data is plotted.
View Statistics: Display basic statistics (mean, median, standard deviation, min, max) for currently plotted data.
Save Plots: Save plots in various formats (e.g., PNG, JPG, PDF, SVG) with customizable resolution (DPI).

Installation
Prerequisites
Python 3.x
Required Python packages:
tkinter (GUI library)
pandas (data analysis)
matplotlib (data visualization)

Installation Steps
Clone or download this repository.
Ensure you have the necessary dependencies installed by running
Copy code: pip install pandas matplotlib

Run the main application script:
Copy code: python plotty_VER7_5.pyw

Usage
1. Load Data
Click on the Load Data button.
Select a CSV file and specify the delimiter and number of header lines to skip.
2. Configure Data
Select the column to use as the X-axis.
Select one or more columns for the Y-axis.
Optionally, provide variable names for legend labels.
3. Plot Data
Click on the Plot button to generate the plot.
Plots are updated only if new columns or variable names are selected.
4. Customize Plot
Click on Tune Plot to open a dialog for setting the plot title, X-axis, and Y-axis labels.
Changes are saved and persist even if additional data is plotted later.
5. Show Statistics
Click on Show Statistics to display a window with basic statistics (mean, median, etc.) for the currently plotted data.
6. Save Plot
Click on Save Plot to open a dialog for specifying resolution (DPI) and format (e.g., PNG, JPG).
Save the plot with custom settings.
GUI Controls
Load Data: Opens a file dialog to load a dataset.
Plot: Generates a plot based on selected data columns.
Clear Plot: Clears the current plot and resets selected data.
Tune Plot: Opens a dialog for customizing plot labels and title.
Save Plot: Opens a dialog for saving the plot with customizable settings.
Show Statistics: Displays basic statistics for the currently plotted data.
Exit: Closes the application.

Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.


NB: 
You can also build you own exe file as follow: 
pyinstaller --onefile plotty_VER7_5.pyw --icon iconfile.png
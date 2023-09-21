# Plotty
It imports various libraries and modules, including tkinter for the GUI, pandas for data manipulation,
and matplotlib for plotting.
- The select_file function opens a file dialog to allow the user to select a data file.
- The analyze_data function processes the selected data file with user-defined parameters, including header lines, time filters, column separator, and variable names. It then plots the data.
- The clean_plot function clears the current plot.
- The plot_chart function plots a chart based on the selected variable.
- The show_next_chart and show_previous_chart functions allow the user to navigate between different charts when multiple variables are selected.
- The save_plot function saves the current chart as an image file.
- The create_statistics_tab function sets up a tab for displaying descriptive statistics of the data.
- The update_statistics function calculates and displays descriptive statistics for the selected data.
- The main part of the program creates a GUI window using tkinter and sets up various frames, buttons, entry fields, and charts for data analysis and visualization.
The application's main loop (root.mainloop()) runs the GUI and waits for user interactions.

The statistics are calculated using Pandas and the "describe" method.
This method is applied to the filtered_df_stat, which is a DataFrame that stores the filtered data,
with columns renamed based on the user-defined variable names.

The describe method is applied to a subset of filtered_df_stat, specifically the columns containing the data for each variable.
This is done with the filtered_df_stat.iloc[:, 1:L+1].describe() line. L is the number of variables.

The describe method generates summary statistics for each variable, including:

Count: The number of non-null (valid) data points.
Mean: The average value of the variable.
Std: The standard deviation, a measure of the spread of the data.
Min: The minimum value in the data.
25%: The 25th percentile value.
50% (median): The median (50th percentile) value.
75%: The 75th percentile value.
Max: The maximum value in the data.
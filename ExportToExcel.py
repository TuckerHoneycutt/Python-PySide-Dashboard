# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:23:00 2024

@author: kayla.green
"""

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, PieChart, ScatterChart, Reference, Series

def plot_chart_in_excel(df, xaxis, yaxis, charttitle="", charttype = "Scatter", file_name="output_with_chart.xlsx", sheet_name="Sheet1"):
    """
    Creates an Excel workbook with a Line chart based on the DataFrame.
    
    Parameters:
    - df: pandas DataFrame to be plotted
    - file_name: name of the output Excel file (default "output_with_chart.xlsx")
    - sheet_name: name of the Excel sheet to write data to (default "Sheet1")
    """
    
    # Create an Excel writer object
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        # Write the DataFrame to Excel
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Get the workbook and sheet objects
        workbook = writer.book
        sheet = workbook[sheet_name]
        
        if charttype == "Line":
            chart = LineChart()
        elif charttype == "Scatter":
            chart = ScatterChart()
        elif charttype == "Pie":
            chart = PieChart()
            
        chart.title = charttitle
        chart.style = 13  # Set style (optional)
        chart.x_axis.title = xaxis
        chart.y_axis.title = yaxis
        
        # Define the data range for the chart
        startRow = df.index[0]+1
        x_index = df.columns.get_loc(xaxis)+1
        y_index = df.columns.get_loc(yaxis)+1
        
        print(x_index)
        print(y_index)
        
        if charttype == "Line":
            data = Reference(sheet, min_col=x_index, min_row=startRow, max_col=y_index, max_row=startRow + len(df))
            chart.add_data(data, titles_from_data=True)
            
            # Define the categories for the x-axis (Year)
            categories = Reference(sheet, min_col=x_index, min_row=startRow, max_row=startRow + len(df))
            chart.set_categories(categories)
        elif charttype == "Scatter":
            # Select data for the scatter plot
            x_values = Reference(sheet, min_col=x_index, min_row=startRow, max_row=startRow + len(df))  # X-axis values
            y_values = Reference(sheet, min_col=y_index, min_row=startRow, max_row=startRow + len(df))  # Y-axis values

            # Create a Series object for the scatter plot and add data
            series = Series(y_values, x_values, title="Data Series")
            chart.series.append(series)
            
        elif charttype == "Pie":
            # Select data for the pie chart
            data = Reference(sheet, min_col=x_index, min_row=startRow, max_col=y_index, max_row=startRow + len(df))  # Y-axis values (numeric)
            chart.add_data(data, titles_from_data=True)

        # Define the categories/Series
        categories = Reference(sheet, min_col=x_index, min_row=startRow, max_row=startRow + len(df))
        chart.set_categories(categories)
        
        # Create a chart sheet and add the chart to it
        chart_sheet = workbook.create_chartsheet()
        chart_sheet.add_chart(chart)
        
    workbook.save(file_name)
    print(f"Excel file '{file_name}' has been saved with the chart.")
    workbook.close()

# Example usage
# Creating a sample DataFrame
data = {
    'Year': [2020, 2021, 2022, 2023, 2024],
    'Sales': [150, 200, 250, 300, 350],
    'Profit': [30, 50, 60, 70, 90]
}
df = pd.DataFrame(data)

# Call the function to save DataFrame and plot to Excel
plot_chart_in_excel(df, 'Year', 'Sales', 'Year vs Sales', file_name="sales_and_profit_chart.xlsx", sheet_name="Sheet1")

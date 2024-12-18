import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math
import CoordinateCalculator as CC
import TimeCalculator as TC

class DataFrameGrapher:
    def __init__(self, root):
        self.root = root
        self.root.title("DataFrame Grapher")
        self.df = None  # Initialize DataFrame to None

        # Create Matplotlib figure and axis
        self.fig = None
        self.ax = None

        self._createMenuBar()
        self.create_widgets()


    def _createMenuBar(self):
        # Create a menu bar
        menu_bar = tk.Menu(self.root)
        # Create the Options menu
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Settings")
        options_menu.add_command(label="Preferences")
        menu_bar.add_cascade(label="Options", menu=options_menu)

        # Create the Edit menu
        # tool_menu = tk.Menu(menu_bar, tearoff=0)
        # tool_menu.add_command(label="Time Conversions", command = TC.CreateTimeConversionWindow)
        # tool_menu.add_command(label="Coordinate Conversion", command = CC.CreatePositionConversionWindow)
        # menu_bar.add_cascade(label="Tools", menu=tool_menu)

        # Create the Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        help_menu.add_command(label="How To Guide")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Display the menu bar
        self.root.config(menu=menu_bar)

    def create_widgets(self):
        # Load button
        load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        load_button.place(x=15, y=10)

        # Chart type selection
        self.chart_type_label = tk.Label(self.root, text="Select Chart Type:")
        self.chart_type_label.place(x=15, y=50)

        self.chart_type = tk.StringVar(value="Pie")  # Default selection
        chart_types = [("Scatter", "Scatter"), ("Bar", "Bar"), ("Line", "Line"), ("Pie", "Pie")]

        for text, value in chart_types:
            rb = tk.Radiobutton(self.root, text=text, variable=self.chart_type, value=value)
            rb.place(x=120 + (chart_types.index((text, value)) * 70), y=50)

        # Plot and export buttons
        self.export_button = tk.Button(self.root, text="Export to Excel", command=self.export_to_excel, state="disabled")
        self.export_button.place(x=580, y=10)

        # Labels for axis selection
        axis_labels = ['X-Axis', 'Y-Axis', 'Series By']
        self.axis_comboboxes = {}

        for i, label in enumerate(axis_labels):
            lbl = ttk.Label(self.root, text=label)
            lbl.place(x=15 + (i * 215), y=90)
            combobox = ttk.Combobox(self.root, values=[])
            combobox.place(x=65 + (i * 215), y=90)
            self.axis_comboboxes[label] = combobox

    def load_file(self):
        plot_button = tk.Button(self.root, text="New Plot Graph", command=self.plot_graph)
        plot_button.place(x=80, y=10)

        file_path = filedialog.askopenfilename()
        if file_path.endswith((".xlsx", ".csv")):
            self.df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            print(f"{'Excel' if file_path.endswith('.xlsx') else 'CSV'} loaded successfully!")
            self.update_comboboxes()
        else:
            messagebox.showerror("File Error", "Please select a valid Excel or CSV file.")

    def update_comboboxes(self):
        # Populate comboboxes with DataFrame columns
        filecols = self.df.columns.tolist()
        for combobox in self.axis_comboboxes.values():
            combobox['values'] = filecols

    def plot_graph(self):
        if self.df is None:
            print("No DataFrame loaded. Please load a CSV file first.")
            return

        # Update Plot
        Update_plot_button = tk.Button(self.root, text="Update Plot Graph", command=self.plot_graph_update)
        Update_plot_button.place(x=190, y=10)

        # Access selected values
        Xcol = self.axis_comboboxes['X-Axis'].get()
        Ycol = self.axis_comboboxes['Y-Axis'].get()
        groupcol = self.axis_comboboxes['Series By'].get()

        # Create Matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100)


        # Grouping and plotting logic
        if groupcol:
            grouped = self.df.groupby(groupcol)
            chart_type = self.chart_type.get()
            if chart_type  == "Pie":
                x = len(grouped)
                sqrt = math.sqrt(x)
                if int(sqrt) < sqrt:
                    sqrt = sqrt + 1

                sqrt = int(sqrt)
                i = (sqrt*100) + (sqrt*10) + 1

                for name, group in grouped:
                    self.ax = self.fig.add_subplot(i)
                    self.plot_group(self.ax, group, Xcol, Ycol, name)
                    i = i + 1
            else:
                self.ax = self.fig.add_subplot(111)
                for name, group in grouped:
                    self.plot_group(self.ax, group, Xcol, Ycol, name)
                self.fig.legend()
        else:
            self.ax = self.fig.add_subplot(111)
            self.plot_group(self.ax, self.df, Xcol, Ycol)

        # Create and display Matplotlib canvas
        self.show_canvas(self.fig)

    def plot_graph_update(self):
        # Access selected values
        Xcol = self.axis_comboboxes['X-Axis'].get()
        Ycol = self.axis_comboboxes['Y-Axis'].get()
        groupcol = self.axis_comboboxes['Series By'].get()

        # Create Matplotlib figure
        fig = self.fig

        # Grouping and plotting logic
        if groupcol:
            grouped = self.df.groupby(groupcol)
            chart_type = self.chart_type.get()
            if chart_type  == "Pie":
                x = len(grouped)
                sqrt = math.sqrt(x)
                if int(sqrt) < sqrt:
                    sqrt = sqrt + 1

                sqrt = int(sqrt)
                i = (sqrt*100) + (sqrt*10) + 1

                for name, group in grouped:
                    ax = fig.add_subplot(i)
                    self.plot_group(ax, group, Xcol, Ycol, name)
                    i = i + 1
            else:
                ax = self.fig.add_subplot(111)
                for name, group in grouped:
                    self.plot_group(ax, group, Xcol, Ycol, name)
                self.fig.legend()
        else:
            self.ax = self.fig.add_subplot(111)
            self.plot_group(self.ax, self.df, Xcol, Ycol)

        # Create and display Matplotlib canvas
        self.show_canvas(fig)

    def show_canvas(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(x=5, y=150)

        # Add Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.root, pack_toolbar=False)
        toolbar.place(x=5, y=140)

    def plot_group(self, ax, group, Xcol, Ycol, label=None):
        chart_type = self.chart_type.get()
        if chart_type == "Line":
            ax.plot(group[Xcol], group[Ycol], label=label)
        elif chart_type == "Bar":
            ax.bar(group[Xcol], group[Ycol], label=label)
        elif chart_type == "Scatter":
            ax.scatter(group[Xcol], group[Ycol], label=label)
        elif chart_type == "Pie":
            relative_counts = group[Xcol].value_counts(normalize=True)
            ax.pie(relative_counts, labels=relative_counts.index.tolist(),
                   autopct='%1.1f%%', shadow=True, startangle=140)


    def export_to_excel(self):
        # Placeholder for the export functionality
        print("Export functionality is not yet implemented.")

def CreateSimplePlottingWindow():
    plotroot = tk.Tk()
    windowGeom = '700x600'
    plotroot.geometry(windowGeom)
    DataFrameGrapher(plotroot)
    plotroot.mainloop()

    plotroot = tk.Tk()
    windowGeom = '700x600'
    plotroot.geometry(windowGeom)
    DataFrameGrapher(plotroot)
    plotroot.mainloop()

if __name__ == "__main__":
    CreateSimplePlottingWindow()

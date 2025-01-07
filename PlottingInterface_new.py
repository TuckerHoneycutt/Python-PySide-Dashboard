import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QCheckBox, QGridLayout, QMessageBox,
                             QFileDialog, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette, QScreen
import pandas as pd
from tkinter import filedialog
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCharts import QChart, QChartView, QPieSeries

import WindowConfigFile as wc
import HeaderDictionary as head

class PlottingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCEND - Plotting")

        # Get screen size and set initial window size
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        # Initialize state variables
        self.convert_from_file = False
        self.filename = ""
        self.new_filename = ""
        self.current_from_type = None
        self.df = pd.DataFrame()

        # Create main widget with horizontal layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_horizontal = QHBoxLayout(main_widget)
        main_horizontal.setSpacing(0)
        main_horizontal.setContentsMargins(0, 0, 0, 0)

        # Create and add sidebar
        sidebar = self.create_sidebar()
        main_horizontal.addWidget(sidebar)

        # Create scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1a1a1a;
            }
            QScrollBar:vertical {
                background-color: #1a1a1a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #3d3d3d;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Create content widget
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(20)

        scroll.setWidget(content_widget)
        main_horizontal.addWidget(scroll)

        # Setup the main conversion interface
        self.setup_conversion_interface()

    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #1f2937;")
        sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        # Add logo or title
        title = QLabel("ASCEND")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold; padding: 20px;")
        sidebar_layout.addWidget(title)

        # Create a button group to ensure only one button can be checked at a time
        self.button_group = []

        # Add conversion type buttons
        plot_types = ["Scatter/Line", "Bar", "Pie"]
        for plot_types in plot_types:
            btn = wc.SidebarButton(plot_types)
            btn.clicked.connect(lambda checked, t=plot_types: self.handle_from_type_change(t))
            sidebar_layout.addWidget(btn)
            self.button_group.append(btn)

        # Select first button by default
        if self.button_group:
            self.button_group[0].setChecked(True)
            self.current_from_type = plot_types[0]

        # Add stretch to push buttons to top
        sidebar_layout.addStretch()

        return sidebar

    def handle_from_type_change(self, from_type):
        # Update current from type
        self.current_from_type = from_type

        # Update button states
        for btn in self.button_group:
            btn.setChecked(btn.text() == from_type)

        # Update the conversion interface
        self.update_conversion_interface()

    def setup_conversion_interface(self):
        
        # File conversion checkbox
        file_layout = QHBoxLayout()
        self.file_check = QCheckBox("Convert from file")
        self.file_check.setStyleSheet("""
            QCheckBox {
                color: white;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #2563eb;
                border: 2px solid #2563eb;
                border-radius: 4px;
            }
        """)
        self.file_check.stateChanged.connect(self.load_file)
        file_layout.addWidget(self.file_check)
        file_layout.addStretch()
        self.content_layout.addLayout(file_layout)
        
        # Converting From heading (static display)
        label_layout = QHBoxLayout()
        self.from_type_label = QLabel()
        self.from_type_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px 0;
        """)
        label_layout.addWidget(self.from_type_label)

        self.date_combo = wc.ModernComboBox()
        self.date_combo.addItems(list(head.Date_dict.keys()))
        self.date_combo.currentIndexChanged.connect(self.update_comboboxes)

        #file_layout.addWidget(ref_label, 0, 0)
        label_layout.addWidget(self.date_combo)
        self.date_combo.hide()
        self.content_layout.addLayout(label_layout)
        
        # Input section
        input_layout = QGridLayout()
        self.input_labels = []
        self.input_combos = []

        for i in range(4):
            label = QLabel()
            label.setStyleSheet("color: white; font-weight: 500;")
            combo = wc.ModernComboBox()

            input_layout.addWidget(label, i, 0)
            input_layout.addWidget(combo, i, 1)

            self.input_labels.append(label)
            self.input_combos.append(combo)

            label.hide()
            combo.hide()

        self.content_layout.addLayout(input_layout)

        # Convert button
        convert_btn = QPushButton("Plot")
        convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 40px;
                font-size: 16px;
                font-weight: 600;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        convert_btn.clicked.connect(self.perform_plot)
        self.content_layout.addWidget(convert_btn, alignment=Qt.AlignCenter)

        # Initialize the interface with the default from type
        self.update_conversion_interface()

    def update_conversion_interface(self):
        # Update the from type display
        self.from_type_label.setText(f"Plot Type: {self.current_from_type}")

        # Update the fields
        self.update_comboboxes()
   
    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path.endswith((".xlsx", ".csv")):
            self.df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            print(f"{'Excel' if file_path.endswith('.xlsx') else 'CSV'} loaded successfully!")
            self.update_comboboxes()
        else:
            QMessageBox.warning(self, "File Error", "Please select a valid Excel or CSV file.")

    def update_comboboxes(self):
        # Populate comboboxes with DataFrame columns
        filecols = [''] + self.df.columns.tolist()
        
        for i, label_text in enumerate(self.input_labels):
            self.input_labels[i].hide()
            self.input_combos[i].hide()
            
        if "Scatter" in self.current_from_type or "Line" in self.current_from_type:
            input_fields  = ['X-Axis', 'Y-Axis', 'Z-Axis', 'Series By']
        elif "Bar" in self.current_from_type:
            input_fields  = ['X-Axis', 'Y-Axis', 'Series By']
        elif "Pie" in self.current_from_type:
            input_fields  = ['X-Axis', 'Series By']
        else:
            input_fields  = []
            
        for i, label_text in enumerate(input_fields):
            self.input_labels[i].setText(label_text)
            self.input_labels[i].show()
            self.input_combos[i].show()

        for combobox in self.input_combos:
            combobox.addItems(filecols)
 
    def perform_plot(self, ChartType = "Count"):
        # Create a QVBoxLayout
        layout = QVBoxLayout()
        if "Scatter" in self.current_from_type or "Line" in self.current_from_type:
            self.plot_widget = pg.PlotWidget()
            x = self.input_combos[0].currentText()
            y = self.input_combos[1].currentText()
            z = self.input_combos[2].currentText()
            groupBy = self.input_combos[3].currentText()
            
            if ChartType == "Scatter":
                self.plot_widget.plot(self.df[x], self.df[y], pen=None, symbol='o', symbolSize=5, symbolBrush='r') 
            elif ChartType == "Line":
                self.plot_widget.plot(self.df[x], self.df[y], pen='r')  # 'r' is for red color

        elif "Bar" in self.current_from_type:
            x = self.input_combos[0].currentText()
            y = self.input_combos[1].currentText()
            groupBy = self.input_combos[2].currentText()
            
            self.plot_widget = pg.plot()
            bargraph = pg.BarGraphItem(x = self.df[x], height = self.df[y], width = 0.6, brush ='g')
            self.plot_widget.addItem(bargraph)
            
        elif "Pie" in self.current_from_type:
           x = self.input_combos[0].currentText()
           groupBy = self.input_combos[1].currentText()

           self.series = QPieSeries()
           # print(x)
           # print(groupBy)
           
           # # Plotting a pie chart using matplotlib (since PyQtGraph doesn't have native support)
           if groupBy == "":
               pie_data = self.df.groupby(x)
           else:
               pie_data = self.df.groupby(groupBy)
           
           if ChartType == "Count":
               total = len(self.df[x])
               self.series = QPieSeries()
               for name, group in pie_data:
                   self.series.append(str(name), group[x].count()/total)
           elif ChartType == "Sum": 
               total = self.df[x].sum()
               self.series = QPieSeries()
               for name, group in pie_data:
                   self.series.append(str(name), group[x].sum()/total)
                   
           self.chart = QChart()
           self.chart.addSeries(self.series)
           self.chart.setTitle(str(x))
           self._chart_view = QChartView(self.chart)
           self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

           self.setCentralWidget(self._chart_view)

        layout.addWidget(self.plot_widget)
        self.content_layout.addLayout(layout)

def main():
    app = QApplication(sys.argv)

    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Set application style
    app.setStyle("Fusion")

    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#1a1a1a"))
    palette.setColor(QPalette.WindowText, QColor("#ffffff"))
    palette.setColor(QPalette.Base, QColor("#2d2d2d"))
    palette.setColor(QPalette.AlternateBase, QColor("#333333"))
    palette.setColor(QPalette.ToolTipBase, QColor("#ffffff"))
    palette.setColor(QPalette.ToolTipText, QColor("#ffffff"))
    palette.setColor(QPalette.Text, QColor("#ffffff"))
    palette.setColor(QPalette.Button, QColor("#2d2d2d"))
    palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
    palette.setColor(QPalette.BrightText, QColor("#ff0000"))
    palette.setColor(QPalette.Link, QColor("#2563eb"))
    palette.setColor(QPalette.Highlight, QColor("#2563eb"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = PlottingWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

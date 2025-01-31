import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QCheckBox, QGridLayout, QMessageBox,
                             QFileDialog, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette, QScreen
import pandas as pd
import json
import importlib
import inspect

import CoordinateTransformations as CT
import WindowConfigFile as wc
import HeaderDictionary as head

def import_module_from_file(file_name):
    module_name = os.path.splitext(file_name)[0]
    return importlib.import_module(module_name)

def list_Conversion_files_in_folder(folder_path):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)
        
        # Word to filter by
        word = "Transformations"
        
        # Filter the list to include only names that contain the word
        filtered_names = [name for name in files if word in name and 'Coordinate' not in name and 'Time' not in name]
        filtered_names = [name.replace("Transformations.py", '') for name in filtered_names]
        
        return filtered_names
    except Exception as e:
        return str(e) 
        
class CoordinateConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCEND - Position Conversions")

        # Get screen size and set initial window size
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.8))

        # Initialize state variables
        self.convert_from_file = False
        self.filename = ""
        self.new_filename = ""
        self.current_from_type = None

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

        # Create a button group to ensure only one button can be checked at a Position
        self.button_group = []

        # Get the current folder path
        current_folder_path = os.path.dirname(os.path.abspath(__file__))
        files = list_Conversion_files_in_folder(current_folder_path)

        for Conversion_type in files:
            btn = wc.SidebarButton(Conversion_type)
            btn.clicked.connect(lambda checked, t=Conversion_type: self.handle_from_type_change(t))
            sidebar_layout.addWidget(btn)
            self.button_group.append(btn)

        # Select first button by default
        if self.button_group:
            self.button_group[0].setChecked(True)
            self.current_from_type = Conversion_type[0]

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
        
        self.file_check.stateChanged.connect(self.handle_file_conversion)
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
        self.content_layout.addLayout(label_layout)
        
        # Input section
        input_layout = QGridLayout()
        self.input_fields = wc.ModernLineEdit()
        input_layout.addWidget(self.input_fields, 0, 1)
        self.input_fields.hide()
        
        self.input_combos = wc.ModernComboBox()
        input_layout.addWidget(self.input_combos, 0, 2)
        self.input_combos.hide()
        
        self.input_labels = wc.ModernComboBox()
        input_layout.addWidget(self.input_labels, 0, 0)
        self.input_labels.hide()
    
        self.content_layout.addLayout(input_layout)

        # Converting To section
        to_layout = QHBoxLayout()
        to_label = QLabel("Convert To:")
        to_label.setStyleSheet("color: white; font-weight: bold;")
        to_layout.addWidget(to_label)

        self.content_layout.addLayout(to_layout)
        
        
        # Output section
        output_layout = QGridLayout()

        self.output_labels = wc.ModernComboBox()
        self.output_fields = wc.ModernLineEdit()
        self.output_fields.setReadOnly(True)

        output_layout.addWidget(self.output_labels, 0, 0)
        output_layout.addWidget(self.output_fields, 0, 1)

        self.content_layout.addLayout(output_layout)

        # Convert button
        convert_btn = QPushButton("Convert")
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
        convert_btn.clicked.connect(self.perform_conversion)
        self.content_layout.addWidget(convert_btn, alignment=Qt.AlignCenter)

        # Initialize the interface with the default from type
        self.update_conversion_interface()

    def update_conversion_interface(self):
        # Update the from type display
        self.from_type_label.setText(f"Converting from: {self.current_from_type}")

        # Update the fields
        self.update_fields()
        
    # Function to get unique words separated by '2'
    def get_unique_words(self, functions):
        words = set()
        for func_name, _ in functions:
            parts = func_name.split('2')
            words.update(parts)
        return words
    
    def update_fields(self):
        try:
            self.module = import_module_from_file(self.current_from_type + "Transformations.py")
        except:
            self.module = ''

        functions = inspect.getmembers(self.module, inspect.isfunction)

        self.input_labels.clear()
        self.input_labels.addItems(self.get_unique_words(functions))
        self.input_labels.show()
        
        self.output_labels.clear()
        self.output_labels.addItems(self.get_unique_words(functions))
        self.output_labels.show()
        
        if self.convert_from_file:
            columns = self.df.columns.tolist()

            self.input_fields.hide()
            self.input_combos.clear()
            self.input_combos.addItems(columns)
            self.input_combos.show()
            
        else:
            self.input_fields.show()
            self.input_combos.hide()

        if self.convert_from_file == False:
            self.output_fields.show()

        else:
            # Hide unused output fields
            self.output_fields.hide()
                
    def handle_file_conversion(self, state):
        self.convert_from_file = bool(state)
        if self.convert_from_file:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Select Input File", "", "CSV Files (*.csv);;All Files (*.*)")
            if filename:
                self.filename = filename
                self.new_filename = os.path.splitext(filename)[0] + "_converted" + os.path.splitext(filename)[1]

                try:
                    self.df = pd.read_csv(filename)

                except Exception as e:
                    QMessageBox.warning(self, "File Error", f"Error reading file: {str(e)}")
                    self.file_check.setChecked(False)
                    self.convert_from_file = False
        
        self.update_fields()

    def convert_single(self):
        from_type = self.input_labels.currentText()
        to_type = self.output_labels.currentText()
        
        try:
            # Regular input collection for other types
            if self.input_fields.isVisible():
                value = self.input_fields.text().strip()
                if not value:
                    QMessageBox.warning(self, "Error", "Please fill in all visible input fields.")
                    return

            # Perform conversion
            results = self.perform_Position_conversion(from_type, to_type, value)

            print(results)
            # Update output fields
            if self.output_fields.isVisible():
                if type(results) == pd.Series:
                    result = results.tolist()
                    
                if type(results) == list:
                    if len(results) == 1:
                        result = result[0]

                self.output_fields.setText(str(results))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Conversion failed: {str(e)}")

    def convert_file(self):
  
        to_type = self.to_combo.currentText()

        try:
            # Regular input collection for other types
            input_values = []
            for i, combo in enumerate(self.input_combos):
                if combo.isVisible():
                    col = combo.currentText()
                    value = self.df[col]
                    key = self.input_labels[i].text()
                    
                    if key in self.user_data.keys():
                        if col not in self.user_data[key]:
                            head.UpdateHeaders('Position_Time_Headers.json', self.user_data, key, col)
                    else:
                        head.UpdateHeaders('Position_Time_Headers.json', self.user_data, key, col)
                        
                    input_values.append(value)
                else:
                    input_values.append(None)


            self.df.to_csv(self.new_filename, index=False)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Conversion failed: {str(e)}")

    def perform_Position_conversion(self, from_type, to_type, input_values):
        # Helper function to perform the actual Position conversion
        print(input_values)
        
        function_name_to_call = from_type+"2"+to_type
        print(function_name_to_call)
        if hasattr(self.module, function_name_to_call):
            function_to_call = getattr(self.module, function_name_to_call)
            result = function_to_call(input_values)
        else:
            result = None
            
        return result

    def perform_conversion(self):
        if self.convert_from_file:
            self.convert_file()
        else:
            self.convert_single()

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

    window = CoordinateConverterWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

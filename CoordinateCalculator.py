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

import CoordinateTransformations as CT
import WindowConfigFile as wc
import HeaderDictionary as head

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

        # Add conversion type buttons
        Position_types = list(head.Position_dict.keys())
        for Position_type in Position_types:
            btn = wc.SidebarButton(Position_type)
            btn.clicked.connect(lambda checked, t=Position_type: self.handle_from_type_change(t))
            sidebar_layout.addWidget(btn)
            self.button_group.append(btn)

        # Select first button by default
        if self.button_group:
            self.button_group[0].setChecked(True)
            self.current_from_type = Position_types[0]

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

        self.unit_combo = wc.ModernComboBox()
        self.unit_combo.addItems(['Degrees', 'Radians', 'Deg:Min:Sec'])
        self.unit_combo.currentIndexChanged.connect(self.update_fields)

        label_layout.addWidget(self.unit_combo)
        self.unit_combo.hide()
        self.content_layout.addLayout(label_layout)
        
        # Input section
        input_layout = QGridLayout()
        self.input_labels = []
        self.input_fields = []
        self.input_combos = []

        for i in range(4):
            label = QLabel()
            label.setStyleSheet("color: white; font-weight: 500;")
            field = wc.ModernLineEdit()
            combo = wc.ModernComboBox()

            input_layout.addWidget(label, i, 0)
            input_layout.addWidget(field, i, 1)
            input_layout.addWidget(combo, i, 2)

            self.input_labels.append(label)
            self.input_fields.append(field)
            self.input_combos.append(combo)

            label.hide()
            field.hide()
            combo.hide()

        self.content_layout.addLayout(input_layout)

        # Reference Position section
        ref_layout = QGridLayout()
        self.ref_BigLabel = QLabel("Reference Position:")
        self.ref_BigLabel.setStyleSheet("color: white; font-weight: bold;")
        self.ref_combo = wc.ModernComboBox()
        universal_frames = {key: value for key, value in head.PosFrame_dict.items() if value == "Universal"}
        self.ref_combo.addItems(universal_frames)
        self.ref_combo.currentIndexChanged.connect(self.handle_reference_change)

        ref_layout.addWidget(self.ref_BigLabel, 0, 0)
        ref_layout.addWidget(self.ref_combo, 0, 1)
        
        self.ref_labels = []
        self.ref_fields = []
        self.ref_combos = []

        for i in range(4):
            field = wc.ModernLineEdit()
            combo = wc.ModernComboBox()
            label = QLabel()
            
            ref_layout.addWidget(label, i+1, 0)
            ref_layout.addWidget(field, i+1, 1)
            ref_layout.addWidget(combo, i+1, 2)
            
            self.ref_fields.append(field)
            self.ref_combos.append(combo)
            self.ref_labels.append(label)

            field.hide()
            combo.hide()
            label.hide()
            
        self.ref_BigLabel.hide()
        
        self.content_layout.addLayout(ref_layout)
        
        # Converting To section
        to_layout = QHBoxLayout()
        to_label = QLabel("Convert To:")
        to_label.setStyleSheet("color: white; font-weight: bold;")
        self.to_combo = wc.ModernComboBox()
        self.to_combo.addItems(list(head.Position_dict.keys()))
        self.to_combo.currentIndexChanged.connect(self.update_fields)
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_combo)
        
        self.unit_combo2 = wc.ModernComboBox()
        self.unit_combo2.addItems(['Degrees', 'Radians', 'Deg:Min:Sec'])
        self.unit_combo2.currentIndexChanged.connect(self.update_fields)
        self.unit_combo2.hide()
        to_layout.addWidget(self.unit_combo2)

        self.content_layout.addLayout(to_layout)
        
        
        # Output section
        output_layout = QGridLayout()
        self.output_labels = []
        self.output_fields = []

        for i in range(4):
            label = QLabel()
            label.setStyleSheet("color: white; font-weight: 500;")
            field = wc.ModernLineEdit()
            field.setReadOnly(True)

            output_layout.addWidget(label, i, 0)
            output_layout.addWidget(field, i, 1)

            self.output_labels.append(label)
            self.output_fields.append(field)

            label.hide()
            field.hide()

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

    def update_fields(self):
        
        input_fields  = head.Position_dict
        labels = input_fields.get(self.current_from_type, [])
        # Load existing data from file
        try:
            with open('Position_Time_Headers.json', 'r') as file:
                self.user_data = json.load(file)
        except FileNotFoundError:
            self.user_data = {}
            
        if self.current_from_type == "LLA":
            self.unit_combo.show()
        else:
            self.unit_combo.hide()

        for i, label_text in enumerate(labels):
            if i < len(self.input_labels):
                self.input_labels[i].setText(label_text)
                self.input_labels[i].show()
                
                if self.convert_from_file:
                    columns = self.df.columns.tolist()

                    self.input_fields[i].hide()
                    combo = self.input_combos[i]
                    combo.clear()
                    combo.addItems(columns)
                    if label_text in self.user_data.keys():
                        common_values = list(filter(lambda x: x in columns, self.user_data[label_text]))
                        if len(common_values)>0:
                            combo.setCurrentText(common_values[0])
                    combo.show()
                    
                else:
                    self.input_fields[i].show()
                    self.input_combos[i].hide()

        # Hide unused input fields
        for i in range(len(labels), len(self.input_labels)):
            self.input_labels[i].hide()
            self.input_fields[i].hide()
            self.input_combos[i].hide()

        # Update output fields based on selected "to" type
        output_fields = head.Position_dict

        labels = output_fields.get(self.to_combo.currentText())
        if self.to_combo.currentText() == "LLA":
            self.unit_combo2.show()
        else:
            self.unit_combo2.hide()
        
        if self.convert_from_file == False:
            for i, label_text in enumerate(labels):
                if i < len(self.output_labels):
                    self.output_labels[i].setText(label_text)
                    self.output_labels[i].show()
                    self.output_fields[i].show()

            # Hide unused output fields
            for i in range(len(labels), len(self.output_labels)):
                self.output_labels[i].hide()
                self.output_fields[i].hide()
        else:
            # Hide unused output fields
            for i in range(len(self.output_labels)):
                self.output_labels[i].hide()
                self.output_fields[i].hide()
                
        self.update_reference_fields()

    def update_reference_fields(self):
        needs_reference = False

        # Show reference fields only for specific conversions
        if (head.PosFrame_dict[self.current_from_type] == "Local" or 
            head.PosFrame_dict[self.to_combo.currentText()] == "Local"):
            
            needs_reference = True

        if needs_reference:
            self.ref_BigLabel.show()
            self.ref_combo.show()
            ref_type = self.ref_combo.currentText()            
            reference_labels = head.Position_dict[ref_type]

            for i, label in enumerate(reference_labels):
                if i < len(self.ref_fields):
                    self.ref_fields[i].show()
                    self.ref_labels[i].show()
                    self.ref_labels[i].setText(label)

            # Hide unused reference fields
            for i in range(len(reference_labels), len(self.ref_fields)):
                self.ref_fields[i].hide()
                self.ref_labels[i].hide()
        else:
            self.ref_BigLabel.hide()
            self.ref_combo.hide()
            for field in self.ref_fields:
                field.hide()
                
            for label in self.ref_labels:
                label.hide()
                
    def handle_reference_change(self):
        self.update_reference_fields()

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
        to_type = self.to_combo.currentText()

        try:
            # Regular input collection for other types
            input_values = []
            for field in self.input_fields:
                if field.isVisible():
                    value = field.text().strip()
                    if not value:
                        QMessageBox.warning(self, "Error", "Please fill in all visible input fields.")
                        return
                    input_values.append(value)
                else:
                    input_values.append(None)

            # Collect reference values if needed
            ref_values = []
            for field in self.ref_fields:
                if field.isVisible():
                    value = field.text().strip()
                    if not value:
                        QMessageBox.warning(self, "Error", "Please fill in all visible reference fields.")
                        return
                    ref_values.append(value)
                else:
                    ref_values.append(None)

            # Perform conversion
            results = self.perform_Position_conversion(input_values, ref_values, to_type)

            # Handle different numbers of results
            if not isinstance(results, (list, tuple)):
                results = [results]

            # Update output fields
            for i, (field, result) in enumerate(zip(self.output_fields, results)):
                if field.isVisible():
                    if type(result) == pd.Series:
                        result = result.tolist()
                        
                    if type(result) == list:
                        if len(result) == 1:
                            result = result[0]

                    field.setText(str(result))

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

            # Collect reference values if needed
            ref_values = []
            for field in self.ref_fields:
                if field.isVisible():
                    value = field.text().strip()
                    if not value:
                        QMessageBox.warning(self, "Error", "Please fill in all visible reference fields.")
                        return
                    ref_values.append(value)
                else:
                    ref_values.append(None)

            # Perform conversion
            results = self.perform_Position_conversion(input_values, ref_values, to_type)

            labels = head.Position_dict.get(self.to_combo.currentText(), [])

            for i, (field, result) in enumerate(zip(labels, results)):
                self.df[field] = result
            
            self.df.to_csv(self.new_filename, index=False)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Conversion failed: {str(e)}")

    def perform_Position_conversion(self, input_values, ref_values, to_type):
        # Helper function to perform the actual Position conversion
        if len(input_values) < 4:
            input_values.extend([None] * (4 - len(input_values)))

        return CT.MasterCoordinatesConvert(
            self.current_from_type, to_type,
            input1var=input_values[0],
            input2var=input_values[1],
            input3var=input_values[2],
            input4var=input_values[3] if len(input_values) > 3 else None,
            input5var=input_values[4] if len(input_values) > 4 else None,
            refput1var=ref_values[0] if ref_values else None,
            refput2var=ref_values[1] if len(ref_values) > 1 else None,
            refput3var=ref_values[2] if len(ref_values) > 2 else None,
            refput4var=ref_values[3] if len(ref_values) > 3 else None,
            units = self.unit_combo.currentText(), 
            CoordanateRef = self.ref_combo.currentText(), 
            CoordanateUnits = self.unit_combo2.currentText(), 
            returnUnits = self.unit_combo2.currentText()
        )

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

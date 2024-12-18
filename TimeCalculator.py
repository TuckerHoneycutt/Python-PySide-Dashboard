import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QCheckBox, QGridLayout, QMessageBox,
                             QFileDialog, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette, QScreen
import pandas as pd
import numpy as np
import calendar
from datetime import datetime, timedelta
from operator import attrgetter

import TimeTransformations as TT

# Modern UI Components
class ModernComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 8px 15px;
                min-width: 150px;
                font-weight: 500;
            }
            QComboBox:hover, QComboBox:focus {
                border-color: #2563eb;
                background-color: #333333;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #2563eb;
                outline: none;
                border-radius: 8px;
                padding: 5px;
            }
        """)

class ModernLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                padding: 8px 15px;
                min-width: 150px;
                font-weight: 500;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background-color: #333333;
            }
            QLineEdit:disabled {
                background-color: #252525;
                color: #666;
            }
        """)

class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                text-align: left;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:checked {
                background-color: #1d4ed8;
            }
        """)
        self.setCheckable(True)
        self.setMinimumHeight(50)

class TimeConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCEND - Time Conversions")

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

        # Create a button group to ensure only one button can be checked at a time
        self.button_group = []

        # Add conversion type buttons
        time_types = ["EPOCH", "GPS", "TOD", "SSM", "MCI", "JD", "Int_Date", "Str_Date"]
        for time_type in time_types:
            btn = SidebarButton(time_type)
            btn.clicked.connect(lambda checked, t=time_type: self.handle_from_type_change(t))
            sidebar_layout.addWidget(btn)
            self.button_group.append(btn)

        # Select first button by default
        if self.button_group:
            self.button_group[0].setChecked(True)
            self.current_from_type = time_types[0]

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
        # Converting From heading (static display)
        self.from_type_label = QLabel()
        self.from_type_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px 0;
        """)
        self.content_layout.addWidget(self.from_type_label)

        # Converting To section
        to_layout = QVBoxLayout()
        to_label = QLabel("Convert To:")
        to_label.setStyleSheet("color: white; font-weight: bold;")
        self.to_combo = ModernComboBox()
        self.to_combo.addItems(["EPOCH", "GPS", "TOD", "SSM", "MCI", "JD", "Int_Date", "Str_Date"])
        self.to_combo.currentIndexChanged.connect(self.update_fields)
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_combo)
        self.content_layout.addLayout(to_layout)

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

        # Input section
        input_layout = QGridLayout()
        self.input_labels = []
        self.input_fields = []
        self.input_combos = []

        for i in range(4):
            label = QLabel()
            label.setStyleSheet("color: white; font-weight: 500;")
            field = ModernLineEdit()
            combo = ModernComboBox()

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

        # Reference time section
        ref_layout = QGridLayout()
        ref_label = QLabel("Reference Time:")
        ref_label.setStyleSheet("color: white; font-weight: bold;")
        self.ref_combo = ModernComboBox()
        self.ref_combo.addItems(['JD', 'Int_Date', 'Str_Date'])
        self.ref_combo.currentIndexChanged.connect(self.handle_reference_change)

        ref_layout.addWidget(ref_label, 0, 0)
        ref_layout.addWidget(self.ref_combo, 0, 1)

        self.ref_fields = []
        self.ref_combos = []

        for i in range(4):
            field = ModernLineEdit()
            combo = ModernComboBox()

            ref_layout.addWidget(field, i+1, 0)
            ref_layout.addWidget(combo, i+1, 1)

            self.ref_fields.append(field)
            self.ref_combos.append(combo)

            field.hide()
            combo.hide()

        self.content_layout.addLayout(ref_layout)

        # Output section
        output_layout = QGridLayout()
        self.output_labels = []
        self.output_fields = []

        for i in range(4):
            label = QLabel()
            label.setStyleSheet("color: white; font-weight: 500;")
            field = ModernLineEdit()
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
        # Update input fields based on current from type
        if self.current_from_type == "EPOCH":
            # For epoch, we only show one input field for the timestamp
            self.input_labels[0].setText("Epoch Timestamp")
            self.input_labels[0].show()
            self.input_fields[0].show()
            self.input_combos[0].hide()

            # Hide other input fields
            for i in range(1, len(self.input_labels)):
                self.input_labels[i].hide()
                self.input_fields[i].hide()
                self.input_combos[i].hide()
        else:
            # Regular input collection for other types
            input_fields = {
                "GPS": ["Seconds", "Nanoseconds"],
                "TOD": ["Year", "Julian Date", "Time"],
                "SSM": ["Year", "Julian Date", "Seconds"],
                "MCI": ["Year", "Julian Date", "Count", "Reference Time", "Reference Count"],
                "JD": ["Year", "Julian Date"],
                "Int_Date": ["Year", "Month", "Day"],
                "Str_Date": ["Date String"]
            }

            labels = input_fields.get(self.current_from_type, [])
            for i, label_text in enumerate(labels):
                if i < len(self.input_labels):
                    self.input_labels[i].setText(label_text)
                    self.input_labels[i].show()
                    self.input_fields[i].show()
                    self.input_combos[i].hide()

            # Hide unused input fields
            for i in range(len(labels), len(self.input_labels)):
                self.input_labels[i].hide()
                self.input_fields[i].hide()
                self.input_combos[i].hide()

        # Update output fields based on selected "to" type
        to_type = self.to_combo.currentText()
        output_fields = {
            "EPOCH": ["Nanoseconds"],
            "GPS": ["Seconds", "Nanoseconds"],
            "TOD": ["Year", "Julian Date", "Time"],
            "SSM": ["Year", "Julian Date", "Seconds"],
            "MCI": ["Year", "Julian Date", "Count"],
            "JD": ["Year", "Julian Date"],
            "Int_Date": ["Year", "Month", "Day"],
            "Str_Date": ["Date String"]
        }

        labels = output_fields.get(to_type, [])
        for i, label_text in enumerate(labels):
            if i < len(self.output_labels):
                self.output_labels[i].setText(label_text)
                self.output_labels[i].show()
                self.output_fields[i].show()

        # Hide unused output fields
        for i in range(len(labels), len(self.output_labels)):
            self.output_labels[i].hide()
            self.output_fields[i].hide()

        self.update_reference_fields()

    def update_reference_fields(self):
        to_type = self.to_combo.currentText()

        # Show reference fields only for specific conversions
        needs_reference = (self.current_from_type in ["MCI"] or
                         to_type in ["MCI"])

        if needs_reference:
            self.ref_combo.show()
            ref_type = self.ref_combo.currentText()

            if ref_type == "JD":
                ref_labels = ["Year", "Julian Date"]
            elif ref_type == "Int_Date":
                ref_labels = ["Year", "Month", "Day"]
            else:  # Str_Date
                ref_labels = ["Date String"]

            for i, label in enumerate(ref_labels):
                if i < len(self.ref_fields):
                    self.ref_fields[i].show()
                    self.ref_fields[i].setPlaceholderText(label)

            # Hide unused reference fields
            for i in range(len(ref_labels), len(self.ref_fields)):
                self.ref_fields[i].hide()
        else:
            self.ref_combo.hide()
            for field in self.ref_fields:
                field.hide()

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
                    df = pd.read_csv(filename)
                    columns = df.columns.tolist()

                    # Show combos and hide input fields for visible inputs
                    visible_count = sum(1 for label in self.input_labels if label.isVisible())
                    for i in range(visible_count):
                        self.input_fields[i].hide()
                        combo = self.input_combos[i]
                        combo.clear()
                        combo.addItems(columns)
                        combo.show()
                except Exception as e:
                    QMessageBox.warning(self, "File Error", f"Error reading file: {str(e)}")
                    self.file_check.setChecked(False)
                    self.convert_from_file = False
        else:
            # Hide combos and show input fields
            for i in range(len(self.input_labels)):
                if self.input_labels[i].isVisible():
                    self.input_combos[i].hide()
                    self.input_fields[i].show()

    def convert_single(self):
        to_type = self.to_combo.currentText()

        try:
            # Special handling for epoch input
            if self.current_from_type == "EPOCH":
                epoch_str = self.input_fields[0].text().strip()
                if not epoch_str:
                    QMessageBox.warning(self, "Error", "Please enter an epoch timestamp.")
                    return

                try:
                    epoch_value = float(epoch_str)
                    seconds = int(epoch_value)
                    nanoseconds = int((epoch_value - seconds) * 1e9)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Invalid epoch value. Please enter a valid number.")
                    return

                input_values = [seconds, nanoseconds, None, None]
            else:
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
            results = self.perform_time_conversion(input_values, ref_values, to_type)

            # Handle different numbers of results
            if not isinstance(results, (list, tuple)):
                results = [results]

            # Update output fields
            for i, (field, result) in enumerate(zip(self.output_fields, results)):
                if field.isVisible():
                    field.setText(str(result))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Conversion failed: {str(e)}")

    def perform_time_conversion(self, input_values, ref_values, to_type):
        # Helper function to perform the actual time conversion
        if len(input_values) < 4:
            input_values.extend([None] * (4 - len(input_values)))

        return TT.MasterTimeConvert(
            self.current_from_type, to_type,
            input1var=input_values[0],
            input2var=input_values[1],
            input3var=input_values[2],
            input4var=input_values[3],
            indate=self.ref_combo.currentText(),
            refput1var=ref_values[0] if ref_values else None,
            refput2var=ref_values[1] if len(ref_values) > 1 else None,
            outdate=self.ref_combo.currentText()
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

    window = TimeConverterWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

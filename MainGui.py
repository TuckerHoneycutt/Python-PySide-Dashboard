import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QLabel,
                             QStackedWidget, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QPalette, QColor, QScreen, QGuiApplication

import WindowConfigFile as wc
import TimeCalculator as TC
import PlotingInterface as GI
import CoordinateCalculator as CC

class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                text-align: center;
                font-weight: 500;
                min-width: 40px;
                min-height: 40px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:checked {
                background-color: #1d4ed8;
            }
        """)
        self.setCheckable(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TriVector - ASCEND")
        # Add an Ascend Home button from Kayla

        # Set window to full screen size
        self.showMaximized()

        # Style the window
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {wc.Overall_background};
            }}
            QMenuBar {{
                background-color: #333333;
                color: white;
                padding: 5px;
            }}
            QMenuBar::item:selected {{
                background-color: #2196F3;
            }}
            QMenu {{
                background-color: #333333;
                color: white;
                border: 1px solid #444444;
            }}
            QMenu::item:selected {{
                background-color: #2196F3;
            }}
        """)

        # Create menu bar
        self._create_menu_bar()

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create horizontal layout for sidebar and content
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create and add vertical bar
        vertical_bar = self.create_vertical_bar()
        main_layout.addWidget(vertical_bar)

        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create and add pages
        self.create_pages()

        # Set initial page
        self.stacked_widget.setCurrentIndex(0)

    def create_vertical_bar(self):
        # Create vertical bar widget
        # Needs to add 1 layer deeper and nested Calculator -> Time & Coordinate Claulator & Basic Calculator
        vertical_bar = QFrame()
        vertical_bar.setFixedWidth(60)
        vertical_bar.setStyleSheet("""
            QFrame {
                background-color: #1f2937;
                border-right: 1px solid #374151;
            }
        """)

        # Create vertical layout
        vertical_layout = QVBoxLayout(vertical_bar)
        vertical_layout.setContentsMargins(0, 10, 0, 10)
        vertical_layout.setSpacing(5)

        # Add logo or title
        title = QLabel("AS")
        title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        vertical_layout.addWidget(title)

        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #374151; margin: 5px 10px;")
        vertical_layout.addWidget(separator)

        # Create vertical bar buttons
        self.home_button = SidebarButton("🏠")
        # Have just 1 Calculator icon instead of multiple different icons . Figure out why that icon color is being changed to black and white
        # Change from clock to calculator
        self.time_button = SidebarButton("⏰")
        # Just Calculator
        # Change from pin to plotting
        self.coord_button = SidebarButton("📍")
        # Add powerpoint creation button
        # Add word document creation button
        # File input into dataframe that persists at the top with conversion dialog for what type of file to convert to and from and have new file the same name with '_imported' at the end of the filename

        # Add tooltips
        self.home_button.setToolTip("Home")
        self.time_button.setToolTip("Time Calculator")
        self.coord_button.setToolTip("Coordinate Calculator")

        # Add buttons to layout
        vertical_layout.addWidget(self.home_button)
        vertical_layout.addWidget(self.time_button)
        vertical_layout.addWidget(self.coord_button)

        # Connect button signals
        self.home_button.clicked.connect(lambda: self.switch_page(0))
        self.time_button.clicked.connect(lambda: self.switch_page(1))
        self.coord_button.clicked.connect(lambda: self.switch_page(2))

        # Add stretch to push buttons to top
        vertical_layout.addStretch()

        return vertical_bar

    def create_pages(self):
        # Create home page
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_layout.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("Welcome to Ascend!!")
        welcome_label.setStyleSheet("""
            color: #333333;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
        """)
        welcome_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(welcome_label)

        # Create time calculator page
        time_page = TC.TimeConverterWindow()

        # Create coordinate calculator page
        coord_page = CC.CoordinateConverterWindow()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(home_page)
        self.stacked_widget.addWidget(time_page)
        self.stacked_widget.addWidget(coord_page)

    def switch_page(self, index):
        # Update button states
        buttons = [self.home_button, self.time_button, self.coord_button]
        for i, button in enumerate(buttons):
            button.setChecked(i == index)

        # Switch to selected page
        self.stacked_widget.setCurrentIndex(index)

    def _create_menu_bar(self):
        menubar = self.menuBar()

        # Options Menu
        options_menu = QMenu("Options", self)
        options_menu.addAction("Settings")
        options_menu.addAction("Preferences")
        menubar.addMenu(options_menu)

        # Tools Menu
        tools_menu = QMenu("Tools", self)
        tools_menu.addAction("Simple Graphs", GI.CreateSimplePlottingWindow)
        menubar.addMenu(tools_menu)

        # Help Menu
        help_menu = QMenu("Help", self)
        help_menu.addAction("About")
        help_menu.addAction("How To Guide")
        menubar.addMenu(help_menu)

def main():
    app = QApplication(sys.argv)

    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Set application-wide font
    app_font = QFont("Segoe UI", 10)
    app.setFont(app_font)

    # Set application style
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

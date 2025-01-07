# -*- coding: utf-8 -*-
"""
Spyder Editor

This script will be used for all Coordanate Conversion as the 
base of the ASCEND tool.
"""
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QLineEdit, QCheckBox, QGridLayout, QMessageBox,
                             QFileDialog, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette, QScreen
import pandas as pd
from tkinter.font import Font

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




entrysize = 130
linespace = 25
columnspace = 20

Overall_background="black" 
Overall_foreground="white"

hide_Entrybox = Overall_background
Unhide_Entrybox = 'white'

GuiFont=('Arial', 10)

def configure_color_style_Entrybox(style, color_name):
    style.theme_use('clam')
    style.configure(f'{color_name}.TEntry',
                    fieldbackground=color_name,
                    background=color_name,
                    foreground='black',
                    insertcolor='black')
    
def configure_color_style_Label(Label):
    Label.config(background=Overall_background, foreground=Overall_foreground)
    
def hide_widgets(self, widget_list):
    for widget in widget_list:
        if type(widget) == list:
            for w in widget:
                w.place_forget()
        else:
            widget.place_forget()
            
def place_widgets(self, combo_list, entry_list, labels, xPlacement, yPlacement, Label_List=[], refchoice = '', useRef = False):
    """Place widgets based on the labels provided."""
    needRefbox = False
    for i, label_text in enumerate(labels):
        if type(label_text) == str:
            if useRef == False: 
                if "Ref" not in label_text and "ref" not in label_text:
                    if i < len(combo_list):
                        if len(Label_List) > 0:
                            Label_List[i].config(text=label_text)
                            Label_List[i].place(x=xPlacement, y=yPlacement)
                            
                        if self.convertFile.get() != 'ConvertFile':
                            entry_list[i].place(x=xPlacement, y=yPlacement + linespace, width=entrysize)
                        else:
                            combo_list[i].place(x=xPlacement, y=yPlacement + linespace, width=entrysize)
                    
                    xPlacement += entrysize + columnspace
                
            if useRef == True:
                if "Ref" in label_text or "ref" in label_text:
                    needRefbox = True
                    if i < len(combo_list):
                        if len(Label_List) > 0:
                            Label_List[i].config(text=label_text)
                            Label_List[i].place(x=xPlacement, y=yPlacement)
                            
                        if self.convertFile.get() != 'ConvertFile':
                            entry_list[i].place(x=xPlacement, y=yPlacement + linespace, width=entrysize)
                        else:
                            combo_list[i].place(x=xPlacement, y=yPlacement + linespace, width=entrysize)
                    
                
                    xPlacement += entrysize + columnspace
        
    if needRefbox == True:
        refchoice.place(x=xPlacement, y=yPlacement + linespace, width=70)
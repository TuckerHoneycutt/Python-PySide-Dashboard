# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 14:45:52 2024

@author: kayla.green
"""

#TrivectorModules
import CoordinateTransformations as CT
import WindowConfigFile as wc
import HeaderDictionary as head
import BasicFunctions as bf

import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox

width=600
height=450
startx = 65
starty_primary = 65
output_y = height/2 + height/10

entrysize = 130
linespace = 25
columnspace = 20

df = pd.DataFrame()

filecols = []

Input_Label_List=[]
Refput_Label_List=[]
Output_Label_List=[]

class DataFramePosCon:
    def __init__(self, pos_root):
        
        global Input_Label_List
        global Output_Label_List
        
        self.convertFile = tk.StringVar()
        self.FileName = tk.StringVar()
        self.NewFileName = tk.StringVar()
        
        self.root = pos_root
        self.root.title("ASCEND - Basic Calcuations")
        self.root.resizable(False, False)

        canvas = tk.Canvas(self.root, width=width, height=height, bg=wc.Overall_background)
        canvas.place(x=0, y=0)

        self.Input_entry_List = []
        self.Input_Combo_List  = []
        self.Output_entry_List = []
        self.Output_Combo_List  = []
        
        style = ttk.Style(self.root)
        wc.configure_color_style_Entrybox(style, wc.Unhide_Entrybox)
        Label_font = wc.GuiFont
        
        # Create the Combobox widget
        self.Calcuations_combobox = ttk.Combobox(self.root, textvariable="")
        
        starty = 25

        # Create a Label widget with text
        Calcuations_label = ttk.Label(self.root, text='Calculations')

        wc.configure_color_style_Label(Calcuations_label)

        Calcuations_label.place(x=25, y=starty)

        self.Calcuations_combobox['values'] = ['Update Rate', 'Subtraction', 'Statistics']
        self.Calcuations_combobox.place(x=startx + 75, y=starty, width=70)
        self.Calcuations_combobox.bind('<<ComboboxSelected>>', lambda event: self.ConvertHandler(event, "From"))


        ttk.Checkbutton(self.root, text='Convert a File', command=self.ChooseFiletoConvert,
                        variable=self.convertFile, onvalue='ConvertFile',
                        offvalue='NoFile').place(x=startx+150, y=starty)

        File_label = ttk.Label(self.root, textvariable = self.FileName, font=Label_font)
        wc.configure_color_style_Label(File_label)
        File_label.place(x=startx+300, y=starty)

        New_File_label = ttk.Label(self.root, textvariable = self.NewFileName, font=Label_font)
        wc.configure_color_style_Label(New_File_label)
        New_File_label.place(x=25, y=output_y + linespace)

        Convert_button = tk.Button(self.root, text="Calculate", command=self.CalculateDataframe)
        Convert_button.place(x=165, y=height-35)
        
    def ChooseFiletoConvert(self):
        starty = starty_primary + linespace

        PosFrom = self.From_combobox.get()
        PosTo = self.To_combobox.get()

        widget_list = [self.Input_entry_List + self.Output_entry_List +
                       self.Input_Combo_List + self.Output_Combo_List]
        
        wc.hide_widgets(self, widget_list)
                
        if self.convertFile.get() == 'ConvertFile':
            FileName, NewFileName, df = bf.handle_file_conversion()
            self.FileName.set(FileName)
            self.NewFileName.set(NewFileName)
            filecols = df.columns.tolist()

            In_Combo['values'] = filecols
            
        else:
            self.FileName.set("")
            self.NewFileName.set("")

    def CalculateDataframe():
        print("working it")

def CreatePositionConversionWindow():
    pos_root = tk.Tk()
    windowGeom = str(width)+'x'+str(height)
    pos_root.geometry(windowGeom)

    DataFramePosCon(pos_root)

    pos_root.mainloop()

if __name__ == "__main__":
    CreatePositionConversionWindow()
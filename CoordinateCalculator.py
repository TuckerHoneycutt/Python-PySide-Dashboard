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

max_values = max(head.Position_dict, key=lambda k: len(head.Position_dict[k]))

Input_Label_List=[]
Refput_Label_List=[]
Output_Label_List=[]

class DataFramePosCon:
    def __init__(self, pos_root):
        
        global Input_Label_List
        global Refput_Label_List
        global Output_Label_List
        
        self.convertFile = tk.StringVar()
        self.FileName = tk.StringVar()
        self.NewFileName = tk.StringVar()
        
        self.root = pos_root
        self.root.title("ASCEND - Position Conversions")
        self.root.resizable(False, False)

        canvas = tk.Canvas(self.root, width=width, height=height, bg=wc.Overall_background)
        canvas.place(x=0, y=0)

        self.Input_entry_List = []
        self.Input_Combo_List  = []
        self.Refput_entry_List = []
        self.Refput_Combo_List  = []
        self.Output_entry_List = []
        self.Output_Combo_List  = []
        
        style = ttk.Style(self.root)
        wc.configure_color_style_Entrybox(style, wc.Unhide_Entrybox)
        Label_font = wc.GuiFont
        
        # Create the Combobox widget
        self.From_combobox = ttk.Combobox(self.root, textvariable="")
        self.To_combobox = ttk.Combobox(self.root, textvariable="")
        self.RefRef_combobox = ttk.Combobox(self.root)
        self.RefIn_combobox = ttk.Combobox(self.root)
        self.RefOut_combobox = ttk.Combobox(self.root)

        starty = 25

        # Create a Label widget with text
        from_label = ttk.Label(self.root, text='Convert From')
        to_label = ttk.Label(self.root, text='Convert To')

        wc.configure_color_style_Label(from_label)
        wc.configure_color_style_Label(to_label)

        from_label.place(x=25, y=starty)
        to_label.place(x=25, y=output_y)

        self.From_combobox['values'] = list(head.Position_dict.keys())
        self.From_combobox.place(x=startx + 75, y=starty, width=70)
        self.From_combobox.bind('<<ComboboxSelected>>', lambda event: self.ConvertHandler(event, "From"))

        self.To_combobox['values'] = list(head.Position_dict.keys())
        self.To_combobox.place(x=startx + 75, y=output_y, width=70)
        self.To_combobox.bind('<<ComboboxSelected>>', lambda event: self.ConvertHandler(event, "To"))

        self.RefIn_combobox['values'] = ('LLA deg', 'LLA rad', 'ECEF', 'UTM')
        self.RefIn_combobox.current(0)
        self.RefIn_combobox.bind('<<ComboboxSelected>>', lambda event: self.Ref_handler())
        
        self.RefOut_combobox['values'] = ('LLA deg', 'LLA rad', 'ECEF', 'UTM')
        self.RefOut_combobox.current(0)
        self.RefOut_combobox.bind('<<ComboboxSelected>>', lambda event: self.Ref_handler())

        self.RefRef_combobox['values'] = ('LLA deg', 'LLA rad', 'ECEF', 'UTM')
        self.RefRef_combobox.current(0)
        self.RefRef_combobox.bind('<<ComboboxSelected>>', lambda event: self.Ref_handler())


        ttk.Checkbutton(self.root, text='Convert a File', command=self.ChooseFiletoConvert,
                        variable=self.convertFile, onvalue='ConvertFile',
                        offvalue='NoFile').place(x=startx+150, y=starty)

        File_label = ttk.Label(self.root, textvariable = self.FileName, font=Label_font)
        wc.configure_color_style_Label(File_label)
        File_label.place(x=startx+300, y=starty)

        New_File_label = ttk.Label(self.root, textvariable = self.NewFileName, font=Label_font)
        wc.configure_color_style_Label(New_File_label)
        New_File_label.place(x=25, y=output_y + linespace)

        i=0

        while i < len(head.Position_dict[max_values]):
            Input_Label_List.append(ttk.Label(self.root, textvariable = "", font=Label_font))
            self.Input_entry_List.append(tk.Entry(self.root))
            self.Input_Combo_List.append(ttk.Combobox(self.root))
            
            Refput_Label_List.append(ttk.Label(self.root, textvariable = "", font=Label_font))
            self.Refput_entry_List.append(tk.Entry(self.root))
            self.Refput_Combo_List.append(ttk.Combobox(self.root))
            
            Output_Label_List.append(ttk.Label(self.root, textvariable = "", font=Label_font))
            self.Output_entry_List.append(tk.Entry(self.root))
            self.Output_Combo_List.append(ttk.Combobox(self.root))

            wc.configure_color_style_Label(Input_Label_List[i])
            wc.configure_color_style_Label(Refput_Label_List[i])
            wc.configure_color_style_Label(Output_Label_List[i])
            
            i=i+1
            
        Convert_button = tk.Button(self.root, text="Convert", command=self.ConvertPosition)
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

            for In_Combo, Ref_Combo in zip(self.Input_Combo_List, self.Refput_Combo_List):
                In_Combo['values'] = filecols
                Ref_Combo['values'] = filecols 
        else:
            self.FileName.set("")
            self.NewFileName.set("")

        Posto_labels = head.Position_dict.get(PosTo, [])
        Posfrom_labels = head.Position_dict.get(PosFrom, [])
        
        wc.place_widgets(self, self.Input_Combo_List, self.Input_entry_List, Posto_labels, startx, starty)
        wc.place_widgets(self, self.Output_Combo_List, self.Output_entry_List, Posfrom_labels, startx, starty)

        self.Ref_handler()

    def Ref_handler(self):
        print("finding references")
        startyref = starty_primary + 3*linespace
        Pos_labels = []
        
        if self.From_combobox.get() != '' and self.To_combobox.get() != '':
            if head.PosFrame_dict[self.From_combobox.get()] != head.PosFrame_dict[self.To_combobox.get()]:
                print('Reference Needed To')                                                 
                PosRef = self.RefRef_combobox['values'][self.RefRef_combobox.current()]
                
                if "LLA" in PosRef:
                    Pos_labels = head.Position_dict["LLA"]
                else:
                    Pos_labels = head.Position_dict[PosRef]
                
                self.RefRef_combobox.place(x=startx, y=startyref + linespace, width=70)
                    
        widget_list = [self.Refput_entry_List + self.Refput_Combo_List +
                       Refput_Label_List]
        
        wc.hide_widgets(self, widget_list)
        
        print("placing reference widgets")
        wc.place_widgets(self, self.Refput_Combo_List, self.Refput_entry_List, Pos_labels, startx, startyref, Label_List=Refput_Label_List, refchoice = self.RefRef_combobox) 
        
    def ConvertHandler(self, event, WayVar): 
        PosFrom = self.From_combobox.get()
        PosTo = self.To_combobox.get()
        
        if WayVar == "From":
            starty = starty_primary
            Label_List = Input_Label_List
            entry_List = self.Input_entry_List
            combo_list = self.Output_Combo_List
            Pos_labels = head.Position_dict.get(PosFrom, [])
        elif WayVar == "To":
            starty = output_y + linespace
            Label_List = Output_Label_List
            entry_List = self.Output_entry_List
            combo_list = self.Output_Combo_List
            Pos_labels = head.Position_dict.get(PosTo, [])
        
        widget_list = [Label_List + entry_List]
        wc.hide_widgets(self, widget_list)
            
        wc.place_widgets(self, combo_list, entry_List, Pos_labels, startx, starty, Label_List=Label_List)
        self.Ref_handler()                                         
    
                
    def ConvertPosition(self):
        
        PosFrom = self.From_combobox.get()
        PosTo = self.To_combobox.get()
        reslist = []
        
        k=0
        while k < len(self.Output_entry_List):
            self.Output_entry_List[k].config(state='normal')
            self.Output_entry_List[k].delete(0, tk.END)
            k=k+1

        if self.To_combobox.current() != -1 and self.From_combobox.current() != -1:
            if self.convertFile.get() != 'ConvertFile':
                
                    input_vars = [entry.get() for entry in self.Input_entry_List]

                    if self.To_combobox.current() != -1 and self.From_combobox.current() != -1:
                        if self.convertFile.get() != 'ConvertFile':
                                print("finding entries")
                                input_vars = [entry.get() for entry in self.Input_entry_List]
                                print(len(head.Position_dict[PosTo]))

                                if len(head.Position_dict[PosTo]) == 3:
                
                                    res1, res2, res3 = CT.MasterCoordinatesConvert(PosFrom, PosTo, 
                                                input_vars[0], input_vars[1],input_vars[2])
                                    
                                    reslist = [res1, res2, res3]
                                    
                                elif len(head.Position_dict[PosTo]) == 4:
                                    res1, res2, res3, res4 = CT.MasterCoordinatesConvert(PosFrom, PosTo, 
                                                input_vars[0], input_vars[1],input_vars[2])
                                    
                                    reslist = [res1, res2, res3, res4]
                                    
                        else:
                                print("finding entries")
                                input_vars = [entry.get() for entry in self.Input_entry_List]
                                print(len(head.Position_dict[PosTo]))

                                if len(head.Position_dict[PosTo]) == 3:
                
                                    res1, res2, res3 = CT.MasterCoordinatesConvert(PosFrom, PosTo, 
                                                self.df[input_vars[0]], self.df[input_vars[1]], self.df[input_vars[2]])
                                    
                                    reslist = [res1, res2, res3]
                                    
                                elif len(head.Position_dict[PosTo]) == 4:
                                    res1, res2, res3, res4 = CT.MasterCoordinatesConvert(PosFrom, PosTo, 
                                                self.df[input_vars[0]], self.df[input_vars[1]], self.df[input_vars[2]])
                                    
                                    reslist = [res1, res2, res3, res4]
 
            k=0
            while k < len(reslist):
                self.Output_entry_List[k].insert(0, str(reslist[k]))
                self.Output_entry_List[k].config(state='disabled')
                k=k+1 
                
        else:
            messagebox.showinfo("ASCEND", "Please fill out both cooridnate options.")

def CreatePositionConversionWindow():
    pos_root = tk.Tk()
    windowGeom = str(width)+'x'+str(height)
    pos_root.geometry(windowGeom)

    DataFramePosCon(pos_root)

    pos_root.mainloop()

if __name__ == "__main__":
    CreatePositionConversionWindow()
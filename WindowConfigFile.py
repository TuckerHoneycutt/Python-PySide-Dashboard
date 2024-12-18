# -*- coding: utf-8 -*-
"""
Spyder Editor

This script will be used for all Coordanate Conversion as the 
base of the ASCEND tool.
"""
from tkinter.font import Font

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
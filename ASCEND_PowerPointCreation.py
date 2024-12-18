# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 20:14:20 2024

@author: kayla.green
"""

from pptx import Presentation
from pptx.util import Inches
import os 
import pandas as pd
import numpy as np

MasterLocation = r"C:\Users\kayla.green\Documents\Tools\Masters"

def TriVector_PPTX_Title(prs, cover_photo, title_str, subtitle_str):
    
    # Title slide
    slide_layout = prs.slide_layouts[0]  # 0 is the layout for title slides
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[2]

    title.text = title_str
    subtitle.text = subtitle_str
    photo = cover_photo

    return prs

def TriVector_PPTX_ContentSlide(prs, title_str, information, bulletpoints = [], level = []):
    slide_layout = prs.slide_layouts[2]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    content = slide.placeholders[1]

    title.text = title_str
    content.text = information
    
    if len(bulletpoints) != 0:
        i = 0
        shapes = slide.shapes
        content_box = shapes.placeholders[1]
        text_frame = content_box.text_frame
        while i < len(bulletpoints):
            p = text_frame.add_paragraph()

            p.level = level[i] 
            p.text = bulletpoints[i]
            
            i = i + 1
            
    return prs

def ASCEND_Overview(prs):
    title_str = "Overview"
    information = ""
    bp = ["In-house system engineering and analysis toolsets are what can separate businesses from each other in the DoD support contractor environment", 
          "SETA and lab contractors don't generally produce material products, but engineering reviews, test plans, test reports, and analysis products are considered deliverables to a DoD Customer",
          "Software tools that can help keep quality work while speeding up the delivery time of analysis are extremely valued due to USG implementation on Agile development",
          "Diagrams of these tools or past deliverables can be provided in proposals to help the USG and primes understand a company's capability to handle the Engineering Cycle in an agile communityASCEND_Overview",
          "By developing a toolset with IRAD, TriVector could develop a Advanced System Engineering tool set that would be proprietary and would not be allowed to distribute the source code to USG or other SETA companies on a contract."]
    
    bp_level = [1,1,1,1,1]

    prs = TriVector_PPTX_ContentSlide(prs, title_str, information, bulletpoints = bp, level = bp_level)
    return prs

def ASCEND_Conclusion(prs):
    title_str = "Conclusion"
    information = ""
    bp = ["By developing ASCEND, TriVector will be able to help provide quality support quickly in all aspects of the System Engineering process.", 
          "With the implementation of ASCEND, TriVector can become an industry leader for the USG and SETA by helping solve issues and streamlining the System Engineering process.",
          "This TriVector-owned product can be leveraged in proposals, SIBRs and other potential avenues to grow the business and provide valuable aid to the USG."]
          
    bp_level = [1,1,1,1,1]

    prs = TriVector_PPTX_ContentSlide(prs, title_str, information, bulletpoints = bp, level = bp_level)
    return prs

def ASCEND_Capabilities(prs):
    title_str = "ASCEND will help TriVector rise above"
    information = ""
    bp = ["What does this provide TriVector?", 
          "By developing ASCEND, TriVector will be able to help provide quality support quickly in all aspects of the System Engineering process for the USG implementation on Agile development.",
          "Who needs these capabilities?",
          "The System Engineering process is used in all USG systems. As technology needs become more complex and solutions need to be provided faster, TriVector can leverave ASCEND capabilities as an industry leader for the USG and SETA by helping solve issues and streamlining the System Engineering process.",
          "How many organizations need this capability?",
          "All USG systems need System Engineering support in some way. Some examples of organizations are IFMC, IFPC, MDA, and IF.", 
          "How could TriVector use this capability to grow our company?", 
          "This TriVector-owned product can be leveraged in proposals, SIBRs and other potential avenues to grow the business and provide valuable aid to the USG."]
    
    bp_level = [1,2,1,2,1,2,1,2]

    prs = TriVector_PPTX_ContentSlide(prs, title_str, information, bulletpoints = bp, level = bp_level)
    return prs
    
def ASCEND_Weekly_Progress(prs):
    
    excel_file = r"C:\Users\kayla.green\Documents\ASCEND_Tracker.xlsx"
    
    df = pd.read_excel(excel_file, sheet_name='Product Due Outs', skiprows=1)

    titles = df['Main Task'].unique()

    for t in titles:
        slide_layout = prs.slide_layouts[2]
        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = t
        
        temp = df[df['Main Task']==t]

        print(df.columns.tolist())
        mainbullet = temp['Sub-Task'].unique()

        if len(mainbullet) != 1:
            shapes = slide.shapes
            content_box = shapes.placeholders[1]
            text_frame = content_box.text_frame
            
            for mb in mainbullet:
                p = text_frame.add_paragraph()
    
                p.level = 1
                p.text = str(mb) #+ ' - ' + temp[temp['Sub-Task'] == mb]['Assigned Tasks'].iloc[0]
                
                temp2 = temp[temp['Sub-Task']==mb]
                subbullet = temp2.dropna(subset=['Sub-Sub Task'])

                if len(subbullet['Sub-Sub Task']) != 0:
                    for sb in subbullet['Sub-Sub Task']:
                        p = text_frame.add_paragraph()
        
                        p.level = 2 
                        if temp2[temp2['Sub-Sub Task'] == sb]['STATUS'].iloc[0] == 'Complete':
                            p.text = str(sb) + ' - DONE'
                        elif temp2[temp2['Sub-Sub Task'] == sb]['STATUS'].iloc[0] == 'In Progress':
                            p.text = str(sb) + ' - WORKING ' + temp2[temp2['Sub-Sub Task'] == sb]['Assigned Tasks'].iloc[0]
                        else:
                            p.text = str(sb) + ' - ' + temp2[temp2['Sub-Sub Task'] == sb]['Assigned Tasks'].iloc[0]
    return prs

def ASCEND_ppt_creation(SlideOrder, Title_str, cover_photo, savepath, openaftercreation = True):
    
    TriVector_Master = r"\TriVector_Master.pptx"
    subtitle_str = "Reaching New Heights Every Day!"
    
    # Create a presentation object
    prs = Presentation(MasterLocation + TriVector_Master) 
    
    for slide in SlideOrder:
        if slide == "Title":
            prs = TriVector_PPTX_Title(prs, cover_photo, Title_str, subtitle_str) 
        elif slide == "Overview":  
            prs = ASCEND_Overview(prs)
        elif slide == "Capabilities":
            prs = ASCEND_Capabilities(prs)
        elif slide == "Updates":
            prs = ASCEND_Weekly_Progress(prs)    
        elif slide == "Conclusion":
            prs = ASCEND_Conclusion(prs)
        
    prs.save(savepath)
    
    if openaftercreation == True:
        os.startfile(savepath)
        
    return prs

LTAMDS_Master = r"\LTAMDS_Master.pptx"
IFMC_Master = r"\IFMC_Master.pptx"

title_str = "ASCEND – TriVector's System Engineering Tool"
cover_photo = r"C:\Users\kayla.green\Documents\Tools\Photos\Cover_Picture_Trivector.png"
savepath = r"C:\Users\kayla.green\Documents\Tools\presentation.pptx"

SlideOrder = ["Title", "Conclusion", "Overview", "Updates"]
ASCEND_ppt_creation(SlideOrder, title_str, cover_photo, savepath)

SlideOrder = ["Title", "Mission Overview", "Test Objectives", "Analysis Objectives", "Go-No-Go Criteria", "JIRA"]
#(SlideOrder, title_str, cover_photo, savepath)

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
import BasicPowerPointCreation as BPPC

MasterLocation = r"C:\Users\kayla.green\Documents\Tools\Masters"

def ASCEND_Overview(prs):
    title_str = "Overview"

    bp = ["In-house system engineering and analysis toolsets are what can separate businesses from each other in the DoD support contractor environment", 
          "SETA and lab contractors don't generally produce material products, but engineering reviews, test plans, test reports, and analysis products are considered deliverables to a DoD Customer",
          "Software tools that can help keep quality work while speeding up the delivery time of analysis are extremely valued due to USG implementation on Agile development",
          "Diagrams of these tools or past deliverables can be provided in proposals to help the USG and primes understand a company's capability to handle the Engineering Cycle in an agile communityASCEND_Overview",
          "By developing a toolset with IRAD, TriVector could develop a Advanced System Engineering tool set that would be proprietary and would not be allowed to distribute the source code to USG or other SETA companies on a contract."]
    
    bp_level = [1,1,1,1,1]

    prs = BPPC.PPTX_ContentSlide(prs, title_str = title_str, bulletpoints = bp, level = bp_level)
    
    return prs

def ASCEND_Conclusion(prs):
    title_str = "Conclusion"
    bp = ["By developing ASCEND, TriVector will be able to help provide quality support quickly in all aspects of the System Engineering process.", 
          "With the implementation of ASCEND, TriVector can become an industry leader for the USG and SETA by helping solve issues and streamlining the System Engineering process.",
          "This TriVector-owned product can be leveraged in proposals, SIBRs and other potential avenues to grow the business and provide valuable aid to the USG."]
          
    bp_level = [1,1,1,1,1]

    prs = BPPC.PPTX_ContentSlide(prs, title_str= title_str, bulletpoints = bp, level = bp_level)

    return prs

def ASCEND_Capabilities(prs):
    title_str = "ASCEND will help TriVector rise above"
    bp = ["What does this provide TriVector?", 
          "By developing ASCEND, TriVector will be able to help provide quality support quickly in all aspects of the System Engineering process for the USG implementation on Agile development.",
          "Who needs these capabilities?",
          "The System Engineering process is used in all USG systems. As technology needs become more complex and solutions need to be provided faster, TriVector can leverave ASCEND capabilities as an industry leader for the USG and SETA by helping solve issues and streamlining the System Engineering process.",
          "How many organizations need this capability?",
          "All USG systems need System Engineering support in some way. Some examples of organizations are IFMC, IFPC, MDA, and IF.", 
          "How could TriVector use this capability to grow our company?", 
          "This TriVector-owned product can be leveraged in proposals, SIBRs and other potential avenues to grow the business and provide valuable aid to the USG."]
    
    bp_level = [1,2,1,2,1,2,1,2]

    prs = BPPC.PPTX_ContentSlide(prs, title_str= title_str, bulletpoints = bp, level = bp_level)

    return prs
    
def ASCEND_Weekly_Progress(prs):
    
    excel_file = r"C:\Users\kayla.green\Documents\ASCEND_Tracker.xlsx"
    
    df = pd.read_excel(excel_file, sheet_name='Product Due Outs', skiprows=1)

    titles = df['Main Task'].unique()
    
    for t in titles:
        bp = []
        bp_level = []
        
        temp = df[df['Main Task']==t]

        mainbullet = temp[temp['Sub-Task'].notna()]['Sub-Task'].unique()

        if len(mainbullet) != 1:
            for mb in mainbullet:
                bp = bp + [mb]
                bp_level = bp_level  + [1]
                
                temp2 = temp[temp['Sub-Task']==mb]
                subbullet = temp2.dropna(subset=['Sub-Sub Task'])

                if len(subbullet['Sub-Sub Task']) != 0:
                    for sb in subbullet['Sub-Sub Task']:
                        bp_level = bp_level  + [2]

                        if temp2[temp2['Sub-Sub Task'] == sb]['STATUS'].iloc[0] == 'Complete':
                            bp = bp + [str(sb) + ' - DONE ']
                        elif temp2[temp2['Sub-Sub Task'] == sb]['STATUS'].iloc[0] == 'In Progress':
                            bp = bp + [str(sb) + ' - WORKING '+ temp2[temp2['Sub-Sub Task'] == sb]['Assigned Tasks'].iloc[0]]
                        else:
                            bp = bp + [str(sb) + ' - ' + temp2[temp2['Sub-Sub Task'] == sb]['Assigned Tasks'].iloc[0]]
       
        prs = BPPC.PPTX_ContentSlide(prs, title_str= t, bulletpoints = bp, level = bp_level)
    
    return prs

def ASCEND_ppt_creation(prs, SlideOrder):

    for slide in SlideOrder:
        if slide == "Overview":  
            prs = ASCEND_Overview(prs)
        elif slide == "Capabilities":
            prs = ASCEND_Capabilities(prs)
        elif slide == "Updates":
            prs = ASCEND_Weekly_Progress(prs)    
        elif slide == "Conclusion":
            prs = ASCEND_Conclusion(prs)
        
    return prs


MasterLocation = r"C:\Users\kayla.green\Documents\Tools\Masters"
Master = MasterLocation + r"\TriVector_Master.pptx"

title_str = "ASCEND – TriVector's System Engineering Tool"
subtitle_str = "Reaching New Heights Every Day!"
savepath = r"C:\Users\kayla.green\Documents\Tools\presentation.pptx"

prs = BPPC.PPTX_Creation(title_str, subtitle_str = subtitle_str, PPT_Master = Master)

SlideOrder = ["Overview", "Capabilities", "Updates", "Conclusion"]
ASCEND_ppt_creation(prs, SlideOrder)

BPPC.PPTX_Save(prs, savepath)

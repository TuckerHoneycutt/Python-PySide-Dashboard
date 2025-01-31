# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 12:52:04 2025

@author: kayla.green
"""

import BasicPowerPointCreation as BPPC
import matplotlib.pyplot as plt
import io

MasterLocation = r"C:\Users\kayla.green\Documents\Tools\Masters"
Master = MasterLocation + r"\TriVector_Master.pptx"
#Master = ""

title_str = "ASCEND – TriVector's System Engineering Tool"
subtitle_str = "Reaching New Heights Every Day!"
prs = BPPC.PPTX_Creation(title_str, subtitle_str = subtitle_str, PPT_Master = Master)

Sectiontitle_str = "Section 1"
prs = BPPC.PPTX_SectionBreak(prs, title_str, subtitle_str = subtitle_str)

BPPC.PPTX_ContentSlide(prs, title_str)
BPPC.PPTX_ContentSlide(prs, title_str, information="This is just a test to see how this looks.")
BPPC.PPTX_ContentSlide(prs, title_str, bulletpoints=["love", "laughter", "hot tea", "yay", "sdfs", "love", "laughter", "hot tea", "yay", "sdfs"], level=[0,1,2,0,1,0,1,2,0,1])
BPPC.PPTX_ContentSlide(prs, title_str, information="This is just a test to see how this looks.", bulletpoints=["love", "laughter", "hot tea", "yay"])
BPPC.PPTX_ContentSlide(prs, title_str, information="This is just a test to see how this looks.", bannertxt="TEST is GOOD")

Sectiontitle_str = "Section 2"
prs = BPPC.PPTX_SectionBreak(prs, Sectiontitle_str)

# Create a sample plot
plt.figure(figsize=(6, 4))
plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
plt.title('Sample Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Save the plot to a BytesIO object
image_stream = io.BytesIO()
plt.savefig(image_stream, format='png')
image_stream.seek(0)  # Rewind the stream to the beginning
plt.close()
BPPC.PPTX_ContentSlide(prs, title_str, information="This is just a test to see how this looks.", bannertxt="TEST is GOOD", photoChart=[image_stream])

savepath = r"C:\Users\kayla.green\Desktop\presentation.pptx"
BPPC.PPTX_Save(prs, savepath)

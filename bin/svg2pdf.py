#!/usr/bin/env python3
""" Pure python svg2pdf:

To install requirements:
    pip3 install reportlab svglib

"""
import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def svg2pdf(input_svg,output_pdf):
    drawing = svg2rlg(input_svg)
    renderPDF.drawToFile(drawing, output_pdf)

if __name__ == "__main__":
    svg2pdf(sys.argv[1],sys.argv[2])
    

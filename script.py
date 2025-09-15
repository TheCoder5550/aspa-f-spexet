import time

import struct
import imghdr
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from os import listdir
from os.path import isfile, join

from reportlab.lib.enums import *
from reportlab.platypus import Flowable, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil

from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)

width, height = A4

# Register font before it can be used
pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))

font = "Vera"
font_bold = "VeraBd"

def isImage(path):
    ext = imghdr.what(path)
    return ext in ["gif", "png", "jpeg"]

def get_bottom_info():
    f = open('input/bottomtext.txt', 'r', encoding='utf-8')
    lines = [line.rstrip() for line in f]
    if len(lines) == 0:
        return ""
    return lines[0]

def get_additional_info():
    f = open('input/subtext.txt', 'r', encoding='utf-8')
    lines = [line.rstrip() for line in f]
    return lines

def get_texts():
    texts = []
    f = open('input/texter.csv', 'r', encoding='utf-8')

    tuple_list = []
    # Get all the lines
    for line in f:
        linelen = len(line)
        line_last = line[linelen-1:]
        if(line_last == '\n'):
            line = line[:-1]
        texts.append(line)
    # split all the lines
    for text in texts:
        strs = text.split(',')
        a = strs[0], strs[1]
        tuple_list.append(a)
    return tuple_list

def get_images():
    mypath = "input/bilder"
    onlyfiles = [mypath + "/" + f for f in listdir(mypath) if isfile(join(mypath, f)) and isImage(join(mypath, f))]
    onlyfiles.sort()
    print("Hittade dessa bilder:")
    print("\n".join(onlyfiles))
    print("---------------------")
    return onlyfiles

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def create_pdf(index, maxCount, filename, top_text, imagepath, bottom_text, borders = False):
    def draw_text_top(c,txt):
        def get_center_x_coord(w):
            return (width - w)/2
        def get_center_y_coord(y,h):
            y = y + (maxHeight - h)/2
            return y
        maxHeight = 130
        maxWidth = 0.8*width
        c.setFillColor(black)
        c.setStrokeColor(black)
        y = height - maxHeight - 10
        if (borders):
            c.rect(get_center_x_coord(maxWidth),y,maxWidth,maxHeight)

        fontSize = 40
        fontName = font_bold


        def draw_text(fontSize,y):
            lineheight = fontSize + 5
            lines = simpleSplit(txt,fontName, fontSize,maxWidth)
            if (len(lines)>2):
                draw_text(fontSize*0.9,y)
            else:
                lines.reverse()
                for line in lines:
                    x = get_center_x_coord(stringWidth(line, fontName, fontSize))
                    c.setFont(fontName, fontSize)
                    c.drawString(x,y,line)
                    y = y + lineheight
        draw_text(fontSize,y)
    def draw_logo(canvas):
        logo = "input/loggan.png"
        logo_size = 40*mm
        margin = 10*mm
        x = width-logo_size - margin
        y = margin
        c.drawImage(logo, x, y, logo_size, logo_size, mask='auto')
    def draw_image(c,path):
        def get_center_x_coord(image_width):
            return (width - image_width)/2
        def get_center_y_coord(y,image_height):
            y = y + (maxHeight - image_height)/2
            return y

        maxWidth = 0.8*width
        maxHeight = height * 0.5
        y = 250
        x = get_center_x_coord(maxWidth)
        image_x, image_y = get_image_size(path)
        ratio = image_y/image_x
        def get_size(ratio):
            image_width = maxWidth
            image_height = ratio * image_width
            if(image_height>maxHeight):
                image_height = maxHeight
                image_width = image_height/ratio
            return image_width, image_height

        c.setFillColor(black)
        c.setStrokeColor(black)
        if (borders):
            c.rect(x,y,maxWidth,maxHeight)

        image_x, image_y = get_size(ratio)
        c.drawImage(path, get_center_x_coord(image_x), get_center_y_coord(y,image_y), image_x, image_y)
    def draw_text_bottom(canvas, text, fontsize = 60):

        def get_center_x_coord(text,fontName,fontsize):
            strwidth = stringWidth(text, fontName, fontsize)
            x = (width - strwidth)/2
            return x

        fontName = font_bold
        maxWidth = 0.8*width
        canvas.setFillColor(black)
        canvas.setStrokeColor(black)
        canvas.setFont(fontName, fontsize)
        lines = simpleSplit(text,fontName,fontsize,maxWidth)
        if(len(lines)>1):
            draw_text_bottom(canvas, text, fontsize*0.9)
        else:
            y = 170
            canvas.drawString(get_center_x_coord(text,fontName,fontsize),y,text)
            
            # Smaller text
            fontName = font
            fontsize = 20
            canvas.setFont(fontName, fontsize)

            for i in range(len(additional_info)):
                text = additional_info[i]
                y -= fontsize * 1.25
                canvas.drawString(get_center_x_coord(text, fontName, fontsize), y, text)  
            
            y = 20
            canvas.drawString(get_center_x_coord(bottom_info, fontName, fontsize), y, bottom_info)

    def draw_count(canvas):
        fontName = font
        fontsize = 15
        canvas.setFont(fontName, fontsize)
        canvas.drawString(20, 20, str(index + 1) + "/" + str(maxCount))

    c = canvas.Canvas(filename, pagesize=A4)

    draw_logo(c)
    draw_text_bottom(c,bottom_text)
    draw_image(c,imagepath)
    draw_text_top(c,top_text)
    draw_count(c)

    c.showPage()
    c.save()

def createOutputDir():
    outDir = "./output/"
    if os.path.exists(outDir) and os.path.isdir(outDir):
        shutil.rmtree(outDir)
    Path(outDir).mkdir(parents=False, exist_ok=True)

def generate_all_the_things():
    createOutputDir()

    tuple_texts = get_texts()
    image_names = get_images()

    missmatch_len = len(tuple_texts) != len(image_names)
    if missmatch_len:
        print("VARNING: Antalet texter and bilder matchar inte!")
        print(str(len(tuple_texts)) + " texter")
        print(str(len(image_names)) + " bilder")
        print("---------------------")

    for i in range(0,len(tuple_texts)):
        top_text, bottom_text = tuple_texts[i]
        image_path = image_names[i]

        procent = i/len(tuple_texts) * 100
        progress = "{0:.1f}".format(procent) + "%"
        print(progress.ljust(7, " ") + "Arbetar på bild " + image_path + " med texten \"" + top_text + "\"" )
        
        filename = "output/" + str(i+1) + ".pdf"
        create_pdf(i, len(tuple_texts), filename,top_text,image_path, bottom_text)

    print("Klart.")

bottom_info = get_bottom_info()
additional_info = get_additional_info()
generate_all_the_things()
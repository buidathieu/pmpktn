# -*- encoding: utf-8 -*-
from initialize import logo
import print_func.fonts

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit

import datetime as dt





def make_bill_pdf(filename, data):
    global x
    global y
    x = default_x
    y = default_y
    c = canvas.Canvas(filename=filename,
                      pagesize=A5)
    # draw
    drawLayout(c, data)
    # Next page
    c.showPage()
    # output to pdf
    c.save()

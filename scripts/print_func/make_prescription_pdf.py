# -*- encoding: utf-8 -*-
from initialize import logo
import print_func.fonts

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit

import datetime as dt


# some configs
logo_size = 3 * cm
logo_x = 1.5 * cm
logo_y = A5[1] - 1 * cm - logo_size
title_text = "PHÒNG KHÁM"
title_x = 6 * cm
title_y = A5[1] - 2 * cm
title_fontName = 'SVN-Sansation'
title_fontSize = 20
title_horizontalScale = 110

title_2_text = 'CHUYÊN KHOA NHI'
title_2_x = 6 * cm
title_2_y = A5[1] - 3 * cm
title_2_fontName = 'SVN-Sansation'
title_2_fontSize = 26

address_text = "355 Đặng Nguyên Cẩn, Phường 13, Quận 6, TPHCM"
address_x = 6 * cm
address_y = A5[1] - 3.5 * cm
address_fontName = "EBGaramond"
address_fontSize = 8

title_3_text = "TOA THUỐC"
title_3_x = 6 * cm
title_3_y = logo_y - 0.5 * cm
title_3_fontName = "Merriweather"
title_3_fontSize = 16

info_fontName = 'Alegreya-italic'

height_x = 7 * cm
weight_x = 10.5 * cm

quantity_x = 12 * cm
max_num_of_med = 6

followup_x = 1 * cm
followup_y = 4.6 * cm
followup_border = 7 * cm
followup_fontSize = 10

date_x = 9 * cm
date_y = followup_y

signature_x = date_x + 1.5 * cm
signature_y = followup_y - 0.6 * cm

# set default
default_x = 1 * cm
default_y = A5[1] - logo_size - 2 * cm
text_spacing = 0.6 * cm


class customLine():
    def __init__(self, text, x, y,
                 fontName="Alegreya", fontSize=12,
                 horizontalScale=100, leading=None,
                 label=False):
        self.text = text
        self.x = x
        self.y = y
        self.fontName = fontName
        self.fontSize = fontSize
        self.horizontalScale = horizontalScale
        if not leading:
            self.leading = fontSize * 1.2
        else:
            self.leading = leading
        if label:
            self.fontName = "EBGaramond-semibold"
            self.fontSize = 12

    def draw(self, c):
        c.saveState()
        obj = c.beginText()
        obj.setTextOrigin(self.x, self.y)
        obj.setFont(self.fontName, self.fontSize, self.leading)
        obj.setHorizScale(self.horizontalScale)
        obj.textLine(self.text)
        c.drawText(obj)
        c.restoreState()

        return c.stringWidth(self.text, self.fontName, self.fontSize)\
            * self.horizontalScale / 100

    def draw_multi(self, c, right_border=1 * cm, leading=0.4 * cm):
        c.saveState()
        width = A5[0] - self.x - right_border
        lines = simpleSplit(self.text,
                            self.fontName,
                            self.fontSize,
                            width)
        obj = c.beginText()
        obj.setTextOrigin(self.x, self.y)
        obj.setFont(self.fontName, self.fontSize, self.leading)
        obj.setLeading(leading)
        obj.textLines('\n'.join(lines))
        c.drawText(obj)
        c.restoreState()
        return (leading * len(lines)) - leading


def drawLayout(c, data):
    global x
    global y

    def nextrow():
        global x
        global y
        x = 1 * cm
        y -= text_spacing

    # draw logo
    c.drawImage(logo,
                logo_x, logo_y,
                logo_size, logo_size)

    # draw Phong kham
    customLine(
        title_text,
        title_x,
        title_y,
        title_fontName,
        title_fontSize,
        title_horizontalScale).draw(c)

    # draw chuyen khoa nhi
    customLine(
        title_2_text,
        title_2_x,
        title_2_y,
        title_2_fontName,
        title_2_fontSize).draw(c)

    # draw address
    customLine(
        address_text,
        address_x,
        address_y,
        address_fontName,
        address_fontSize).draw(c)

    c.roundRect(address_x - 0.2 * cm,
                address_y - 0.2 * cm,
                8 * cm,
                title_y - address_y + 1 * cm,
                radius=10)

    # draw toa thuoc
    customLine(
        title_3_text,
        title_3_x,
        title_3_y,
        title_3_fontName,
        title_3_fontSize).draw(c)

    # draw name
    label_width = customLine('Họ tên: ', x, y, label=True).draw(c)
    customLine(data['name'], x + label_width, y, info_fontName).draw(c)

    # draw gender
    x = 8.5 * cm
    label_width = customLine("Giới tính: ", x, y, label=True).draw(c)
    gender_width = customLine(
        data['gender'], x + label_width, y, info_fontName).draw(c)

    # draw age
    x += (label_width + gender_width + 0.5 * cm)
    label_width = customLine("Tuổi: ", x, y, label=True).draw(c)
    customLine(data['age'], x + label_width, y, info_fontName).draw(c)

    # draw address
    nextrow()
    label_width = customLine("Địa chỉ: ", x, y, label=True).draw(c)
    text_height = customLine(
        data['address'], x + label_width, y, info_fontName).draw_multi(c)
    y -= text_height
    if data['address']=='':
        y -= 0.3 * cm

    # draw diagnosis
    nextrow()
    label_width = customLine("Chẩn đoán: ", x, y, label=True).draw(c)
    text_height = customLine(
        data['diagnosis'], x + label_width, y, info_fontName).draw_multi(c)
    y -= text_height

    # before med list + height + weight
    nextrow()
    customLine("Thuốc ", x, y, label=True).draw(c)
    label_width = customLine("Chiều cao: ", height_x, y, label=True).draw(c)
    customLine(f"{data['height']} cm", height_x + label_width, y).draw(c)
    label_width = customLine("Cân nặng: ", weight_x, y, label=True).draw(c)
    customLine(f"{data['weight']} Kg", weight_x + label_width, y).draw(c)

    # draw meds
    c.setDash(1, 2)
    for i, ld in enumerate(data['linedrugs']):
        if i <= max_num_of_med:
            nextrow()
            name_width = customLine(
                f"{i+1}. {ld[0]}", x, y, label=True).draw(c)
            c.line(x + name_width, y, quantity_x, y)
            customLine(ld[2], quantity_x, y).draw(c)

            nextrow()
            x += 1 * cm
            customLine(ld[1], x, y).draw(c)

    # draw followup
    x = followup_x
    y = followup_y
    customLine("Dặn dò:", x, y, label=True).draw(c)
    customLine(data['followup'],
               followup_x, followup_y - text_spacing,
               fontSize=followup_fontSize).draw_multi(c, followup_border)

    # draw date
    today = dt.date.today()
    text = f'Ngày {today.day} tháng {today.month} năm {today.year}'
    customLine(text, date_x, date_y).draw(c)

    # draw signature
    customLine('Ký tên', signature_x, signature_y, label=True).draw(c)


def make_prescription_pdf(filename, data):
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

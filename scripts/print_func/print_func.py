# -*- encoding: utf-8 -*-
from .make_pdf import make_pdf
import datetime as dt
import subprocess
import os


class MyPrinter():
    MAKE_PDF_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = "prescription.pdf"
    file = os.path.join(MAKE_PDF_DIR, filename)

    def start_print_job(self):
        if os.name == 'nt':
            import win32print
            printer_name = win32print.GetDefaultPrinter()
            subprocess.run(['gs', '-sPapersize=A5',
                            '-sDEVICE=mswinpr2',
                            f'-sOutputFile=%printer%{printer_name}',
                            '-dBATCH', '-dNOPAUSE',
                            self.file])

    def print_pdf(self):
        make_pdf(self.file, self.data)
        self.start_print_job()

    def preview_pdf(self):
        make_pdf(self.file, self.data)
        os.startfile(self.file)

    def feed_data(self, name="", age="", gender="",
                  address="", diagnosis="",
                  weight="", height="",
                  linedrugs=[], followup=""):
        self.data = {
            "name": name,
            "age": age,
            "gender": gender,
            "address": address,
            "diagnosis": diagnosis,
            "weight": weight,
            "height": height,
            "linedrugs": linedrugs,
            "followup": followup
        }
    
    def preview_test(self):
        data = {
            "name": "Vương Kiến Thanh",
            "age": "20 tuổi",
            "gender": "nam",
            "address": "my example address " * 8,
            "diagnosis": "hen phế quản " * 15,
            "weight": "30",
            "height": "165",
            "linedrugs": [["amoxicillin 500mg", "Ngày uống 3 lần, lần 1 viên", "15 viên"],
                          ["paracetamol 500mg", "Ngày uống 3 lần, lần 1 viên", "15 viên"],
                          ["pectol", "Ngày uống 2 lần, lần 5 ml", "1 chai"],
                          ["carbocystein 200mg", "Ngày uống 3 lần, lần 1 gói", "15 gói"],
                          ["prednison 5mg", "Ngày uống 3 lần, lần 1 viên", "15 viên"],
                          ["duphalac 15mg", "Ngày uống 1 lần, lần 1 gói", "5 gói"]],
            "followup": "tái khám khi có gì lạ" + " x" * 200
        }
        file = os.path.join(self.MAKE_PDF_DIR, "test.pdf")
        make_pdf(file, data)
        os.startfile(file)

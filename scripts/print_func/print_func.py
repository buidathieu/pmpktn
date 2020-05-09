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
        self.start_print_job(self.file)

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
  
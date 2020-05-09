# -*- encoding: utf-8 -*-
from .make_pdf import make_pdf
import datetime as dt
import subprocess
import os


class MyPrinter():
    MAKE_PDF_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = "prescription.pdf"
    file = os.path.join(MAKE_PDF_DIR, filename)
    
    def start_print_job(filepath):
        if os.name == 'nt':
            import win32print
            printer_name = win32print.GetDefaultPrinter()
            subprocess.run(['gs', '-sPapersize=A5',
                            '-sDEVICE=mswinpr2',
                            f'-sOutputFile=%printer%{printer_name}',
                            '-dBATCH', '-dNOPAUSE',
                            file])

    @classmethod
    def print_pdf(data):
        make_pdf(file, data)
        start_print_job(file)

    @classmethod
    def preview_pdf(data):
        make_pdf(file, data)
        os.startfile(file)

    @classmethod
    def make_print_data(name="", age="", gender="",
                        address="", diagnosis="",
                        weight="", height="",
                        linedrugs=[], followup=""):
        return {
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
  
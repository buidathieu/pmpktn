# -*- encoding: utf-8 -*-
from .make_prescription_pdf import make_prescription_pdf
from .make_bill_pdf import make_bill_pdf
from initialize import *
import subprocess
import os


class MyPrinter():
    MAKE_PDF_DIR = os.path.dirname(os.path.abspath(__file__))

    def start_print_job(self, filename):
        if os.name == 'nt':
            import win32print
            printer_name = win32print.GetDefaultPrinter()
            print(printer_name)
            subprocess.run(['gs', '-sPAPERSIZE=a5',
                            '-sDEVICE=mswinpr2',
                            f'-sOutputFile=%printer%{printer_name}',
                            '-dBATCH', '-dNOPAUSE',
                            filename])

    def make_prescription_printdata(self, mv):
        assert mv.patient is not None
        assert mv.visit is not None
        filename = "prescription.pdf"
        filename = os.path.join(self.MAKE_PDF_DIR, filename)
        pg = mv.order_book.GetPage(0)
        f = mv.order_book.GetPage(0).followup.Value
        if f in setting["followup_dict"].keys():
            f = setting["followup_dict"][f]
        data = {
            "name": mv.name.Value,
            "age": mv.age.Value,
            "gender": mv.gender.Value,
            "address": mv.address.Value,
            "diagnosis": mv.diag.Value,
            "weight": pg.weight.Value,
            "height": "",
            "linedrugs": pg.d_list.build_linedrugs_for_pdf(),
            "followup": f
        }
        return filename, data

    def print_prescription_pdf(self, mv):
        filename, data = self.make_prescription_printdata(mv)
        make_prescription_pdf(filename, data)
        self.start_print_job(filename)

    def preview_prescription_pdf(self, mv):
        filename, data = self.make_prescription_printdata(mv)
        make_prescription_pdf(filename, data)
        os.startfile(filename)

    def make_bill_printdata(self, mv):
        assert mv.patient is not None
        assert mv.visit is not None
        filename = "bill.pdf"
        filename = os.path.join(self.MAKE_PDF_DIR, filename)
        pg = mv.order_book.GetPage(0)
        tg = mv.order_book.GetPage(1)
        data = {
            "name": mv.name.Value,
            "age": mv.age.Value,
            "gender": mv.gender.Value,
            "address": mv.address.Value,
            "diagnosis": mv.diag.Value,
            "drug_price": pg.d_list.get_total_price,
            "therapies": tg.t_list.therapy_list
        }
        return filename, data

    def print_bill_pdf(self, mv):
        filename, data = self.make_bill_printdata(mv)
        make_bill_pdf(filename, data)
        self.start_print_job(filename)

    def preview_bill_pdf(self, mv):
        filename, data = self.make_bill_printdata(mv)
        make_bill_pdf(filename, data)
        os.startfile(filename)

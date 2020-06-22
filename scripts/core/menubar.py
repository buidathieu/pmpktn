from initialize import *
import other_func as otf
import db_sql.db_func as dbf
from .core_func import onSaveVisit
from print_func.my_printer import MyPrinter
from nurse_view import NurseView
import wx


class MyMenuBar(wx.MenuBar):

    def __init__(self, mv):
        super().__init__()
        self.mv = mv
        self.printer = MyPrinter()
        self._createMenu()
        

    def _createMenu(self):
        homeMenu = wx.Menu()
        menuNurseview = homeMenu.Append(wx.ID_ANY, "Cửa sổ điều dưỡng nhận bệnh")
        homeMenu.AppendSeparator()
        menuPrint = homeMenu.Append(wx.ID_PRINT, "Print\tCTRL+P")
        menuPrintPreview = homeMenu.Append(wx.ID_ANY, "Print Preview")
        homeMenu.AppendSeparator()
        menuPrintBillPreview = homeMenu.Append(wx.ID_ANY, "In hoá đơn")
        homeMenu.AppendSeparator()
        menuRefresh = homeMenu.Append(wx.ID_REFRESH, "Refresh\tF5")
        menuExit = homeMenu.Append(wx.ID_EXIT, "Exit\tALT+F4")

        patientmenu = wx.Menu()
        menuSaveVisit = patientmenu.Append(id_save_visit, "Lưu lượt khám\tF3")

        reportmenu = wx.Menu()
        menuReportToday = reportmenu.Append(wx.ID_ANY, "Báo cáo hôm nay")

        self.Append(homeMenu, "Home")
        self.Append(patientmenu, "Bệnh nhân")
        self.Append(reportmenu, "Báo cáo")

        self.Bind(wx.EVT_MENU, self.onNurseview, menuNurseview)
        self.Bind(wx.EVT_MENU, self.onPrint, menuPrint)
        self.Bind(wx.EVT_MENU, self.onPrintPreview, menuPrintPreview)
        self.Bind(wx.EVT_MENU, self.onPrintBillPreview, menuPrintBillPreview)
        self.Bind(wx.EVT_MENU, self.onRefresh, menuRefresh)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onSaveVisit, menuSaveVisit)
        self.Bind(wx.EVT_MENU, self.onReportToday, menuReportToday)

    def onNurseview(self, e):
        NurseView(None).Show()

    def onPrint(self, e):
        self.printer.print_prescription_pdf(self.mv)

    def onPrintPreview(self, e):
        self.printer.preview_prescription_pdf(self.mv)

    def onPrintBillPreview(self, e):
        self.printer.preview_bill_pdf(self.mv)

    def onSaveVisit(self, e):
        onSaveVisit(self.mv)

    def onExit(self, e):
        self.mv.Close()

    def onRefresh(self, e):
        self.mv.Refresh()

    def onReportToday(self, e):
        count, income, cost, sale, profit = [
            otf.bill_int_to_str(i) for i in dbf.GetTodayReport()]

        with wx.MessageDialog(self.mv,
                              f"Tổng số lượt khám: {count}\n"
                              f"Tổng thu: {income}\n\n"
                              f"Tiền thuốc vốn: {cost}\n"
                              f"Tiền thuốc bán ra: {sale}\n"
                              f"Lời từ thuốc: {profit}",
                              "Báo cáo hôm nay") as dlg:
            dlg.ShowModal()

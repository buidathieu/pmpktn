from initialize import *
from core.__init__ import *
import other_func.other_func as otf
import db_sql.db_func as dbf
from add_edit_patient_dialog.add_patient_dialog import NewPatientDialog
from print_func.print_func import MyPrinter
import wx


class MyMenuBar(wx.MenuBar):

    def __init__(self, mv):
        super().__init__()
        self.mv = mv
        self._createMenu()
        self.printer = MyPrinter()

    def _createMenu(self):
        homeMenu = wx.Menu()
        menuPrint = homeMenu.Append(wx.ID_PRINT, "Print\tCTRL+P")
        menuPrintPreview = homeMenu.Append(wx.ID_ANY, "Print Preview")
        homeMenu.AppendSeparator()
        menuRefresh = homeMenu.Append(wx.ID_REFRESH, "Refresh\tF5")
        menuExit = homeMenu.Append(wx.ID_EXIT, "Exit\tALT+F4")

        patientmenu = wx.Menu()
        menuNewVisit = patientmenu.Append(id_new_visit, "Lượt khám mới\tF2")
        menuSaveVisit = patientmenu.Append(id_save_visit, "Lưu lượt khám\tF3")

        reportmenu = wx.Menu()
        menuReportToday = reportmenu.Append(wx.ID_ANY, "Báo cáo hôm nay")

        self.Append(homeMenu, "Home")
        self.Append(patientmenu, "Bệnh nhân")
        self.Append(reportmenu, "Báo cáo")

        self.Bind(wx.EVT_MENU, self.onPrint, menuPrint)
        self.Bind(wx.EVT_MENU, self.onPrintPreview, menuPrintPreview)
        self.Bind(wx.EVT_MENU, self.onRefresh, menuRefresh)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onNewVisit, menuNewVisit)
        self.Bind(wx.EVT_MENU, self.onSaveVisit, menuSaveVisit)
        self.Bind(wx.EVT_MENU, self.onReportToday, menuReportToday)

    def feed_data_to_printer(self):
        return self.printer.feed_data(
            name=self.mv.basic_info.name.Value,
            age=self.mv.basic_info.age.Value,
            gender=gender_dict[self.mv.basic_info.gender.Selection],
            address=self.mv.basic_info.address.Value,
            diagnosis=self.mv.visit_info.diag.Value,
            weight=self.mv.visit_info.weight.Value,
            height="",
            linedrugs = self.mv.visit_info.d_list.build_linedrugs_for_pdf(),
            followup=self.mv.visit_info.followup.Value
        )

    def onPrint(self, e):
        self.feed_data_to_printer()
        self.printer.print_pdf()

    def onPrintPreview(self, e):
        self.feed_data_to_printer()
        self.printer.preview_pdf()

    def onNewVisit(self, e):
        self.mv.visit_info.NewVisit()

    def onSaveVisit(self, e):
        self.mv.visit_info.SaveVisit()

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

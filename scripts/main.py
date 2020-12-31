from core.main_view import MainView
import wx


def mainloop():
    app = wx.App()
    MainView(None).Show()
    app.MainLoop()


if __name__ == "__main__":
    mainloop()

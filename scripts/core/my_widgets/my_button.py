import wx

class MyButton(wx.Button):

    def __init__(self, parent, label, bitmap):
        super().__init__(parent, label=label)
        self.SetBitmap(wx.Bitmap(bitmap))

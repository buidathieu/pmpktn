import wx

class MyButton(wx.Button):

    def __init__(self, parent, label, bitmap):
        super().__init__(parent)
        self.SetBitmap(wx.Bitmap(bitmap))
        self.SetLabel(label)

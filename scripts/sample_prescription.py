from initialize import *
import db_sql.db_func as dbf
import other_func as otf
import wx
import logging


class SamplePrescriptionDialog(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, title="Toa mẫu")
        self.sess = parent.sess
        self.sample_prescription_list = dbf.query_sample_prescription_list(
            self.sess).all()
        self.tree = self._createTree()
        self.add_btn = self._createAddBtn()
        self.upd_btn = self._createUpdBtn()
        self.del_btn = self._createDelBtn()
        self.apply_btn = self._createApplyBtn()
        self.cancel_btn = self._createCancelBtn()

        self._setSizer()
        self.RefreshTree()
        self._bind()
        logging.debug(
            "SamplePrescriptionDialog initialized, using mainview session")

    def _createTree(self):
        w = wx.TreeCtrl(self, size=tree_size,
                        style=wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT)
        return w

    def _createAddBtn(self):
        btn = wx.Button(self, label="Thêm")
        btn.Bind(wx.EVT_BUTTON, self.onAddSamplePrescription)
        return btn

    def _createUpdBtn(self):
        btn = wx.Button(self, label="Sửa")
        btn.Bind(wx.EVT_BUTTON, self.onUpdSamplePrescription)
        return btn

    def _createDelBtn(self):
        btn = wx.Button(self, label="Xóa")
        btn.Bind(wx.EVT_BUTTON, self.onDelSamplePrescription)
        return btn

    def _createApplyBtn(self):
        btn = wx.Button(self, wx.ID_APPLY)
        btn.SetDefault()
        btn.Bind(wx.EVT_BUTTON, self.onApplyBtn)
        return btn

    def _createCancelBtn(self):
        btn = wx.Button(self, wx.ID_CANCEL)
        btn.Bind(wx.EVT_BUTTON, self.onCancelBtn)
        return btn

    def _setSizer(self):
        editbtns = wx.BoxSizer(wx.HORIZONTAL)
        editbtns.AddStretchSpacer()
        editbtns.Add(self.add_btn, 0, wx.RIGHT, 5)
        editbtns.Add(self.upd_btn, 0, wx.RIGHT, 5)
        editbtns.Add(self.del_btn, 0, wx.RIGHT, 5)

        applybtns = wx.StdDialogButtonSizer()
        applybtns.AddButton(self.cancel_btn)
        applybtns.AddButton(self.apply_btn)
        applybtns.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(editbtns, 0, wx.EXPAND | wx.ALL ^ wx.TOP, 5)
        sizer.Add(applybtns, 0, wx.EXPAND | wx.ALL ^ wx.TOP, 5)
        self.SetSizerAndFit(sizer)

    def RefreshTree(self):
        t = self.tree
        t.DeleteAllItems()
        root = t.AddRoot("All sample prescriptions")
        for i in self.sample_prescription_list:
            ps = t.AppendItem(root, i.name)
            for ld in i.samplelinedrugs:
                t.AppendItem(ps, ld.drug.name)

    def _bind(self):
        self.Bind(wx.EVT_CLOSE, self.onCloseDialog)

    def onCloseDialog(self, e):
        try:
            self.sess.commit()
        except Exception:
            print("something happened and sess rollback")
            self.sess.rollback()
        finally:
            e.Skip()

    def onCancelBtn(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onApplyBtn(self, e):
        ps, idx = self.get_selected_sample_prescription()
        assert idx != -1
        self.EndModal(wx.ID_APPLY)

    def onAddSamplePrescription(self, e):
        with AddEditSamplePrescriptionDialog(self,
                                             mode='add') as dlg:
            dlg.ShowModal()

    def onUpdSamplePrescription(self, e):
        ps, idx = self.get_selected_sample_prescription()
        assert idx != -1
        with AddEditSamplePrescriptionDialog(self,
                                             mode='edit',
                                             ps=ps) as dlg:
            dlg.ShowModal()

    def onDelSamplePrescription(self, e):
        ps, idx = self.get_selected_sample_prescription()
        with wx.MessageDialog(self,
                              f'Xoá toa mẫu "{ps.name}"?',
                              "Xoá toa mẫu",
                              style=wx.OK | wx.CANCEL) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.sample_prescription_list.pop(idx)
                dbf.del_sample_prescription(ps, self.sess)
                self.RefreshTree()

    def get_selected_sample_prescription(self):
        '''
        return SamplePrescription and its index in list
        '''
        sel = self.tree.Selection
        if sel.IsOk():
            idx = 0
            root = self.tree.GetRootItem()
            # up 1 level if linedrug
            if self.tree.GetItemParent(sel) != root:
                sel = self.tree.GetItemParent(sel)
            (child, cookie) = self.tree.GetFirstChild(root)
            # find idx
            while True:
                if child == sel:
                    break
                else:
                    (child, cookie) = self.tree.GetNextChild(root, cookie)
                    idx += 1
            return self.sample_prescription_list[idx], idx
        else:
            return None, -1


class AddEditSamplePrescriptionDialog(wx.Dialog):

    def __init__(self, parent, mode, ps=None):
        self.mode = mode
        if mode == 'add':
            title = 'Thêm toa mẫu'
        elif mode == 'edit':
            title = 'Sửa toa mẫu'
        super().__init__(parent=parent, title=title,
                         size=add_edit_prescription_dialog_size)

        self.drugs = dbf.query_drugWH_list(self.Parent.sess).all()
        self.drugs.sort(key=lambda x: x.name)
        self.drugWH_id_list = []

        self.name = self._createName()
        self.ld_list = self._createLinedrugList()
        self.drugpicker = self._createDrugPicker()
        self.times = self._createTimes()
        self.dosage_per = self._createDosagePer()
        self.add_btn = self._createAddBtn()
        self.del_btn = self._createDelBtn()
        self.save_btn = self._createSaveBtn()
        self.cancel_btn = self._createCancelBtn()
        self._setSizer()
        if mode == 'edit':
            self.ps = ps
            self.drugWH_id_list = [i.drug_id for i in self.ps.samplelinedrugs]
            self.prefill(self.ps)

    def _createName(self):
        w = wx.TextCtrl(self)
        w.SetHint('Tên toa mẫu')
        return w

    def _createLinedrugList(self):
        w = wx.ListCtrl(self, style=wx.LC_REPORT)
        w.AppendColumn('Tên', width=d_name_w)
        w.AppendColumn('Số cữ', width=d_socu_w)
        w.AppendColumn('Liều 1 cữ', width=d_l1cu_w)
        return w

    def _createDrugPicker(self):
        choices = [f"{i.name} ({i.usage_unit})" for i in self.drugs]
        w = wx.Choice(self,
                      choices=choices)
        return w

    def _createTimes(self):
        w = wx.TextCtrl(self)
        w.SetHint('Số cữ')
        w.Bind(wx.EVT_CHAR, otf.only_nums)
        return w

    def _createDosagePer(self):
        w = wx.TextCtrl(self)
        w.SetHint('Liều 1 cữ')
        w.Bind(
            wx.EVT_CHAR,
            lambda e: otf.only_nums(e,
                                    decimal=True,
                                    slash=True)
        )
        return w

    def _createAddBtn(self):
        w = wx.BitmapButton(self, bitmap=wx.Bitmap(plus_bm))
        w.Bind(wx.EVT_BUTTON, self.onAdd)
        return w

    def _createDelBtn(self):
        w = wx.BitmapButton(self, bitmap=wx.Bitmap(minus_bm))
        w.Bind(wx.EVT_BUTTON, self.onDel)
        return w

    def _createSaveBtn(self):
        w = wx.Button(self, id=wx.ID_SAVE)
        w.SetDefault()
        w.Bind(wx.EVT_BUTTON, self.onSave)
        return w

    def _createCancelBtn(self):
        w = wx.Button(self, id=wx.ID_CANCEL)
        return w

    def _setSizer(self):
        btns = wx.BoxSizer(wx.HORIZONTAL)
        btns.AddMany([
            (0, 0, 1),
            (self.add_btn, 0, wx.RIGHT, 5),
            (self.del_btn,),
        ])

        stdbtns = wx.StdDialogButtonSizer()
        stdbtns.AddButton(self.save_btn)
        stdbtns.AddButton(self.cancel_btn)
        stdbtns.Realize()

        info = wx.GridSizer(2, 2, 10, 5)
        info.AddMany([
            (wx.StaticText(self, label="Số cữ"), 1),
            (self.times, 8,),
            (wx.StaticText(self, label="Liều 1 cữ"), 1),
            (self.dosage_per, 8,),


        ])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
            (self.name, 0, wx.EXPAND | wx.ALL, 10),
            (self.ld_list, 1, wx.EXPAND | wx.ALL ^ wx.TOP, 10),
            (self.drugpicker, 0, wx.EXPAND | wx.ALL ^ wx.TOP, 10),
            (info, 0, wx.ALL ^ wx.TOP, 10),
            (btns, 0, wx.EXPAND | wx.ALL ^ wx.TOP, 10),
            (stdbtns, 0, wx.EXPAND | wx.ALL ^ wx.TOP, 10),
        ])
        self.SetSizerAndFit(sizer)

    def prefill(self, ps):
        self.name.ChangeValue(ps.name)
        for ld in ps.samplelinedrugs:
            self.ld_list.Append([
                ld.drug.name,
                ld.times,
                ld.dosage_per
            ])

    def onAdd(self, e):
        idx = self.drugpicker.Selection
        assert idx != wx.NOT_FOUND
        assert self.times.Value != ''
        assert self.dosage_per.Value != ''
        item = self.ld_list.FindItem(-1, self.drugs[idx].name)
        assert item == wx.NOT_FOUND
        self.ld_list.Append(
            [self.drugs[idx].name, self.times.Value, self.dosage_per.Value])
        self.drugWH_id_list.append(self.drugs[idx].id)

    def onDel(self, e):
        idx = self.ld_list.GetFirstSelected()
        assert idx != -1
        self.ld_list.DeleteItem(idx)
        self.drugWH_id_list.pop(idx)

    def onSave(self, e):
        try:
            assert self.name.Value != ""
            sess = self.Parent.sess
            if self.mode == 'add':
                with wx.MessageDialog(self,
                                      "Lưu toa mẫu mới?",
                                      "Lưu toa mẫu",
                                      style=wx.OK | wx.CANCEL) as dlg:
                    if dlg.ShowModal() == wx.ID_OK:
                        ps = self.add_sample_prescription(sess)
                        self.Parent.sample_prescription_list.append(ps)
                        self.Parent.RefreshTree()
                        self.EndModal(wx.ID_OK)
            elif self.mode == 'edit':
                with wx.MessageDialog(self,
                                      "Lưu thay đổi toa mẫu ?",
                                      "Lưu toa mẫu",
                                      style=wx.OK | wx.CANCEL) as dlg:
                    if dlg.ShowModal() == wx.ID_OK:
                        self.upd_sample_prescription(sess)
                        self.Parent.RefreshTree()
                        self.EndModal(wx.ID_OK)
        except AssertionError:
            with wx.MessageDialog(self,
                                  "Lỗi chưa nhập tên toa mẫu",
                                  "Lưu toa mẫu", style=wx.OK) as dlg:
                dlg.ShowModal()

    def add_sample_prescription(self, sess):
        samplelinedrugs = self.build_samplelinedrugs()
        ps = dbf.add_sample_prescription(
            self.name.Value, samplelinedrugs, sess)
        return ps

    def upd_sample_prescription(self, sess):
        samplelinedrugs = self.build_samplelinedrugs()
        dbf.upd_sample_prescription(
            self.ps, self.name.Value, samplelinedrugs, sess)

    def build_samplelinedrugs(self):
        times = [self.ld_list.GetItemText(i, 1)
                 for i in range(self.ld_list.ItemCount)]
        dosage_per = [self.ld_list.GetItemText(i, 2)
                      for i in range(self.ld_list.ItemCount)]
        return zip(self.drugWH_id_list, times, dosage_per)

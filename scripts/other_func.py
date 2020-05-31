import wx
import datetime as dt
from initialize import setting


def bd_to_age(bd):
    if isinstance(bd, (dt.datetime, dt.date)):
        now = dt.date.today()
        delta = (now - bd).days
    elif isinstance(bd, wx.DateTime):
        now = wx.DateTime.Today()
        delta = (now - bd).GetDays()
    try:
        if delta <= 60:
            age = f'{delta} ngày tuổi'
        elif delta <= (30 * 24):
            age = f'{int(delta / 30)} tháng tuổi'
        else:
            age = f'{int(delta / 365)} tuổi'
    except ValueError:
        age = "ERROR"
    return age


def age_to_bd(age, py=False):
    age = age.upper()
    now = wx.DateTime.Today()
    span = wx.DateSpan()
    if "TH" in age:
        span.SetMonths(int(age.partition("TH")[0].strip(" ")))
    elif "T" in age:
        span.SetYears(int(age.partition("T")[0].strip(" ")))
    elif "NG" in age:
        span.SetDays(int(age.partition("NG")[0].strip(" ")))
    res = now.Subtract(span)
    if py:
        return wxdate2pydate(res)
    else:
        return res


def pydate2wxdate(date):
    assert isinstance(date, (dt.datetime, dt.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTime.FromDMY(*dmy)


def wxdate2pydate(date):
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return dt.date(*ymd)
    else:
        return None


def bill_str_to_int(bill_str):
    bill = bill_str.split(".")
    res = ""
    for i in bill:
        res += i
    try:
        return int(res)
    except ValueError:
        return setting['cong_kham_benh']


def bill_int_to_str(bill_int):
    bill = str(bill_int)
    res = ''
    x, y = divmod(len(bill), 3)
    if y != 0:
        res += bill[:y] + '.'
    for i in range(x):
        res += bill[(y + 3 * i):(y + 3 + 3 * i)] + "."
    return res[:-1]


def only_nums(e, decimal=False, slash=False):
    x = e.KeyCode
    nums = list(range(48, 58)) + list(range(324, 334)) +\
        [wx.WXK_BACK, wx.WXK_DELETE,
         wx.WXK_TAB, wx.WXK_LEFT, wx.WXK_RIGHT]
    if decimal:
        nums += [46, wx.WXK_DECIMAL]
    if slash:
        nums += [47, wx.WXK_DIVIDE]
    if x in nums:
        e.Skip()
        

def onTab(e, dst):
    if e.KeyCode == wx.WXK_TAB:
        dst.SetFocus()
    else:
        e.Skip()

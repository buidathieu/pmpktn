from initialize import FONTS_PATH

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os

# family path
Merriweather_fonts = os.path.join(FONTS_PATH, "Merriweather")
EBGaramond_fonts = os.path.join(FONTS_PATH, "EBGaramond")
Alegreya_fonts = os.path.join(FONTS_PATH, "Alegreya")
SVN_fonts = os.path.join(FONTS_PATH, "SVN")

# register name
pdfmetrics.registerFont(TTFont(
    'Merriweather',
    os.path.join(Merriweather_fonts, 'Merriweather-Regular.ttf')))
pdfmetrics.registerFont(TTFont(
    'Alegreya',
    os.path.join(Alegreya_fonts, 'Alegreya-Regular.ttf')))
pdfmetrics.registerFont(TTFont(
    'Alegreya-italic',
    os.path.join(Alegreya_fonts, 'Alegreya-Italic.ttf')))
pdfmetrics.registerFont(TTFont(
    'EBGaramond',
    os.path.join(EBGaramond_fonts, 'static', 'EBGaramond-Regular.ttf')))
pdfmetrics.registerFont(TTFont(
    'EBGaramond-semibold',
    os.path.join(EBGaramond_fonts, 'static', 'EBGaramond-SemiBold.ttf')))
pdfmetrics.registerFont(TTFont(
    'SVN-Cookies',
    os.path.join(SVN_fonts, 'SVN-Cookies.ttf')))
pdfmetrics.registerFont(TTFont(
    'SVN-Sansation',
    os.path.join(SVN_fonts, 'SVN-Sansation.ttf')))

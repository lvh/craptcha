"""
A best-effort approach at preprocessing a captcha image.
"""
from ImageOps import autocontrast

from craptcha import destripe, derotate, segment
from craptcha.tools import autocrop, deborder, scale, simplify

def composed(*functions):
    def g(x):
        for f in functions:
            x = f(x)
        return x

    return g


fixImage = composed(deborder, simplify, destripe.destripe)
fixGlyph = composed(autocrop, autocontrast, derotate.derotate, scale)


def preprocess(image):
    image = fixImage(image)
    glyphs = [glyph.convert("L") for glyph in segment.segment(image)]
    return map(fixGlyph, glyphs)
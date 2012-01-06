"""
Tools for segmenting preprocessed captchas into separate glyphs.
"""
import Image
import itertools


def segment(image):
    pixels = list(image.getdata())

    width, height = image.size
    BOTTOM_LEFT = width * (height - 1)
    columns = (pixels[i:BOTTOM_LEFT + i:width] for i in xrange(width))

    segments = []
    inSegment = False

    for column in columns:
        if _isWhite(column):
            inSegment = False
        else:
            if inSegment:
                segment.append(column)
            else: # whitespace or start -> new segment
                inSegment = True
                segment = [column]
                segments.append(segment)

    return [_recombineColumns(cols) for cols in segments]


def _recombineColumns(columns):
    width, height = len(columns), len(columns[0])
    recombined = Image.new("RGB", (width, height))

    rows = zip(*columns)
    pixels = list(itertools.chain.from_iterable(rows))
    recombined.putdata(pixels)
    return recombined


def _isWhite(pixels):
    return set(pixels) == set([(255, 255, 255)])
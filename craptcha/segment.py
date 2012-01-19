"""
Tools for segmenting preprocessed captchas into separate glyphs.
"""
import Image
import itertools

from craptcha import tools


def segment(image):
    columns = tools.getColumns(image)

    segments = []
    inSegment = False

    for column in columns:
        if tools.isWhite(column):
            inSegment = False
        else:
            if inSegment:
                segment.append(column)
            else: # whitespace or start -> new segment
                inSegment = True
                segment = [column]
                segments.append(segment)

    images = [_recombineColumns(cols) for cols in segments]
    return filter(lambda img: min(img.size) > 5, images)


def _recombineColumns(columns):
    width, height = len(columns), len(columns[0])
    recombined = Image.new("RGB", (width, height))

    rows = zip(*columns)
    pixels = list(itertools.chain.from_iterable(rows))
    recombined.putdata(pixels)
    return recombined


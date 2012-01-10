import functools
import Image
import ImageOps
import math

from craptcha import tools


BLACK = 0


def _inverted(f):
    @functools.wraps(f)
    def decorated(image, *a, **kw):
        image = ImageOps.invert(image.convert("L"))
        applied = f(image, *a, **kw)
        return ImageOps.invert(applied)
    return decorated


@_inverted
def derotate(image):
    """
    Forces an image into a consistent rotation.
    """
    angle = _getAngle(image)
    if angle:
        return image.rotate(-angle, Image.BICUBIC, expand=True)
    else:
        return image


def _getAngle(image):
    top, bottom = _leftmostPixelPerHalf(image)
    dx, dy = [ct - cb for ct, cb in zip(top, bottom)]

    if dx == 0:
        return 0

    angle = math.degrees(math.atan(float(dx) / dy))
    return angle


def _leftmostPixelPerHalf(image):
    rows = list(tools.getRows(image))

    for y, row in enumerate(rows):
        try:
            x = _first(row)[0]
            top = x, y
            break
        except ValueError:
            continue

    for fromBottom, row in enumerate(reversed(rows)):
        try:
            x = _first(row)[0]
            bottom = x, len(rows) - fromBottom
            return top, bottom
        except ValueError:
            continue


def _first(pixels, predicate=lambda p: p != BLACK):
    """
    Finds the index and element of the first object in the sequence to satisfy
    the predicate.
    """
    for idx, pixel in enumerate(pixels):
        if predicate(pixel):
            return idx, pixel
    else:
        raise ValueError("no pixels found satisfying predicate")
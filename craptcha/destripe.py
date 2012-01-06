"""
Tools for removing the vertical and horizontal bars from the captcha.
"""
from craptcha import tools


def _borderColors(image):
    width, height = image.size
    pixels = list(image.getdata())

    BOTTOM_LEFT = width * (height - 1)
    BOTTOM_RIGHT = width * height

    top = pixels[0:width]
    bottom = pixels[BOTTOM_LEFT:BOTTOM_RIGHT]
    right = pixels[width - 1:BOTTOM_RIGHT - 1:width]
    left = pixels[0:BOTTOM_LEFT:width]

    seen = set(top) | set(right) | set(bottom) | set(left)

    return seen


def destripe(image):
    destriped = tools.filterColors(image, _borderColors(image))

    cropped = destriped
    while len(tools.getColors(destriped)) > 2:
        cropped = tools.deborder(cropped)
        newBorderColors = _borderColors(cropped)
        destriped = tools.filterColors(destriped, newBorderColors)

    return destriped
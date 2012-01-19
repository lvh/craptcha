"""
Tools for removing the vertical and horizontal bars from the captcha.
"""
import ImageEnhance

from craptcha import segment, tools


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


def _simpleDestripe(image):
    destriped = cropped = tools.simplify(image)
    while len(tools.getColors(destriped)) > 2:
        newBorderColors = _borderColors(cropped)
        destriped = tools.filterColors(destriped, newBorderColors)
        cropped = tools.deborder(cropped)

    return destriped


def _segmentCondition(image, segmentor=segment.segment):
    return len(segmentor(image)) == 3


def destripe(image, condition=_segmentCondition):
    #import pdb; pdb.set_trace()

    def enhance(image, factor):
        image = ImageEnhance.Color(image).enhance(factor/5)
        image = ImageEnhance.Contrast(image).enhance(factor)
        return image

    enhanced = image
    factor = 1.0
    while True:
        if factor != 1.0:
            enhanced = enhance(image, factor)
        destriped = _simpleDestripe(enhanced)

        if condition(destriped) or factor > 40:
            return destriped

        factor += 1.0
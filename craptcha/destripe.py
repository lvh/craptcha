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


def _segmentCondition(image, segmentor=segment.segment):
    return len(segmentor(image)) == 3


def _simpleDestripe(image, condition=_segmentCondition):
    destriped = cropped = tools.simplify(image, 8)
    while not condition(destriped):
        newBorderColors = _borderColors(cropped)
        destriped = tools.filterColors(destriped, newBorderColors)
        cropped = tools.deborder(cropped)

    return destriped


def destripe(image, condition=_segmentCondition):
    def enhance(image, factor):
        image = ImageEnhance.Color(image).enhance(factor/5)
        image = ImageEnhance.Contrast(image).enhance(factor)
        return image

    enhanced = destriped = image
    factor = 1.0
    while True:
        if factor != 1.0:
            enhanced = enhance(image, factor)

        try:
            destriped = _simpleDestripe(enhanced)
        except ValueError: # border too wide in destripe step
            pass

        if condition(destriped) or factor > 5:
            return destriped

        factor += 1.0

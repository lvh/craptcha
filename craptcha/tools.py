"""
Generic image manipulation tools.
"""
import functools
import Image
import ImageChops
import ImageOps
import itertools


deborder = functools.partial(ImageOps.crop, border=1)


def getColors(image):
    return set(color for (count, color) in image.getcolors())


def filterColors(image, colors, newColor=(255, 255, 255)):
    """
    Turns a bunch of colors into a new color.
    """
    new = Image.new("RGB", image.size)
    newData = [p if p not in colors else newColor for p in image.getdata()]
    new.putdata(newData)
    return new


def simplify(image, colors=4):
    result = image.convert("P", palette=Image.ADAPTIVE, colors=colors)
    return result.convert("RGB")


def getColumns(image):
    pixels = list(image.getdata())
    width, height = image.size
    BOTTOM_LEFT = width * (height - 1)
    return (pixels[i:BOTTOM_LEFT + i:width] for i in xrange(width))


def getRows(image):
    return itertools.izip(*[iter(image.getdata())] * image.size[0])


def isWhite(pixels):
    return set(pixels) == set([(255, 255, 255)])


def autocrop(image, backgroundColor=255):
    background = Image.new(image.mode, image.size, backgroundColor)
    boundingBox = ImageChops.difference(image, background).getbbox()
    return image.crop(boundingBox)


def scale(image, size=(25, 25)):
    return image.resize(size, Image.ANTIALIAS)


def showPixel(image, pixel, color=(255, 0, 0)):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.putpixel(pixel, color)
    image.show()
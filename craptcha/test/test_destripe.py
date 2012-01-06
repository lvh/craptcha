from twisted.trial import unittest

from craptcha import destripe, samples, tools
from craptcha.test import tools as cttools


@cttools.generateCaptchaTests
class DestripeTest(unittest.TestCase):
    def test_simple(self):
        """
        Tests the destriping algorithm on a simple image with thick borders
        and a dot in the middle. The borders are red, green, blue and yellow,
        the dot is black and the remaining area is white. The result should
        be a white picture with the dot in the middle remaining.
        """
        image, solution = samples.getSample("algorithmTests", "border.gif")
        self.assertEqual(len(tools.getColors(image)), 6)

        destriped = destripe.destripe(image)
        destripedColors = tools.getColors(destriped)
        self.assertEqual(len(destripedColors), 2)
        WHITE, BLACK = (255, 255, 255), (0, 0, 0)
        self.assertEqual(destripedColors, set([WHITE, BLACK]))

        width, height = image.size
        dotPixel = image.getpixel((width // 2, height // 2))
        self.assertEqual(dotPixel, BLACK)


    worksOn = "easy", "conjoined", "lowContrast"
    failsOn = "difficult",


    def _captchaTest(self, image, solution):
        debordered = tools.deborder(image)
        simplified = tools.simplify(debordered)
        self.assertEqual(len(tools.getColors(simplified)), 4)

        destriped = destripe.destripe(simplified)
        destripedColors = tools.getColors(destriped)
        self.assertEqual(len(destripedColors), 2)
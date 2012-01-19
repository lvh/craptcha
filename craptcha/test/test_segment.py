from twisted.trial import unittest

from craptcha import destripe, segment, samples, tools
from craptcha.test import tools as cttools


@cttools.generateCaptchaTests
class SegmentTest(unittest.TestCase):
    def test_simple(self):
        image, solution = samples.getSample("algorithmTests", "segmentable.gif")
        segments = segment.segment(image)
        self.assertEqual(len(segments), 2)


    worksOn = "easy",
    failsOn = "conjoined", "lowContrast", "difficult"


    def _captchaTest(self, image, solution):
        debordered = tools.deborder(image)
        destriped = destripe.destripe(debordered)
        segments = segment.segment(destriped)
        self.assertEqual(len(segments), 3)
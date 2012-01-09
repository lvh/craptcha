import ImageOps

from twisted.trial import unittest

from craptcha import derotate, samples


class DerotateTest(unittest.TestCase):
    def _derotationTest(self, imageName):
        import pdb; pdb.set_trace(); from craptcha import tools
        image = samples.getSample("algorithmTests", imageName)[0]
        inverted = ImageOps.invert(image.convert("L"))
        before = derotate._getAngle(inverted)

        derotated = derotate.derotate(image)
        invertedDerotated = ImageOps.invert(derotated)
        after = derotate._getAngle(invertedDerotated)

        self.assertLess(abs(after), abs(before))
        self.assertLess(abs(after), 10.0)


    def test_slash(self):
        self._derotationTest("slash.gif")


    def test_backslash(self):
        self._derotationTest("backslash.gif")
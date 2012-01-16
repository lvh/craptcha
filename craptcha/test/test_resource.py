import os

from twisted.trial import unittest

from craptcha import resource, samples


class MockClassifier(object):
    def classify(self, glyphs):
        return "abc"


def mockPreprocessor(image):
    return []


class MockRequest(object):
    def __init__(self):
        path = os.path.join(samples._samplesPath, "easy", "2SY.jpg")
        self.content = open(path)



class ResourceTest(unittest.TestCase):
    def setUp(self):
        self.resource = resource.Resource(mockPreprocessor, MockClassifier())


    def test_simple(self):
        request = MockRequest()
        body = self.resource.render_POST(request)
        self.assertEqual(body, "abc")


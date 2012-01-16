"""
Web access for the captcha cracker.
"""
import Image

from twisted.web import resource


class Resource(resource.Resource):
    def __init__(self, preprocessor, classifier):
        self._preprocessor = preprocessor
        self._classifier = classifier


    def render_POST(self, request):
        image = Image.open(request.content)
        glyphs = self._preprocessor(image)
        return "".join(self._classifier.classify(glyphs))

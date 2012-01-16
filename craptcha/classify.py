"""
Classification for preprocessed captcha glyphs.
"""
import numpy
from sklearn import svm, preprocessing
import string


def _flatten(images):
    flattened = []
    for image in images:
        features = numpy.array(image.getdata(), numpy.float)
        flattened.append(preprocessing.normalize(features))
    return preprocessing.scale(flattened)


alphabet = string.ascii_letters + string.digits

_atoi = dict((x, i) for (i, x) in enumerate(alphabet))
_itoa = dict((i, x) for (i, x) in enumerate(alphabet))



class Classifier(object):
    def __init__(self):
        self._svc = svm.SVC(scale_C=True)


    def train(self, pairs):
        """
        Trains the classifier with a number of (image, solution) pairs.
        """
        images, solutions = zip(*pairs)
        flattened = _flatten(images)
        indices = [_atoi[solution] for solution in solutions]
        self._svc.fit(flattened, indices)


    def predict(self, glyphs):
        flattened = _flatten(glyphs)
        predictions = self._svc.predict(flattened)
        return [_itoa[p] for p in predictions]

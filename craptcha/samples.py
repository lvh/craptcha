import collections
import Image
import os

from craptcha import preprocess


_samplesPath = os.path.join(os.path.dirname(__file__), "samples")


def getSample(group, filename):
    solution = os.path.basename(filename).split(".")[0]
    path = os.path.join(_samplesPath, group, filename)
    image = Image.open(path).convert("RGB")

    return image, solution


samples = {}

for group in ("easy", "difficult", "conjoined", "lowContrast", "borderless"):
    samples[group] = groupSamples = []
    for fn in os.listdir(os.path.join(_samplesPath, group)):
        if os.path.splitext(fn)[1] in (".jpg", ".gif"):
            groupSamples.append(getSample(group, fn))



class TrainingSet(object):
    def __init__(self):
        self._samples = collections.defaultdict(list)


    def add(self, pairs):
        for captcha, solution in pairs:
            glyphs = preprocess.preprocess(captcha)
            for symbol, glyph in zip(solution, glyphs):
                self._samples[symbol].append(glyph)


    def getPairs(self):
        for symbol, glyphs in self._samples.iteritems():
            for glyph in glyphs:
                yield glyph, symbol
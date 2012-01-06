import Image
import os


_samplesPath = os.path.join(os.path.dirname(__file__), "samples")


def getSample(group, filename):
    solution = os.path.basename(filename).split(".")[0]
    path = os.path.join(_samplesPath, group, filename)
    image = Image.open(path).convert("RGB")

    return image, solution


samples = {}

for group in ("easy", "difficult", "conjoined", "lowContrast"):
    samples[group] = groupSamples = []
    for fn in os.listdir(os.path.join(_samplesPath, group)):
        if os.path.splitext(fn)[1] in (".jpg", ".gif"):
            groupSamples.append(getSample(group, fn))

import os
import functools

from craptcha import samples


def generateCaptchaTests(cls):
    test = cls._captchaTest

    for group in cls.worksOn + cls.failsOn:
        if group in cls.failsOn:
            todo = "{} fails for {} captchas".format(cls.__name__, group)
        else:
            todo = False

        for image, solution in samples.samples[group]:
            @functools.wraps(test)
            def generatedTest(self, image=image, solution=solution):
                test(self, image, solution)

            generatedTest.todo = todo

            generatedName = "test_{}Captcha_{}".format(group, solution)
            setattr(cls, generatedName, generatedTest)

    return cls

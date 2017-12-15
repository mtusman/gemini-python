import sys
import os
sys.path.insert(0, '..')
from gemini import meta


class A(metaclass=meta.Meta):
    # This will class will only have one argument for init: cached
    def __init__(self, cached=True):
        self.cached = cached


class B(metaclass=meta.Meta):
    # Will test if Meta class will stil work for classes with one more than one
    # args other cached
    def __init__(self, sandbox=True, cached=True):
        self.sandbox = sandbox
        self.cached = cached


class TestMetaClass:
    def test_A(self):
        x = A()
        y = A()
        assert id(x) == id(y)
        x = A(cached=False)
        y = A()
        assert id(x) != id(y)
        x = A(cached=False)
        y = A(cached=False)
        assert id(x) != id(y)

    def test_B(self):
        x = B()
        y = B()
        assert id(x) == id(y)
        x = B(sandbox=True)
        y = B(True)
        z = B()
        assert id(x) == id(y) == id(z)
        x = B(sandbox=False)
        y = B(False)
        assert id(x) == id(y)
        x = B(cached=False)
        y = B(cached=False)
        assert id(x) != id(y)

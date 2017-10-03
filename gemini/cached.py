# cached.py
# Mohammad Usman
#
# A metaclass that creates catched instances.

import weakref


class Cached(type):
    def __init__(self, *args, **kwargs):
        self.__cache = weakref.WeakValueDictionary()
        super().__init__(*args, **kwargs)

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

# cached.py
# Mohammad Usman
#
# A metaclass that creates catched instances.

import weakref


class Cached(type):
    def __init__(self, *args, **kwargs):
        self.__cache = weakref.WeakValueDictionary()
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if kwargs == {'sandbox': False}:
            key = args + (False,)
        elif kwargs == {'sandbox': True}:
            key = args + (True,)
        else:
            if len(args) == 1 or len(args) == 3:
                key = args
            else:
                key = args + (False,)
        if key in self.__cache:
            return self.__cache[key]
        else:
            obj = super().__call__(*args, **kwargs)
            self.__cache[key] = obj
            return obj

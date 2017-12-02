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
        if '{} {}'.format(args, kwargs) in self.__cache:
            return self.__cache['{} {}'.format(args, kwargs)]
        else:
            obj = super().__call__(*args, **kwargs)
            self.__cache['{} {}'.format(args, kwargs)] = obj
            return obj

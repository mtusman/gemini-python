# meta.py
# Mohammad Usman
#
# A metaclass that creates catched instances.

import weakref


class Meta(type):
    def __init__(self, *args, **kwargs):
        self.__cache = weakref.WeakValueDictionary()
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        key = str(obj.__dict__)
        if "'cached': True" in key:
            if key in self.__cache:
                return self.__cache[key]
            else:
                self.__cache[key] = obj
                return obj
        else:
            return obj

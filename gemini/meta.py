# meta.py
# Mohammad Usman
#
# A metaclass that creates catched instances.

from .debugly import typeassert
from types import FunctionType
import weakref


class Meta(type):
    def __new__(cls, clsname, bases, clsdict):
        new_dict = {}
        prepared_dict = dict(clsdict)
        for key, value in prepared_dict.items():
            if isinstance(value, FunctionType):
                func = typeassert(sandbox=bool, cached=bool, product_str=str,
                                  since=str, public_api_key=str,
                                  private_api_key=str, method=str,
                                  payload=dict, symbol=str, amount=str,
                                  price=str, side=str, options=list,
                                  order_id=str, limit_trades=int, currency=str,
                                  label=str, address=str, base_url=str,
                                  order=dict, symbolFilter=list,
                                  eventTypeFilter=list, apiSessionFilter=list,
                                  type=str, dir=str,
                                  newline_selection=str)(value)
                new_dict[key] = func
            else:
                new_dict[key] = value
        return super().__new__(cls, clsname, bases, new_dict)

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

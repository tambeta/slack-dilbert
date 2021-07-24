import collections

from collections.abc import Mapping, MutableMapping

class AllowException:
    def __init__(self, exc=Exception):
        self.exc = exc

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (self.exc and exc_type and issubclass(exc_type, self.exc)):
            return True
        return False
        
class staticproperty(property):
    def __init__(self, getter):       
        super().__init__(getter)
        self.getter = getter
    
    def __get__(self, obj, objtype=None):
        return self.getter()

def mapping_to_namedtuple(mapping, class_name):

    """ Recursively convert a mapping to a namedtuple. """

    nt = collections.namedtuple(class_name, mapping.keys())(**mapping)

    for (k, v) in mapping.items():
        if not (isinstance(v, Mapping) or isinstance(v, MutableMapping)):
            continue
        nt = nt._replace(**{k: mapping_to_namedtuple(v, class_name)})

    return nt

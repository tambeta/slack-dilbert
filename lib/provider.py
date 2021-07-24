import glob
import importlib
import inspect
import re

from abc import ABC, abstractmethod

from .util import staticproperty

class Provider(ABC):
    
    """ An abstract class to be implemented by a concrete Provider. """
    
    @staticproperty
    def all_providers():
        
        """ Locate all provider classes and return these. """
        
        all_providers = []
        provider_filter = lambda m: inspect.isclass(m) and re.search(r"\wProvider$", m.__name__)        
        package = importlib.import_module("lib.providers")
        members = inspect.getmembers(package)        
        paths = next(v for v in members if v[0] == "__path__")[1]
        
        for path in paths:
            for filename in glob.glob(f"{path}/*.py"):
                basename = re.search(r"(\w+)\.py$", filename)[1]
                module = importlib.import_module(f"lib.providers.{basename}")
                providers = map(lambda m: m[1], inspect.getmembers(module, provider_filter))
                
                all_providers += providers
                
        return all_providers
     
    @classmethod
    @property
    def id(cls):
        
        """ A lowercase string uniquely identifying the resource supplied by the
        provider. Constructed from the class name if not provided by the
        subclass.
        """
        
        return re.sub(r"Provider$", "", cls.__name__).lower()
        
    @abstractmethod
    def fetch_latest_resource():
        
        """ An implementation must return the latest Resource of this provider.
        Subsequent calls must yield resources with a monotonically increasing
        string ID. A resource is only considered fresh if its ID is greater than
        (determined by string ordering) some previously observed resource.
        """
        

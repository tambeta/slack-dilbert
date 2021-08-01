import glob
import importlib
import inspect
import re

from abc import ABC, abstractmethod

import bs4

from lib.user_agent import UserAgent

class Provider(ABC):
    
    """ An abstract class to be implemented by a concrete Provider. """
    
    @staticmethod
    def get_providers(ids=None):
        
        """ Locate all provider classes and return these. Pass a list of IDs to
        limit the set of returned providers.
        """
        
        all_providers = []
        package = importlib.import_module("lib.providers")
        members = inspect.getmembers(package)        
        paths = next(v for v in members if v[0] == "__path__")[1]
        
        def provider_filter(m):
            return inspect.isclass(m) \
                and re.search(r"\wProvider$", m.__name__) \
                and (not ids or m.id in ids)
        
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
    
    @property
    @staticmethod
    @abstractmethod
    def fullname():
        
        """ A human-readable full name identifying the resource. """
        
        pass
    
    @abstractmethod
    def fetch_latest_resource():
        
        """ An implementation must return the latest Resource of this provider.
        Subsequent calls must yield resources with a monotonically increasing
        string ID. A resource is only considered fresh if its ID is greater than
        (determined by string ordering) some previously observed resource.
        """

    def _fetch_soup(self, url):

        """ Fetch a HTML document and return it parsed into BeautifulSoup. As a
        special case, support `file` schema URLs.
        """
        
        if url.startswith("file:"):
            with open(re.sub(r"^file://", "", url)) as f:
                html = f.read()
        else:
            ua = UserAgent()
            response = ua.get(url)
            html = response.text

            if not response.ok:
              response.raise_for_status()

        return bs4.BeautifulSoup(html, "html.parser")    


from abc import ABC, abstractmethod

class Provider(ABC):
    def __init__(self):
        pass
        
    @property
    @abstractmethod
    def id():
        pass
        
    @abstractmethod
    def fetch_latest_resource():
        pass

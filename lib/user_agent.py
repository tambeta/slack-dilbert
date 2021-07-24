
import requests

from lib.configloader import config

class UserAgent:
    
    """ A thin wrapper around Requests. For now, provides a `get` method
    applying the User-Agent.
    """
    
    def get(self, url, *args, headers={}, **kwargs):
        headers.update({"User-Agent": config.user_agent})        
        return requests.get(url, *args, headers=headers, **kwargs)
        

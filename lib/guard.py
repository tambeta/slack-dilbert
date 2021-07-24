import configparser
import os

from lib.configloader import config

class Guard:
    
    """ Encapsulates the guard file storing latest posted IDs for each
    resource.
    """
    
    ID_KEY = "latest_id"
    
    def __init__(self):        
        fn = config.guard_fn
        self.guardfile = configparser.ConfigParser()

        if not os.access(fn, os.R_OK | os.W_OK):
            raise PermissionError(f"Guard file {fn} is not readable or writable")            
        elif not self.guardfile.read(fn):
            raise IOError(f"Could not read guard file {fn}")

    def is_resource_fresh(self, provider, resource):        
        section = self._get_section(provider)
        latest_id = section.get(self.ID_KEY)        
        
        return latest_id is None or latest_id < resource.id

    def write_id(self, provider, resource):
        section = self._get_section(provider)
        section[self.ID_KEY] = resource.id
        
        with open(config.guard_fn, "w") as f:
            self.guardfile.write(f)

    def _get_section(self, provider):
        if not self.guardfile.has_section(provider.id):
            raise KeyError(
                f"Guard file has no section for provider \"{provider.id}\": " \
                "create manually for safety"
            )
            
        return self.guardfile[provider.id]


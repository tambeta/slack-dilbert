
from lib.util import mapping_to_namedtuple

import importlib
import os

class ConfigLoader:

    """ A class for loading the configuration from lib.config.*, according
    to the environment passed in the environment variable `envvar`. The
    default environment is always loaded; the secondary environment
    overwrites the default configuration values.
    """

    CONFIG_PKG = "lib.config"

    def __init__(self, envvar=None):
        config = self._load_env("default")
        env = None

        if (envvar and (env := os.environ.get(envvar, None))):
            config.update(self._load_env(env))

        self.env = env
        self.config = config

    def _load_env(self, env):
        return importlib.import_module("{}.{}".format(self.CONFIG_PKG, env)).config

config = mapping_to_namedtuple(ConfigLoader().config, "Config")

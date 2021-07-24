
import xdg

config = dict(
    user_agent = "comicbot/0.1",
    log_level = "info",
    user_config_fn = xdg.XDG_CONFIG_HOME / "dilbertrc",
    guard_fn = xdg.XDG_CACHE_HOME / "dilbertts"
)

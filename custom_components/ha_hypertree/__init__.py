"""HA Hypertree — interactive tree visualizations for Home Assistant."""

from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import async_register_built_in_panel, async_remove_panel
from homeassistant.components.http import StaticPathConfig
import homeassistant.helpers.config_validation as cv

DOMAIN = "ha_hypertree"
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

JS_URL = f"/{DOMAIN}/hypertree.js"

# aiohttp raises "Added route will never be executed, method GET is already
# registered" if the same url_path is registered twice on one hass instance.
# That happens whenever async_setup_entry runs more than once - a second config
# entry for the same domain, or a reload after the integration folder was
# swapped out from under a running instance. HA's http static path registry
# lives for the lifetime of hass, so remember what we already registered and
# make the second call a no-op instead of a hard failure. The process-level set
# is exactly the right lifetime: it is dropped when hass restarts, at which
# point the registry is empty again.
_REGISTERED_PATHS: set[str] = set()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    panel_path = str(Path(__file__).parent / "hypertree.js")

    if JS_URL not in _REGISTERED_PATHS:
        await hass.http.async_register_static_paths(
            [StaticPathConfig(JS_URL, panel_path, False)]
        )
        _REGISTERED_PATHS.add(JS_URL)

    async_register_built_in_panel(
        hass=hass,
        component_name="custom",
        sidebar_title="Hypertree",
        sidebar_icon="mdi:graph",
        frontend_url_path="hypertree",
        config={
            "_panel_custom": {
                "name": "ha-panel-hypertree",
                "js_url": JS_URL,
            }
        },
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    async_remove_panel(hass, "hypertree")
    return True

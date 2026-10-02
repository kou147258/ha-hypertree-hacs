"""Config flow for HA Hypertree."""

from homeassistant.config_entries import ConfigFlow

DOMAIN = "ha_hypertree"


class HypertreeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if user_input is not None:
            return self.async_create_entry(title="HA Hypertree 中文版", data={})
        return self.async_show_form(step_id="user")

"""The unipi_neuron integration."""
import asyncio
import json
import logging

import voluptuous as vol
from evok_ws_client import *
from websockets.exceptions import ConnectionClosedError

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME, CONF_TYPE
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN

CONF_RECONNECT = "reconnect_time"

DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Required(CONF_TYPE): vol.In(CONF_NEURON_TYPES),
        vol.Optional(CONF_RECONNECT): cv.time_period_seconds
    }
)


CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [DEVICE_SCHEMA])},
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the unipi_neuron component."""
    #_LOGGER.info("In async setup!!!!!!!!")
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    conf = config[DOMAIN]

    for neuron_conf in conf:
        name = neuron_conf[CONF_NAME]
        ip_addr = neuron_conf[CONF_IP_ADDRESS]
        entity_reconnect_time = neuron_conf[CONF_RECONNECT]
        #default 30 seconds for reconnection to unipi device
        reconnect_seconds = 30
        if entity_reconnect_time is not None:
            reconnect_seconds = entity_reconnect_time.seconds

        _LOGGER.info("Setting up Neuron %s on IP:%s", name, ip_addr)
        neuron = UnipiEvokWsClient(ip_addr, neuron_conf[CONF_TYPE], name)

        hass.loop.create_task(evok_connection(hass, neuron, reconnect_seconds))
        hass.data[DOMAIN][name] = neuron
    return True



async def evok_connection(hass, neuron, reconnect_seconds):
    def evok_update_dispatch_send(name, device, circuit, value):
        _LOGGER.debug("SENDING Dispacher on %s %s", device, circuit)
        hass.loop.call_soon_threadsafe(
            async_dispatcher_send, hass, f"{DOMAIN}_{name}_{device}_{circuit}"
        )

    # Keep connection and subscription to websocket server on Unipi
    # Reconnect if connection is lost
    while True:
        try:
            try:
                await neuron.evok_close()
            except Exception:
                pass

            if not await neuron.evok_connect():
                await asyncio.sleep(reconnect_seconds)
                continue

            await neuron.evok_register_default_filter_dev()
            await neuron.evok_full_state_sync()

            while True:
                if not await neuron.evok_receive(True, evok_update_dispatch_send):
                    break
        except ConnectionClosedError as ex:
            _LOGGER.warning(f"WebSocket connection lost: {ex.reason}. Reconnecting in {reconnect_seconds} seconds.")
        except Exception as ex:
            _LOGGER.error(f"An unexpected error occurred in the connection loop: {ex}. Reconnecting in {reconnect_seconds} seconds.")

        await asyncio.sleep(reconnect_seconds)
    

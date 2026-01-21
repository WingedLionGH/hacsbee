"""The ToDo Manager integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import storage

from .const import DOMAIN, DATA_STORAGE, STORAGE_VERSION
from .coordinator import TodoCoordinator
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the ToDo Manager component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ToDo Manager from a config entry."""
    
    # Initialize storage
    store = storage.Store(hass, STORAGE_VERSION, f"{DOMAIN}_storage")
    hass.data[DOMAIN][DATA_STORAGE] = store
    
    # Initialize coordinator
    coordinator = TodoCoordinator(hass, store)
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Load data
    await coordinator.async_load_data()
    
    # Setup entities
    await coordinator.async_setup_entities()
    
    # Setup services
    await async_setup_services(hass)
    
    # Forward entry setup
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

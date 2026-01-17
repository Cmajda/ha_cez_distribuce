"""Platform for binary sensor integration."""
from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.components.sensor import PLATFORM_SCHEMA as BASE_PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .base_entity import CezHdoBaseEntity
from . import downloader

_LOGGER = logging.getLogger(__name__)

CONF_EAN = "ean"
CONF_SIGNAL = "signal"

PLATFORM_SCHEMA = BASE_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EAN): cv.string,
        vol.Optional(CONF_SIGNAL): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO binary sensor platform."""
    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    entities = [
        LowTariffActive(ean, signal),
        HighTariffActive(ean, signal),
    ]
    add_entities(entities, False)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO binary sensor platform (async)."""

    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    from .registry_cleanup import async_cleanup_entity_registry_if_ean_changed

    await async_cleanup_entity_registry_if_ean_changed(hass, ean)

    entities = [
        LowTariffActive(ean, signal),
        HighTariffActive(ean, signal),
    ]
    async_add_entities(entities, False)


class CezHdoBinarySensor(CezHdoBaseEntity, BinarySensorEntity):
    """Base class for CEZ HDO binary sensors."""

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:power"

    @property
    def device_class(self) -> str | None:
        """Return the device class of the sensor."""
        return None

    def _get_signal(self, hdo_json: dict | None):
        """Vrátí signál pro dnešní den z již načtených dat (bez file I/O)."""
        if self.signal:
            return self.signal

        if not hdo_json:
            return None

        data_level = hdo_json.get("data")
        if isinstance(data_level, dict) and "data" in data_level:
            data_level = data_level.get("data")
        signals: list[dict[str, Any]] = []
        if isinstance(data_level, dict):
            signals = data_level.get("signals", []) or []

        from datetime import datetime

        today = datetime.now().strftime("%d.%m.%Y")
        for s in signals:
            if downloader.normalize_datum(s.get("datum")) == today and s.get("signal"):
                return s["signal"]

        if signals and signals[0].get("signal"):
            return signals[0]["signal"]
        return None


class LowTariffActive(CezHdoBinarySensor):
    """Binary sensor for low tariff active state."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffActive", signal)

    @property
    def is_on(self) -> bool | None:
        """Return True if low tariff is active."""
        try:
            hdo_data = self._get_hdo_data()
            return hdo_data[0]  # low_tariff_active
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s LowTariffActive failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
            return None


class HighTariffActive(CezHdoBinarySensor):
    """Binary sensor for high tariff active state."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffActive", signal)

    @property
    def is_on(self) -> bool | None:
        """Return True if high tariff is active."""
        try:
            hdo_data = self._get_hdo_data()
            return hdo_data[4]  # high_tariff_active
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s HighTariffActive failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
            return None

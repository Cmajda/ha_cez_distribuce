"""Platform for binary sensor integration."""
from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant.components.binary_sensor import (
    PLATFORM_SCHEMA,
    BinarySensorEntity,
)
from homeassistant.components.sensor import PLATFORM_SCHEMA as BASE_PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .base_entity import CezHdoBaseEntity

_LOGGER = logging.getLogger(__name__)

CONF_REGION = "region"
CONF_CODE = "code"

PLATFORM_SCHEMA = BASE_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_REGION): cv.string,
        vol.Required(CONF_CODE): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO binary sensor platform."""
    region = config[CONF_REGION]
    code = config[CONF_CODE]

    entities = [
        LowTariffActive(region, code),
        HighTariffActive(region, code),
    ]
    add_entities(entities, True)


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


class LowTariffActive(CezHdoBinarySensor):
    """Binary sensor for low tariff active state."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "LowTariffActive")

    @property
    def is_on(self) -> bool:
        """Return True if low tariff is active."""
        hdo_data = self._get_hdo_data()
        return hdo_data[0]  # low_tariff_active


class HighTariffActive(CezHdoBinarySensor):
    """Binary sensor for high tariff active state."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "HighTariffActive")

    @property
    def is_on(self) -> bool:
        """Return True if high tariff is active."""
        hdo_data = self._get_hdo_data()
        return hdo_data[4]  # high_tariff_active

"""Platform for sensor integration."""
from __future__ import annotations
import logging
from datetime import time, timedelta
from typing import Any
import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .base_entity import CezHdoBaseEntity

_LOGGER = logging.getLogger(__name__)

CONF_REGION = "region"
CONF_CODE = "code"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
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
    """Set up the CEZ HDO sensor platform."""
    region = config[CONF_REGION]
    code = config[CONF_CODE]

    entities = [
        LowTariffStart(region, code),
        LowTariffEnd(region, code),
        LowTariffDuration(region, code),
        HighTariffStart(region, code),
        HighTariffEnd(region, code),
        HighTariffDuration(region, code),
    ]
    add_entities(entities, True)


class CezHdoSensor(CezHdoBaseEntity, SensorEntity):
    """Base class for CEZ HDO sensors."""

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock"


class LowTariffStart(CezHdoSensor):
    """Sensor for low tariff start time."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "LowTariffStart")

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[1]  # low_tariff_start


class LowTariffEnd(CezHdoSensor):
    """Sensor for low tariff end time."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "LowTariffEnd")

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[2]  # low_tariff_end


class LowTariffDuration(CezHdoSensor):
    """Sensor for low tariff duration."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "LowTariffDuration")

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        duration = hdo_data[3]  # low_tariff_duration
        if duration is None:
            return None
        return str(duration)


class HighTariffStart(CezHdoSensor):
    """Sensor for high tariff start time."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "HighTariffStart")

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[5]  # high_tariff_start


class HighTariffEnd(CezHdoSensor):
    """Sensor for high tariff end time."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "HighTariffEnd")

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[6]  # high_tariff_end


class HighTariffDuration(CezHdoSensor):
    """Sensor for high tariff duration."""

    def __init__(self, region: str, code: str) -> None:
        """Initialize the sensor."""
        super().__init__(region, code, "HighTariffDuration")

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        duration = hdo_data[7]  # high_tariff_duration
        if duration is None:
            return None
        return str(duration)
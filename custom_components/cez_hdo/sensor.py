"""Platform for sensor integration."""
from __future__ import annotations

import logging
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
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, DATA_COORDINATOR
from .coordinator import CezHdoCoordinator, CezHdoData
from . import downloader

_LOGGER = logging.getLogger(__name__)

CONF_EAN = "ean"
CONF_SIGNAL = "signal"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EAN): cv.string,
        vol.Optional(CONF_SIGNAL): cv.string,
    }
)

# Entity metadata for stable IDs and friendly names
ENTITY_META = {
    "LowTariffStart": {
        "object_id": "cez_hdo_lowtariffstart",
        "friendly": "ČEZ HDO nízký tarif začátek",
    },
    "LowTariffEnd": {
        "object_id": "cez_hdo_lowtariffend",
        "friendly": "ČEZ HDO nízký tarif konec",
    },
    "LowTariffDuration": {
        "object_id": "cez_hdo_lowtariffduration",
        "friendly": "ČEZ HDO nízký tarif zbývá",
    },
    "HighTariffStart": {
        "object_id": "cez_hdo_hightariffstart",
        "friendly": "ČEZ HDO vysoký tarif začátek",
    },
    "HighTariffEnd": {
        "object_id": "cez_hdo_hightariffend",
        "friendly": "ČEZ HDO vysoký tarif konec",
    },
    "HighTariffDuration": {
        "object_id": "cez_hdo_hightariffduration",
        "friendly": "ČEZ HDO vysoký tarif zbývá",
    },
    "CurrentPrice": {
        "object_id": "cez_hdo_currentprice",
        "friendly": "ČEZ HDO aktuální cena",
    },
    "HdoSchedule": {
        "object_id": "cez_hdo_schedule",
        "friendly": "ČEZ HDO rozvrh",
    },
    "RawData": {
        "object_id": "cez_hdo_raw_data",
        "friendly": "ČEZ HDO surová data",
    },
}


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO sensor platform (async)."""
    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    # Clean up old entities if EAN changed
    from .registry_cleanup import async_cleanup_entity_registry_if_ean_changed
    await async_cleanup_entity_registry_if_ean_changed(hass, ean)

    # Create or get coordinator
    coordinator = await _async_get_coordinator(hass, ean, signal)

    # Create entities
    entities = [
        LowTariffStart(coordinator, ean),
        LowTariffEnd(coordinator, ean),
        LowTariffDuration(coordinator, ean),
        HighTariffStart(coordinator, ean),
        HighTariffEnd(coordinator, ean),
        HighTariffDuration(coordinator, ean),
        CurrentPrice(coordinator, ean),
        HdoSchedule(coordinator, ean),
        CezHdoRawData(coordinator, ean),
    ]
    async_add_entities(entities, False)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO sensor platform (sync - deprecated)."""
    _LOGGER.warning(
        "Synchronous setup_platform is deprecated. "
        "Use async_setup_platform instead."
    )


async def _async_get_coordinator(
    hass: HomeAssistant, ean: str, signal: str | None
) -> CezHdoCoordinator:
    """Get or create coordinator instance."""
    # Check if coordinator already exists
    if DOMAIN in hass.data and DATA_COORDINATOR in hass.data[DOMAIN]:
        coordinator = hass.data[DOMAIN][DATA_COORDINATOR]
        _LOGGER.debug("Using existing coordinator")
        return coordinator

    # Create new coordinator
    coordinator = CezHdoCoordinator(hass, ean, signal)
    
    # Initialize - this loads cache and triggers first refresh
    # Use async_initialize() for YAML platforms (not async_config_entry_first_refresh)
    await coordinator.async_initialize()
    
    # Store in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][DATA_COORDINATOR] = coordinator
    
    _LOGGER.debug("Created new coordinator for EAN: %s", ean)
    return coordinator


class CezHdoSensor(CoordinatorEntity[CezHdoCoordinator], SensorEntity):
    """Base class for CEZ HDO sensors using CoordinatorEntity."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.ean = ean
        self._name = name
        
        # Set entity metadata
        meta = ENTITY_META.get(name, {})
        self._attr_unique_id = f"{ean}_{name.lower()}"
        self._attr_suggested_object_id = meta.get("object_id", f"cez_hdo_{name.lower()}")
        self._attr_name = meta.get("friendly", f"ČEZ HDO {name}")

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock"

    @property
    def data(self) -> CezHdoData:
        """Get coordinator data."""
        return self.coordinator.data


class LowTariffStart(CezHdoSensor):
    """Sensor for low tariff start time."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "LowTariffStart")

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.low_tariff_start:
            return self.data.low_tariff_start.strftime("%H:%M")
        return None


class LowTariffEnd(CezHdoSensor):
    """Sensor for low tariff end time."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "LowTariffEnd")

    @property
    def icon(self) -> str:
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.low_tariff_end:
            return self.data.low_tariff_end.strftime("%H:%M")
        return None


class LowTariffDuration(CezHdoSensor):
    """Sensor for low tariff duration."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "LowTariffDuration")

    @property
    def icon(self) -> str:
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.low_tariff_duration:
            return downloader.format_duration(self.data.low_tariff_duration)
        return None


class HighTariffStart(CezHdoSensor):
    """Sensor for high tariff start time."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "HighTariffStart")

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.high_tariff_start:
            return self.data.high_tariff_start.strftime("%H:%M")
        return None


class HighTariffEnd(CezHdoSensor):
    """Sensor for high tariff end time."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "HighTariffEnd")

    @property
    def icon(self) -> str:
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.high_tariff_end:
            return self.data.high_tariff_end.strftime("%H:%M")
        return None


class HighTariffDuration(CezHdoSensor):
    """Sensor for high tariff duration."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "HighTariffDuration")

    @property
    def icon(self) -> str:
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.high_tariff_duration:
            return downloader.format_duration(self.data.high_tariff_duration)
        return None


class CurrentPrice(CezHdoSensor):
    """Sensor for current electricity price based on active tariff."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "CurrentPrice")

    @property
    def icon(self) -> str:
        return "mdi:currency-usd"

    @property
    def native_unit_of_measurement(self) -> str:
        return "Kč/kWh"

    @property
    def device_class(self) -> str:
        return "monetary"

    @property
    def native_value(self) -> float | None:
        """Return the current price based on active tariff."""
        return self.coordinator.current_price

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        return {
            "low_tariff_price": self.data.low_tariff_price,
            "high_tariff_price": self.data.high_tariff_price,
            "active_tariff": "low" if self.data.low_tariff_active else "high",
        }


class CezHdoRawData(CezHdoSensor):
    """Sensor for raw HDO JSON data and timestamp."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "RawData")
        self._attr_unique_id = f"{ean}_raw_data"

    @property
    def native_value(self) -> str | None:
        """Return the timestamp from cache in format 'DD.MM.YYYY HH:mm'."""
        if self.data.last_update:
            return self.data.last_update.strftime("%d.%m.%Y %H:%M")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return the full JSON data as attribute."""
        if self.data.raw_data is None:
            return {}
        ts = self.data.last_update.isoformat() if self.data.last_update else None
        return {"raw_json": {"timestamp": ts, "data": self.data.raw_data}}


class HdoSchedule(CezHdoSensor):
    """Sensor providing HDO schedule data for graphs (ApexCharts compatible)."""

    def __init__(self, coordinator: CezHdoCoordinator, ean: str) -> None:
        super().__init__(coordinator, ean, "HdoSchedule")

    @property
    def icon(self) -> str:
        return "mdi:chart-timeline-variant"

    @property
    def native_value(self) -> str | None:
        """Return today's date as state value."""
        from datetime import datetime
        return datetime.now().strftime("%d.%m.%Y")

    @property
    def extra_state_attributes(self) -> dict:
        """Return schedule data suitable for ApexCharts timeline graph."""
        return {
            "schedule": self.data.schedule,
            "days": 7,
            "signal": self.coordinator.signal,
            "last_update": self.data.last_update.isoformat() if self.data.last_update else None,
        }

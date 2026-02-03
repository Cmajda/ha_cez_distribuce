"""Platform for sensor integration."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, DATA_COORDINATOR
from .coordinator import CezHdoCoordinator, CezHdoData
from . import downloader
from .const import mask_ean, ean_short, sanitize_signal

_LOGGER = logging.getLogger(__name__)

CONF_EAN = "ean"
CONF_SIGNAL = "signal"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EAN): cv.string,
        vol.Optional(CONF_SIGNAL): cv.string,
    }
)

# Entity metadata for stable IDs and translation keys
ENTITY_META = {
    "LowTariffStart": {
        "object_id": "cez_hdo_lowtariffstart",
        "translation_key": "lowtariffstart",
    },
    "LowTariffEnd": {
        "object_id": "cez_hdo_lowtariffend",
        "translation_key": "lowtariffend",
    },
    "LowTariffDuration": {
        "object_id": "cez_hdo_lowtariffduration",
        "translation_key": "lowtariffduration",
    },
    "HighTariffStart": {
        "object_id": "cez_hdo_hightariffstart",
        "translation_key": "hightariffstart",
    },
    "HighTariffEnd": {
        "object_id": "cez_hdo_hightariffend",
        "translation_key": "hightariffend",
    },
    "HighTariffDuration": {
        "object_id": "cez_hdo_hightariffduration",
        "translation_key": "hightariffduration",
    },
    "CurrentPrice": {
        "object_id": "cez_hdo_currentprice",
        "translation_key": "currentprice",
    },
    "HdoSchedule": {
        "object_id": "cez_hdo_schedule",
        "translation_key": "schedule",
    },
    "RawData": {
        "object_id": "cez_hdo_raw_data",
        "translation_key": "rawdata",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CEZ HDO sensors from a config entry."""
    # Get coordinator from hass.data
    entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
    coordinator = entry_data.get(DATA_COORDINATOR)
    ean = entry_data.get("ean")
    signal = entry_data.get("signal")
    entity_suffix = entry_data.get("entity_suffix")

    if not coordinator or not ean:
        _LOGGER.error("Coordinator or EAN not found for entry %s", entry.entry_id)
        return

    # Create entities with entry_id for unique identification
    entry_id = entry.entry_id
    entities = [
        LowTariffStart(coordinator, ean, entry_id, signal, entity_suffix),
        LowTariffEnd(coordinator, ean, entry_id, signal, entity_suffix),
        LowTariffDuration(coordinator, ean, entry_id, signal, entity_suffix),
        HighTariffStart(coordinator, ean, entry_id, signal, entity_suffix),
        HighTariffEnd(coordinator, ean, entry_id, signal, entity_suffix),
        HighTariffDuration(coordinator, ean, entry_id, signal, entity_suffix),
        CurrentPrice(coordinator, ean, entry_id, signal, entity_suffix),
        HdoSchedule(coordinator, ean, entry_id, signal, entity_suffix),
        CezHdoRawData(coordinator, ean, entry_id, signal, entity_suffix),
    ]
    async_add_entities(entities)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO sensor platform from YAML (async)."""
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
    _LOGGER.warning("Synchronous setup_platform is deprecated. Use async_setup_platform instead.")


async def _async_get_coordinator(hass: HomeAssistant, ean: str, signal: str | None) -> CezHdoCoordinator:
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

    _LOGGER.debug("Created new coordinator for EAN: %s", mask_ean(ean))
    return coordinator


class CezHdoSensor(CoordinatorEntity[CezHdoCoordinator], SensorEntity):
    """Base class for CEZ HDO sensors using CoordinatorEntity."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        name: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.ean = ean
        self._name = name
        self._entry_id = entry_id
        self._signal = signal
        self._entity_suffix = entity_suffix

        # Set entity metadata
        meta = ENTITY_META.get(name, {})
        # Include entry_id in unique_id if from config entry (prevents duplicates with YAML)
        if entry_id:
            self._attr_unique_id = f"{entry_id}_{ean}_{name.lower()}"
        else:
            self._attr_unique_id = f"{ean}_{name.lower()}"

        # Build object_id using entity_suffix from config or auto-generate
        base_object_id = meta.get("object_id", f"cez_hdo_{name.lower()}")
        if entity_suffix:
            # Use user-defined suffix
            self._object_id = f"{base_object_id}_{entity_suffix}"
        else:
            # Auto-generate suffix from EAN and signal (fallback for YAML config)
            ean4 = ean_short(ean)
            signal_safe = sanitize_signal(signal) if signal else ""
            if signal_safe:
                self._object_id = f"{base_object_id}_{ean4}_{signal_safe}"
            else:
                self._object_id = f"{base_object_id}_{ean4}" if ean4 else base_object_id
        self.entity_id = f"sensor.{self._object_id}"

        # Use translation_key for localized entity names
        # When has_entity_name=True and translation_key is set,
        # HA looks up name in translations/xx.json under entity.sensor.{translation_key}.name
        self._attr_has_entity_name = True
        self._attr_translation_key = meta.get("translation_key", name.lower())

        # Device info - group all entities under one device per EAN+signal combination
        # This ensures each signal for same EAN has its own device
        if signal:
            device_id = f"{ean}_{signal}"
            device_name = f"ČEZ HDO ({signal})"
        else:
            device_id = ean
            device_name = f"ČEZ HDO ({ean[-6:]})"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Cmajda",
            model="HDO",
            configuration_url="https://github.com/Cmajda/ha_cez_distribuce?tab=readme-ov-file#%EF%B8%8F%C4%8Dez-hdo-home-assistant-%EF%B8%8F",
        )

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

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "LowTariffStart", entry_id, signal, entity_suffix)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.low_tariff_start:
            return self.data.low_tariff_start.strftime("%H:%M")
        return None


class LowTariffEnd(CezHdoSensor):
    """Sensor for low tariff end time."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "LowTariffEnd", entry_id, signal, entity_suffix)

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

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "LowTariffDuration", entry_id, signal, entity_suffix)

    @property
    def icon(self) -> str:
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.low_tariff_duration and self.data.low_tariff_duration.total_seconds() > 0:
            return downloader.format_duration(self.data.low_tariff_duration)
        # Return "00:00" when low tariff is not active
        return "00:00"


class HighTariffStart(CezHdoSensor):
    """Sensor for high tariff start time."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "HighTariffStart", entry_id, signal, entity_suffix)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.high_tariff_start:
            return self.data.high_tariff_start.strftime("%H:%M")
        return None


class HighTariffEnd(CezHdoSensor):
    """Sensor for high tariff end time."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "HighTariffEnd", entry_id, signal, entity_suffix)

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

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "HighTariffDuration", entry_id, signal, entity_suffix)

    @property
    def icon(self) -> str:
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.data.high_tariff_duration and self.data.high_tariff_duration.total_seconds() > 0:
            return downloader.format_duration(self.data.high_tariff_duration)
        # Return "00:00" when high tariff is not active
        return "00:00"


class CurrentPrice(CezHdoSensor):
    """Sensor for current electricity price based on active tariff."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "CurrentPrice", entry_id, signal, entity_suffix)

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

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "RawData", entry_id, signal, entity_suffix)

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

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(coordinator, ean, "HdoSchedule", entry_id, signal, entity_suffix)

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
            "low_tariff_price": self.data.low_tariff_price,
            "high_tariff_price": self.data.high_tariff_price,
        }

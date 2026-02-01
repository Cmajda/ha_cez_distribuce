"""Platform for binary sensor integration."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.components.sensor import PLATFORM_SCHEMA as BASE_PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, DATA_COORDINATOR
from .coordinator import CezHdoCoordinator, CezHdoData
from .const import mask_ean, ean_short, sanitize_signal

_LOGGER = logging.getLogger(__name__)

CONF_EAN = "ean"
CONF_SIGNAL = "signal"

PLATFORM_SCHEMA = BASE_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EAN): cv.string,
        vol.Optional(CONF_SIGNAL): cv.string,
    }
)

# Entity metadata for stable IDs and translation keys
ENTITY_META = {
    "LowTariffActive": {
        "object_id": "cez_hdo_lowtariffactive",
        "translation_key": "lowtariffactive",
    },
    "HighTariffActive": {
        "object_id": "cez_hdo_hightariffactive",
        "translation_key": "hightariffactive",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CEZ HDO binary sensors from a config entry."""
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
        LowTariffActive(coordinator, ean, entry_id, signal, entity_suffix),
        HighTariffActive(coordinator, ean, entry_id, signal, entity_suffix),
    ]
    async_add_entities(entities)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO binary sensor platform from YAML (async)."""
    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    # Clean up old entities if EAN changed
    from .registry_cleanup import async_cleanup_entity_registry_if_ean_changed

    await async_cleanup_entity_registry_if_ean_changed(hass, ean)

    # Get or create coordinator (sensor platform creates it first usually)
    coordinator = await _async_get_coordinator(hass, ean, signal)

    # Create entities
    entities = [
        LowTariffActive(coordinator, ean),
        HighTariffActive(coordinator, ean),
    ]
    async_add_entities(entities, False)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO binary sensor platform (sync - deprecated)."""
    _LOGGER.warning(
        "Synchronous setup_platform is deprecated. " "Use async_setup_platform instead."
    )


async def _async_get_coordinator(
    hass: HomeAssistant, ean: str, signal: str | None
) -> CezHdoCoordinator:
    """Get or create coordinator instance."""
    # Check if coordinator already exists (sensor platform usually creates it first)
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


class CezHdoBinarySensor(CoordinatorEntity[CezHdoCoordinator], BinarySensorEntity):
    """Base class for CEZ HDO binary sensors using CoordinatorEntity."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        name: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        """Initialize the binary sensor."""
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
        self.entity_id = f"binary_sensor.{self._object_id}"

        # Use translation_key for localized entity names
        # When has_entity_name=True and translation_key is set,
        # HA looks up name in translations/xx.json under entity.binary_sensor.{translation_key}.name
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
        return "mdi:power"

    @property
    def device_class(self) -> str | None:
        """Return the device class of the sensor."""
        return None

    @property
    def data(self) -> CezHdoData:
        """Get coordinator data."""
        return self.coordinator.data


class LowTariffActive(CezHdoBinarySensor):
    """Binary sensor for low tariff active state."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(
            coordinator, ean, "LowTariffActive", entry_id, signal, entity_suffix
        )

    @property
    def is_on(self) -> bool | None:
        """Return True if low tariff is active."""
        return self.data.low_tariff_active


class HighTariffActive(CezHdoBinarySensor):
    """Binary sensor for high tariff active state."""

    def __init__(
        self,
        coordinator: CezHdoCoordinator,
        ean: str,
        entry_id: str | None = None,
        signal: str | None = None,
        entity_suffix: str | None = None,
    ) -> None:
        super().__init__(
            coordinator, ean, "HighTariffActive", entry_id, signal, entity_suffix
        )

    @property
    def is_on(self) -> bool | None:
        """Return True if high tariff is active."""
        return self.data.high_tariff_active

"""Platform for sensor integration."""
from __future__ import annotations
import logging
from . import downloader
import voluptuous as vol
from datetime import timedelta, datetime, date
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import requests
from lxml import html, etree

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=3600)
_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"
CONF_REGION = "region"
CONF_CODE = "code"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_REGION): cv.string,
        vol.Required(CONF_CODE): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    region = config.get(CONF_REGION)
    code = config.get(CONF_CODE)

    ents = []
    ents.append(LowTariffStart(region, code))
    ents.append(LowTariffEnd(region, code))
    add_entities(ents)

class LowTariffStart(SensorEntity):
    def __init__(self, region, code):
        """Initialize the sensor."""
        self._name = "LowTariffStart"
        self.region = region
        self.code = code
        self.responseJson = "[]"
        self.update()

    """Representation of a Sensor."""

    @property
    def name(self):
        return DOMAIN + "_" + self._name
    
    @property
    def unique_id(self):
        return DOMAIN + self._name
    
    @property
    def icon(self):
        return "mdi:home-clock"
    
    @property
    def should_poll(self):
        return True
    
    @property
    def extra_state_attributes(self):
        attributes = {}
        attributes["response_json"] = self.responseJson
        return attributes
    
    @property
    def native_value(self):
        result = downloader.isHdo(self.responseJson["data"])
        low_tariff, closest_start_timeL, closest_end_timeL, duration_time_L, high_tariff, closest_start_timeH, closest_end_timeH, duration_time_H = result
        return closest_start_timeL
    
    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self):
        response = requests.get(
            downloader.getRequestUrl(self.region, self.code))
        if response.status_code == 200:
            self.responseJson = response.json()
            self.last_update_success = True
        else:
            self.last_update_success = False
            
class LowTariffEnd(SensorEntity):
    def __init__(self, region, code):
        """Initialize the sensor."""
        self._name = "LowTariffEnd"
        self.region = region
        self.code = code
        self.responseJson = "[]"
        self.update()

    """Representation of a Sensor."""

    @property
    def name(self):
        return DOMAIN + "_" + self._name
    
    @property
    def unique_id(self):
        return DOMAIN + self._name
    
    @property
    def icon(self):
        return "mdi:home-clock-outline"
    
    @property
    def should_poll(self):
        return True
        
    @property
    def native_value(self):
        result = downloader.isHdo(self.responseJson["data"])
        low_tariff, closest_start_timeL, closest_end_timeL, duration_time_L, high_tariff, closest_start_timeH, closest_end_timeH, duration_time_H = result
        return closest_end_timeL
    
    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self):
        response = requests.get(
            downloader.getRequestUrl(self.region, self.code))
        if response.status_code == 200:
            self.responseJson = response.json()
            self.last_update_success = True
        else:
            self.last_update_success = False
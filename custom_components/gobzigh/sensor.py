"""Sensor platform for GOBZIGH integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfLength,
    UnitOfVolume,
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import get_device_info
from .const import DOMAIN, LIQUID_TYPE_MAP, UNIT_MAP
from .coordinator import GobzighDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    # Main sensor reading
    SensorEntityDescription(
        key="sensor_val",
        name="Distance",
        native_unit_of_measurement=UnitOfLength.CENTIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ruler",
    ),
    # Tank dimensions
    SensorEntityDescription(
        key="height",
        name="Tank Height",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:arrow-expand-vertical",
    ),
    SensorEntityDescription(
        key="width",
        name="Tank Width", 
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:arrow-expand-horizontal",
    ),
    SensorEntityDescription(
        key="length",
        name="Tank Length",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:arrow-expand-horizontal",
    ),
    SensorEntityDescription(
        key="sensor_distance",
        name="Sensor Distance",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:tape-measure",
    ),
    # Calculated values
    SensorEntityDescription(
        key="water_height",
        name="Liquid Height",
        native_unit_of_measurement=UnitOfLength.METERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:waves",
    ),
    SensorEntityDescription(
        key="current_volume",
        name="Current Volume",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    SensorEntityDescription(
        key="max_volume",
        name="Max Volume",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cube-outline",
    ),
    SensorEntityDescription(
        key="percentage",
        name="Fill Percentage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water-percent",
    ),
    # Device info
    SensorEntityDescription(
        key="firmware_version",
        name="Firmware Version",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:information-outline",
    ),
    SensorEntityDescription(
        key="liquid_type",
        name="Liquid Type",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:liquid-spot",
    ),
    SensorEntityDescription(
        key="ip_address",
        name="IP Address",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:ip-network",
    ),
    # Consumption
    SensorEntityDescription(
        key="consumption_day",
        name="Daily Consumption",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="consumption_week",
        name="Weekly Consumption",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:chart-line",
    ),
    SensorEntityDescription(
        key="consumption_month",
        name="Monthly Consumption",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:chart-line",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GOBZIGH sensors from a config entry."""
    coordinator: GobzighDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for device_id, device_data in coordinator.data.items():
        # Only create sensors for liquid level devices (WLSV0)
        if device_data.get("model_name") == "WLSV0":
            for description in SENSOR_DESCRIPTIONS:
                entities.append(GobzighSensor(coordinator, device_id, description))

    async_add_entities(entities)


class GobzighSensor(CoordinatorEntity[GobzighDataUpdateCoordinator], SensorEntity):
    """Representation of a GOBZIGH sensor."""

    def __init__(
        self,
        coordinator: GobzighDataUpdateCoordinator,
        device_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get(self._device_id, {})
        return get_device_info(device_data)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        device_data = self.coordinator.data.get(self._device_id, {})
        device_name = device_data.get("name", "Unknown Device")
        return f"{device_name} {self.entity_description.name}"

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        device_data = self.coordinator.data.get(self._device_id, {})
        if not device_data:
            return None

        key = self.entity_description.key
        
        # Handle direct sensor values
        if key == "sensor_val":
            return device_data.get("sensor_val")
            
        elif key == "firmware_version":
            return device_data.get("firmware_version")
            
        elif key == "ip_address":
            return device_data.get("ap_ip")
            
        elif key == "liquid_type":
            liquid_type_code = device_data.get("settings", {}).get("liquid_type", 0)
            return LIQUID_TYPE_MAP.get(liquid_type_code, "Unknown")

        # Handle settings-based values (converted to meters)
        elif key in ["height", "width", "length"]:
            settings = device_data.get("settings", {})
            value = settings.get(key, 0)
            return round(value / 100, 2)  # Convert cm to m
            
        elif key == "sensor_distance":
            settings = device_data.get("settings", {})
            value = settings.get("s_dist", 0)
            return round(value / 100, 2)  # Convert cm to m

        # Handle calculated values
        elif key == "water_height":
            return self._calculate_water_height(device_data)
            
        elif key == "current_volume":
            return self._calculate_current_volume(device_data)
            
        elif key == "max_volume":
            return self._calculate_max_volume(device_data)
            
        elif key == "percentage":
            return self._calculate_percentage(device_data)

        # Handle consumption
        elif key.startswith("consumption_"):
            consumption = device_data.get("consumption", {})
            consumption_type = key.split("_")[1]  # day, week, month
            return consumption.get(consumption_type, 0)

        return None

    def _calculate_water_height(self, device_data: dict) -> float | None:
        """Calculate liquid height in meters."""
        settings = device_data.get("settings", {})
        sensor_val = device_data.get("sensor_val", 0)
        
        height = settings.get("height", 0) / 100  # Convert to meters
        s_dist = settings.get("s_dist", 0) / 100  # Convert to meters
        sensor_reading = sensor_val / 100  # Convert to meters
        
        water_height = height + s_dist - sensor_reading
        return round(max(0, water_height), 2)

    def _calculate_current_volume(self, device_data: dict) -> float | None:
        """Calculate current volume in cubic meters."""
        water_height = self._calculate_water_height(device_data)
        if water_height is None or water_height <= 0:
            return 0
            
        settings = device_data.get("settings", {})
        width = settings.get("width", 0) / 100  # Convert to meters
        length = settings.get("length", 0) / 100  # Convert to meters
        
        volume = water_height * width * length
        return round(volume, 2)

    def _calculate_max_volume(self, device_data: dict) -> float | None:
        """Calculate maximum volume in cubic meters."""
        settings = device_data.get("settings", {})
        height = settings.get("height", 0) / 100  # Convert to meters
        width = settings.get("width", 0) / 100  # Convert to meters
        length = settings.get("length", 0) / 100  # Convert to meters
        
        volume = height * width * length
        return round(volume, 2)

    def _calculate_percentage(self, device_data: dict) -> int | None:
        """Calculate fill percentage."""
        current_volume = self._calculate_current_volume(device_data)
        max_volume = self._calculate_max_volume(device_data)
        
        if not current_volume or not max_volume or max_volume == 0:
            return 0
            
        percentage = (current_volume / max_volume) * 100
        return round(percentage, 0)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self.coordinator.data.get(self._device_id, {})
        
        # For the main sensor, add comprehensive attributes
        if self.entity_description.key == "sensor_val":
            connected_time = device_data.get("connected")
            last_connected = None
            if connected_time:
                try:
                    last_connected = dt_util.parse_datetime(connected_time)
                except (ValueError, TypeError):
                    pass
                    
            return {
                "room_name": device_data.get("room_name"),
                "room_id": device_data.get("room_id"),
                "location_id": device_data.get("loc_id"),
                "connection_status": device_data.get("connection_status"),
                "is_updating": device_data.get("is_updating"),
                "last_connected": last_connected,
                "next_firmware": device_data.get("next_firmware"),
                "settings": device_data.get("settings"),
            }
            
        return None

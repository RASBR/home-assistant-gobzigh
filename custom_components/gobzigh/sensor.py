"""Gobzigh sensor platform."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfLength, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_CONSUMPTION,
    ATTR_CONNECTION_STATUS,
    ATTR_FIRMWARE_VERSION,
    ATTR_MODEL_NAME,
    ATTR_NEXT_FIRMWARE,
    ATTR_ROOM_NAME,
    ATTR_SETTINGS,
    DOMAIN,
    SETTINGS_HEIGHT,
    SETTINGS_LENGTH,
    SETTINGS_S_DIST,
    SETTINGS_WIDTH,
    UNIT_CUBIC_METERS,
    UNIT_METERS,
    UNIT_PERCENTAGE,
)
from .coordinator import GobzighCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gobzigh sensors."""
    coordinator: GobzighCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities: list[SensorEntity] = []
    
    # Check if this is a device entry (has device_id) or main entry (has user_id only)
    if "device_id" in config_entry.data:
        # This is a device-specific entry
        device_id = config_entry.data["device_id"]
        device_data = config_entry.data.get("device_data", {})
        model_name = device_data.get("model_name", "")
        
        # Add device to coordinator monitoring
        await coordinator.async_add_device(device_id)
        
        # Create sensors based on device type
        if model_name == "WLSV0":  # Liquid Level device
            entities.extend(_create_liquid_level_sensors(coordinator, device_id, device_data))
    
    async_add_entities(entities)


def _create_liquid_level_sensors(
    coordinator: GobzighCoordinator, device_id: str, device_data: Dict[str, Any]
) -> list[SensorEntity]:
    """Create sensors for liquid level device."""
    device_name = device_data.get("name", "Gobzigh Device")
    
    return [
        GobzighLiquidLevelSensor(coordinator, device_id, device_name),
        GobzighTankHeightSensor(coordinator, device_id, device_name),
        GobzighTankWidthSensor(coordinator, device_id, device_name),
        GobzighTankLengthSensor(coordinator, device_id, device_name),
        GobzighSensorDistanceSensor(coordinator, device_id, device_name),
        GobzighWaterHeightSensor(coordinator, device_id, device_name),
        GobzighCurrentVolumeSensor(coordinator, device_id, device_name),
        GobzighMaxVolumeSensor(coordinator, device_id, device_name),
        GobzighPercentageSensor(coordinator, device_id, device_name),
        GobzighConnectionSensor(coordinator, device_id, device_name),
    ]


class GobzighSensorEntity(CoordinatorEntity, SensorEntity):
    """Base Gobzigh sensor entity."""

    def __init__(
        self,
        coordinator: GobzighCoordinator,
        device_id: str,
        device_name: str,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_name = device_name
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{device_id}_{sensor_type}"

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get("device_data", {}).get(self._device_id, {})
        model_name = device_data.get(ATTR_MODEL_NAME, "Unknown")
        firmware_version = device_data.get(ATTR_FIRMWARE_VERSION, "Unknown")
        
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Gobzigh",
            "model": model_name,
            "sw_version": firmware_version,
            "connections": {("mac", self._device_id)},
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data.get("device_data", {})
        )

    def _get_device_data(self) -> Dict[str, Any]:
        """Get current device data."""
        return self.coordinator.data.get("device_data", {}).get(self._device_id, {})


class GobzighLiquidLevelSensor(GobzighSensorEntity):
    """Gobzigh liquid level sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "level")
        self._attr_name = f"{device_name}"
        self._attr_native_unit_of_measurement = "cm"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        sensor_val = device_data.get("sensor_val")
        return float(sensor_val) if sensor_val is not None else None

    @property
    def extra_state_attributes(self) -> Dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self._get_device_data()
        return {
            "relay_state": device_data.get("relay_state"),
            "connection_status": device_data.get(ATTR_CONNECTION_STATUS),
            "firmware_version": device_data.get(ATTR_FIRMWARE_VERSION),
            "model_name": device_data.get(ATTR_MODEL_NAME),
            "room_name": device_data.get(ATTR_ROOM_NAME),
            "settings": device_data.get(ATTR_SETTINGS),
            "consumption": device_data.get(ATTR_CONSUMPTION),
            "next_firmware": device_data.get(ATTR_NEXT_FIRMWARE),
        }


class GobzighTankHeightSensor(GobzighSensorEntity):
    """Tank height sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "tank_height")
        self._attr_name = f"{device_name} Height"
        self._attr_native_unit_of_measurement = UNIT_METERS
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        height = settings.get(SETTINGS_HEIGHT)
        return round(float(height) / 100, 2) if height is not None else None


class GobzighTankWidthSensor(GobzighSensorEntity):
    """Tank width sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "tank_width")
        self._attr_name = f"{device_name} Width"
        self._attr_native_unit_of_measurement = UNIT_METERS
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        width = settings.get(SETTINGS_WIDTH)
        return round(float(width) / 100, 2) if width is not None else None


class GobzighTankLengthSensor(GobzighSensorEntity):
    """Tank length sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "tank_length")
        self._attr_name = f"{device_name} Length"
        self._attr_native_unit_of_measurement = UNIT_METERS
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        length = settings.get(SETTINGS_LENGTH)
        return round(float(length) / 100, 2) if length is not None else None


class GobzighSensorDistanceSensor(GobzighSensorEntity):
    """Sensor distance sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "sensor_distance")
        self._attr_name = f"{device_name} Sensor Distance"
        self._attr_native_unit_of_measurement = UNIT_METERS
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        s_dist = settings.get(SETTINGS_S_DIST)
        return round(float(s_dist) / 100, 2) if s_dist is not None else None


class GobzighWaterHeightSensor(GobzighSensorEntity):
    """Water height sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "water_height")
        self._attr_name = f"{device_name} Water Height"
        self._attr_native_unit_of_measurement = UNIT_METERS
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        
        sensor_val = device_data.get("sensor_val")
        height = settings.get(SETTINGS_HEIGHT)
        s_dist = settings.get(SETTINGS_S_DIST)
        
        if all(x is not None for x in [sensor_val, height, s_dist]):
            tank_height = float(height) / 100  # Convert cm to m
            sensor_distance = float(s_dist) / 100  # Convert cm to m
            sensor_reading = float(sensor_val) / 100  # Convert cm to m
            
            water_height = tank_height + sensor_distance - sensor_reading
            return round(max(0, water_height), 2)
        
        return None


class GobzighCurrentVolumeSensor(GobzighSensorEntity):
    """Current volume sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "current_volume")
        self._attr_name = f"{device_name} Current Volume"
        self._attr_native_unit_of_measurement = UNIT_CUBIC_METERS
        self._attr_device_class = SensorDeviceClass.VOLUME
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        sensor_val = device_data.get("sensor_val")
        
        height = settings.get(SETTINGS_HEIGHT)
        width = settings.get(SETTINGS_WIDTH)
        length = settings.get(SETTINGS_LENGTH)
        s_dist = settings.get(SETTINGS_S_DIST)
        
        if all(x is not None for x in [sensor_val, height, width, length, s_dist]):
            # Calculate water height
            tank_height = float(height) / 100
            sensor_distance = float(s_dist) / 100
            sensor_reading = float(sensor_val) / 100
            water_height = max(0, tank_height + sensor_distance - sensor_reading)
            
            # Calculate volume
            tank_width = float(width) / 100
            tank_length = float(length) / 100
            volume = water_height * tank_width * tank_length
            return round(volume, 2)
        
        return None


class GobzighMaxVolumeSensor(GobzighSensorEntity):
    """Maximum volume sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "max_volume")
        self._attr_name = f"{device_name} Max Volume"
        self._attr_native_unit_of_measurement = UNIT_CUBIC_METERS
        self._attr_device_class = SensorDeviceClass.VOLUME
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        
        height = settings.get(SETTINGS_HEIGHT)
        width = settings.get(SETTINGS_WIDTH)
        length = settings.get(SETTINGS_LENGTH)
        
        if all(x is not None for x in [height, width, length]):
            tank_height = float(height) / 100
            tank_width = float(width) / 100
            tank_length = float(length) / 100
            volume = tank_height * tank_width * tank_length
            return round(volume, 2)
        
        return None


class GobzighPercentageSensor(GobzighSensorEntity):
    """Percentage sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "percentage")
        self._attr_name = f"{device_name} Percentage"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        # Get current and max volume from other sensors
        device_data = self._get_device_data()
        settings = device_data.get(ATTR_SETTINGS, {})
        sensor_val = device_data.get("sensor_val")
        
        height = settings.get(SETTINGS_HEIGHT)
        width = settings.get(SETTINGS_WIDTH)
        length = settings.get(SETTINGS_LENGTH)
        s_dist = settings.get(SETTINGS_S_DIST)
        
        if all(x is not None for x in [sensor_val, height, width, length, s_dist]):
            # Calculate current volume
            tank_height = float(height) / 100
            sensor_distance = float(s_dist) / 100
            sensor_reading = float(sensor_val) / 100
            water_height = max(0, tank_height + sensor_distance - sensor_reading)
            
            tank_width = float(width) / 100
            tank_length = float(length) / 100
            current_volume = water_height * tank_width * tank_length
            
            # Calculate max volume
            max_volume = tank_height * tank_width * tank_length
            
            if max_volume > 0:
                percentage = (current_volume / max_volume) * 100
                return round(percentage, 0)
        
        return None


class GobzighConnectionSensor(GobzighSensorEntity):
    """Connection status sensor."""

    def __init__(self, coordinator: GobzighCoordinator, device_id: str, device_name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "connection")
        self._attr_name = f"{device_name} Connected"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["connected", "disconnected"]

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        connection_status = device_data.get(ATTR_CONNECTION_STATUS)
        return "connected" if connection_status else "disconnected"

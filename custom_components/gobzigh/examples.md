# GOBZIGH Integration Configuration Examples

## Basic Configuration
After installing the integration, you only need to provide your User ID during setup. All devices will be automatically discovered and configured.

## Device Information Example
When a WLSV0 liquid level device is discovered, it will create entities like:

```yaml
# Main sensor (distance reading)
sensor.pool_tank_distance:
  friendly_name: "Pool Tank Distance"
  unit_of_measurement: "cm"
  device_class: "distance"
  state_class: "measurement"

# Calculated volume sensors
sensor.pool_tank_current_volume:
  friendly_name: "Pool Tank Current Volume"
  unit_of_measurement: "m³"
  device_class: "volume"
  state_class: "measurement"

sensor.pool_tank_fill_percentage:
  friendly_name: "Pool Tank Fill Percentage"
  unit_of_measurement: "%"
  state_class: "measurement"

# Connection status
binary_sensor.pool_tank_connection_status:
  friendly_name: "Pool Tank Connection Status"
  device_class: "connectivity"

# Relay control (if available)
switch.pool_tank_relay:
  friendly_name: "Pool Tank Relay"
```

## Automation Examples

### Low Level Alert
```yaml
automation:
  - alias: "Pool Tank Low Level Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.pool_tank_fill_percentage
      below: 20
    action:
      service: notify.notify
      data:
        message: "Pool tank is low ({{ states('sensor.pool_tank_fill_percentage') }}%)"
```

### High Consumption Alert
```yaml
automation:
  - alias: "High Daily Water Consumption"
    trigger:
      platform: numeric_state
      entity_id: sensor.pool_tank_consumption_day
      above: 500
    action:
      service: notify.notify
      data:
        message: "High water consumption today: {{ states('sensor.pool_tank_consumption_day') }}L"
```

### Auto-refill Based on Level
```yaml
automation:
  - alias: "Auto Refill Pool Tank"
    trigger:
      platform: numeric_state
      entity_id: sensor.pool_tank_fill_percentage
      below: 30
    condition:
      condition: state
      entity_id: binary_sensor.pool_tank_connection_status
      state: 'on'
    action:
      service: switch.turn_on
      entity_id: switch.pool_tank_relay

  - alias: "Stop Refill Pool Tank"
    trigger:
      platform: numeric_state
      entity_id: sensor.pool_tank_fill_percentage
      above: 90
    action:
      service: switch.turn_off
      entity_id: switch.pool_tank_relay
```

## Dashboard Card Examples

### Liquid Level Card
```yaml
type: entities
entities:
  - entity: sensor.pool_tank_fill_percentage
    name: Fill Level
  - entity: sensor.pool_tank_current_volume
    name: Current Volume
  - entity: sensor.pool_tank_liquid_height
    name: Liquid Height
  - entity: binary_sensor.pool_tank_connection_status
    name: Online
  - entity: switch.pool_tank_relay
    name: Refill Pump
title: Pool Tank Status
```

### Consumption Tracking
```yaml
type: statistics-graph
entities:
  - sensor.pool_tank_consumption_day
  - sensor.pool_tank_consumption_week
  - sensor.pool_tank_consumption_month
title: Water Consumption
chart_type: line
period: day
```

## Service Call Examples

### Refresh Device Data
```yaml
service: gobzigh.refresh_device
data:
  device_id: "b0b21c51a460"
```

### Control Relay
```yaml
service: gobzigh.control_relay
data:
  device_id: "b0b21c51a460"
  state: true  # Turn on
```

## Template Sensors for Advanced Calculations

### Refill Time Estimate
```yaml
template:
  - sensor:
      - name: "Pool Tank Refill Time"
        unit_of_measurement: "min"
        state: >
          {% set current = states('sensor.pool_tank_current_volume') | float %}
          {% set max_vol = states('sensor.pool_tank_max_volume') | float %}
          {% set rate = 0.1 %}  # Refill rate in m³/min
          {% if max_vol > current and rate > 0 %}
            {{ ((max_vol - current) / rate) | round(0) }}
          {% else %}
            0
          {% endif %}
```

### Efficiency Tracking
```yaml
template:
  - sensor:
      - name: "Pool Tank Efficiency"
        unit_of_measurement: "%"
        state: >
          {% set daily = states('sensor.pool_tank_consumption_day') | float %}
          {% set capacity = states('sensor.pool_tank_max_volume') | float * 1000 %}  # Convert to liters
          {% if capacity > 0 %}
            {{ (100 - (daily / capacity * 100)) | round(1) }}
          {% else %}
            100
          {% endif %}
```

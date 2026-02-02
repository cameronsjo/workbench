# HAP Characteristics Reference

Comprehensive reference for HomeKit Accessory Protocol (HAP) characteristics in HAP-NodeJS.

## Overview

Characteristics represent individual data points within a service. Each characteristic has a UUID, value format, permissions, and optional constraints (min/max values, valid values, etc.).

**HAP-NodeJS Access**: `hap.Characteristic.<Name>` or `Characteristic.<Name>`

**UUID Base**: `0000XXXX-0000-1000-8000-0026BB765291` (where XXXX is the short UUID in hex)

---

## Value Formats

| Format | Description | HAP-NodeJS Constant |
|--------|-------------|---------------------|
| `bool` | Boolean true/false | `Formats.BOOL` |
| `uint8` | Unsigned 8-bit integer (0-255) | `Formats.UINT8` |
| `uint16` | Unsigned 16-bit integer (0-65535) | `Formats.UINT16` |
| `uint32` | Unsigned 32-bit integer | `Formats.UINT32` |
| `uint64` | Unsigned 64-bit integer | `Formats.UINT64` |
| `int` | Signed 32-bit integer | `Formats.INT` |
| `float` | 32-bit floating point | `Formats.FLOAT` |
| `string` | UTF-8 string (max 256 bytes) | `Formats.STRING` |
| `tlv8` | Base64-encoded TLV8 data | `Formats.TLV8` |
| `data` | Base64-encoded binary data | `Formats.DATA` |

---

## Permissions

| Permission | Description | HAP-NodeJS Constant |
|------------|-------------|---------------------|
| Paired Read | Readable by paired controllers | `Perms.PAIRED_READ` |
| Paired Write | Writable by paired controllers | `Perms.PAIRED_WRITE` |
| Notify/Events | Supports event notifications | `Perms.NOTIFY` or `Perms.EVENTS` |
| Timed Write | Requires timed write procedure | `Perms.TIMED_WRITE` |
| Write Response | Returns response on write | `Perms.WRITE_RESPONSE` |
| Hidden | Hidden from user interface | `Perms.HIDDEN` |
| Additional Authorization | Requires extra auth | `Perms.ADDITIONAL_AUTHORIZATION` |

**Common Permission Combinations**:
- Read-only: `[PAIRED_READ, NOTIFY]`
- Read-write: `[PAIRED_READ, PAIRED_WRITE, NOTIFY]`
- Write-only: `[PAIRED_WRITE]`

---

## Units

| Unit | Description | HAP-NodeJS Constant |
|------|-------------|---------------------|
| Celsius | Temperature in Celsius | `Units.CELSIUS` |
| Percentage | Percentage (0-100) | `Units.PERCENTAGE` |
| Arc Degrees | Angle in degrees (0-360) | `Units.ARC_DEGREE` |
| Lux | Light level in lux | `Units.LUX` |
| Seconds | Time in seconds | `Units.SECONDS` |

---

## State Characteristics

### On

**UUID**: `00000025-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.On`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Paired Write, Notify |

**Values**: `true` = on, `false` = off

**Used By**: Switch, Outlet, Lightbulb, Fan

**HomeKit Behavior**: Primary control for power state. Siri responds to "turn on/off" commands.

---

### Active

**UUID**: `000000B0-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Active`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Inactive, 1 = Active |

**Used By**: AirPurifier, HeaterCooler, HumidifierDehumidifier, Fanv2, Television, Valve

**HomeKit Behavior**: Used for devices with more complex state machines than simple on/off.

---

### InUse

**UUID**: `000000D2-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.InUse`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not In Use, 1 = In Use |

**Used By**: Valve, IrrigationSystem

**HomeKit Behavior**: Indicates whether water is actually flowing (vs. just being active/open).

---

### OutletInUse

**UUID**: `00000026-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.OutletInUse`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Notify |

**Used By**: Outlet

**HomeKit Behavior**: Indicates if something is plugged into the outlet and drawing power.

---

### IsConfigured

**UUID**: `000000D6-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.IsConfigured`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Not Configured, 1 = Configured |

**Used By**: Valve, InputSource

**HomeKit Behavior**: Controls whether the service appears in Home app.

---

## Lighting Characteristics

### Brightness

**UUID**: `00000008-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Brightness`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |
| Min Step | 1 |

**Used By**: Lightbulb, Doorbell

**HomeKit Behavior**: Controls light intensity. Siri responds to "dim" and percentage commands.

---

### Hue

**UUID**: `00000013-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Hue`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | arcdegrees |
| Min Value | 0 |
| Max Value | 360 |
| Min Step | 1 |

**Used By**: Lightbulb

**HomeKit Behavior**: Color hue on color wheel. Used with Saturation for full color control. Siri responds to color names.

---

### Saturation

**UUID**: `0000002F-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Saturation`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |
| Min Step | 1 |

**Used By**: Lightbulb

**HomeKit Behavior**: Color saturation. 0 = white, 100 = fully saturated color.

---

### ColorTemperature

**UUID**: `000000CE-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ColorTemperature`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Paired Write, Notify |
| Min Value | 140 (7142K - cool) |
| Max Value | 500 (2000K - warm) |
| Min Step | 1 |

**Used By**: Lightbulb

**HomeKit Behavior**: Color temperature in mireds (micro reciprocal degrees). Lower = cooler/bluer, higher = warmer/yellower.

---

### CurrentAmbientLightLevel

**UUID**: `0000006B-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentAmbientLightLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Unit | lux |
| Min Value | 0.0001 |
| Max Value | 100000 |

**Used By**: LightSensor

**HomeKit Behavior**: Reports ambient light level for automation triggers.

---

## Temperature Characteristics

### CurrentTemperature

**UUID**: `00000011-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentTemperature`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Unit | celsius |
| Min Value | -270 |
| Max Value | 100 |
| Min Step | 0.1 |

**Used By**: Thermostat, TemperatureSensor, HeaterCooler

**HomeKit Behavior**: Reports current temperature. Home app displays in user's preferred unit.

---

### TargetTemperature

**UUID**: `00000035-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetTemperature`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | celsius |
| Min Value | 10 |
| Max Value | 38 |
| Min Step | 0.1 |

**Used By**: Thermostat

**HomeKit Behavior**: Sets desired temperature. Siri responds to "set temperature to X degrees".

---

### TemperatureDisplayUnits

**UUID**: `00000036-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TemperatureDisplayUnits`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Celsius, 1 = Fahrenheit |

**Used By**: Thermostat, HeaterCooler

**HomeKit Behavior**: Sets display preference on physical device (not Home app).

---

### CoolingThresholdTemperature

**UUID**: `0000000D-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CoolingThresholdTemperature`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | celsius |
| Min Value | 10 |
| Max Value | 35 |
| Min Step | 0.1 |

**Used By**: Thermostat, HeaterCooler

**HomeKit Behavior**: Temperature above which cooling activates (in Auto mode).

---

### HeatingThresholdTemperature

**UUID**: `00000012-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.HeatingThresholdTemperature`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | celsius |
| Min Value | 0 |
| Max Value | 25 |
| Min Step | 0.1 |

**Used By**: Thermostat, HeaterCooler

**HomeKit Behavior**: Temperature below which heating activates (in Auto mode).

---

### CurrentHeatingCoolingState

**UUID**: `0000000F-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentHeatingCoolingState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Off, 1 = Heat, 2 = Cool |

**Used By**: Thermostat

**HomeKit Behavior**: Reports what the thermostat is currently doing.

---

### TargetHeatingCoolingState

**UUID**: `00000033-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetHeatingCoolingState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Off, 1 = Heat, 2 = Cool, 3 = Auto |

**Used By**: Thermostat

**HomeKit Behavior**: Sets desired operating mode. Siri responds to "set to heat/cool/auto".

---

### CurrentHeaterCoolerState

**UUID**: `000000B1-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentHeaterCoolerState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Inactive, 1 = Idle, 2 = Heating, 3 = Cooling |

**Used By**: HeaterCooler

**HomeKit Behavior**: Reports current operational state.

---

### TargetHeaterCoolerState

**UUID**: `000000B2-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetHeaterCoolerState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Auto, 1 = Heat, 2 = Cool |

**Used By**: HeaterCooler

**HomeKit Behavior**: Sets desired mode for standalone heater/cooler devices.

---

## Humidity Characteristics

### CurrentRelativeHumidity

**UUID**: `00000010-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentRelativeHumidity`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |
| Min Step | 1 |

**Used By**: HumiditySensor, Thermostat, HumidifierDehumidifier

**HomeKit Behavior**: Reports current humidity level.

---

### TargetRelativeHumidity

**UUID**: `00000034-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetRelativeHumidity`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |
| Min Step | 1 |

**Used By**: Thermostat, HumidifierDehumidifier

**HomeKit Behavior**: Sets desired humidity level.

---

### RelativeHumidityHumidifierThreshold

**UUID**: `000000C9-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.RelativeHumidityHumidifierThreshold`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: HumidifierDehumidifier

**HomeKit Behavior**: Humidity level below which humidifying activates (in Auto mode).

---

### RelativeHumidityDehumidifierThreshold

**UUID**: `000000C8-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.RelativeHumidityDehumidifierThreshold`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: HumidifierDehumidifier

**HomeKit Behavior**: Humidity level above which dehumidifying activates (in Auto mode).

---

### CurrentHumidifierDehumidifierState

**UUID**: `000000B3-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentHumidifierDehumidifierState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Inactive, 1 = Idle, 2 = Humidifying, 3 = Dehumidifying |

**Used By**: HumidifierDehumidifier

---

### TargetHumidifierDehumidifierState

**UUID**: `000000B4-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetHumidifierDehumidifierState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Humidifier or Dehumidifier, 1 = Humidifier, 2 = Dehumidifier |

**Used By**: HumidifierDehumidifier

---

## Air Quality Characteristics

### AirQuality

**UUID**: `00000095-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.AirQuality`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Unknown, 1 = Excellent, 2 = Good, 3 = Fair, 4 = Inferior, 5 = Poor |

**Used By**: AirQualitySensor

**HomeKit Behavior**: Overall air quality index shown in Home app.

---

### PM2_5Density

**UUID**: `000000C6-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.PM2_5Density`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1000 |

**Used By**: AirQualitySensor

**HomeKit Behavior**: Fine particulate matter (PM2.5) in micrograms per cubic meter.

---

### PM10Density

**UUID**: `000000C7-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.PM10Density`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1000 |

**Used By**: AirQualitySensor

**HomeKit Behavior**: Coarse particulate matter (PM10) in micrograms per cubic meter.

---

### VOCDensity

**UUID**: `000000C8-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.VOCDensity`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1000 |

**Used By**: AirQualitySensor

**HomeKit Behavior**: Volatile organic compounds in micrograms per cubic meter.

---

### OzoneDensity

**UUID**: `000000C3-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.OzoneDensity`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1000 |

**Used By**: AirQualitySensor

---

### NitrogenDioxideDensity

**UUID**: `000000C4-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.NitrogenDioxideDensity`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1000 |

**Used By**: AirQualitySensor

---

### SulphurDioxideDensity

**UUID**: `000000C5-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SulphurDioxideDensity`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1000 |

**Used By**: AirQualitySensor

---

### CarbonDioxideDetected

**UUID**: `00000092-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CarbonDioxideDetected`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Normal, 1 = Abnormal |

**Used By**: CarbonDioxideSensor

**HomeKit Behavior**: Triggers critical notification when abnormal.

---

### CarbonDioxideLevel

**UUID**: `00000093-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CarbonDioxideLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 100000 |

**Used By**: CarbonDioxideSensor, AirQualitySensor

**HomeKit Behavior**: CO2 level in parts per million (ppm).

---

### CarbonDioxidePeakLevel

**UUID**: `00000094-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CarbonDioxidePeakLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 100000 |

**Used By**: CarbonDioxideSensor

---

### CarbonMonoxideDetected

**UUID**: `00000069-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CarbonMonoxideDetected`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Normal, 1 = Abnormal |

**Used By**: CarbonMonoxideSensor

**HomeKit Behavior**: Triggers critical notification when abnormal.

---

### CarbonMonoxideLevel

**UUID**: `00000090-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CarbonMonoxideLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: CarbonMonoxideSensor, AirQualitySensor

**HomeKit Behavior**: CO level in parts per million (ppm).

---

### CarbonMonoxidePeakLevel

**UUID**: `00000091-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CarbonMonoxidePeakLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: CarbonMonoxideSensor

---

### CurrentAirPurifierState

**UUID**: `000000A9-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentAirPurifierState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Inactive, 1 = Idle, 2 = Purifying Air |

**Used By**: AirPurifier

---

### TargetAirPurifierState

**UUID**: `000000A8-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetAirPurifierState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Manual, 1 = Auto |

**Used By**: AirPurifier

---

### FilterChangeIndication

**UUID**: `000000AC-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.FilterChangeIndication`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Filter OK, 1 = Change Filter |

**Used By**: FilterMaintenance

**HomeKit Behavior**: Triggers maintenance notification when filter needs changing.

---

### FilterLifeLevel

**UUID**: `000000AB-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.FilterLifeLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: FilterMaintenance

**HomeKit Behavior**: Remaining filter life as percentage.

---

### ResetFilterIndication

**UUID**: `000000AD-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ResetFilterIndication`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Write |
| Min Value | 1 |
| Max Value | 1 |

**Used By**: FilterMaintenance

**HomeKit Behavior**: Write-only characteristic to reset filter life counter.

---

## Security Characteristics

### SecuritySystemCurrentState

**UUID**: `00000066-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SecuritySystemCurrentState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Stay Arm, 1 = Away Arm, 2 = Night Arm, 3 = Disarmed, 4 = Alarm Triggered |

**Used By**: SecuritySystem

**HomeKit Behavior**: Reports current alarm state. State 4 triggers critical notification.

---

### SecuritySystemTargetState

**UUID**: `00000067-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SecuritySystemTargetState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Stay Arm, 1 = Away Arm, 2 = Night Arm, 3 = Disarm |

**Used By**: SecuritySystem

**HomeKit Behavior**: Sets desired alarm state. Siri responds to "arm/disarm" commands.

---

### SecuritySystemAlarmType

**UUID**: `0000008E-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SecuritySystemAlarmType`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Max Value | 1 |

**Used By**: SecuritySystem

---

### LockCurrentState

**UUID**: `0000001D-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LockCurrentState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Unsecured, 1 = Secured, 2 = Jammed, 3 = Unknown |

**Used By**: LockMechanism

**HomeKit Behavior**: Reports actual lock state. State 2 (Jammed) triggers notification.

---

### LockTargetState

**UUID**: `0000001E-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LockTargetState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Unsecured, 1 = Secured |

**Used By**: LockMechanism

**HomeKit Behavior**: Sets desired lock state. Siri responds to "lock/unlock" commands.

---

### LockControlPoint

**UUID**: `00000019-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LockControlPoint`

| Property | Value |
|----------|-------|
| Format | tlv8 |
| Permissions | Paired Write |

**Used By**: LockManagement

---

### LockManagementAutoSecurityTimeout

**UUID**: `0000001A-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LockManagementAutoSecurityTimeout`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | seconds |

**Used By**: LockManagement

**HomeKit Behavior**: Auto-lock timeout in seconds.

---

### LockLastKnownAction

**UUID**: `0000001C-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LockLastKnownAction`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0-10 (various lock/unlock actions) |

**Used By**: LockManagement

---

### AdministratorOnlyAccess

**UUID**: `00000001-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.AdministratorOnlyAccess`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Paired Write, Notify |

**Used By**: LockManagement

**HomeKit Behavior**: When true, only admin users can control the lock.

---

## Sensor State Characteristics

### MotionDetected

**UUID**: `00000022-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.MotionDetected`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Notify |

**Used By**: MotionSensor

**HomeKit Behavior**: Triggers motion notifications and automations.

---

### OccupancyDetected

**UUID**: `00000071-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.OccupancyDetected`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not Detected, 1 = Detected |

**Used By**: OccupancySensor

**HomeKit Behavior**: Indicates room occupancy for automations.

---

### ContactSensorState

**UUID**: `0000006A-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ContactSensorState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Contact Detected (closed), 1 = Contact Not Detected (open) |

**Used By**: ContactSensor

**HomeKit Behavior**: Reports door/window open/closed state for notifications and automations.

---

### LeakDetected

**UUID**: `00000070-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LeakDetected`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not Detected, 1 = Detected |

**Used By**: LeakSensor

**HomeKit Behavior**: Triggers critical notification when leak detected.

---

### SmokeDetected

**UUID**: `00000076-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SmokeDetected`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not Detected, 1 = Detected |

**Used By**: SmokeSensor

**HomeKit Behavior**: Triggers critical notification when smoke detected.

---

## Door/Window Position Characteristics

### CurrentPosition

**UUID**: `0000006D-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentPosition`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: Door, Window, WindowCovering

**HomeKit Behavior**: Current position where 0 = fully closed, 100 = fully open.

---

### TargetPosition

**UUID**: `0000007C-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetPosition`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: Door, Window, WindowCovering

**HomeKit Behavior**: Sets desired position. Siri responds to percentage commands.

---

### PositionState

**UUID**: `00000072-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.PositionState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Decreasing, 1 = Increasing, 2 = Stopped |

**Used By**: Door, Window, WindowCovering

**HomeKit Behavior**: Reports movement direction.

---

### HoldPosition

**UUID**: `0000006F-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.HoldPosition`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Write |

**Used By**: Door, Window, WindowCovering

**HomeKit Behavior**: Write true to stop movement at current position.

---

### ObstructionDetected

**UUID**: `00000024-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ObstructionDetected`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Notify |

**Used By**: GarageDoorOpener, Door, Window, WindowCovering

**HomeKit Behavior**: Reports if something is blocking the door/window.

---

### CurrentDoorState

**UUID**: `0000000E-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentDoorState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Open, 1 = Closed, 2 = Opening, 3 = Closing, 4 = Stopped |

**Used By**: GarageDoorOpener

**HomeKit Behavior**: Reports garage door state.

---

### TargetDoorState

**UUID**: `00000032-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetDoorState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Open, 1 = Closed |

**Used By**: GarageDoorOpener

**HomeKit Behavior**: Sets desired door state. Siri responds to "open/close garage".

---

### CurrentHorizontalTiltAngle

**UUID**: `0000006C-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentHorizontalTiltAngle`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Notify |
| Unit | arcdegrees |
| Min Value | -90 |
| Max Value | 90 |

**Used By**: WindowCovering, Slats

---

### TargetHorizontalTiltAngle

**UUID**: `0000007B-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetHorizontalTiltAngle`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | arcdegrees |
| Min Value | -90 |
| Max Value | 90 |

**Used By**: WindowCovering, Slats

---

### CurrentVerticalTiltAngle

**UUID**: `0000006E-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentVerticalTiltAngle`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Notify |
| Unit | arcdegrees |
| Min Value | -90 |
| Max Value | 90 |

**Used By**: WindowCovering, Slats

---

### TargetVerticalTiltAngle

**UUID**: `0000007D-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetVerticalTiltAngle`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | arcdegrees |
| Min Value | -90 |
| Max Value | 90 |

**Used By**: WindowCovering, Slats

---

## Fan Characteristics

### RotationDirection

**UUID**: `00000028-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.RotationDirection`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Clockwise, 1 = Counter-clockwise |

**Used By**: Fan, Fanv2

**HomeKit Behavior**: Controls fan rotation direction.

---

### RotationSpeed

**UUID**: `00000029-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.RotationSpeed`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: Fan, Fanv2, AirPurifier, HumidifierDehumidifier

**HomeKit Behavior**: Fan speed as percentage. Siri responds to speed commands.

---

### SwingMode

**UUID**: `000000B6-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SwingMode`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Disabled, 1 = Enabled |

**Used By**: Fanv2, HeaterCooler, HumidifierDehumidifier

**HomeKit Behavior**: Controls oscillation/swing mode.

---

### CurrentFanState

**UUID**: `000000AF-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentFanState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Inactive, 1 = Idle, 2 = Blowing Air |

**Used By**: Fanv2

---

### TargetFanState

**UUID**: `000000BF-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetFanState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Manual, 1 = Auto |

**Used By**: Fanv2

---

### LockPhysicalControls

**UUID**: `000000A7-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.LockPhysicalControls`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Control Lock Disabled, 1 = Control Lock Enabled |

**Used By**: Fanv2, AirPurifier, HeaterCooler, HumidifierDehumidifier

**HomeKit Behavior**: Enables child lock on physical device controls.

---

## Battery Characteristics

### StatusLowBattery

**UUID**: `00000079-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.StatusLowBattery`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Normal, 1 = Low |

**Used By**: Battery, most sensors

**HomeKit Behavior**: Triggers low battery notification.

---

### BatteryLevel

**UUID**: `00000068-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.BatteryLevel`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: Battery

**HomeKit Behavior**: Reports battery percentage.

---

### ChargingState

**UUID**: `0000008F-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ChargingState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not Charging, 1 = Charging, 2 = Not Chargeable |

**Used By**: Battery

**HomeKit Behavior**: Reports charging status.

---

## Status Characteristics

### StatusActive

**UUID**: `00000075-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.StatusActive`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Notify |

**Used By**: Most sensors

**HomeKit Behavior**: Indicates if sensor is actively monitoring.

---

### StatusFault

**UUID**: `00000077-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.StatusFault`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = No Fault, 1 = General Fault |

**Used By**: Most services

**HomeKit Behavior**: Reports device malfunction.

---

### StatusTampered

**UUID**: `0000007A-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.StatusTampered`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not Tampered, 1 = Tampered |

**Used By**: Most sensors

**HomeKit Behavior**: Reports if sensor has been tampered with.

---

## Media Characteristics

### CurrentMediaState

**UUID**: `000000E0-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentMediaState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Play, 1 = Pause, 2 = Stop, 3 = Loading, 4 = Interrupted |

**Used By**: SmartSpeaker, Television

---

### TargetMediaState

**UUID**: `00000137-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetMediaState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Play, 1 = Pause, 2 = Stop |

**Used By**: SmartSpeaker, Television

**HomeKit Behavior**: Controls playback state.

---

### Volume

**UUID**: `00000119-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Volume`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: Speaker, Microphone, SmartSpeaker, TelevisionSpeaker, Doorbell

**HomeKit Behavior**: Controls volume level. Siri responds to volume commands.

---

### Mute

**UUID**: `0000011A-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Mute`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Paired Write, Notify |

**Used By**: Speaker, Microphone, SmartSpeaker, TelevisionSpeaker

**HomeKit Behavior**: Controls mute state.

---

### ProgrammableSwitchEvent

**UUID**: `00000073-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ProgrammableSwitchEvent`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Single Press, 1 = Double Press, 2 = Long Press |

**Used By**: StatelessProgrammableSwitch, Doorbell

**HomeKit Behavior**: Triggers automations based on button press type. **Note**: This is a null-value characteristic - it only sends events, never stores a value.

---

### RemoteKey

**UUID**: `000000E1-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.RemoteKey`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Write |
| Valid Values | 0 = Rewind, 1 = Fast Forward, 2 = Next Track, 3 = Previous Track, 4 = Arrow Up, 5 = Arrow Down, 6 = Arrow Left, 7 = Arrow Right, 8 = Select, 9 = Back, 10 = Exit, 11 = Play/Pause, 15 = Info |

**Used By**: Television

**HomeKit Behavior**: Simulates remote control button presses.

---

## Accessory Information Characteristics

### Identify

**UUID**: `00000014-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Identify`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Write |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Write-only. Causes accessory to identify itself (flash lights, beep, etc.).

---

### Manufacturer

**UUID**: `00000020-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Manufacturer`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |
| Max Length | 64 |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Displayed in accessory details.

---

### Model

**UUID**: `00000021-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Model`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |
| Max Length | 64 |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Displayed in accessory details.

---

### Name

**UUID**: `00000023-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Name`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |
| Max Length | 64 |

**Used By**: AccessoryInformation, most services

**HomeKit Behavior**: Display name in Home app. User can rename accessories.

---

### ConfiguredName

**UUID**: `000000E3-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ConfiguredName`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read, Paired Write, Notify |

**Used By**: Television, InputSource, SmartSpeaker

**HomeKit Behavior**: User-configurable name that persists across resets.

---

### SerialNumber

**UUID**: `00000030-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SerialNumber`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |
| Max Length | 64 |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Displayed in accessory details.

---

### FirmwareRevision

**UUID**: `00000052-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.FirmwareRevision`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Displayed in accessory details. Used for update notifications.

---

### HardwareRevision

**UUID**: `00000053-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.HardwareRevision`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |

**Used By**: AccessoryInformation

---

### Version

**UUID**: `00000037-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Version`

| Property | Value |
|----------|-------|
| Format | string |
| Permissions | Paired Read |
| Max Length | 64 |

**Used By**: ProtocolInformation, LockManagement

---

### AccessoryFlags

**UUID**: `000000A6-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.AccessoryFlags`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Notify |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Bitmask of accessory capabilities.

---

### ProductData

**UUID**: `00000220-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ProductData`

| Property | Value |
|----------|-------|
| Format | data |
| Permissions | Paired Read |

**Used By**: AccessoryInformation

**HomeKit Behavior**: Encrypted product identification data.

---

## Valve/Irrigation Characteristics

### ValveType

**UUID**: `000000D5-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ValveType`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Generic, 1 = Irrigation, 2 = Shower Head, 3 = Water Faucet |

**Used By**: Valve

**HomeKit Behavior**: Determines icon and behavior in Home app.

---

### SetDuration

**UUID**: `000000D3-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SetDuration`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | seconds |
| Min Value | 0 |
| Max Value | 3600 |

**Used By**: Valve

**HomeKit Behavior**: Auto-shutoff duration when valve is activated.

---

### RemainingDuration

**UUID**: `000000D4-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.RemainingDuration`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Notify |
| Unit | seconds |
| Max Value | 3600 |

**Used By**: Valve, IrrigationSystem

**HomeKit Behavior**: Displays countdown timer in Home app.

---

### ProgramMode

**UUID**: `000000D1-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ProgramMode`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = No Program Scheduled, 1 = Program Scheduled, 2 = Program Scheduled (Manual Mode) |

**Used By**: IrrigationSystem

---

### ServiceLabelIndex

**UUID**: `000000CB-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ServiceLabelIndex`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read |
| Min Value | 1 |

**Used By**: StatelessProgrammableSwitch, Valve

**HomeKit Behavior**: Index for multi-button/multi-zone accessories.

---

### ServiceLabelNamespace

**UUID**: `000000CD-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ServiceLabelNamespace`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read |
| Valid Values | 0 = Dots, 1 = Arabic Numerals |

**Used By**: ServiceLabel

**HomeKit Behavior**: Determines label style for indexed services.

---

### WaterLevel

**UUID**: `000000B5-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.WaterLevel`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Unit | percentage |
| Min Value | 0 |
| Max Value | 100 |

**Used By**: HumidifierDehumidifier

**HomeKit Behavior**: Water tank level indicator.

---

## Television/Input Characteristics

### ActiveIdentifier

**UUID**: `000000E7-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ActiveIdentifier`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Paired Write, Notify |
| Min Value | 0 |

**Used By**: Television, TargetControl

**HomeKit Behavior**: Currently selected input source identifier.

---

### Identifier

**UUID**: `000000E6-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Identifier`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read |
| Min Value | 0 |

**Used By**: InputSource

**HomeKit Behavior**: Unique identifier for this input source.

---

### InputSourceType

**UUID**: `000000DB-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.InputSourceType`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Other, 1 = Home Screen, 2 = Tuner, 3 = HDMI, 4 = Composite Video, 5 = S Video, 6 = Component Video, 7 = DVI, 8 = Airplay, 9 = USB, 10 = Application |

**Used By**: InputSource

---

### InputDeviceType

**UUID**: `000000DC-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.InputDeviceType`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Other, 1 = TV, 2 = Recording, 3 = Tuner, 4 = Playback, 5 = Audio System, 6 = Unknown 6 |

**Used By**: InputSource

---

### CurrentVisibilityState

**UUID**: `00000135-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentVisibilityState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Shown, 1 = Hidden |

**Used By**: InputSource

---

### TargetVisibilityState

**UUID**: `00000134-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetVisibilityState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Shown, 1 = Hidden |

**Used By**: InputSource

**HomeKit Behavior**: Controls whether input appears in selection menu.

---

### SleepDiscoveryMode

**UUID**: `000000E8-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SleepDiscoveryMode`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Not Discoverable, 1 = Always Discoverable |

**Used By**: Television

---

### ClosedCaptions

**UUID**: `000000DD-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ClosedCaptions`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Disabled, 1 = Enabled |

**Used By**: Television

---

### PictureMode

**UUID**: `000000E2-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.PictureMode`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0-13 (various picture modes) |

**Used By**: Television

---

### PowerModeSelection

**UUID**: `000000DF-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.PowerModeSelection`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Write |
| Valid Values | 0 = Show, 1 = Hide |

**Used By**: Television

---

## Slat Characteristics

### CurrentSlatState

**UUID**: `000000AA-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentSlatState`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Notify |
| Valid Values | 0 = Fixed, 1 = Jammed, 2 = Swinging |

**Used By**: Slats

---

### SlatType

**UUID**: `000000C0-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SlatType`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read |
| Valid Values | 0 = Horizontal, 1 = Vertical |

**Used By**: Slats

---

### CurrentTiltAngle

**UUID**: `000000C1-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.CurrentTiltAngle`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Notify |
| Unit | arcdegrees |
| Min Value | -90 |
| Max Value | 90 |

**Used By**: Slats

---

### TargetTiltAngle

**UUID**: `000000C2-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.TargetTiltAngle`

| Property | Value |
|----------|-------|
| Format | int |
| Permissions | Paired Read, Paired Write, Notify |
| Unit | arcdegrees |
| Min Value | -90 |
| Max Value | 90 |

**Used By**: Slats

---

## Diagnostics Characteristics

### Ping

**UUID**: `0000023C-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.Ping`

| Property | Value |
|----------|-------|
| Format | data |
| Permissions | Paired Read |

**Used By**: AccessoryRuntimeInformation

**HomeKit Behavior**: Connectivity check.

---

### ActivityInterval

**UUID**: `0000023B-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.ActivityInterval`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Min Step | 1 |

**Used By**: AccessoryRuntimeInformation

---

### HeartBeat

**UUID**: `0000024A-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.HeartBeat`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Notify |

**Used By**: AccessoryRuntimeInformation

**HomeKit Behavior**: Increments periodically to indicate accessory is alive.

---

### SleepInterval

**UUID**: `0000023A-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.SleepInterval`

| Property | Value |
|----------|-------|
| Format | uint32 |
| Permissions | Paired Read, Notify |
| Min Value | 0 |
| Min Step | 1 |

**Used By**: AccessoryRuntimeInformation

---

## Audio/Video Configuration Characteristics

### AudioFeedback

**UUID**: `00000005-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.AudioFeedback`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Paired Write, Notify |

**Used By**: LockManagement

**HomeKit Behavior**: Enables/disables audio feedback on lock operations.

---

### NightVision

**UUID**: `0000011B-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.NightVision`

| Property | Value |
|----------|-------|
| Format | bool |
| Permissions | Paired Read, Paired Write, Notify |

**Used By**: CameraOperatingMode

**HomeKit Behavior**: Controls infrared night vision mode.

---

### DiagonalFieldOfView

**UUID**: `00000224-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.DiagonalFieldOfView`

| Property | Value |
|----------|-------|
| Format | float |
| Permissions | Paired Read, Notify |
| Unit | arcdegrees |
| Min Value | 0 |
| Max Value | 360 |

**Used By**: CameraOperatingMode

---

### HomeKitCameraActive

**UUID**: `0000021B-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.HomeKitCameraActive`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Off, 1 = On |

**Used By**: CameraOperatingMode

---

### EventSnapshotsActive

**UUID**: `00000223-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.EventSnapshotsActive`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Disable, 1 = Enable |

**Used By**: CameraOperatingMode

---

### PeriodicSnapshotsActive

**UUID**: `00000225-0000-1000-8000-0026BB765291`
**Constant**: `Characteristic.PeriodicSnapshotsActive`

| Property | Value |
|----------|-------|
| Format | uint8 |
| Permissions | Paired Read, Paired Write, Notify |
| Valid Values | 0 = Disable, 1 = Enable |

**Used By**: CameraOperatingMode

---

## Setting Characteristic Properties

Use `setProps()` to customize characteristic constraints:

```typescript
service.getCharacteristic(Characteristic.CurrentTemperature)
  .setProps({
    minValue: -40,
    maxValue: 60,
    minStep: 0.5
  });
```

### Available Props

```typescript
interface CharacteristicProps {
  format: Formats;
  unit?: Units;
  perms: Perms[];
  minValue?: number;
  maxValue?: number;
  minStep?: number;
  maxLen?: number;
  validValues?: number[];
  validValueRanges?: [number, number];
  adminOnlyAccess?: Access[];
}
```

---

## References

- [HAP-NodeJS GitHub Repository](https://github.com/homebridge/HAP-NodeJS)
- [HAP-NodeJS Characteristic Class](https://developers.homebridge.io/HAP-NodeJS/classes/Characteristic.html)
- [CharacteristicDefinitions.ts](https://github.com/homebridge/HAP-NodeJS/blob/latest/src/lib/definitions/CharacteristicDefinitions.ts)
- [Apple HomeKit Developer Documentation](https://developer.apple.com/documentation/homekit)
- [esp-homekit Characteristics Reference](https://github.com/maximkulkin/esp-homekit/blob/master/include/homekit/characteristics.h)

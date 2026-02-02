# HAP Services Reference

Comprehensive reference for HomeKit Accessory Protocol (HAP) services in HAP-NodeJS.

## Overview

Services group functionality to provide context for accessories. Each service contains required and optional characteristics. HAP enforces a limit of 100 services per accessory and 100 characteristics per service.

**HAP-NodeJS Access**: `hap.Service.<ServiceName>` or `Service.<ServiceName>`

**UUID Base**: `0000XXXX-0000-1000-8000-0026BB765291` (where XXXX is the short UUID)

---

## Lighting Services

### Lightbulb

**UUID**: `00000043-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Lightbulb`

Controls light fixtures including dimmable and color-changing bulbs.

| Characteristic | Required | Type |
|----------------|----------|------|
| On | Yes | bool |
| Brightness | No | uint8 (0-100%) |
| Hue | No | float (0-360 arc degrees) |
| Saturation | No | float (0-100%) |
| ColorTemperature | No | uint32 (140-500 mireds) |
| Name | No | string |

**Use Cases**: Ceiling lights, lamps, LED strips, smart bulbs (Hue, LIFX)

### LightSensor

**UUID**: `00000084-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.LightSensor`

Reports ambient light levels.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentAmbientLightLevel | Yes | float (0.0001-100000 lux) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Light sensors for automation triggers, daylight detection

---

## Climate Services

### Thermostat

**UUID**: `0000004A-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Thermostat`

Controls heating and cooling systems.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentHeatingCoolingState | Yes | uint8 (0=Off, 1=Heat, 2=Cool) |
| TargetHeatingCoolingState | Yes | uint8 (0=Off, 1=Heat, 2=Cool, 3=Auto) |
| CurrentTemperature | Yes | float (-270 to 100 Celsius) |
| TargetTemperature | Yes | float (10-38 Celsius) |
| TemperatureDisplayUnits | Yes | uint8 (0=Celsius, 1=Fahrenheit) |
| CoolingThresholdTemperature | No | float |
| HeatingThresholdTemperature | No | float |
| CurrentRelativeHumidity | No | float (0-100%) |
| TargetRelativeHumidity | No | float (0-100%) |
| Name | No | string |

**Use Cases**: HVAC systems, smart thermostats (Nest, Ecobee)

### HeaterCooler

**UUID**: `000000BC-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.HeaterCooler`

Controls standalone heating/cooling devices.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 (0=Inactive, 1=Active) |
| CurrentHeaterCoolerState | Yes | uint8 (0=Inactive, 1=Idle, 2=Heating, 3=Cooling) |
| TargetHeaterCoolerState | Yes | uint8 (0=Auto, 1=Heat, 2=Cool) |
| CurrentTemperature | Yes | float |
| CoolingThresholdTemperature | No | float |
| HeatingThresholdTemperature | No | float |
| RotationSpeed | No | float |
| SwingMode | No | uint8 |
| TemperatureDisplayUnits | No | uint8 |
| LockPhysicalControls | No | uint8 |
| Name | No | string |

**Use Cases**: Space heaters, portable AC units, mini-splits

### HumidifierDehumidifier

**UUID**: `000000BD-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.HumidifierDehumidifier`

Controls humidity devices.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 |
| CurrentHumidifierDehumidifierState | Yes | uint8 (0=Inactive, 1=Idle, 2=Humidifying, 3=Dehumidifying) |
| TargetHumidifierDehumidifierState | Yes | uint8 (0=Auto, 1=Humidify, 2=Dehumidify) |
| CurrentRelativeHumidity | Yes | float (0-100%) |
| RelativeHumidityHumidifierThreshold | No | float |
| RelativeHumidityDehumidifierThreshold | No | float |
| RotationSpeed | No | float |
| SwingMode | No | uint8 |
| WaterLevel | No | float |
| LockPhysicalControls | No | uint8 |
| Name | No | string |

**Use Cases**: Humidifiers, dehumidifiers, combo units

### TemperatureSensor

**UUID**: `0000008A-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.TemperatureSensor`

Reports temperature readings.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentTemperature | Yes | float (-270 to 100 Celsius) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Room temperature sensors, outdoor thermometers

### HumiditySensor

**UUID**: `00000082-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.HumiditySensor`

Reports humidity levels.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentRelativeHumidity | Yes | float (0-100%) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Humidity sensors, weather stations

---

## Air Quality Services

### AirPurifier

**UUID**: `000000BB-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AirPurifier`

Controls air purification devices.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 (0=Inactive, 1=Active) |
| CurrentAirPurifierState | Yes | uint8 (0=Inactive, 1=Idle, 2=Purifying) |
| TargetAirPurifierState | Yes | uint8 (0=Manual, 1=Auto) |
| RotationSpeed | No | float (0-100%) |
| SwingMode | No | uint8 |
| LockPhysicalControls | No | uint8 |
| Name | No | string |

**Use Cases**: Air purifiers, HEPA filter systems

**Linked Services**: FilterMaintenance, AirQualitySensor, Fan

### AirQualitySensor

**UUID**: `0000008D-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AirQualitySensor`

Reports air quality metrics.

| Characteristic | Required | Type |
|----------------|----------|------|
| AirQuality | Yes | uint8 (0=Unknown, 1=Excellent, 2=Good, 3=Fair, 4=Inferior, 5=Poor) |
| OzoneDensity | No | float (0-1000 ug/m3) |
| NitrogenDioxideDensity | No | float (0-1000 ug/m3) |
| SulphurDioxideDensity | No | float (0-1000 ug/m3) |
| PM2_5Density | No | float (0-1000 ug/m3) |
| PM10Density | No | float (0-1000 ug/m3) |
| VOCDensity | No | float (0-1000 ug/m3) |
| CarbonMonoxideLevel | No | float |
| CarbonDioxideLevel | No | float |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Air quality monitors, environmental sensors

### FilterMaintenance

**UUID**: `000000BA-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.FilterMaintenance`

Tracks filter status and maintenance needs.

| Characteristic | Required | Type |
|----------------|----------|------|
| FilterChangeIndication | Yes | uint8 (0=No Change, 1=Change Filter) |
| FilterLifeLevel | No | float (0-100%) |
| ResetFilterIndication | No | uint8 |
| Name | No | string |

**Use Cases**: HVAC filters, purifier filters, vacuum filters

---

## Fan Services

### Fan

**UUID**: `00000040-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Fan`

Basic fan control (legacy service).

| Characteristic | Required | Type |
|----------------|----------|------|
| On | Yes | bool |
| RotationDirection | No | int (0=Clockwise, 1=Counter-clockwise) |
| RotationSpeed | No | float (0-100%) |
| Name | No | string |

**Use Cases**: Simple fans without advanced features

### Fanv2

**UUID**: `000000B7-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Fanv2`

Advanced fan control with more features.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 (0=Inactive, 1=Active) |
| CurrentFanState | No | uint8 (0=Inactive, 1=Idle, 2=Blowing) |
| TargetFanState | No | uint8 (0=Manual, 1=Auto) |
| RotationDirection | No | int |
| RotationSpeed | No | float |
| SwingMode | No | uint8 (0=Disabled, 1=Enabled) |
| LockPhysicalControls | No | uint8 |
| Name | No | string |

**Use Cases**: Ceiling fans, tower fans, fans with oscillation

---

## Security Services

### SecuritySystem

**UUID**: `0000007E-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.SecuritySystem`

Controls security alarm systems.

| Characteristic | Required | Type |
|----------------|----------|------|
| SecuritySystemCurrentState | Yes | uint8 (0=StayArm, 1=AwayArm, 2=NightArm, 3=Disarmed, 4=AlarmTriggered) |
| SecuritySystemTargetState | Yes | uint8 (0=StayArm, 1=AwayArm, 2=NightArm, 3=Disarm) |
| SecuritySystemAlarmType | No | uint8 |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| Name | No | string |

**Use Cases**: Home security systems, alarm panels

### LockMechanism

**UUID**: `00000045-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.LockMechanism`

Controls physical lock mechanisms.

| Characteristic | Required | Type |
|----------------|----------|------|
| LockCurrentState | Yes | uint8 (0=Unsecured, 1=Secured, 2=Jammed, 3=Unknown) |
| LockTargetState | Yes | uint8 (0=Unsecured, 1=Secured) |
| Name | No | string |

**Use Cases**: Smart locks, deadbolts, door locks

### LockManagement

**UUID**: `00000044-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.LockManagement`

Manages lock configuration and access codes.

| Characteristic | Required | Type |
|----------------|----------|------|
| LockControlPoint | Yes | tlv8 |
| Version | Yes | string |
| Logs | No | tlv8 |
| AudioFeedback | No | bool |
| LockManagementAutoSecurityTimeout | No | uint32 |
| AdministratorOnlyAccess | No | bool |
| LockLastKnownAction | No | uint8 |
| CurrentDoorState | No | uint8 |
| MotionDetected | No | bool |
| Name | No | string |

**Use Cases**: Lock administration, access logs, auto-lock settings

### AccessCode

**UUID**: `00000260-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AccessCode`

Manages access codes for locks (iOS 15+).

| Characteristic | Required | Type |
|----------------|----------|------|
| AccessCodeControlPoint | Yes | tlv8 |
| AccessCodeSupportedConfiguration | Yes | tlv8 |
| ConfigurationState | Yes | uint16 |

**Use Cases**: PIN code management for smart locks

### NFCAccess

**UUID**: `00000266-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.NFCAccess`

Manages NFC-based access (iOS 15+).

| Characteristic | Required | Type |
|----------------|----------|------|
| NFCAccessControlPoint | Yes | tlv8 |
| NFCAccessSupportedConfiguration | Yes | tlv8 |
| ConfigurationState | Yes | uint16 |

**Use Cases**: NFC key cards, digital keys

---

## Sensor Services

### MotionSensor

**UUID**: `00000085-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.MotionSensor`

Detects motion events.

| Characteristic | Required | Type |
|----------------|----------|------|
| MotionDetected | Yes | bool |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: PIR sensors, motion detectors for automation

### OccupancySensor

**UUID**: `00000086-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.OccupancySensor`

Detects room occupancy.

| Characteristic | Required | Type |
|----------------|----------|------|
| OccupancyDetected | Yes | uint8 (0=NotDetected, 1=Detected) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Presence detection, room occupancy tracking

### ContactSensor

**UUID**: `00000080-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.ContactSensor`

Detects contact state (open/closed).

| Characteristic | Required | Type |
|----------------|----------|------|
| ContactSensorState | Yes | uint8 (0=Detected/Closed, 1=NotDetected/Open) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Door/window sensors, cabinet sensors

### LeakSensor

**UUID**: `00000083-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.LeakSensor`

Detects water leaks.

| Characteristic | Required | Type |
|----------------|----------|------|
| LeakDetected | Yes | uint8 (0=NotDetected, 1=Detected) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Water leak sensors, flood detection

### SmokeSensor

**UUID**: `00000087-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.SmokeSensor`

Detects smoke.

| Characteristic | Required | Type |
|----------------|----------|------|
| SmokeDetected | Yes | uint8 (0=NotDetected, 1=Detected) |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: Smoke detectors, fire alarms

### CarbonMonoxideSensor

**UUID**: `0000007F-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.CarbonMonoxideSensor`

Detects carbon monoxide.

| Characteristic | Required | Type |
|----------------|----------|------|
| CarbonMonoxideDetected | Yes | uint8 (0=Normal, 1=Abnormal) |
| CarbonMonoxideLevel | No | float (0-100 ppm) |
| CarbonMonoxidePeakLevel | No | float |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: CO detectors, combo smoke/CO alarms

### CarbonDioxideSensor

**UUID**: `00000097-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.CarbonDioxideSensor`

Detects carbon dioxide levels.

| Characteristic | Required | Type |
|----------------|----------|------|
| CarbonDioxideDetected | Yes | uint8 (0=Normal, 1=Abnormal) |
| CarbonDioxideLevel | No | float (0-100000 ppm) |
| CarbonDioxidePeakLevel | No | float |
| StatusActive | No | bool |
| StatusFault | No | uint8 |
| StatusTampered | No | uint8 |
| StatusLowBattery | No | uint8 |
| Name | No | string |

**Use Cases**: CO2 monitors, indoor air quality sensors

---

## Door and Window Services

### Door

**UUID**: `00000081-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Door`

Controls motorized doors.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentPosition | Yes | uint8 (0-100%, 0=closed) |
| TargetPosition | Yes | uint8 (0-100%) |
| PositionState | Yes | uint8 (0=Decreasing, 1=Increasing, 2=Stopped) |
| HoldPosition | No | bool |
| ObstructionDetected | No | bool |
| Name | No | string |

**Use Cases**: Motorized doors, automated entry doors

### Window

**UUID**: `0000008B-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Window`

Controls motorized windows.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentPosition | Yes | uint8 (0-100%) |
| TargetPosition | Yes | uint8 (0-100%) |
| PositionState | Yes | uint8 |
| HoldPosition | No | bool |
| ObstructionDetected | No | bool |
| Name | No | string |

**Use Cases**: Motorized windows, skylights

### WindowCovering

**UUID**: `0000008C-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.WindowCovering`

Controls blinds, shades, and curtains.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentPosition | Yes | uint8 (0-100%) |
| TargetPosition | Yes | uint8 (0-100%) |
| PositionState | Yes | uint8 |
| HoldPosition | No | bool |
| CurrentHorizontalTiltAngle | No | int (-90 to 90) |
| TargetHorizontalTiltAngle | No | int |
| CurrentVerticalTiltAngle | No | int |
| TargetVerticalTiltAngle | No | int |
| ObstructionDetected | No | bool |
| Name | No | string |

**Use Cases**: Blinds, shades, curtains, shutters

### GarageDoorOpener

**UUID**: `00000041-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.GarageDoorOpener`

Controls garage doors.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentDoorState | Yes | uint8 (0=Open, 1=Closed, 2=Opening, 3=Closing, 4=Stopped) |
| TargetDoorState | Yes | uint8 (0=Open, 1=Closed) |
| ObstructionDetected | Yes | bool |
| LockCurrentState | No | uint8 |
| LockTargetState | No | uint8 |
| Name | No | string |

**Use Cases**: Garage door openers, carport gates

### Slats

**UUID**: `000000B9-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Slats`

Controls slat/louver angle.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentSlatState | Yes | uint8 (0=Fixed, 1=Jammed, 2=Swinging) |
| SlatType | Yes | uint8 (0=Horizontal, 1=Vertical) |
| CurrentTiltAngle | No | int (-90 to 90) |
| TargetTiltAngle | No | int |
| SwingMode | No | uint8 |
| Name | No | string |

**Use Cases**: Louvers, vents, adjustable blinds

---

## Switch and Outlet Services

### Switch

**UUID**: `00000049-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Switch`

Simple on/off control.

| Characteristic | Required | Type |
|----------------|----------|------|
| On | Yes | bool |
| Name | No | string |

**Use Cases**: Generic switches, relays, any on/off device

### Outlet

**UUID**: `00000047-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Outlet`

Controls power outlets.

| Characteristic | Required | Type |
|----------------|----------|------|
| On | Yes | bool |
| OutletInUse | Yes | bool |
| Name | No | string |

**Use Cases**: Smart plugs, power strips, wall outlets

### StatelessProgrammableSwitch

**UUID**: `00000089-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.StatelessProgrammableSwitch`

Button that triggers events without maintaining state.

| Characteristic | Required | Type |
|----------------|----------|------|
| ProgrammableSwitchEvent | Yes | uint8 (0=Single, 1=Double, 2=Long) |
| ServiceLabelIndex | No | uint8 |
| Name | No | string |

**Use Cases**: Remote buttons, wall switches, scene controllers

### StatefulProgrammableSwitch

**UUID**: `00000088-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.StatefulProgrammableSwitch`

Button that maintains on/off state.

| Characteristic | Required | Type |
|----------------|----------|------|
| ProgrammableSwitchEvent | Yes | uint8 |
| ProgrammableSwitchOutputState | Yes | uint8 |
| Name | No | string |

**Use Cases**: Toggle switches, latching buttons

---

## Camera Services

### CameraRTPStreamManagement

**UUID**: `00000110-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.CameraRTPStreamManagement`

Manages live video streaming.

| Characteristic | Required | Type |
|----------------|----------|------|
| SupportedVideoStreamConfiguration | Yes | tlv8 |
| SupportedAudioStreamConfiguration | Yes | tlv8 |
| SupportedRTPConfiguration | Yes | tlv8 |
| SelectedRTPStreamConfiguration | Yes | tlv8 |
| StreamingStatus | Yes | tlv8 |
| SetupEndpoints | Yes | tlv8 |

**Use Cases**: Live camera feeds, video doorbells

### CameraRecordingManagement

**UUID**: `00000204-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.CameraRecordingManagement`

Manages HomeKit Secure Video recording.

| Characteristic | Required | Type |
|----------------|----------|------|
| SupportedCameraRecordingConfiguration | Yes | tlv8 |
| SupportedVideoRecordingConfiguration | Yes | tlv8 |
| SupportedAudioRecordingConfiguration | Yes | tlv8 |
| SelectedCameraRecordingConfiguration | Yes | tlv8 |
| RecordingAudioActive | No | uint8 |

**Use Cases**: HomeKit Secure Video cameras

### CameraOperatingMode

**UUID**: `0000021A-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.CameraOperatingMode`

Controls camera operation modes.

| Characteristic | Required | Type |
|----------------|----------|------|
| EventSnapshotsActive | Yes | uint8 |
| HomeKitCameraActive | Yes | uint8 |
| PeriodicSnapshotsActive | No | uint8 |
| CameraOperatingModeIndicator | No | uint8 |
| ThirdPartyCameraActive | No | uint8 |
| ManuallyDisabled | No | uint8 |
| NightVision | No | bool |
| DiagonalFieldOfView | No | float |

**Use Cases**: Camera settings, privacy modes

### Doorbell

**UUID**: `00000121-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Doorbell`

Video doorbell functionality.

| Characteristic | Required | Type |
|----------------|----------|------|
| ProgrammableSwitchEvent | Yes | uint8 |
| Brightness | No | int |
| Volume | No | uint8 |
| Mute | No | bool |
| Name | No | string |

**Use Cases**: Video doorbells (Ring, Nest Hello)

---

## Audio Services

### Speaker

**UUID**: `00000113-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Speaker`

Controls speaker output.

| Characteristic | Required | Type |
|----------------|----------|------|
| Mute | Yes | bool |
| Volume | No | uint8 (0-100%) |
| Name | No | string |

**Use Cases**: Connected speakers, audio receivers

### Microphone

**UUID**: `00000112-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Microphone`

Controls microphone input.

| Characteristic | Required | Type |
|----------------|----------|------|
| Mute | Yes | bool |
| Volume | No | uint8 |
| Name | No | string |

**Use Cases**: Smart speakers with microphones, intercom systems

### SmartSpeaker

**UUID**: `00000228-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.SmartSpeaker`

Controls smart speaker playback.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentMediaState | Yes | uint8 (0=Play, 1=Pause, 2=Stop, 3=Loading, 4=Interrupted) |
| TargetMediaState | Yes | uint8 (0=Play, 1=Pause, 2=Stop) |
| ConfiguredName | No | string |
| Mute | No | bool |
| Volume | No | uint8 |
| Name | No | string |

**Use Cases**: HomePod-like speakers, smart audio systems

### AudioStreamManagement

**UUID**: `00000127-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AudioStreamManagement`

Manages audio streaming sessions.

| Characteristic | Required | Type |
|----------------|----------|------|
| SupportedAudioStreamConfiguration | Yes | tlv8 |
| SelectedAudioStreamConfiguration | Yes | tlv8 |

**Use Cases**: Two-way audio, intercom systems

---

## Television Services

### Television

**UUID**: `000000D8-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Television`

Controls TVs and video devices.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 |
| ActiveIdentifier | Yes | uint32 |
| ConfiguredName | No | string |
| SleepDiscoveryMode | Yes | uint8 |
| RemoteKey | No | uint8 |
| Brightness | No | int |
| ClosedCaptions | No | uint8 |
| DisplayOrder | No | tlv8 |
| CurrentMediaState | No | uint8 |
| TargetMediaState | No | uint8 |
| PictureMode | No | uint8 |
| PowerModeSelection | No | uint8 |

**Use Cases**: Smart TVs, streaming boxes, projectors

### InputSource

**UUID**: `000000D9-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.InputSource`

Represents a TV input source.

| Characteristic | Required | Type |
|----------------|----------|------|
| ConfiguredName | Yes | string |
| InputSourceType | Yes | uint8 |
| IsConfigured | Yes | uint8 |
| CurrentVisibilityState | Yes | uint8 |
| Identifier | No | uint32 |
| InputDeviceType | No | uint8 |
| TargetVisibilityState | No | uint8 |
| Name | No | string |

**Use Cases**: HDMI inputs, apps, streaming services

### TelevisionSpeaker

**UUID**: `00000113-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.TelevisionSpeaker`

Controls TV audio output.

| Characteristic | Required | Type |
|----------------|----------|------|
| Mute | Yes | bool |
| Active | No | uint8 |
| Volume | No | uint8 |
| VolumeControlType | No | uint8 |
| VolumeSelector | No | uint8 |

**Use Cases**: TV volume control, soundbar integration

---

## Water Services

### Valve

**UUID**: `000000D0-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Valve`

Controls water valves.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 |
| InUse | Yes | uint8 |
| ValveType | Yes | uint8 (0=Generic, 1=Irrigation, 2=Shower, 3=Faucet) |
| SetDuration | No | uint32 (seconds) |
| RemainingDuration | No | uint32 |
| IsConfigured | No | uint8 |
| ServiceLabelIndex | No | uint8 |
| StatusFault | No | uint8 |
| Name | No | string |

**Use Cases**: Sprinkler valves, water shut-offs

### Faucet

**UUID**: `000000D7-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Faucet`

Controls smart faucets.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 |
| StatusFault | No | uint8 |
| Name | No | string |

**Use Cases**: Smart faucets, touchless fixtures

### IrrigationSystem

**UUID**: `000000CF-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.IrrigationSystem`

Controls sprinkler systems.

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 |
| ProgramMode | Yes | uint8 (0=None, 1=Scheduled, 2=Manual) |
| InUse | Yes | uint8 |
| RemainingDuration | No | uint32 |
| StatusFault | No | uint8 |
| Name | No | string |

**Linked Services**: Valve services for each zone

**Use Cases**: Smart sprinkler controllers (Rachio, RainMachine)

---

## Network Services

### WiFiRouter

**UUID**: `0000020A-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.WiFiRouter`

Manages WiFi router settings.

| Characteristic | Required | Type |
|----------------|----------|------|
| ConfiguredName | Yes | string |
| ManagedNetworkEnable | Yes | uint8 |
| NetworkAccessViolationControl | Yes | tlv8 |
| NetworkClientProfileControl | Yes | tlv8 |
| NetworkClientStatusControl | Yes | tlv8 |
| RouterStatus | Yes | uint8 |
| SupportedRouterConfiguration | Yes | tlv8 |
| WANConfigurationList | Yes | tlv8 |
| WANStatusList | Yes | tlv8 |

**Use Cases**: HomeKit-enabled routers (Eero, Linksys Velop)

### WiFiSatellite

**UUID**: `0000020F-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.WiFiSatellite`

Represents mesh network satellite nodes.

| Characteristic | Required | Type |
|----------------|----------|------|
| WiFiSatelliteStatus | Yes | uint8 |

**Use Cases**: Mesh network extenders/satellites

---

## Battery and Power Services

### Battery

**UUID**: `00000096-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Battery`

Reports battery status (renamed from BatteryService).

| Characteristic | Required | Type |
|----------------|----------|------|
| StatusLowBattery | Yes | uint8 (0=Normal, 1=Low) |
| BatteryLevel | No | uint8 (0-100%) |
| ChargingState | No | uint8 (0=NotCharging, 1=Charging, 2=NotChargeable) |

**Use Cases**: Battery-powered sensors, portable devices

---

## Accessory Information Services

### AccessoryInformation

**UUID**: `0000003E-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AccessoryInformation`

Required on every accessory - provides identification info.

| Characteristic | Required | Type |
|----------------|----------|------|
| Identify | Yes | bool (write-only) |
| Manufacturer | Yes | string |
| Model | Yes | string |
| Name | Yes | string |
| SerialNumber | Yes | string |
| FirmwareRevision | Yes | string |
| HardwareRevision | No | string |
| AccessoryFlags | No | uint32 |
| AppMatchingIdentifier | No | string |
| ProductData | No | data |

**Use Cases**: Required for all accessories

### ProtocolInformation

**UUID**: `000000A2-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.ProtocolInformation`

Protocol version information.

| Characteristic | Required | Type |
|----------------|----------|------|
| Version | Yes | string |

**Use Cases**: HAP protocol versioning

### ServiceLabel

**UUID**: `000000CC-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.ServiceLabel`

Labels for multi-button accessories.

| Characteristic | Required | Type |
|----------------|----------|------|
| ServiceLabelNamespace | Yes | uint8 (0=Dots, 1=Numbers) |

**Use Cases**: Multi-button remotes, scene controllers

---

## Assistant Services

### Siri

**UUID**: `00000133-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Siri`

Siri voice assistant integration.

| Characteristic | Required | Type |
|----------------|----------|------|
| SiriInputType | Yes | uint8 |
| SiriEnable | No | uint8 |
| SiriEngineVersion | No | string |
| SiriLightOnUse | No | uint8 |
| SiriListening | No | uint8 |
| SiriTouchToUse | No | uint8 |

**Use Cases**: HomePod, Siri-enabled devices

### SiriEndpoint

**UUID**: `00000253-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.SiriEndpoint`

Siri endpoint configuration.

| Characteristic | Required | Type |
|----------------|----------|------|
| SiriEndpointSessionStatus | Yes | tlv8 |
| SiriAudioSessionConfiguration | Yes | tlv8 |

**Use Cases**: Siri voice processing

### Assistant

**UUID**: `0000026A-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Assistant`

Generic voice assistant service (iOS 15+).

| Characteristic | Required | Type |
|----------------|----------|------|
| Active | Yes | uint8 |
| Identifier | Yes | uint32 |
| Name | Yes | string |

**Use Cases**: Third-party voice assistants

---

## Diagnostics Services

### Diagnostics

**UUID**: `00000237-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Diagnostics`

Diagnostic data reporting.

| Characteristic | Required | Type |
|----------------|----------|------|
| SupportedDiagnosticsSnapshot | Yes | tlv8 |

**Use Cases**: Debug information, troubleshooting

### AccessoryRuntimeInformation

**UUID**: `00000239-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AccessoryRuntimeInformation`

Runtime metrics and information.

| Characteristic | Required | Type |
|----------------|----------|------|
| Ping | Yes | data |
| ActivityInterval | No | uint32 |
| HeartBeat | No | uint32 |
| SleepInterval | No | uint32 |

**Use Cases**: Heartbeat monitoring, activity tracking

### AccessoryMetrics

**UUID**: `00000270-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AccessoryMetrics`

Accessory performance metrics (iOS 15+).

| Characteristic | Required | Type |
|----------------|----------|------|
| AccessoryMetrics | Yes | tlv8 |
| SupportedAccessoryMetrics | Yes | tlv8 |

**Use Cases**: Performance monitoring

---

## Threading and Transport Services

### ThreadTransport

**UUID**: `00000701-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.ThreadTransport`

Thread network transport management.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentTransport | Yes | bool |
| ThreadControlPoint | Yes | tlv8 |
| ThreadNodeCapabilities | Yes | uint16 |
| ThreadStatus | Yes | uint16 |

**Use Cases**: Thread-enabled devices

### WiFiTransport

**UUID**: `0000022A-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.WiFiTransport`

WiFi transport management.

| Characteristic | Required | Type |
|----------------|----------|------|
| CurrentTransport | Yes | bool |
| WiFiCapabilities | Yes | uint32 |
| WiFiConfigurationControl | Yes | tlv8 |

**Use Cases**: WiFi network configuration

### TransferTransportManagement

**UUID**: `00000203-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.TransferTransportManagement`

Bulk data transfer management.

| Characteristic | Required | Type |
|----------------|----------|------|
| SupportedTransferTransportConfiguration | Yes | tlv8 |
| SetupTransferTransport | Yes | tlv8 |

**Use Cases**: Firmware updates, large data transfers

---

## Access Control Services

### AccessControl

**UUID**: `000000DA-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.AccessControl`

IP-based access control.

| Characteristic | Required | Type |
|----------------|----------|------|
| AccessControlLevel | Yes | uint16 |
| PasswordSetting | No | tlv8 |

**Use Cases**: Network access restrictions

### Pairing

**UUID**: `00000055-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.Pairing`

HAP pairing management.

| Characteristic | Required | Type |
|----------------|----------|------|
| PairingFeatures | Yes | uint8 |
| PairSetup | Yes | tlv8 |
| PairVerify | Yes | tlv8 |
| PairingPairings | Yes | tlv8 |

**Use Cases**: Device pairing (internal service)

---

## Target Control Services

### TargetControl

**UUID**: `00000125-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.TargetControl`

Apple TV remote control.

| Characteristic | Required | Type |
|----------------|----------|------|
| ActiveIdentifier | Yes | uint32 |
| Active | Yes | uint8 |
| ButtonEvent | Yes | tlv8 |

**Use Cases**: Apple TV remote

### TargetControlManagement

**UUID**: `00000122-0000-1000-8000-0026BB765291`
**Constant**: `hap.Service.TargetControlManagement`

Remote control configuration.

| Characteristic | Required | Type |
|----------------|----------|------|
| TargetControlSupportedConfiguration | Yes | tlv8 |
| TargetControlList | Yes | tlv8 |

**Use Cases**: Multi-device remote management

---

## References

- [HAP-NodeJS GitHub Repository](https://github.com/homebridge/HAP-NodeJS)
- [HAP-NodeJS API Documentation](https://developers.homebridge.io/HAP-NodeJS/modules.html)
- [Apple HomeKit Developer Documentation](https://developer.apple.com/documentation/homekit)
- [HomeKit Accessory Protocol Specification](https://developer.apple.com/apple-home/) (MFi Program required)

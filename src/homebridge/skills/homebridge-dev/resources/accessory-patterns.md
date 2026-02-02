# Homebridge Accessory Implementation Patterns

Reference implementations for common HomeKit accessory types. Each pattern includes TypeScript and JavaScript versions with proper error handling.

## Platform Accessory Base Structure

### TypeScript

```typescript
import type {
  CharacteristicValue,
  PlatformAccessory,
  Service,
} from 'homebridge';
import type { ExamplePlatform } from './platform.js';

export class ExampleAccessory {
  private service: Service;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    // Set accessory information
    this.accessory.getService(this.platform.Service.AccessoryInformation)!
      .setCharacteristic(this.platform.Characteristic.Manufacturer, 'Manufacturer')
      .setCharacteristic(this.platform.Characteristic.Model, 'Model')
      .setCharacteristic(this.platform.Characteristic.SerialNumber, 'Serial');

    // Get or create service
    this.service = this.accessory.getService(this.platform.Service.Switch)
      || this.accessory.addService(this.platform.Service.Switch);

    this.service.setCharacteristic(
      this.platform.Characteristic.Name,
      accessory.context.device.name,
    );

    // Register handlers
    this.service.getCharacteristic(this.platform.Characteristic.On)
      .onSet(this.setOn.bind(this))
      .onGet(this.getOn.bind(this));
  }

  async setOn(value: CharacteristicValue): Promise<void> {
    try {
      // Your device control logic here
      this.platform.log.debug('Set On ->', value);
    } catch (error) {
      this.platform.log.error('Failed to set On:', error);
      throw new this.platform.api.hap.HapStatusError(
        this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
      );
    }
  }

  async getOn(): Promise<CharacteristicValue> {
    try {
      // Your device status logic here
      return false;
    } catch (error) {
      this.platform.log.error('Failed to get On:', error);
      throw new this.platform.api.hap.HapStatusError(
        this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
      );
    }
  }
}
```

### JavaScript

```javascript
class ExampleAccessory {
  constructor(platform, accessory) {
    this.platform = platform;
    this.accessory = accessory;

    // Set accessory information
    this.accessory.getService(this.platform.Service.AccessoryInformation)
      .setCharacteristic(this.platform.Characteristic.Manufacturer, 'Manufacturer')
      .setCharacteristic(this.platform.Characteristic.Model, 'Model')
      .setCharacteristic(this.platform.Characteristic.SerialNumber, 'Serial');

    // Get or create service
    this.service = this.accessory.getService(this.platform.Service.Switch)
      || this.accessory.addService(this.platform.Service.Switch);

    this.service.setCharacteristic(
      this.platform.Characteristic.Name,
      accessory.context.device.name,
    );

    // Register handlers
    this.service.getCharacteristic(this.platform.Characteristic.On)
      .onSet(this.setOn.bind(this))
      .onGet(this.getOn.bind(this));
  }

  async setOn(value) {
    try {
      // Your device control logic here
      this.platform.log.debug('Set On ->', value);
    } catch (error) {
      this.platform.log.error('Failed to set On:', error);
      throw new this.platform.api.hap.HapStatusError(
        this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
      );
    }
  }

  async getOn() {
    try {
      // Your device status logic here
      return false;
    } catch (error) {
      this.platform.log.error('Failed to get On:', error);
      throw new this.platform.api.hap.HapStatusError(
        this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
      );
    }
  }
}

module.exports = { ExampleAccessory };
```

## Sensors

### Motion Sensor

**Service:** `MotionSensor`
**Required Characteristic:** `MotionDetected` (boolean)

#### TypeScript

```typescript
export class MotionSensorAccessory {
  private service: Service;
  private motionDetected = false;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.MotionSensor)
      || this.accessory.addService(this.platform.Service.MotionSensor);

    this.service.setCharacteristic(
      this.platform.Characteristic.Name,
      accessory.context.device.name,
    );

    this.service.getCharacteristic(this.platform.Characteristic.MotionDetected)
      .onGet(this.getMotionDetected.bind(this));

    // Optional characteristics
    this.service.getCharacteristic(this.platform.Characteristic.StatusActive)
      .onGet(() => true);

    this.service.getCharacteristic(this.platform.Characteristic.StatusFault)
      .onGet(() => this.platform.Characteristic.StatusFault.NO_FAULT);
  }

  async getMotionDetected(): Promise<CharacteristicValue> {
    return this.motionDetected;
  }

  // Call this when motion is detected from your device
  updateMotionDetected(detected: boolean): void {
    this.motionDetected = detected;
    this.service.updateCharacteristic(
      this.platform.Characteristic.MotionDetected,
      detected,
    );
    this.platform.log.debug('Motion detected:', detected);
  }
}
```

#### JavaScript

```javascript
class MotionSensorAccessory {
  constructor(platform, accessory) {
    this.platform = platform;
    this.accessory = accessory;
    this.motionDetected = false;

    this.service = this.accessory.getService(this.platform.Service.MotionSensor)
      || this.accessory.addService(this.platform.Service.MotionSensor);

    this.service.setCharacteristic(
      this.platform.Characteristic.Name,
      accessory.context.device.name,
    );

    this.service.getCharacteristic(this.platform.Characteristic.MotionDetected)
      .onGet(this.getMotionDetected.bind(this));
  }

  async getMotionDetected() {
    return this.motionDetected;
  }

  updateMotionDetected(detected) {
    this.motionDetected = detected;
    this.service.updateCharacteristic(
      this.platform.Characteristic.MotionDetected,
      detected,
    );
  }
}
```

### Contact Sensor (Door/Window)

**Service:** `ContactSensor`
**Required Characteristic:** `ContactSensorState`

#### TypeScript

```typescript
export class ContactSensorAccessory {
  private service: Service;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.ContactSensor)
      || this.accessory.addService(this.platform.Service.ContactSensor);

    this.service.getCharacteristic(this.platform.Characteristic.ContactSensorState)
      .onGet(this.getContactState.bind(this));
  }

  async getContactState(): Promise<CharacteristicValue> {
    // 0 = CONTACT_DETECTED (closed), 1 = CONTACT_NOT_DETECTED (open)
    return this.platform.Characteristic.ContactSensorState.CONTACT_DETECTED;
  }

  updateContactState(isOpen: boolean): void {
    const state = isOpen
      ? this.platform.Characteristic.ContactSensorState.CONTACT_NOT_DETECTED
      : this.platform.Characteristic.ContactSensorState.CONTACT_DETECTED;

    this.service.updateCharacteristic(
      this.platform.Characteristic.ContactSensorState,
      state,
    );
  }
}
```

### Temperature Sensor

**Service:** `TemperatureSensor`
**Required Characteristic:** `CurrentTemperature`

#### TypeScript

```typescript
export class TemperatureSensorAccessory {
  private service: Service;
  private currentTemperature = 20; // Celsius

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.TemperatureSensor)
      || this.accessory.addService(this.platform.Service.TemperatureSensor);

    this.service.getCharacteristic(this.platform.Characteristic.CurrentTemperature)
      .setProps({
        minValue: -40,
        maxValue: 100,
        minStep: 0.1,
      })
      .onGet(this.getCurrentTemperature.bind(this));
  }

  async getCurrentTemperature(): Promise<CharacteristicValue> {
    return this.currentTemperature;
  }

  updateTemperature(celsius: number): void {
    this.currentTemperature = celsius;
    this.service.updateCharacteristic(
      this.platform.Characteristic.CurrentTemperature,
      celsius,
    );
  }
}
```

### Humidity Sensor

**Service:** `HumiditySensor`
**Required Characteristic:** `CurrentRelativeHumidity`

#### TypeScript

```typescript
export class HumiditySensorAccessory {
  private service: Service;
  private currentHumidity = 50;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.HumiditySensor)
      || this.accessory.addService(this.platform.Service.HumiditySensor);

    this.service.getCharacteristic(this.platform.Characteristic.CurrentRelativeHumidity)
      .setProps({
        minValue: 0,
        maxValue: 100,
        minStep: 1,
      })
      .onGet(this.getCurrentHumidity.bind(this));
  }

  async getCurrentHumidity(): Promise<CharacteristicValue> {
    return this.currentHumidity;
  }

  updateHumidity(percent: number): void {
    this.currentHumidity = Math.max(0, Math.min(100, percent));
    this.service.updateCharacteristic(
      this.platform.Characteristic.CurrentRelativeHumidity,
      this.currentHumidity,
    );
  }
}
```

### Leak Sensor

**Service:** `LeakSensor`
**Required Characteristic:** `LeakDetected`

#### TypeScript

```typescript
export class LeakSensorAccessory {
  private service: Service;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.LeakSensor)
      || this.accessory.addService(this.platform.Service.LeakSensor);

    this.service.getCharacteristic(this.platform.Characteristic.LeakDetected)
      .onGet(this.getLeakDetected.bind(this));

    // Optional: Battery level
    this.service.getCharacteristic(this.platform.Characteristic.StatusLowBattery)
      .onGet(() => this.platform.Characteristic.StatusLowBattery.BATTERY_LEVEL_NORMAL);
  }

  async getLeakDetected(): Promise<CharacteristicValue> {
    // 0 = LEAK_NOT_DETECTED, 1 = LEAK_DETECTED
    return this.platform.Characteristic.LeakDetected.LEAK_NOT_DETECTED;
  }

  updateLeakDetected(leakDetected: boolean): void {
    const state = leakDetected
      ? this.platform.Characteristic.LeakDetected.LEAK_DETECTED
      : this.platform.Characteristic.LeakDetected.LEAK_NOT_DETECTED;

    this.service.updateCharacteristic(
      this.platform.Characteristic.LeakDetected,
      state,
    );
  }
}
```

### Smoke Sensor

**Service:** `SmokeSensor`
**Required Characteristic:** `SmokeDetected`

#### TypeScript

```typescript
export class SmokeSensorAccessory {
  private service: Service;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.SmokeSensor)
      || this.accessory.addService(this.platform.Service.SmokeSensor);

    this.service.getCharacteristic(this.platform.Characteristic.SmokeDetected)
      .onGet(this.getSmokeDetected.bind(this));
  }

  async getSmokeDetected(): Promise<CharacteristicValue> {
    // 0 = SMOKE_NOT_DETECTED, 1 = SMOKE_DETECTED
    return this.platform.Characteristic.SmokeDetected.SMOKE_NOT_DETECTED;
  }

  updateSmokeDetected(detected: boolean): void {
    const state = detected
      ? this.platform.Characteristic.SmokeDetected.SMOKE_DETECTED
      : this.platform.Characteristic.SmokeDetected.SMOKE_NOT_DETECTED;

    this.service.updateCharacteristic(
      this.platform.Characteristic.SmokeDetected,
      state,
    );
  }
}
```

### Carbon Monoxide Sensor

**Service:** `CarbonMonoxideSensor`
**Required Characteristic:** `CarbonMonoxideDetected`

#### TypeScript

```typescript
export class CarbonMonoxideSensorAccessory {
  private service: Service;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.CarbonMonoxideSensor)
      || this.accessory.addService(this.platform.Service.CarbonMonoxideSensor);

    this.service.getCharacteristic(this.platform.Characteristic.CarbonMonoxideDetected)
      .onGet(this.getCODetected.bind(this));

    // Optional: CO level in PPM
    this.service.getCharacteristic(this.platform.Characteristic.CarbonMonoxideLevel)
      .onGet(() => 0);

    // Optional: Peak CO level
    this.service.getCharacteristic(this.platform.Characteristic.CarbonMonoxidePeakLevel)
      .onGet(() => 0);
  }

  async getCODetected(): Promise<CharacteristicValue> {
    // 0 = CO_LEVELS_NORMAL, 1 = CO_LEVELS_ABNORMAL
    return this.platform.Characteristic.CarbonMonoxideDetected.CO_LEVELS_NORMAL;
  }

  updateCODetected(detected: boolean, level?: number): void {
    const state = detected
      ? this.platform.Characteristic.CarbonMonoxideDetected.CO_LEVELS_ABNORMAL
      : this.platform.Characteristic.CarbonMonoxideDetected.CO_LEVELS_NORMAL;

    this.service.updateCharacteristic(
      this.platform.Characteristic.CarbonMonoxideDetected,
      state,
    );

    if (level !== undefined) {
      this.service.updateCharacteristic(
        this.platform.Characteristic.CarbonMonoxideLevel,
        level,
      );
    }
  }
}
```

## Switches and Outlets

### Switch

**Service:** `Switch`
**Required Characteristic:** `On`

#### TypeScript

```typescript
export class SwitchAccessory {
  private service: Service;
  private isOn = false;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.Switch)
      || this.accessory.addService(this.platform.Service.Switch);

    this.service.getCharacteristic(this.platform.Characteristic.On)
      .onSet(this.setOn.bind(this))
      .onGet(this.getOn.bind(this));
  }

  async setOn(value: CharacteristicValue): Promise<void> {
    this.isOn = value as boolean;
    this.platform.log.info('Switch set to:', this.isOn ? 'ON' : 'OFF');
    // Send command to your device here
  }

  async getOn(): Promise<CharacteristicValue> {
    return this.isOn;
  }
}
```

#### JavaScript

```javascript
class SwitchAccessory {
  constructor(platform, accessory) {
    this.platform = platform;
    this.accessory = accessory;
    this.isOn = false;

    this.service = this.accessory.getService(this.platform.Service.Switch)
      || this.accessory.addService(this.platform.Service.Switch);

    this.service.getCharacteristic(this.platform.Characteristic.On)
      .onSet(this.setOn.bind(this))
      .onGet(this.getOn.bind(this));
  }

  async setOn(value) {
    this.isOn = value;
    this.platform.log.info('Switch set to:', this.isOn ? 'ON' : 'OFF');
  }

  async getOn() {
    return this.isOn;
  }
}
```

### Outlet with Power Monitoring

**Service:** `Outlet`
**Required Characteristics:** `On`, `OutletInUse`
**Optional:** Eve characteristics for power monitoring

#### TypeScript

```typescript
export class OutletAccessory {
  private service: Service;
  private isOn = false;
  private inUse = false;
  private currentPower = 0; // Watts

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.service = this.accessory.getService(this.platform.Service.Outlet)
      || this.accessory.addService(this.platform.Service.Outlet);

    // Required characteristics
    this.service.getCharacteristic(this.platform.Characteristic.On)
      .onSet(this.setOn.bind(this))
      .onGet(this.getOn.bind(this));

    this.service.getCharacteristic(this.platform.Characteristic.OutletInUse)
      .onGet(this.getOutletInUse.bind(this));

    // Optional: Power monitoring via Eve characteristics
    // Requires: import { EveHomeKitTypes } from 'homebridge-lib/EveHomeKitTypes';
    // this.service.addCharacteristic(this.platform.CustomCharacteristics.CurrentConsumption);
    // this.service.getCharacteristic(this.platform.CustomCharacteristics.CurrentConsumption)
    //   .onGet(() => this.currentPower);
  }

  async setOn(value: CharacteristicValue): Promise<void> {
    this.isOn = value as boolean;
    this.platform.log.info('Outlet set to:', this.isOn ? 'ON' : 'OFF');
  }

  async getOn(): Promise<CharacteristicValue> {
    return this.isOn;
  }

  async getOutletInUse(): Promise<CharacteristicValue> {
    // True if something is plugged in and drawing power
    return this.inUse;
  }

  updatePowerConsumption(watts: number): void {
    this.currentPower = watts;
    this.inUse = watts > 0;

    this.service.updateCharacteristic(
      this.platform.Characteristic.OutletInUse,
      this.inUse,
    );

    // If using Eve characteristics:
    // this.service.updateCharacteristic(
    //   this.platform.CustomCharacteristics.CurrentConsumption,
    //   watts,
    // );
  }
}
```

## Lock

**Service:** `LockMechanism`
**Required Characteristics:** `LockCurrentState`, `LockTargetState`

### Lock States

| State | LockCurrentState | LockTargetState |
|-------|------------------|-----------------|
| Unsecured | 0 | 0 |
| Secured | 1 | 1 |
| Jammed | 2 | - |
| Unknown | 3 | - |

#### TypeScript

```typescript
export class LockAccessory {
  private service: Service;
  private currentState: number;
  private targetState: number;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    const Characteristic = this.platform.Characteristic;

    this.currentState = Characteristic.LockCurrentState.SECURED;
    this.targetState = Characteristic.LockTargetState.SECURED;

    this.service = this.accessory.getService(this.platform.Service.LockMechanism)
      || this.accessory.addService(this.platform.Service.LockMechanism);

    this.service.getCharacteristic(Characteristic.LockCurrentState)
      .onGet(this.getLockCurrentState.bind(this));

    this.service.getCharacteristic(Characteristic.LockTargetState)
      .onGet(this.getLockTargetState.bind(this))
      .onSet(this.setLockTargetState.bind(this));
  }

  async getLockCurrentState(): Promise<CharacteristicValue> {
    return this.currentState;
  }

  async getLockTargetState(): Promise<CharacteristicValue> {
    return this.targetState;
  }

  async setLockTargetState(value: CharacteristicValue): Promise<void> {
    const Characteristic = this.platform.Characteristic;
    this.targetState = value as number;

    try {
      if (this.targetState === Characteristic.LockTargetState.SECURED) {
        this.platform.log.info('Locking...');
        // Send lock command to device
        await this.lockDevice();
        this.currentState = Characteristic.LockCurrentState.SECURED;
      } else {
        this.platform.log.info('Unlocking...');
        // Send unlock command to device
        await this.unlockDevice();
        this.currentState = Characteristic.LockCurrentState.UNSECURED;
      }

      // Update current state
      this.service.updateCharacteristic(
        Characteristic.LockCurrentState,
        this.currentState,
      );
    } catch (error) {
      this.platform.log.error('Lock operation failed:', error);
      // Set jammed state on failure
      this.currentState = Characteristic.LockCurrentState.JAMMED;
      this.service.updateCharacteristic(
        Characteristic.LockCurrentState,
        this.currentState,
      );
      throw new this.platform.api.hap.HapStatusError(
        this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
      );
    }
  }

  private async lockDevice(): Promise<void> {
    // Your device lock logic
  }

  private async unlockDevice(): Promise<void> {
    // Your device unlock logic
  }

  // Call when device reports jam
  reportJammed(): void {
    this.currentState = this.platform.Characteristic.LockCurrentState.JAMMED;
    this.service.updateCharacteristic(
      this.platform.Characteristic.LockCurrentState,
      this.currentState,
    );
    this.platform.log.warn('Lock is jammed!');
  }
}
```

#### JavaScript

```javascript
class LockAccessory {
  constructor(platform, accessory) {
    this.platform = platform;
    this.accessory = accessory;

    const Characteristic = this.platform.Characteristic;
    this.currentState = Characteristic.LockCurrentState.SECURED;
    this.targetState = Characteristic.LockTargetState.SECURED;

    this.service = this.accessory.getService(this.platform.Service.LockMechanism)
      || this.accessory.addService(this.platform.Service.LockMechanism);

    this.service.getCharacteristic(Characteristic.LockCurrentState)
      .onGet(this.getLockCurrentState.bind(this));

    this.service.getCharacteristic(Characteristic.LockTargetState)
      .onGet(this.getLockTargetState.bind(this))
      .onSet(this.setLockTargetState.bind(this));
  }

  async getLockCurrentState() {
    return this.currentState;
  }

  async getLockTargetState() {
    return this.targetState;
  }

  async setLockTargetState(value) {
    const Characteristic = this.platform.Characteristic;
    this.targetState = value;

    if (this.targetState === Characteristic.LockTargetState.SECURED) {
      // Lock the device
      this.currentState = Characteristic.LockCurrentState.SECURED;
    } else {
      // Unlock the device
      this.currentState = Characteristic.LockCurrentState.UNSECURED;
    }

    this.service.updateCharacteristic(
      Characteristic.LockCurrentState,
      this.currentState,
    );
  }
}
```

## Thermostat

**Service:** `Thermostat`
**Required Characteristics:** `CurrentHeatingCoolingState`, `TargetHeatingCoolingState`, `CurrentTemperature`, `TargetTemperature`, `TemperatureDisplayUnits`

### Heating/Cooling States

| State | Current | Target |
|-------|---------|--------|
| Off | 0 | 0 |
| Heat | 1 | 1 |
| Cool | 2 | 2 |
| Auto | - | 3 |

#### TypeScript

```typescript
export class ThermostatAccessory {
  private service: Service;

  private currentState = 0; // OFF
  private targetState = 0; // OFF
  private currentTemp = 20;
  private targetTemp = 22;
  private displayUnits = 0; // CELSIUS

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    const Characteristic = this.platform.Characteristic;

    this.service = this.accessory.getService(this.platform.Service.Thermostat)
      || this.accessory.addService(this.platform.Service.Thermostat);

    // Current Heating/Cooling State (read-only)
    this.service.getCharacteristic(Characteristic.CurrentHeatingCoolingState)
      .onGet(() => this.currentState);

    // Target Heating/Cooling State
    this.service.getCharacteristic(Characteristic.TargetHeatingCoolingState)
      .setProps({
        validValues: [
          Characteristic.TargetHeatingCoolingState.OFF,
          Characteristic.TargetHeatingCoolingState.HEAT,
          Characteristic.TargetHeatingCoolingState.COOL,
          Characteristic.TargetHeatingCoolingState.AUTO,
        ],
      })
      .onGet(() => this.targetState)
      .onSet(this.setTargetState.bind(this));

    // Current Temperature (read-only)
    this.service.getCharacteristic(Characteristic.CurrentTemperature)
      .setProps({
        minValue: -40,
        maxValue: 100,
        minStep: 0.1,
      })
      .onGet(() => this.currentTemp);

    // Target Temperature
    this.service.getCharacteristic(Characteristic.TargetTemperature)
      .setProps({
        minValue: 10,
        maxValue: 38,
        minStep: 0.5,
      })
      .onGet(() => this.targetTemp)
      .onSet(this.setTargetTemperature.bind(this));

    // Temperature Display Units
    this.service.getCharacteristic(Characteristic.TemperatureDisplayUnits)
      .onGet(() => this.displayUnits)
      .onSet((value: CharacteristicValue) => {
        this.displayUnits = value as number;
      });

    // Optional: Current Relative Humidity
    this.service.getCharacteristic(Characteristic.CurrentRelativeHumidity)
      .onGet(() => 50);
  }

  async setTargetState(value: CharacteristicValue): Promise<void> {
    this.targetState = value as number;
    this.platform.log.info('Thermostat mode set to:', this.getModeString(this.targetState));
    // Send command to device, then update current state based on device response
  }

  async setTargetTemperature(value: CharacteristicValue): Promise<void> {
    this.targetTemp = value as number;
    this.platform.log.info('Target temperature set to:', this.targetTemp);
    // Send command to device
  }

  private getModeString(state: number): string {
    const modes = ['OFF', 'HEAT', 'COOL', 'AUTO'];
    return modes[state] || 'UNKNOWN';
  }

  updateCurrentTemperature(celsius: number): void {
    this.currentTemp = celsius;
    this.service.updateCharacteristic(
      this.platform.Characteristic.CurrentTemperature,
      celsius,
    );
  }

  updateCurrentState(state: number): void {
    this.currentState = state;
    this.service.updateCharacteristic(
      this.platform.Characteristic.CurrentHeatingCoolingState,
      state,
    );
  }
}
```

#### JavaScript

```javascript
class ThermostatAccessory {
  constructor(platform, accessory) {
    this.platform = platform;
    this.accessory = accessory;

    this.currentState = 0;
    this.targetState = 0;
    this.currentTemp = 20;
    this.targetTemp = 22;
    this.displayUnits = 0;

    const Characteristic = this.platform.Characteristic;

    this.service = this.accessory.getService(this.platform.Service.Thermostat)
      || this.accessory.addService(this.platform.Service.Thermostat);

    this.service.getCharacteristic(Characteristic.CurrentHeatingCoolingState)
      .onGet(() => this.currentState);

    this.service.getCharacteristic(Characteristic.TargetHeatingCoolingState)
      .onGet(() => this.targetState)
      .onSet(this.setTargetState.bind(this));

    this.service.getCharacteristic(Characteristic.CurrentTemperature)
      .onGet(() => this.currentTemp);

    this.service.getCharacteristic(Characteristic.TargetTemperature)
      .onGet(() => this.targetTemp)
      .onSet(this.setTargetTemperature.bind(this));

    this.service.getCharacteristic(Characteristic.TemperatureDisplayUnits)
      .onGet(() => this.displayUnits);
  }

  async setTargetState(value) {
    this.targetState = value;
  }

  async setTargetTemperature(value) {
    this.targetTemp = value;
  }
}
```

## Security System

**Service:** `SecuritySystem`
**Required Characteristics:** `SecuritySystemCurrentState`, `SecuritySystemTargetState`

### Security States

| State | Current | Target |
|-------|---------|--------|
| Stay Arm | 0 | 0 |
| Away Arm | 1 | 1 |
| Night Arm | 2 | 2 |
| Disarmed | 3 | 3 |
| Alarm Triggered | 4 | - |

#### TypeScript

```typescript
export class SecuritySystemAccessory {
  private service: Service;
  private currentState: number;
  private targetState: number;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    const Characteristic = this.platform.Characteristic;

    this.currentState = Characteristic.SecuritySystemCurrentState.DISARMED;
    this.targetState = Characteristic.SecuritySystemTargetState.DISARM;

    this.service = this.accessory.getService(this.platform.Service.SecuritySystem)
      || this.accessory.addService(this.platform.Service.SecuritySystem);

    this.service.getCharacteristic(Characteristic.SecuritySystemCurrentState)
      .onGet(() => this.currentState);

    this.service.getCharacteristic(Characteristic.SecuritySystemTargetState)
      .setProps({
        validValues: [
          Characteristic.SecuritySystemTargetState.STAY_ARM,
          Characteristic.SecuritySystemTargetState.AWAY_ARM,
          Characteristic.SecuritySystemTargetState.NIGHT_ARM,
          Characteristic.SecuritySystemTargetState.DISARM,
        ],
      })
      .onGet(() => this.targetState)
      .onSet(this.setTargetState.bind(this));

    // Optional: Fault status
    this.service.getCharacteristic(Characteristic.StatusFault)
      .onGet(() => Characteristic.StatusFault.NO_FAULT);

    // Optional: Tamper status
    this.service.getCharacteristic(Characteristic.StatusTampered)
      .onGet(() => Characteristic.StatusTampered.NOT_TAMPERED);
  }

  async setTargetState(value: CharacteristicValue): Promise<void> {
    const Characteristic = this.platform.Characteristic;
    this.targetState = value as number;

    const stateNames = ['Stay Arm', 'Away Arm', 'Night Arm', 'Disarm'];
    this.platform.log.info('Security system:', stateNames[this.targetState]);

    try {
      // Send command to your security system
      await this.sendArmCommand(this.targetState);

      // Update current state to match target (if not triggered)
      this.currentState = this.targetState;
      this.service.updateCharacteristic(
        Characteristic.SecuritySystemCurrentState,
        this.currentState,
      );
    } catch (error) {
      this.platform.log.error('Failed to set security state:', error);
      throw new this.platform.api.hap.HapStatusError(
        this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
      );
    }
  }

  private async sendArmCommand(state: number): Promise<void> {
    // Your security system API call
  }

  triggerAlarm(): void {
    this.currentState = this.platform.Characteristic.SecuritySystemCurrentState.ALARM_TRIGGERED;
    this.service.updateCharacteristic(
      this.platform.Characteristic.SecuritySystemCurrentState,
      this.currentState,
    );
    this.platform.log.warn('ALARM TRIGGERED!');
  }
}
```

## Camera (RTSP Streaming)

Camera implementation requires the Camera streaming delegate. This is typically done via `homebridge-camera-ffmpeg` or similar, but here's the pattern for custom implementations.

**Service:** `CameraRTPStreamManagement`

#### TypeScript (Platform Setup)

```typescript
import type {
  CameraController,
  CameraStreamingDelegate,
  HAP,
  PrepareStreamCallback,
  PrepareStreamRequest,
  PrepareStreamResponse,
  SnapshotRequest,
  SnapshotRequestCallback,
  StreamingRequest,
  StreamRequestCallback,
} from 'homebridge';

export class CameraAccessory implements CameraStreamingDelegate {
  private readonly hap: HAP;
  controller?: CameraController;

  constructor(
    private readonly platform: ExamplePlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    this.hap = this.platform.api.hap;

    const options = {
      cameraStreamCount: 2,
      delegate: this,
      streamingOptions: {
        supportedCryptoSuites: [this.hap.SRTPCryptoSuites.AES_CM_128_HMAC_SHA1_80],
        video: {
          resolutions: [
            [1920, 1080, 30],
            [1280, 720, 30],
            [640, 480, 30],
          ],
          codec: {
            profiles: [this.hap.H264Profile.BASELINE],
            levels: [this.hap.H264Level.LEVEL3_1],
          },
        },
        audio: {
          twoWayAudio: false,
          codecs: [
            {
              type: this.hap.AudioStreamingCodecType.AAC_ELD,
              samplerate: this.hap.AudioStreamingSamplerate.KHZ_16,
            },
          ],
        },
      },
    };

    this.controller = new this.hap.CameraController(options);
    this.accessory.configureController(this.controller);
  }

  handleSnapshotRequest(
    request: SnapshotRequest,
    callback: SnapshotRequestCallback,
  ): void {
    // Return a snapshot image
    // Use ffmpeg to grab a frame from RTSP stream
    const snapshotBuffer = Buffer.alloc(0); // Replace with actual snapshot
    callback(undefined, snapshotBuffer);
  }

  prepareStream(
    request: PrepareStreamRequest,
    callback: PrepareStreamCallback,
  ): void {
    // Prepare stream response with video/audio RTP info
    const response: PrepareStreamResponse = {
      video: {
        port: request.video.port,
        ssrc: this.hap.CameraController.generateSynchronisationSource(),
        srtp_key: request.video.srtp_key,
        srtp_salt: request.video.srtp_salt,
      },
      audio: {
        port: request.audio.port,
        ssrc: this.hap.CameraController.generateSynchronisationSource(),
        srtp_key: request.audio.srtp_key,
        srtp_salt: request.audio.srtp_salt,
      },
    };
    callback(undefined, response);
  }

  handleStreamRequest(
    request: StreamingRequest,
    callback: StreamRequestCallback,
  ): void {
    // Start/stop ffmpeg process based on request.type
    // START, RECONFIGURE, or STOP
    callback();
  }
}
```

For production camera plugins, use [homebridge-camera-ffmpeg](https://github.com/homebridge-plugins/homebridge-camera-ffmpeg) as a reference or dependency.

## Async Updates and Event Emission

For devices that push updates (WebSocket, MQTT, polling), use `updateCharacteristic`:

```typescript
// In your device event handler
this.device.on('stateChange', (newState) => {
  this.service.updateCharacteristic(
    this.platform.Characteristic.On,
    newState.isOn,
  );
});

// For motion sensors with auto-reset
this.device.on('motion', () => {
  this.service.updateCharacteristic(
    this.platform.Characteristic.MotionDetected,
    true,
  );

  // Auto-reset after 30 seconds
  setTimeout(() => {
    this.service.updateCharacteristic(
      this.platform.Characteristic.MotionDetected,
      false,
    );
  }, 30000);
});
```

## Error Handling

Always throw `HapStatusError` for device communication failures:

```typescript
async getOn(): Promise<CharacteristicValue> {
  try {
    const state = await this.device.getState();
    return state.isOn;
  } catch (error) {
    this.platform.log.error('Failed to get device state:', error);

    // This shows "Not Responding" in Home app
    throw new this.platform.api.hap.HapStatusError(
      this.platform.api.hap.HAPStatus.SERVICE_COMMUNICATION_FAILURE,
    );
  }
}
```

### HAP Status Codes

| Code | Constant | Use Case |
|------|----------|----------|
| -70402 | `SERVICE_COMMUNICATION_FAILURE` | Device unreachable |
| -70403 | `RESOURCE_BUSY` | Device busy |
| -70404 | `READ_ONLY_CHARACTERISTIC` | Write to read-only |
| -70405 | `WRITE_ONLY_CHARACTERISTIC` | Read from write-only |
| -70406 | `NOTIFICATION_NOT_SUPPORTED` | Events not supported |
| -70407 | `OUT_OF_RESOURCE` | Resource exhausted |
| -70408 | `OPERATION_TIMED_OUT` | Request timeout |
| -70409 | `RESOURCE_DOES_NOT_EXIST` | Resource not found |
| -70410 | `INVALID_VALUE_IN_REQUEST` | Bad value |
| -70411 | `INSUFFICIENT_PRIVILEGES` | Auth required |

## References

- [Homebridge Plugin Developer Documentation](https://developers.homebridge.io/)
- [homebridge-plugin-template](https://github.com/homebridge/homebridge-plugin-template)
- [homebridge-examples](https://github.com/homebridge/homebridge-examples)
- [HAP-NodeJS Accessory Examples](https://github.com/homebridge/HAP-NodeJS/tree/latest/src/accessories)
- [HAP-NodeJS Service Types](https://developers.homebridge.io/HAP-NodeJS/modules/_definitions.Services.html)
- [HAP-NodeJS Characteristic Types](https://developers.homebridge.io/HAP-NodeJS/modules/_definitions.Characteristics.html)

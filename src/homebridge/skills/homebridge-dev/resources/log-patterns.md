# Debugging with Logs

This guide covers interpreting Homebridge logs, common error patterns, and systematic debugging approaches.

## Enabling Debug Logging

### Homebridge Debug Mode

Run Homebridge with the `-D` flag for verbose plugin logging:

```bash
# Direct invocation
homebridge -D

# With hb-service
hb-service restart -- -D
```

Via Homebridge UI: Settings > Homebridge Settings > Debug Mode

### HAP-NodeJS Debug Output

For low-level HAP protocol debugging:

```bash
# All HAP-NodeJS output
DEBUG=HAP-NodeJS:* homebridge

# Specific namespaces
DEBUG=HAP-NodeJS:Advertiser homebridge
DEBUG=HAP-NodeJS:Accessory homebridge
DEBUG=HAP-NodeJS:EventedHTTPServer homebridge
```

### Plugin-Specific Debug

Many plugins support their own debug modes:

```bash
# Example: homebridge-hue
DEBUG=hue homebridge -D

# Multiple namespaces
DEBUG=HAP-NodeJS:*,hue homebridge -D
```

## Common Error Messages

### Startup Errors

#### "ERROR LOADING PLUGIN"

```
[2024-01-15 10:00:00] ERROR LOADING PLUGIN homebridge-example:
Error: Cannot find module 'some-dependency'
```

**Causes:**

- Missing npm dependency
- Node.js version mismatch (native modules)
- Corrupted installation

**Solutions:**

```bash
# Reinstall plugin
npm uninstall homebridge-example
npm install homebridge-example

# Rebuild native modules
npm rebuild

# Check Node.js version compatibility
node --version
```

#### "The module was compiled against a different Node.js version"

```
Error: The module was compiled against a different Node.js version
using NODE_MODULE_VERSION 115. This version requires NODE_MODULE_VERSION 127.
```

**Cause:** Native module compiled for different Node.js version

**Solution:**

```bash
# Rebuild all native modules
npm rebuild

# Or reinstall the plugin
npm uninstall homebridge-problematic-plugin
npm install homebridge-problematic-plugin
```

#### "Plugin requires a HomeBridge version of X"

```
Plugin homebridge-old requires a HomeBridge version of ~0.4.53
which does not satisfy the current HomeBridge version of 1.6.0
```

**Cause:** Plugin hasn't been updated for newer Homebridge

**Solutions:**

1. Check for plugin updates: `npm update homebridge-old`
2. Look for alternative/forked plugins
3. Contact plugin author via GitHub issues

### Configuration Errors

#### "No plugin was found for the platform"

```
[2024-01-15 10:00:00] No plugin was found for the platform "BadPlatformName"
```

**Causes:**

- Typo in platform name
- Plugin not installed
- Plugin exports different name than expected

**Solutions:**

1. Check exact platform name in plugin's README
2. Verify plugin is installed: `npm list homebridge-*`
3. Check plugin's `package.json` for `homebridge.platform` value

#### "Config validation failed"

```
[2024-01-15 10:00:00] Config validation failed for platform ExamplePlatform:
[2024-01-15 10:00:00]   - Property 'token' is required
```

**Cause:** Missing or invalid configuration

**Solution:** Check `config.schema.json` for required fields

### Accessory Registration Errors

#### "Cannot add a bridged Accessory with the same UUID"

```
Cannot add a bridged Accessory with the same UUID as another
bridged Accessory: 12345678-1234-1234-1234-123456789012
```

**Causes:**

- Duplicate accessory names
- Plugin not generating unique UUIDs
- Cached accessories conflict

**Solutions:**

```bash
# Clear cached accessories
rm ~/.homebridge/accessories/cachedAccessories

# Use uuid_base in config (plugin-dependent)
{
  "accessory": "Example",
  "name": "My Device",
  "uuid_base": "unique-string-here"
}
```

#### "This plugin is taking long time to load"

```
[2024-01-15 10:00:00] This plugin is taking long time to load
and preventing Homebridge from starting: homebridge-slow-plugin
```

**Causes:**

- Plugin waiting for network/API
- Blocking operation in constructor
- Network timeout issues

**Solutions:**

1. Run as child bridge for isolation
2. Check network connectivity to plugin's API
3. Report issue to plugin author (should use async init)

### Characteristic Errors

#### "characteristic value X is not a valid value"

```
[2024-01-15 10:00:00] [MyDevice] characteristic 'Brightness':
characteristic value 150 is not a valid value (valid values: 0-100)
```

**Cause:** Plugin returning value outside allowed range

**Solutions (for plugin developers):**

```typescript
// Clamp values before setting
const brightness = Math.min(100, Math.max(0, rawValue));
this.service.updateCharacteristic(this.Characteristic.Brightness, brightness);

// Or extend valid range if appropriate
this.service.getCharacteristic(this.Characteristic.Brightness)
  .setProps({ minValue: 0, maxValue: 200 });
```

#### "characteristic value expected valid finite number and received NaN"

```
[2024-01-15 10:00:00] characteristic 'CurrentTemperature':
characteristic value expected valid finite number and received "NaN"
```

**Cause:** Plugin receiving undefined/null and not handling it

**Solution (for plugin developers):**

```typescript
// Always validate before setting
const temp = parseFloat(rawValue);
if (Number.isFinite(temp)) {
  this.service.updateCharacteristic(this.Characteristic.CurrentTemperature, temp);
}
```

#### "value out of range" for temperature

```
[2024-01-15 10:00:00] Ignoring invalid value [-5] for Current Temperature
- below minimum (0)
```

**Cause:** HomeKit default temperature range is 0-100C

**Solution (for plugin developers):**

```typescript
// Extend temperature range for cold climates
this.service.getCharacteristic(this.Characteristic.CurrentTemperature)
  .setProps({ minValue: -40, maxValue: 100 });
```

### HAP-NodeJS Warnings

#### "Could not create mDNS advertisement"

```
Could not create mDNS advertisement. The HAP-Server won't be discoverable:
Error: No such interface found
```

**Causes:**

- Network interface changed
- mDNS service not running
- Firewall blocking port 5353

**Solutions:**

1. Try different mDNS advertiser (ciao, bonjour-hap, avahi, resolved)
2. Check firewall: `sudo ufw allow 5353/udp`
3. Restart mDNS service: `sudo systemctl restart avahi-daemon`

#### "Accessory not reachable"

Not an error in logs, but shown in Home app.

**Causes:**

- Homebridge not running
- Network connectivity issues
- mDNS discovery failing

**Solutions:**

1. Check Homebridge is running
2. Flush iOS DNS cache (Airplane mode on/off)
3. Verify mDNS: `dns-sd -B _hap._tcp`

## Debugging Flowchart

```
Plugin Not Working
        |
        v
[Check if plugin loads] --> No --> Check npm install output
        |                          Check Node.js version
        v                          Check for missing deps
       Yes
        |
        v
[Check config errors] --> Yes --> Validate against schema
        |                         Check required fields
        v                         Check value types
       No
        |
        v
[Accessories appear?] --> No --> Check registerAccessory calls
        |                        Check UUID uniqueness
        v                        Clear cachedAccessories
       Yes
        |
        v
[Responds to HomeKit?] --> No --> Check characteristic handlers
        |                         Enable debug logging
        v                         Check HAP traffic
       Yes
        |
        v
[Correct behavior?] --> No --> Check API responses
        |                      Check value transformations
        v                      Add logging to handlers
       Yes
        |
        v
    Working!
```

## Log Analysis Tips

### Filtering Logs

```bash
# By plugin name
grep '\[MyPlugin\]' homebridge.log

# Errors only
grep -E '(ERROR|Error|error)' homebridge.log

# Warnings and errors
grep -E '(WARN|ERROR|warn|error)' homebridge.log

# Specific characteristic
grep 'CurrentTemperature' homebridge.log
```

### Homebridge UI Log Viewer

- Use the search/filter box
- Filter by log level (info, warn, error, debug)
- Download full log for offline analysis

### Timestamps for Correlation

When reporting issues, always include:

1. Timestamp of the error
2. What action triggered it
3. Several lines before and after the error

### Debug Logging Best Practices (for Plugin Authors)

```typescript
// Use appropriate levels
this.log.info('Device connected');        // Normal operation
this.log.warn('API rate limited');        // Unusual but handled
this.log.error('Failed to reach API');    // Error condition
this.log.debug('Raw API response:', data); // Verbose troubleshooting

// Include context
this.log.error(`Failed to set brightness for ${this.name}:`, error.message);

// Don't log sensitive data
this.log.debug('Using token:', token.substring(0, 8) + '...');
```

## Resources

- [Characteristic Warnings Wiki](https://github.com/homebridge/homebridge/wiki/Characteristic-Warnings)
- [Basic Troubleshooting Wiki](https://github.com/homebridge/homebridge/wiki/Basic-Troubleshooting)
- [HAP-NodeJS FAQ](https://github.com/homebridge/HAP-NodeJS/wiki/FAQ)
- [Logging Interface Docs](https://developers.homebridge.io/homebridge/interfaces/Logging.html)

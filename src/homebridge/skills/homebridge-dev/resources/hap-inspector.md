# HAP Traffic Debugging Guide

This guide covers tools and techniques for inspecting HomeKit Accessory Protocol (HAP) traffic between iOS devices and Homebridge.

## Understanding HAP

### Protocol Overview

HAP (HomeKit Accessory Protocol) is Apple's protocol for smart home communication:

- Runs over HTTP/TCP/IP for WiFi devices
- Uses TLS encryption for security
- JSON-based request/response format
- mDNS (Bonjour) for discovery

### When to Inspect HAP Traffic

- Accessory shows "No Response" intermittently
- Characteristics update incorrectly
- Pairing issues
- Performance problems
- Verifying plugin behavior matches HomeKit expectations

## HAP Debugging Tools

### 1. HAP-NodeJS Debug Output

The simplest approach - enable built-in debug logging:

```bash
# All HAP-NodeJS output
DEBUG=HAP-NodeJS:* homebridge -D

# Specific components
DEBUG=HAP-NodeJS:Accessory homebridge -D
DEBUG=HAP-NodeJS:Characteristic homebridge -D
DEBUG=HAP-NodeJS:EventedHTTPServer homebridge -D
```

**What you'll see:**

```
HAP-NodeJS:Accessory Publishing accessory 'My Device'...
HAP-NodeJS:Characteristic [My Device] Characteristic 'On' value changed: false -> true
HAP-NodeJS:EventedHTTPServer HTTP request: GET /characteristics?id=1.10
```

### 2. hap-client-tool

A CLI tool for directly interacting with HomeKit devices:

```bash
# Install
npm install -g hap-client-tool

# Discover devices on network
hap-client discover

# Pair with a device (will prompt for PIN)
hap-client pair -d <device-id>

# Dump accessory structure
hap-client dump -d <device-id>

# Get characteristic value
hap-client get -d <device-id> -a <aid> -i <iid>

# Set characteristic value
hap-client set -d <device-id> -a <aid> -i <iid> -v <value>
```

**Use cases:**

- Test accessories without iOS device
- Script automated testing
- Verify accessory structure matches expectations

### 3. @homebridge/hap-client

Programmatic HAP client for Node.js:

```typescript
import { HapClient, ServiceType } from '@homebridge/hap-client';

const client = new HapClient({
  debug: true,
  pin: '031-45-154',
  config: {
    bridge: {
      host: '192.168.1.100',
      port: 51826,
    }
  }
});

// List all services
const services = await client.getAllServices();
services.forEach(service => {
  console.log(`${service.serviceName}: ${service.serviceType}`);
});

// Monitor events
client.on('service-update', (service) => {
  console.log('Service updated:', service);
});
```

### 4. Wireshark + mitmproxy

For deep protocol analysis:

#### Setup mitmproxy

```bash
# Install
pip install mitmproxy

# Start proxy
mitmproxy --mode regular --listen-port 8080
```

#### Capture with Wireshark

```bash
# Capture mDNS traffic
sudo tcpdump -i en0 -s 0 -w mdns.pcap port 5353

# Open in Wireshark
wireshark -r mdns.pcap -Y mdns
```

#### Analyze HomeKit Traffic

```bash
# Filter for HAP traffic (typically port 51826 or similar)
wireshark -r capture.pcap -Y "tcp.port == 51826"
```

**Note:** HAP traffic is encrypted. For development debugging, use HAP-NodeJS debug output instead, which shows decrypted content.

### 5. homekitdecode

Decode captured HAP exchanges:

```bash
# Clone the tool
git clone https://github.com/joswr1ght/homekitdecode

# In Wireshark:
# 1. Filter for http
# 2. Right-click a HAP request
# 3. Follow > TCP Stream
# 4. Save as YAML

# Decode the YAML
python homekitdecode.py stream.yaml
```

### 6. dns-sd (macOS)

Verify mDNS advertisement:

```bash
# Browse for HAP services
dns-sd -B _hap._tcp

# Get details for a specific service
dns-sd -L "Homebridge" _hap._tcp
```

## Understanding Request/Response Format

### HAP Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/accessories` | GET | List all accessories and characteristics |
| `/characteristics` | GET | Read characteristic values |
| `/characteristics` | PUT | Write characteristic values |
| `/identify` | POST | Trigger accessory identification |
| `/pairings` | POST | Manage pairings |

### Reading Characteristics

**Request:**

```http
GET /characteristics?id=1.10,1.11 HTTP/1.1
```

**Response:**

```json
{
  "characteristics": [
    { "aid": 1, "iid": 10, "value": true },
    { "aid": 1, "iid": 11, "value": 75 }
  ]
}
```

### Writing Characteristics

**Request:**

```http
PUT /characteristics HTTP/1.1
Content-Type: application/hap+json

{
  "characteristics": [
    { "aid": 1, "iid": 10, "value": false }
  ]
}
```

**Response:**

```json
{
  "characteristics": [
    { "aid": 1, "iid": 10, "status": 0 }
  ]
}
```

### Status Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| -70402 | Invalid value |
| -70404 | Resource busy |
| -70405 | Read only |
| -70406 | Write only |
| -70407 | Notification not supported |
| -70408 | Out of resources |
| -70409 | Timeout |
| -70410 | Resource not found |
| -70411 | Invalid request |

## Common Issues HAP Inspection Reveals

### 1. Slow Characteristic Reads

**Symptom:** Home app shows "Updating..." for long periods

**What to look for:**

```
HAP-NodeJS:EventedHTTPServer HTTP request: GET /characteristics?id=1.10
[2 seconds later]
HAP-NodeJS:EventedHTTPServer HTTP response sent
```

**Solution:** Add caching or async state management in plugin

### 2. Invalid Values

**Symptom:** Characteristic shows wrong value or "No Response"

**What to look for:**

```json
{ "aid": 1, "iid": 10, "value": null, "status": -70402 }
```

**Solution:** Validate values in plugin before returning

### 3. Missing Event Notifications

**Symptom:** Home app doesn't update when device state changes

**What to look for:** No event notifications when state changes

**Solution:** Call `updateCharacteristic()` when state changes:

```typescript
this.service.updateCharacteristic(
  this.Characteristic.On,
  newValue
);
```

### 4. Pairing Failures

**Symptom:** Can't add accessory to Home app

**What to look for in mDNS:**

```bash
dns-sd -B _hap._tcp
# Should show your bridge
# Check sf (status flags) - 0x01 means not paired
```

**Common causes:**

- Duplicate MAC address
- Port conflict
- mDNS not working on network

## Correlating HAP Traffic with Plugin Logs

### Adding Request Tracing

In your plugin:

```typescript
service.getCharacteristic(Characteristic.On)
  .onGet(async () => {
    this.log.debug(`[HAP GET] On characteristic requested`);
    const value = await this.device.isOn();
    this.log.debug(`[HAP GET] Returning On = ${value}`);
    return value;
  })
  .onSet(async (value) => {
    this.log.debug(`[HAP SET] On characteristic set to ${value}`);
    await this.device.setOn(value as boolean);
    this.log.debug(`[HAP SET] On set complete`);
  });
```

### Matching Timestamps

1. Enable HAP-NodeJS debug: `DEBUG=HAP-NodeJS:* homebridge -D`
2. Enable plugin debug: `homebridge -D`
3. Perform the problematic action
4. Match timestamps between HAP requests and plugin logs

Example correlation:

```
10:00:00.100 HAP-NodeJS:EventedHTTPServer HTTP request: PUT /characteristics
10:00:00.101 [MyPlugin] [HAP SET] On characteristic set to true
10:00:00.150 [MyPlugin] Sending command to device...
10:00:02.150 [MyPlugin] Device timed out
10:00:02.151 HAP-NodeJS:EventedHTTPServer HTTP response: 500
```

## Alternative Tools

### Apple HomeKit Accessory Simulator

For macOS developers:

1. Download from Apple Developer portal (requires account)
2. Create simulated accessories
3. Use Wireshark to capture reference traffic
4. Compare with your plugin's behavior

### Home+ App (iOS)

Third-party HomeKit app with debugging features:

- Shows detailed accessory info
- Displays raw characteristic values
- Useful for verifying accessory structure

### Eve App (iOS)

Another third-party app that shows:

- Detailed accessory information
- Room and service assignments
- Some debugging capabilities

## Debugging Checklist

```markdown
## HAP Debugging Checklist

### Discovery Issues
- [ ] mDNS advertising? (`dns-sd -B _hap._tcp`)
- [ ] Correct port/MAC in config?
- [ ] Firewall allowing port 5353?
- [ ] iOS DNS cache cleared?

### Pairing Issues
- [ ] Status flags correct in mDNS?
- [ ] PIN code correct?
- [ ] Accessory not already paired?
- [ ] persistPath writable?

### Response Issues
- [ ] Characteristic handlers implemented?
- [ ] Values in valid range?
- [ ] No blocking calls in handlers?
- [ ] Event notifications firing?

### Performance Issues
- [ ] Handlers returning quickly?
- [ ] State cached appropriately?
- [ ] Not polling API on every request?
```

## Resources

- [HAP-NodeJS GitHub](https://github.com/homebridge/HAP-NodeJS)
- [HAP-NodeJS FAQ](https://github.com/homebridge/HAP-NodeJS/wiki/FAQ)
- [hap-client-tool](https://github.com/forty2/hap-client-tool)
- [@homebridge/hap-client](https://github.com/homebridge/hap-client)
- [HomeKit Accessory Protocol Specification](https://developer.apple.com/homekit/) (requires Apple Developer account)

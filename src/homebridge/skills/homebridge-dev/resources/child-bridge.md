# Child Bridge Patterns

Child bridges allow Homebridge platforms or accessories to run as independent bridges in isolated processes. This guide covers when and how to use them effectively.

## What Are Child Bridges?

A child bridge is a separate HomeKit bridge spawned by Homebridge that:

- Runs in its own Node.js process
- Has its own HAP server and port
- Requires separate pairing in the Home app
- Can crash without affecting the main bridge

Introduced in Homebridge v1.3.0, child bridges provide process isolation without the overhead of managing multiple Homebridge instances.

## When to Use Child Bridges

### Use Cases

| Scenario | Benefit |
|----------|---------|
| Crash-prone plugins | Isolates crashes from main bridge |
| Slow-initializing plugins | Prevents blocking other accessories |
| Resource-heavy plugins | Memory issues don't affect main bridge |
| Multiple accounts | Run same plugin twice (e.g., two Ring accounts) |
| Debugging | Separate logs per child bridge |
| Performance tuning | Identify slow plugins via response times |

### When NOT to Use

- Simple, stable plugins (adds unnecessary complexity)
- Resource-constrained systems (each child uses ~20-30MB RAM)
- When you have many small accessories (use main bridge instead)

## Configuration Methods

### Via Homebridge UI (Recommended)

1. Go to Plugins tab
2. Click the plugin's settings icon
3. Select "Bridge Settings" or "Set Up Child Bridge"
4. Configure and save
5. Restart Homebridge
6. Pair the new bridge in the Home app

### Manual Configuration

Add a `_bridge` block to any platform or accessory in `config.json`:

```json
{
  "platforms": [
    {
      "platform": "ExamplePlatform",
      "name": "My Platform",
      "_bridge": {
        "username": "0E:AD:BE:EF:12:34",
        "port": 51827
      }
    }
  ]
}
```

#### Required Fields

| Field | Description |
|-------|-------------|
| `username` | Unique MAC address (format: `XX:XX:XX:XX:XX:XX`) |
| `port` | Unique port number (not used by main bridge or other child bridges) |

#### Optional Fields

| Field | Description |
|-------|-------------|
| `name` | Display name in Home app (defaults to accessory name) |
| `manufacturer` | Bridge manufacturer info |
| `model` | Bridge model info |
| `firmwareRevision` | Firmware version string |

### Generating Unique Values

```bash
# Generate random MAC address
printf '0E:%02X:%02X:%02X:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256))

# Find available port (check what's in use)
grep -E '"port"' ~/.homebridge/config.json
```

## Platform vs Accessory Child Bridges

### Platform Child Bridges

Most common pattern. The entire platform runs in isolation:

```json
{
  "platform": "RingPlatform",
  "refreshToken": "xxx",
  "_bridge": {
    "username": "0E:11:22:33:44:55",
    "port": 51828
  }
}
```

**Characteristics:**

- All accessories from the platform share one child bridge
- Single QR code to pair
- Platform crash = all its accessories unavailable
- Cannot have multiple platforms on the same child bridge

### Accessory Child Bridges

For accessory-type plugins (less common):

```json
{
  "accessories": [
    {
      "accessory": "HttpSwitch",
      "name": "Garage Door",
      "_bridge": {
        "username": "0E:AA:BB:CC:DD:01",
        "port": 51829
      }
    }
  ]
}
```

### Multiple Accessories on One Child Bridge

Homebridge v1.3.2+ allows grouping accessories on a single child bridge:

```json
{
  "accessories": [
    {
      "accessory": "HttpSwitch",
      "name": "Light 1",
      "_bridge": {
        "username": "0E:AA:BB:CC:DD:01",
        "port": 51830
      }
    },
    {
      "accessory": "HttpSwitch",
      "name": "Light 2",
      "_bridge": {
        "username": "0E:AA:BB:CC:DD:01"
      }
    }
  ]
}
```

**Rules:**

- All accessories MUST be from the same plugin
- All accessories MUST use the same `username`
- Port only needs to be set on the first one
- No UI for this - requires manual config.json editing

## config.schema.json for Plugin Authors

Allow users to enable child bridge mode via UI:

```json
{
  "pluginAlias": "ExamplePlatform",
  "pluginType": "platform",
  "singular": true,
  "schema": {
    "type": "object",
    "properties": {
      "name": {
        "title": "Name",
        "type": "string",
        "required": true
      }
    }
  }
}
```

The Homebridge UI automatically adds the "Bridge Settings" option for platforms. No special schema configuration is needed.

## Common Patterns

### Pattern 1: Crash Isolation

For plugins with external API dependencies that may fail:

```json
{
  "platform": "UnstableCloudService",
  "_bridge": {
    "username": "0E:CR:AS:HI:SO:LA",
    "port": 51831
  }
}
```

If the API causes a crash, only this plugin's accessories become unavailable.

### Pattern 2: Multiple Accounts

Run the same platform plugin twice with different credentials:

```json
{
  "platforms": [
    {
      "platform": "RingPlatform",
      "name": "Home Ring",
      "refreshToken": "home-token",
      "_bridge": {
        "username": "0E:RI:NG:HO:ME:01",
        "port": 51832
      }
    },
    {
      "platform": "RingPlatform",
      "name": "Office Ring",
      "refreshToken": "office-token",
      "_bridge": {
        "username": "0E:RI:NG:OF:IC:02",
        "port": 51833
      }
    }
  ]
}
```

### Pattern 3: Performance Isolation

Isolate slow plugins to prevent HomeKit "No Response":

```json
{
  "platform": "SlowInitPlatform",
  "_bridge": {
    "username": "0E:SL:OW:PL:UG:IN",
    "port": 51834
  }
}
```

## Common Gotchas

### Pairing Issues

**Problem:** Child bridge not appearing in Home app

**Solutions:**

1. Check port is not in use: `lsof -i :51827`
2. Verify unique MAC address
3. Try different mDNS advertiser (Settings > mDNS Advertiser)
4. Restart iOS device to clear DNS cache

### Resource Exhaustion

**Problem:** System becomes slow with many child bridges

**Solutions:**

1. Use "Ciao" mDNS advertiser (lower CPU usage)
2. Limit child bridges to truly problematic plugins
3. Monitor with: `ps aux | grep homebridge`
4. Consider consolidating small plugins on main bridge

### Configuration Conflicts

**Problem:** Duplicate MAC address or port errors

**Solution:** Audit all bridges:

```bash
grep -E '(username|port)' ~/.homebridge/config.json | sort | uniq -d
```

### Lost Accessories After Restart

**Problem:** Child bridge accessories disappear

**Solutions:**

1. Ensure child bridge is paired (check Homebridge UI for QR code)
2. Check child bridge status in Homebridge UI dashboard widget
3. Verify config.json `_bridge` block is intact

## Debugging Child Bridges

### Checking Status

In Homebridge UI:

1. Enable child bridge widget on dashboard
2. Shows running/stopped state per bridge
3. Allows individual restart

### Viewing Logs

Child bridge logs are prefixed with the bridge name:

```
[ExamplePlatform] Initializing...
[ExamplePlatform Child Bridge] Starting child bridge...
```

Filter logs by bridge:

```bash
# In Homebridge UI log viewer, use filter
# Or via command line:
journalctl -u homebridge | grep "Child Bridge"
```

### Restarting Individual Child Bridges

Via Homebridge UI dashboard widget, or via IPC if using `hb-service`:

```bash
hb-service restart-child ExamplePlatform
```

### Checking Process Status

```bash
# List all Homebridge processes
ps aux | grep '[h]omebridge'

# Check memory usage per process
ps -o pid,rss,command -p $(pgrep -f homebridge)
```

## Resources

- [Child Bridges Wiki](https://github.com/homebridge/homebridge/wiki/Child-Bridges)
- [Homebridge Config JSON Explained](https://github.com/homebridge/homebridge/wiki/Homebridge-Config-JSON-Explained)
- [mDNS Options](https://github.com/homebridge/homebridge/wiki/mDNS-Options)

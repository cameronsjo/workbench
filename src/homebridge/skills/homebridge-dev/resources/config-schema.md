# Homebridge Config Schema Patterns

Reference for creating `config.schema.json` files compatible with homebridge-config-ui-x.

## Basic Structure

```json
{
  "pluginAlias": "YourPlatformName",
  "pluginType": "platform",
  "singular": true,
  "strictValidation": false,
  "headerDisplay": "Plugin description shown at top of settings",
  "footerDisplay": "Optional footer text with [markdown](https://example.com) support",
  "schema": {
    "type": "object",
    "required": ["name"],
    "additionalProperties": false,
    "properties": {
      "name": {
        "title": "Name",
        "type": "string",
        "default": "My Platform"
      }
    }
  },
  "form": [],
  "display": null
}
```

### Top-Level Properties

| Property | Required | Description |
|----------|----------|-------------|
| `pluginAlias` | Yes | Must match `PLATFORM_NAME` in your code |
| `pluginType` | Yes | `"platform"` or `"accessory"` |
| `singular` | No | `true` if only one instance allowed |
| `strictValidation` | No | `true` to reject unknown properties |
| `customUi` | No | `true` to use custom UI (iframe-based) |
| `headerDisplay` | No | Markdown text above the form |
| `footerDisplay` | No | Markdown text below the form |

## Field Types

### String

```json
{
  "name": {
    "title": "Device Name",
    "type": "string",
    "default": "My Device",
    "placeholder": "Enter device name",
    "description": "The name shown in HomeKit",
    "required": true,
    "minLength": 1,
    "maxLength": 64
  }
}
```

### Integer

```json
{
  "pollingInterval": {
    "title": "Polling Interval",
    "type": "integer",
    "default": 30,
    "minimum": 5,
    "maximum": 3600,
    "placeholder": 30,
    "description": "How often to poll for updates (seconds)"
  }
}
```

### Number (Decimal)

```json
{
  "temperatureOffset": {
    "title": "Temperature Offset",
    "type": "number",
    "default": 0,
    "minimum": -10,
    "maximum": 10,
    "description": "Calibration offset in degrees"
  }
}
```

### Boolean

```json
{
  "enableDebug": {
    "title": "Enable Debug Logging",
    "type": "boolean",
    "default": false,
    "description": "Show detailed debug information in logs"
  }
}
```

### Enum (Dropdown)

```json
{
  "temperatureUnit": {
    "title": "Temperature Unit",
    "type": "string",
    "default": "celsius",
    "oneOf": [
      { "title": "Celsius", "enum": ["celsius"] },
      { "title": "Fahrenheit", "enum": ["fahrenheit"] }
    ]
  }
}
```

### Enum with Typeahead

```json
{
  "accessoryType": {
    "title": "Accessory Type",
    "type": "string",
    "typeahead": {
      "source": [
        "switch",
        "outlet",
        "lightbulb",
        "motionSensor",
        "contactSensor",
        "temperatureSensor"
      ]
    }
  }
}
```

## Validation Patterns

### IP Address

```json
{
  "ip": {
    "title": "Device IP Address",
    "type": "string",
    "format": "ipv4",
    "required": true
  }
}
```

### IP Address (Manual Pattern)

```json
{
  "ip": {
    "title": "Device IP Address",
    "type": "string",
    "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
    "placeholder": "192.168.1.100"
  }
}
```

### Host:Port

```json
{
  "host": {
    "title": "Host",
    "type": "string",
    "pattern": "^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}:\\d{1,5})|([a-zA-Z0-9.-]+:\\d{1,5})$",
    "placeholder": "192.168.1.100:8080"
  }
}
```

### Port Number

```json
{
  "port": {
    "title": "Port",
    "type": "integer",
    "minimum": 1,
    "maximum": 65535,
    "default": 8080,
    "placeholder": 8080
  }
}
```

### MAC Address

```json
{
  "deviceId": {
    "title": "Device ID",
    "type": "string",
    "pattern": "^[A-Fa-f0-9]{6,12}$",
    "placeholder": "ABC123"
  }
}
```

### URL

```json
{
  "apiUrl": {
    "title": "API URL",
    "type": "string",
    "format": "uri",
    "pattern": "^https?://",
    "placeholder": "https://api.example.com"
  }
}
```

## Credential Handling

### Password Field

Password fields are masked in the UI automatically when the key is named `password` or when using the form layout.

```json
{
  "password": {
    "title": "Password",
    "type": "string",
    "description": "Your account password"
  }
}
```

### Token/API Key

```json
{
  "apiKey": {
    "title": "API Key",
    "type": "string",
    "description": "Get this from your account settings",
    "placeholder": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

### OAuth Placeholder

For OAuth flows, use customUi with plugin-ui-utils:

```json
{
  "pluginAlias": "MyOAuthPlugin",
  "pluginType": "platform",
  "singular": true,
  "customUi": true,
  "schema": {
    "type": "object",
    "properties": {
      "name": {
        "title": "Name",
        "type": "string",
        "required": true
      },
      "refreshToken": {
        "title": "Refresh Token",
        "type": "string",
        "description": "Obtained via OAuth flow in custom UI"
      }
    }
  }
}
```

## Nested Objects

```json
{
  "credentials": {
    "title": "Credentials",
    "type": "object",
    "properties": {
      "username": {
        "title": "Username",
        "type": "string",
        "required": true
      },
      "password": {
        "title": "Password",
        "type": "string",
        "required": true
      }
    }
  }
}
```

## Array of Devices Pattern

### Schema Definition

```json
{
  "devices": {
    "title": "Devices",
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "type": "string",
          "required": true
        },
        "ip": {
          "title": "IP Address",
          "type": "string",
          "format": "ipv4",
          "required": true
        },
        "type": {
          "title": "Device Type",
          "type": "string",
          "oneOf": [
            { "title": "Switch", "enum": ["switch"] },
            { "title": "Outlet", "enum": ["outlet"] },
            { "title": "Light", "enum": ["light"] }
          ],
          "required": true
        },
        "pollingInterval": {
          "title": "Polling Interval",
          "type": "integer",
          "default": 30
        }
      }
    }
  }
}
```

### Form Layout for Arrays

```json
{
  "form": [
    {
      "key": "devices",
      "type": "array",
      "items": [
        "devices[].name",
        "devices[].ip",
        "devices[].type",
        "devices[].pollingInterval"
      ]
    }
  ]
}
```

### Tabarray (Tabbed Interface)

```json
{
  "form": [
    {
      "key": "devices",
      "type": "tabarray",
      "title": "{{ value.name || 'New Device' }}",
      "items": [
        "devices[].name",
        "devices[].ip",
        "devices[].type"
      ]
    }
  ]
}
```

## Form Layout

The `form` array controls how fields are displayed. Without it, fields render in definition order.

### Basic Form

```json
{
  "form": [
    "name",
    "username",
    "password"
  ]
}
```

### Fieldset (Grouped Fields)

```json
{
  "form": [
    "name",
    {
      "type": "fieldset",
      "title": "Authentication",
      "items": [
        "username",
        "password"
      ]
    }
  ]
}
```

### Expandable Fieldset

```json
{
  "form": [
    "name",
    {
      "type": "fieldset",
      "title": "Advanced Settings",
      "expandable": true,
      "expanded": false,
      "items": [
        "pollingInterval",
        "timeout",
        "enableDebug"
      ]
    }
  ]
}
```

### Flex Row Layout

```json
{
  "form": [
    {
      "type": "flex",
      "flex-flow": "row wrap",
      "items": [
        "username",
        "password"
      ]
    }
  ]
}
```

### Section Within Array

```json
{
  "form": [
    {
      "key": "devices",
      "type": "array",
      "items": [
        "devices[].name",
        "devices[].ip",
        {
          "key": "devices[]",
          "type": "section",
          "title": "Authentication",
          "expandable": true,
          "items": [
            "devices[].username",
            "devices[].password"
          ]
        }
      ]
    }
  ]
}
```

## Conditional Fields

### Simple Condition (Boolean Toggle)

```json
{
  "schema": {
    "type": "object",
    "properties": {
      "enableAdvanced": {
        "title": "Enable Advanced Mode",
        "type": "boolean",
        "default": false
      },
      "advancedOption": {
        "title": "Advanced Option",
        "type": "string"
      }
    }
  },
  "form": [
    "enableAdvanced",
    {
      "key": "advancedOption",
      "condition": "enableAdvanced"
    }
  ]
}
```

### Function Body Condition

```json
{
  "form": [
    "deviceType",
    {
      "key": "brightness",
      "condition": {
        "functionBody": "return model.deviceType === 'light' || model.deviceType === 'dimmer';"
      }
    }
  ]
}
```

### Array Index Condition

```json
{
  "form": [
    {
      "key": "devices",
      "type": "array",
      "items": [
        "devices[].type",
        {
          "key": "devices[].colorMode",
          "condition": {
            "functionBody": "return model.devices && model.devices[arrayIndices[0]].type === 'colorLightbulb';"
          }
        }
      ]
    }
  ]
}
```

### Nested Array Condition

```json
{
  "condition": {
    "functionBody": "return model.devices[arrayIndices[0]].buttons[arrayIndices[1]].mode === 3;"
  }
}
```

## Dependencies

Use `dependencies` for fields that require other fields:

```json
{
  "schema": {
    "type": "object",
    "properties": {
      "username": {
        "title": "Username",
        "type": "string"
      },
      "password": {
        "title": "Password",
        "type": "string"
      },
      "country": {
        "title": "Country",
        "type": "string",
        "enum": ["us", "eu", "cn"]
      }
    },
    "dependencies": {
      "username": ["country"],
      "password": ["country"]
    }
  }
}
```

## Complete Example

```json
{
  "pluginAlias": "ExamplePlatform",
  "pluginType": "platform",
  "singular": true,
  "headerDisplay": "Configure your devices below. See [documentation](https://example.com/docs) for help.",
  "schema": {
    "type": "object",
    "required": ["name"],
    "additionalProperties": false,
    "properties": {
      "name": {
        "title": "Platform Name",
        "type": "string",
        "default": "Example Platform",
        "required": true
      },
      "username": {
        "title": "Username",
        "type": "string"
      },
      "password": {
        "title": "Password",
        "type": "string"
      },
      "devices": {
        "title": "Devices",
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {
              "title": "Name",
              "type": "string",
              "required": true,
              "minLength": 1
            },
            "ip": {
              "title": "IP Address",
              "type": "string",
              "format": "ipv4",
              "required": true
            },
            "type": {
              "title": "Type",
              "type": "string",
              "oneOf": [
                { "title": "Switch", "enum": ["switch"] },
                { "title": "Outlet", "enum": ["outlet"] },
                { "title": "Light", "enum": ["light"] },
                { "title": "Color Light", "enum": ["colorLight"] }
              ],
              "required": true
            },
            "colorMode": {
              "title": "Color Mode",
              "type": "string",
              "oneOf": [
                { "title": "RGB", "enum": ["rgb"] },
                { "title": "RGBW", "enum": ["rgbw"] }
              ]
            },
            "username": {
              "title": "Username",
              "type": "string"
            },
            "password": {
              "title": "Password",
              "type": "string"
            },
            "exclude": {
              "title": "Exclude from HomeKit",
              "type": "boolean",
              "default": false
            }
          }
        }
      },
      "pollingInterval": {
        "title": "Polling Interval",
        "type": "integer",
        "default": 30,
        "minimum": 5,
        "maximum": 3600
      },
      "timeout": {
        "title": "Request Timeout",
        "type": "integer",
        "default": 10000,
        "minimum": 1000,
        "maximum": 60000,
        "description": "Request timeout in milliseconds"
      },
      "enableDebug": {
        "title": "Enable Debug Logging",
        "type": "boolean",
        "default": false
      }
    }
  },
  "form": [
    "name",
    {
      "type": "fieldset",
      "title": "Authentication",
      "expandable": true,
      "items": [
        {
          "type": "flex",
          "flex-flow": "row wrap",
          "items": ["username", "password"]
        }
      ]
    },
    {
      "type": "fieldset",
      "title": "Devices",
      "items": [
        {
          "key": "devices",
          "type": "tabarray",
          "title": "{{ value.name || 'New Device' }}",
          "items": [
            "devices[].name",
            "devices[].ip",
            "devices[].type",
            {
              "key": "devices[].colorMode",
              "condition": {
                "functionBody": "return model.devices && model.devices[arrayIndices[0]].type === 'colorLight';"
              }
            },
            {
              "key": "devices[]",
              "type": "section",
              "title": "Device Authentication",
              "expandable": true,
              "items": [
                {
                  "type": "flex",
                  "flex-flow": "row wrap",
                  "items": ["devices[].username", "devices[].password"]
                }
              ]
            },
            "devices[].exclude"
          ]
        }
      ]
    },
    {
      "type": "fieldset",
      "title": "Advanced Settings",
      "expandable": true,
      "expanded": false,
      "items": [
        "pollingInterval",
        "timeout",
        "enableDebug"
      ]
    }
  ]
}
```

## References

- [Homebridge Plugin Developer Documentation](https://developers.homebridge.io/)
- [homebridge-plugin-template config.schema.json](https://github.com/homebridge/homebridge-plugin-template/blob/latest/config.schema.json)
- [homebridge-shelly config.schema.json](https://github.com/alexryd/homebridge-shelly/blob/master/config.schema.json) - Advanced patterns
- [homebridge-miot config.schema.json](https://github.com/merdok/homebridge-miot/blob/main/config.schema.json) - Complex nested forms
- [plugin-ui-utils](https://github.com/homebridge/plugin-ui-utils) - Custom UI development

# Verified Publisher Guide

This guide covers becoming a verified Homebridge plugin publisher, from NPM organization setup through maintaining verified status.

## NPM Organization Setup

### Scoped Package Options

You have two choices for publishing Homebridge plugins:

1. **Personal/Organization Scope**: `@username/homebridge-plugin-name`
2. **Homebridge Plugins Scope**: `@homebridge-plugins/homebridge-plugin-name` (requires team membership)

### Setting Up Your NPM Organization

```bash
# Create an npm organization (if using your own scope)
npm org create my-org

# Add team members
npm team add my-org:developers username
```

### Publishing Scoped Packages

Scoped packages are private by default. For public Homebridge plugins:

```bash
# First publish - must specify public access
npm publish --access public

# Subsequent publishes inherit the access setting
npm publish
```

In `package.json`:

```json
{
  "name": "@username/homebridge-plugin-name",
  "publishConfig": {
    "access": "public"
  }
}
```

## Plugin Naming Conventions

### Required Format

- **Standard**: `homebridge-{plugin-name}`
- **Scoped**: `@{scope}/homebridge-{plugin-name}`

### Naming Guidelines

- Use lowercase with hyphens
- Be descriptive but concise
- Avoid generic names that conflict with existing plugins
- Include the device/service type: `homebridge-ring`, `homebridge-hue`, `homebridge-tuya`

### Keywords in package.json

Required keywords for Homebridge plugin discovery:

```json
{
  "keywords": [
    "homebridge-plugin"
  ]
}
```

Additional recommended keywords:

```json
{
  "keywords": [
    "homebridge-plugin",
    "homebridge",
    "homekit",
    "smart-home",
    "your-device-type"
  ]
}
```

## Verification Requirements

### Plugin Type

- MUST be a dynamic platform plugin
- MUST NOT duplicate functionality of existing verified plugins

### Publishing and Source Code

- MUST be published to npm
- MUST have source code on GitHub with issues enabled
- SHOULD create GitHub releases with release notes for each version

### Technical Requirements

- MUST run on all supported Node.js LTS versions (currently v20, v22, v24)
- MUST install successfully without errors
- MUST NOT start unless properly configured
- MUST NOT execute post-install scripts that modify the user's system
- MUST NOT require TTY or non-standard startup parameters

### UI and Privacy

- MUST implement the Homebridge Plugin Settings GUI (`config.schema.json`)
- MUST NOT include analytics or user tracking
- MUST store cache/keys in the Homebridge storage directory (not custom locations)

## Verification Request Process

### Step 1: Self-Assessment

Verify your plugin meets all requirements:

```markdown
## Pre-Submission Checklist

- [ ] Dynamic platform plugin
- [ ] Published to npm
- [ ] GitHub repo with issues enabled
- [ ] Works on Node v20, v22, v24
- [ ] Has config.schema.json
- [ ] No analytics/tracking
- [ ] Stores files in Homebridge directory
- [ ] Creates GitHub releases
```

### Step 2: Submit Request

1. Go to [homebridge/plugins](https://github.com/homebridge/plugins)
2. Open a new issue
3. Select the "Plugin Verification Request" template
4. Fill in all required information

### Step 3: Review Process

The Homebridge team will:

1. Review your plugin against requirements
2. Test installation and basic functionality
3. Provide constructive feedback if changes needed
4. Approve and add to verified list

### Step 4: Post-Verification

Once verified:

- Your plugin appears in the Verified Plugins list
- Green verified badge shows in Homebridge UI
- Plugin is prioritized in search results
- You can optionally upload a custom icon

## Badge Integration in README

Add one of these badges to your README after verification:

### Flat Style with Logo

```markdown
[![verified-by-homebridge](https://badgen.net/badge/homebridge/verified/purple)](https://github.com/homebridge/homebridge/wiki/Verified-Plugins)
```

### shields.io Options

```markdown
<!-- Text only -->
[![verified-by-homebridge](https://img.shields.io/badge/homebridge-verified-blueviolet?color=%23491F59&style=flat)](https://github.com/homebridge/homebridge/wiki/Verified-Plugins)

<!-- With logo -->
[![verified-by-homebridge](https://img.shields.io/badge/homebridge-verified-blueviolet?color=%23491F59&style=flat&logoColor=%23FFFFFF&logo=homebridge)](https://github.com/homebridge/homebridge/wiki/Verified-Plugins)

<!-- Large badge -->
[![verified-by-homebridge](https://img.shields.io/badge/homebridge-verified-blueviolet?color=%23491F59&style=for-the-badge&logoColor=%23FFFFFF&logo=homebridge)](https://github.com/homebridge/homebridge/wiki/Verified-Plugins)
```

### Example README Header

```markdown
# Homebridge MyDevice

[![verified-by-homebridge](https://badgen.net/badge/homebridge/verified/purple)](https://github.com/homebridge/homebridge/wiki/Verified-Plugins)
[![npm](https://img.shields.io/npm/v/homebridge-mydevice)](https://www.npmjs.com/package/homebridge-mydevice)
[![npm](https://img.shields.io/npm/dt/homebridge-mydevice)](https://www.npmjs.com/package/homebridge-mydevice)

Control MyDevice from HomeKit using Homebridge.
```

## Maintaining Verified Status

### Ongoing Requirements

- Keep plugin working on new Node.js LTS versions
- Respond to issues in reasonable time
- Maintain security (address vulnerabilities)
- Keep dependencies updated
- Continue following Homebridge best practices

### If You Become Unavailable

Consider:

- Adding maintainers to npm and GitHub
- Documenting how to transfer ownership
- Responding to Homebridge team inquiries about maintenance status

### @homebridge-plugins Migration

For long-term maintenance assurance, you can migrate to `@homebridge-plugins`:

1. Contact the Homebridge team
2. Transfer repository to homebridge-plugins organization
3. Plugin republished under `@homebridge-plugins` scope
4. You remain maintainer with Homebridge team as backup

Benefits:

- Continuity if you become unavailable
- Enhanced visibility
- Homebridge UI provides seamless migration for users

## Resources

- [Verified Plugins Wiki](https://github.com/homebridge/homebridge/wiki/Verified-Plugins)
- [Plugin Development Docs](https://developers.homebridge.io/)
- [Homebridge Discord](https://discord.gg/homebridge) - #plugin-development channel
- [Plugin Template](https://github.com/homebridge/homebridge-plugin-template)

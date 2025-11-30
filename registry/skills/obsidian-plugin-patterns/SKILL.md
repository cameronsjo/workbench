---
name: obsidian-plugin-patterns
description: Modern Obsidian plugin patterns, API usage, and release automation. Triggers on Obsidian plugin development, manifest.json, esbuild, BRAT, or Release Please.
---

# Obsidian Plugin Patterns

Modern patterns and best practices for Obsidian plugin development (2024-2025).

## When This Skill Applies

- Working with `manifest.json` or Obsidian plugin structure
- Using Obsidian API (Plugin, Modal, Setting, Vault, MetadataCache)
- Setting up release automation for Obsidian plugins
- Configuring BRAT beta testing
- Questions about esbuild configuration for Obsidian

## Core Patterns

### Plugin Lifecycle

```typescript
export default class MyPlugin extends Plugin {
  settings: MySettings;

  async onload() {
    await this.loadSettings();
    this.addSettingTab(new MySettingTab(this.app, this));
    this.addCommand({ id: 'cmd', name: 'Command', callback: () => {} });
    this.registerEvent(this.app.workspace.on('file-open', this.onFileOpen));
  }

  onunload() { /* cleanup */ }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULTS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

### Type Guards (Critical)

```typescript
import { TFile, TAbstractFile } from 'obsidian';

function isTFile(file: TAbstractFile | null): file is TFile {
  return file instanceof TFile;
}

// Usage
const file = this.app.vault.getAbstractFileByPath(path);
if (!isTFile(file)) return;
// Now file is TFile
```

### Event Registration (MUST use registerEvent)

```typescript
// ✅ Correct - auto-cleanup on unload
this.registerEvent(
  this.app.metadataCache.on('changed', (file) => {})
);

// ❌ Wrong - memory leak
this.app.metadataCache.on('changed', (file) => {});
```

### MetadataCache Events

| Event | When | Use Case |
|-------|------|----------|
| `changed` | File cache updated | React to file changes |
| `resolved` | All links resolved | Query link graph |
| `deleted` | File removed | Cleanup references |

**Gotcha**: `changed` does NOT fire on rename. Use `vault.on('rename')`.

### Frontmatter Access

```typescript
// Read (cached, fast)
const cache = this.app.metadataCache.getFileCache(file);
const value = cache?.frontmatter?.myField;

// Write
await this.app.fileManager.processFrontMatter(file, (fm) => {
  fm.myField = 'value';
});
```

## Release Pipeline

### Three-Stage Flow

```
[beta] commit → Beta prerelease (BRAT)
    ↓
[rc] commit → Release Candidate
    ↓
Release Please PR merge → Stable release
```

### Commit Keywords

- `[beta]` - Creates BRAT prerelease
- `[rc]` - Creates release candidate, cleans betas
- Regular commits - Accumulate for next release

### Required Release Assets

BRAT requires these files attached to GitHub release:

- `main.js` - Compiled plugin
- `manifest.json` - With matching version
- `styles.css` - If plugin has styles

### Version Alignment

Release tag, manifest.json version, and release title MUST match:

```
Tag: v1.2.0-beta.5+abc1234
manifest.json: { "version": "1.2.0-beta.5+abc1234" }
Title: 🧪 1.2.0-beta.5+abc1234
```

## Build Configuration

### esbuild Externals (Required)

```javascript
external: [
  'obsidian',
  'electron',
  '@codemirror/*',
  '@lezer/*',
  ...builtins,
]
```

### TypeScript Target

- **target**: ES2018 (for async/await)
- **module**: ESNext
- **format**: CommonJS (cjs)

## Common Patterns

### Modal with Keyboard Support

```typescript
class MyModal extends Modal {
  onOpen() {
    this.scope.register([], 'Escape', () => this.close());
    this.scope.register(['Mod'], 'Enter', () => this.submit());
  }
}
```

### Settings with Validation

```typescript
new Setting(containerEl)
  .setName('API Key')
  .addText((text) => {
    text
      .setValue(this.plugin.settings.apiKey)
      .onChange(async (value) => {
        if (this.validateApiKey(value)) {
          this.plugin.settings.apiKey = value;
          await this.plugin.saveSettings();
        }
      });
  });
```

### AbortController for Long Operations

```typescript
private controller: AbortController | null = null;

async fetchData() {
  this.controller = new AbortController();
  try {
    await fetch(url, { signal: this.controller.signal });
  } finally {
    this.controller = null;
  }
}

onunload() {
  this.controller?.abort();
}
```

## File Structure

```
plugin/
├── src/
│   ├── main.ts          # Plugin class
│   ├── settings.ts      # SettingTab
│   ├── types.ts         # Interfaces
│   └── constants.ts     # Magic values
├── manifest.json        # id, name, version, minAppVersion
├── versions.json        # version → minAppVersion mapping
├── esbuild.config.mjs   # Build config
└── .github/workflows/   # CI/CD
```

## References

- [Obsidian Sample Plugin](https://github.com/obsidianmd/obsidian-sample-plugin)
- [Obsidian API Types](https://github.com/obsidianmd/obsidian-api)
- [BRAT Developer Guide](https://github.com/TfTHacker/obsidian42-brat/blob/main/BRAT-DEVELOPER-GUIDE.md)
- [Release Please](https://github.com/googleapis/release-please)

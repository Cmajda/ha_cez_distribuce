# ČEZ HDO Custom Lovelace Card

Vlastní Lovelace karta pro zobrazení informací o HDO (Hromadné dálkové ovládání) od ČEZ Distribuce.

## Funkce

- � **Aktuální stav tarifu** - Zobrazuje zda je právě aktivní nízký nebo vysoký tarif
- ⏰ **Časové informace** - Začátek, konec a zbývající čas aktualního tarifu
- 🎨 **Přizpůsobitelný design** - Možnost úpravy barev a stylů
- 📱 **Responzivní design** - Optimalizováno pro všechny velikosti obrazovek
- 📱 Responsive design
- 🌙 Dark/light theme support

## Installation

### Manual Installation

1. Download the `cez-hdo-card.js` file
2. Copy it to `<config>/www/community/cez-hdo-card/`
3. Add the resource to your `configuration.yaml`:

```yaml
lovelace:
  resources:
    - url: /local/community/cez-hdo-card/cez-hdo-card.js
      type: module
```

4. Restart Home Assistant

### HACS Installation

This card will be available through HACS once the integration is published.

## Configuration

Add the card through the UI or manually in YAML:

```yaml
type: custom:cez-hdo-card
title: "ČEZ HDO"
show_header: true
show_current_state: true
show_schedule: true
theme: auto
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | string | "ČEZ HDO" | Card title |
| `show_header` | boolean | `true` | Show card header |
| `show_current_state` | boolean | `true` | Show current tariff state |
| `show_schedule` | boolean | `true` | Show daily schedule |
| `theme` | string | `auto` | Theme: `auto`, `light`, `dark` |

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Build Process

1. Install dependencies:
   ```bash
   npm install
   ```

2. Build for production:
   ```bash
   npm run build
   ```

3. Development with watch mode:
   ```bash
   npm run dev
   ```

### Project Structure

```
frontend/
├── src/
│   ├── cez-hdo-card.ts         # Main card component
│   ├── cez-hdo-card-editor.ts  # Card editor
│   └── types.ts                # TypeScript definitions
├── dist/                       # Built files
├── package.json
├── tsconfig.json
├── webpack.config.js
└── README.md
```

## License

Apache-2.0
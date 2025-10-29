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

### Automatic Installation (Recommended)

The card is automatically installed and registered when you install the ČEZ HDO integration:

1. Install the ČEZ HDO integration through HACS
2. Restart Home Assistant
3. Card is automatically copied to `/config/www/cez_hdo/` and registered
4. Ready to use immediately - no manual configuration needed!

### Manual Installation (Fallback)

If automatic installation fails for some reason:

1. Download the `cez-hdo-card.js` file
2. Copy it to `<config>/www/cez_hdo/`
3. Add the resource manually in Lovelace → Settings → Resources:
   - URL: `/local/cez_hdo/cez-hdo-card.js`
   - Type: JavaScript Module
4. Restart Home Assistant

### HACS Integration

This card is integrated with the ČEZ HDO integration and deploys automatically.

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

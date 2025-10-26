# ČEZ HDO Development Guide

## 🚀 Quick Start

### 1. Setup projektu

```bash
# Naklonuj repozitář
git clone https://github.com/Cmajda/ha_cez_distribuce.git
cd ha_cez_distribuce

# Postav frontend
./build.sh
```

### 2. Development workflow

```bash
# Přejdi do frontend složky
cd custom_components/cez_hdo/frontend

# Instaluj dependencies
npm install

# Spusť development server
npm run dev

# V jiném terminálu spusť watch mode
npm run watch
```

### 3. Testing

```bash
# Python testy
python -m pytest tests/

# Type checking
mypy custom_components/cez_hdo/

# Linting
ruff check custom_components/cez_hdo/
```

## 📁 Struktura projektu

```
ha_cez_distribuce/
├── custom_components/cez_hdo/
│   ├── __init__.py           # Hlavní inicializace komponenty
│   ├── manifest.json         # HA metadata
│   ├── base_entity.py        # Základní třída pro entity
│   ├── downloader.py         # API client pro ČEZ data
│   ├── binary_sensor.py      # Binární senzory
│   ├── sensor.py            # Časové senzory
│   └── frontend/            # Custom Lovelace karta
│       ├── src/
│       │   ├── cez-hdo-card.ts
│       │   ├── editor.ts
│       │   └── types.ts
│       ├── package.json
│       ├── webpack.config.js
│       └── dist/           # Buildované soubory
├── .github/workflows/      # CI/CD
├── build.sh               # Build skript
└── README.md
```

## 🔧 Vývoj Python komponenty

### Přidání nové entity

1. Rozšiř `base_entity.py` pokud potřebuješ novou funkcionalitu
2. Vytvoř novou třídu v příslušném souboru (sensor.py/binary_sensor.py)
3. Zaregistruj v `setup_platform` funkci

### Úprava API klienta

Všechny změny v `downloader.py`:
- Udržuj zpětnou kompatibilitu
- Přidej proper error handling
- Aktualizuj type hints

## 🎨 Vývoj Frontend karty

### Hot reload development

```bash
cd custom_components/cez_hdo/frontend
npm run dev
```

Otevři browser na `http://localhost:8080` pro live preview.

### Přidání nové konfigurace

1. Aktualizuj `types.ts` s novými interface
2. Přidej do `editor.ts` konfigurace pole
3. Implementuj v `cez-hdo-card.ts`

### Styling

Používáme:
- CSS Custom Properties pro theming
- Flexbox pro layout
- CSS Grid pro složitější layouts

## 🧪 Testing

### Python testy

```bash
# Všechny testy
python -m pytest

# Specifický test
python -m pytest tests/test_downloader.py

# S coverage
python -m pytest --cov=custom_components.cez_hdo
```

### Frontend testy

```bash
cd custom_components/cez_hdo/frontend

# Unit testy
npm test

# E2E testy
npm run test:e2e
```

## 📦 Build a Release

### 1. Příprava

```bash
# Zkontroluj změny
git status

# Spusť všechny testy
npm run test
python -m pytest

# Zkontroluj linting
npm run lint
ruff check .
```

### 2. Verze

```bash
# Aktualizuj verzi v manifest.json
# Vytvoř changelog
# Commit změny
git add .
git commit -m "chore: bump version to 1.1.0"
```

### 3. Build

```bash
# Postav production frontend
./build.sh

# Ověř že vše funguje
ls custom_components/cez_hdo/frontend/dist/
```

### 4. Release

```bash
# Vytvoř tag
git tag v1.1.0
git push origin v1.1.0

# GitHub automaticky vytvoří release
```

## 🐛 Debugging

### Python debugging

```python
# Přidej do kódu
import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Debug message")
```

### Frontend debugging

```javascript
// V browser dev tools
console.log('Card config:', this.config);
console.log('HA entity:', this.hass.states['binary_sensor.cez_hdo_lowtariffactive']);
```

### Common issues

1. **Entity nedostupné** - Zkontroluj configuration.yaml
2. **Karta se neloaduje** - Zkontroluj browser console
3. **Build fails** - Smaž node_modules a reinstaluj

## 📚 Užitečné odkazy

- [Home Assistant Developers](https://developers.home-assistant.io/)
- [Lovelace Card Development](https://developers.home-assistant.io/docs/frontend/custom-ui/custom-card/)
- [LitElement Documentation](https://lit.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 🤝 Contributing

1. Fork repository
2. Vytvoř feature branch
3. Implementuj změny s testy
4. Vytvoř pull request
5. Projdi code review

### Code style

- Python: PEP 8 + Black formatting
- TypeScript: Prettier + ESLint
- Commits: Conventional commits format
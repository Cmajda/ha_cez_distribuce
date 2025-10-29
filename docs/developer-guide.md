# ČEZ HDO - Vývojářská dokumentace

## 📑 Obsah

- [🚀 Úvod pro vývojáře](#-úvod-pro-vývojáře)
- [🏗️ Struktura projektu](#️-struktura-projektu)
- [⚙️ Development prostředí](#️-development-prostředí)
- [🔧 Build a deployment](#-build-a-deployment)
- [🎨 Frontend development](#-frontend-development)
- [🐍 Backend development](#-backend-development)
- [✅ Testování](#-testování)
- [📦 Release workflow](#-release-workflow)
- [🤖 GitHub Copilot instrukce](#-github-copilot-instrukce)

## 🚀 Úvod pro vývojáře

Vítejte v projektu ČEZ HDO integrace pro Home Assistant! Tato dokumentace vám pomůže začít s vývojem.

### Předpoklady

- Python 3.9+
- Node.js 16+
- Home Assistant development prostředí
- Git

## 🏗️ Struktura projektu

```
ha_cez_distribuce/
├── dev/                          # Development workspace
│   ├── src/                      # Python zdrojové soubory
│   │   ├── __init__.py
│   │   ├── binary_sensor.py
│   │   ├── sensor.py
│   │   ├── downloader.py
│   │   ├── base_entity.py
│   │   └── manifest.json
│   ├── frontend/                 # TypeScript frontend
│   │   ├── src/
│   │   │   └── cez-hdo-card-working.ts
│   │   ├── dist/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── webpack.config.js
│   └── deploy-dev.sh            # Build a deployment skript
├── custom_components/cez_hdo/    # Production soubory
│   ├── *.py                     # Python komponenty
│   ├── manifest.json
│   └── frontend/dist/           # Zkompilovaný frontend
├── docs/                        # Dokumentace
│   ├── user-guide.md
│   └── developer-guide.md
└── README.md                    # Hlavní dokumentace
```

### Filosofie struktury

- **`/dev`** - Veškerý development
- **`/custom_components`** - Pouze production-ready soubory pro GitHub
- **Čisté oddělení** - žádné dev soubory v distribuci

## ⚙️ Development prostředí

### První nastavení

1. **Klonování projektu:**
   ```bash
   git clone https://github.com/Cmajda/ha_cez_distribuce.git
   cd ha_cez_distribuce
   ```

2. **Nastavení frontend dependencies:**
   ```bash
   cd dev/frontend
   npm install
   ```

3. **Nastavení Python prostředí:**
   ```bash
   # Doporučeno: použít virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # nebo
   venv\Scripts\activate     # Windows
   ```

### Development workflow

```bash
# 1. Editace v dev struktuře
cd dev/
# Upravte Python soubory v src/
# Upravte TypeScript v frontend/src/

# 2. Build a deployment do HA
./deploy-dev.sh

# 3. Test v Home Assistant
# - Restart HA
# - Zkontrolujte logy
# - Testujte funkčnost

# 4. Clean start (pokud potřeba)
./deploy-dev.sh clean
```

## 🔧 Build a deployment

### Deploy skript

`deploy-dev.sh` provádí:

1. **Version checking** - kontrola verzí mezi dev a production
2. **Frontend build** - npm build z TypeScript
3. **Component deployment** - kopírování do HA
4. **Frontend deployment** - kopírování karty do www
5. **Configuration setup** - automatické přidání do `configuration.yaml`
6. **Verification** - kontrola úspěšnosti

### Použití

```bash
# Standardní deployment
./deploy-dev.sh

# Clean removal (s interaktivním odstraněním konfigurace)
./deploy-dev.sh clean
```

### Customizace prostředí

```bash
# Vlastní Home Assistant config adresář
export HA_CONFIG_DIR="/path/to/your/ha-config"
./deploy-dev.sh
```

## 🎨 Frontend development

### Struktura

```typescript
// dev/frontend/src/cez-hdo-card-working.ts
import { LitElement, html, css } from 'lit';

class CezHdoCard extends LitElement {
  // Lovelace karta implementace
}
```

### Build process

```bash
cd dev/frontend

# Development build
npm run build

# Watch mode (při vývoju)
npm run watch  # pokud je nakonfigurován
```

### Webpack konfigurace

- **Entry point:** `src/cez-hdo-card-working.ts`
- **Output:** `dist/cez-hdo-card.js`
- **Mode:** production pro optimalizaci

## 🐍 Backend development

### Komponenty

- **`__init__.py`** - Hlavní integrace, frontend auto-instalace
- **`sensor.py`** - HDO senzory (časy, duration)
- **`binary_sensor.py`** - HDO binary senzory (active/inactive)
- **`downloader.py`** - API komunikace s ČEZ Distribuce
- **`base_entity.py`** - Společná funkcionalita

### API integrace

```python
# downloader.py
async def fetch_hdo_data(region: str, code: str) -> dict:
    """Stažení HDO dat z ČEZ API"""
    url = f"https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/{region}?code={code}"
    # ... implementace
```

### Debugging

```yaml
# configuration.yaml
logger:
  logs:
    custom_components.cez_hdo: debug
    custom_components.cez_hdo.downloader: debug
```

## ✅ Testování

### Lokální testování

1. **Deploy do test HA instance:**
   ```bash
   HA_CONFIG_DIR="/path/to/test-ha" ./deploy-dev.sh
   ```

2. **Kontrola logů:**
   - Developer Tools → Logs
   - Filtr: `custom_components.cez_hdo`

3. **Test API endpoint:**
   ```bash
   curl "https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/stred?code=405"
   ```

### Validace

- **Python lint:** `flake8`, `black`, `isort`
- **TypeScript:** ESLint, TypeScript compiler
- **Markdown:** Markdown lint (via GitHub Actions)

## 📦 Release workflow

### Pre-release checklist

1. **Aktualizace verzí:**
   - `dev/src/manifest.json`
   - `dev/frontend/package.json`
   - Frontend kód (console.log verze)

2. **Build a test:**
   ```bash
   ./deploy-dev.sh
   # Kompletní test všech funkcí
   ```

3. **Synchronizace production:**
   ```bash
   # Kopírování z dev do custom_components
   # (deploy skript toto dělá automaticky)
   ```

### GitHub release

1. **Commit změn** v dev struktuře
2. **Tag nové verze:** `v1.x.x`
3. **GitHub vytvoří release** automaticky
4. **Uživatelé stáhnou** čisté `custom_components/`

## 🤖 GitHub Copilot instrukce

Pro práci s GitHub Copilot na tomto projektu:

### Template pro začátek práce

```text
@GitHub Copilot - pracovní instrukce:
- Používej isBackground: true pro všechny terminálové příkazy
- Dev struktura: /dev/, Production: /custom_components/
- Build: ./dev/deploy-dev.sh, Clean: ./dev/deploy-dev.sh clean
Řiď se těmito pravidly.
```

### Workflow poznámky

- **Terminálové příkazy:** Vždy `isBackground: true`
- **File operations:** Preferovat dev strukturu
- **Testing:** Použít deploy skript pro validaci

### Troubleshooting

Pokud Copilot "zasekne" na terminálových příkazech:
1. Použijte `isBackground: true`
2. Nekombinujte background/foreground příkazy
3. Připomeňte instrukcí na začátku práce

---

**Happy coding! 🚀**

Pro otázky nebo návrhy vytvořte GitHub issue nebo pull request.

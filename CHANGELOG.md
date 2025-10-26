# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-26

### Added
- 🎨 **Custom Lovelace Card** - Nová TypeScript karta pro lepší zobrazení HDO dat
- 🏗️ **Base Entity Class** - Refaktorovaná architektura s base třídou pro eliminaci duplicit
- 🔧 **Improved Error Handling** - Lepší zpracování chyb a logování
- 📦 **Frontend Build System** - Webpack konfigurace pro TypeScript compilation
- 🧪 **Pre-commit Hooks** - Automatické code quality checks
- 📚 **Development Documentation** - Kompletní návod pro vývojáře

### Changed
- ♻️ **Code Refactoring** - Eliminace duplicitního kódu v sensor třídách
- 🔄 **Update Logic** - Zjednodušená logika pro aktualizaci dat
- 📝 **Dependencies** - Přidány explicitní dependencies (requests, lxml)
- 🏷️ **Type Hints** - Vylepšené type annotations napříč kódem

### Fixed
- 🐛 **HACS Compatibility** - Opravena kompatibilita se standardy HACS
- 🔧 **GitHub Actions** - Aktualizované workflows na nejnovější verze
- 📄 **Manifest** - Synchronizované verze mezi hacs.json a manifest.json

### Technical Details
- **Python Code**: Refaktorováno ~60% duplicitního kódu
- **Frontend**: TypeScript + Webpack + LitElement stack
- **Build System**: Automatizovaný build process
- **Quality**: Pre-commit hooks s Ruff + MyPy
- **Documentation**: Comprehensive dev guide

## [1.0.1] - 2025-10-26

### Fixed
- 🔧 **HACS Validation** - Opraveny problémy s HACS validací
- 📄 **Metadata** - Aktualizovány informace v manifestu

## [1.0.0] - 2024-XX-XX

### Added
- ⚡ **Initial Release** - Základní funkcionalita HDO sensorů
- 📊 **Binary Sensors** - LowTariffActive, HighTariffActive
- ⏰ **Time Sensors** - Start, End, Duration pro oba tarify
- 🌍 **Regional Support** - Západ, Sever, Střed, Východ, Morava
- 📡 **API Integration** - Stahování dat z ČEZ Distribuce

### Technical Implementation
- **Data Source**: `https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/`
- **Update Frequency**: 1 hour throttling
- **Supported Regions**: 5 ČEZ distribution regions
- **Entities**: 8 total (2 binary + 6 regular sensors)

---

## Migration Guide

### From 1.0.x to 1.1.0

1. **Backup Configuration**
   ```yaml
   # Současná konfigurace zůstává stejná
   binary_sensor:
     - platform: cez_hdo
       region: stred
       code: 405
   ```

2. **Update Integration**
   - Přes HACS: automatické update
   - Manuálně: stáhni novou verzi

3. **Optional: Add Custom Card**
   ```yaml
   # Nová Lovelace karta
   type: custom:cez-hdo-card
   entities:
     low_tariff: binary_sensor.cez_hdo_lowtariffactive
     # ... další entity
   ```

4. **Restart Home Assistant**

### Breaking Changes
- ✅ **None** - Zpětná kompatibilita zachována
- ✅ **Entity Names** - Beze změn
- ✅ **Configuration** - Stejná struktura

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Cmajda/ha_cez_distribuce/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Cmajda/ha_cez_distribuce/discussions)
- 📖 **Documentation**: [README.md](README.md)
- 🔧 **Development**: [DEVELOPMENT.md](DEVELOPMENT.md)
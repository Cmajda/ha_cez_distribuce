# ČEZ HDO - TODO

## ✅ Dokončeno

- [x] **Issue 1: www složka** - Opraveno pomocí `hass.config.path()`
- [x] **Issue 2: Logging HA Style Guidelines** - Opraveno
- [x] **DataUpdateCoordinator refaktoring** - Centralizovaná správa dat
- [x] **Config Flow** - GUI konfigurace přes Settings → Devices & Services
- [x] **Oprava duplicitních unique_id** - Entry ID v unique_id pro config entries
- [x] **Oprava set_prices služby** - Funguje i pro config entries
- [x] **Senzor "zbývá"** - Zobrazuje "00:00" místo unknown
- [x] **Deploy skript** - Nepřidává YAML, používá Config Flow
- [x] **Device registry** - Seskupit všechny entity pod jedno "zařízení" v HA
- [x] **Data storage** - Přesunuto z `www/cez_hdo/` do `custom_components/cez_hdo/data/`
- [x] **Diagnostika** - Přidat `diagnostics.py` pro debug export
- [x] **Options Flow** - Možnost upravit nastavení po přidání integrace (změna EAN, signálu)

## 🔮 Možné další kroky

- [ ] **Unit testy** - Pokrytí kódu testy
- [ ] **Update interval** - Změnit z 10 minut na 1 hodinu pro produkci
- [ ] **HACS** - Připravit pro publikaci do HACS
- [ ] **Aktualizovat dokumentaci** - README.md, user-guide.md, RELEASE_NOTES.md pro v3.0.0

# 🎉 Release v1.2.0 - HACS Frontend Integration

## ✨ Nové funkce

### 🔧 HACS Frontend Integration
- **Automatické deployment frontend karty** přes HACS infrastrukturu
- **Nové URL schema**: `/hacsfiles/integrations/cez_hdo/` místo `/local/cez_hdo/`
- **Zjednodušená instalace** - frontend karta se nasadí automaticky s integrací
- **Lepší kompatibilita** s HACS ekosystémem

### 📝 Dokumentace
- **Aktualizované návody** s novými HACS URL
- **Přepracovaný README** s jasnější strukturou
- **Nová user guide** v `docs/` složce

## 🛠️ Technické vylepšení

- **Manifest.json** rozšířen o `"frontend": true` flag
- **Zjednodušený __init__.py** - odstraněno manuální kopírování frontend souborů
- **GitHub Actions** validace prochází bez chyb
- **Pre-commit hooks** pro konzistentní kvalitu kódu

## 🔄 Migration Guide

### Pro nové uživatele
Žádné změny - integrace funguje out-of-the-box s HACS.

### Pro existující uživatele
1. **Aktualizujte integraci** přes HACS
2. **Aktualizujte Lovelace kartu URL** v `configuration.yaml`:
   ```yaml
   lovelace:
     resources:
       - url: /hacsfiles/integrations/cez_hdo/cez-hdo-card.js
         type: module
   ```

## 📋 Kompletní changelog

- ✅ Přidána HACS frontend integrace
- ✅ Aktualizováno URL schema na `/hacsfiles/`
- ✅ Zjednodušen deployment proces
- ✅ Vylepšena dokumentace
- ✅ Opraveny GitHub Actions validace
- ✅ Aktualizovány všechny verze na v1.2.0

## 🎯 Co to znamená pro uživatele

- **Jednodušší instalace** - vše se nasadí automaticky
- **Lepší integrace** s HACS prostředím
- **Stabilnější aktualizace** - konzistentní s HACS standardy
- **Budoucí kompatibilita** s novými HACS funkcemi

---

**Velké díky všem, kdo pomohli s testováním a zpětnou vazbou! 🙏**

**Pro podporu a otázky:** https://github.com/Cmajda/ha_cez_distribuce/issues

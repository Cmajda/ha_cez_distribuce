# ČEZ HDO - Upgrade Guide

## 🔄 Migrace ze starého API na nové EAN API

### ⚠️ Důležité změny v verzi 1.2.0+

**Stará konfigurace (již nepodporována):**
```yaml
sensor:
  - platform: cez_hdo
    code: "405"           # ❌ Již nepodporováno
    region: "stred"       # ❌ Již nepodporováno
```

**Nová konfigurace (povinná):**
```yaml
sensor:
  - platform: cez_hdo
    ean: "VA_EAN_ČÍSLO"   # ✅ Nový povinný parametr
    signal: "a3b4dp01"    # ✅ Volitelný - konkrétní HDO signál
```

### 🔍 Jak najít EAN číslo

EAN číslo vašeho odběrného místa najdete:

- 📄 **Na faktuře za elektřinu** - obvykle označeno jako "EAN" nebo "Kód odběrného místa"
- 🌐 **V zákaznickém portálu ČEZ** - v detailech vaší smlouvy
- 📞 **Kontaktováním zákaznické linky ČEZ**

**Formát:** Dlouhé číselné kód (18 číslic), například `"859182400609846929"`

### 🛠️ Postup migrace

1. **Najděte své EAN číslo** (viz výše)

2. **Zjistěte dostupné signály** pomocí service:
   ```yaml
   # V Home Assistant Developer Tools → Services
   action: cez_hdo.list_signals
   data:
     ean: "VAŠE_EAN_ČÍSLO"
   ```

3. **Aktualizujte configuration.yaml:**
   ```yaml
   # Odstraňte starou konfiguraci
   sensor:
     - platform: cez_hdo
       ean: "VAŠE_EAN_ČÍSLO"
       signal: "a3b4dp01"      # Volitelné - použijte jeden ze seznamu

   binary_sensor:
     - platform: cez_hdo
       ean: "VAŠE_EAN_ČÍSLO"
       signal: "a3b4dp01"      # Stejný signal jako u sensoru
   ```

4. **Restartujte Home Assistant**

### 📊 Co se změnilo

| Stará verze | Nová verze | Poznámka |
|-------------|------------|----------|
| `code: "405"` | `ean: "859182400..."` | EAN z faktury místo regionálního kódu |
| `region: "stred"` | ❌ Odstraněno | Region se určuje automaticky z EAN |
| Jeden signál | Výběr ze signálů | Service `list_signals` zobrazí možnosti |
| Staré API | Nové ČEZ API | Modernější a spolehlivější zdroj dat |

### ✅ Výhody nového API

- 🎯 **Přesnější data** - přímé propojení s ČEZ Distribuce
- 🔄 **Více signálů** - možnost výběru nejvhodnějšího HDO signálu
- 🛡️ **Spolehlivější** - nové API je oficiálně podporované
- 🚀 **Service funkce** - `list_signals` pro snadné zjištění možností

### 🆘 Řešení problémů

**Chyba: "EAN parameter is required"**
- Zkontrolujte, že máte správně zadané EAN číslo v configuration.yaml
- EAN musí být v uvozovkách jako string

**Chyba: "No signals found for EAN"**
- Ověřte správnost EAN čísla na faktuře
- Zkuste kontaktovat ČEZ pro ověření EAN čísla

**Entities nejsou dostupné po migraci:**
- Restartujte Home Assistant
- Zkontrolujte logy v Developer Tools → Logs
- Ověřte syntax YAML konfigurace

### 📖 Další zdroje

- 📘 [Uživatelská dokumentace](user-guide.md) - kompletní návod
- 🛠️ [Service guide](service-guide.md) - jak používat `list_signals`
- 🏗️ [Developer guide](developer-guide.md) - pro vývojáře

---

**Potřebujete pomoc?** Vytvořte [GitHub Issue](https://github.com/Cmajda/ha_cez_distribuce/issues) s detaily vašeho problému.
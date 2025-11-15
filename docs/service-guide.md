# ČEZ HDO - Services a Signal Selection

> 📖 **Poznámka:** Tato funkcionalita je nyní součástí hlavní integrace. Pro základní konfiguraci použijte [uživatelskou dokumentaci](user-guide.md).

## 🛠️ Dostupné Services

### 1. Service `cez_hdo.list_signals`

Služba pro zobrazení dostupných HDO signálů pro zadané EAN číslo.

**Použití:**
```yaml
action: cez_hdo.list_signals
data:
  ean: "VÁŠ_EAN_KÓD"
```

**Výstup v logách Home Assistant:**
```
📡 Nalezené signály pro EAN VÁŠ_EAN_KÓD: a3b4dp01, a3b4dp02, a3b4dp06
```

### 2. Volitelný parametr `signal`

Možnost specifikace konkrétního signálu v konfiguraci.

## 📋 Konfigurace

### Základní konfigurace (používá první nalezený signál)

```yaml
sensor:
  - platform: cez_hdo
    ean: "VÁŠ_EAN_KÓD"

binary_sensor:
  - platform: cez_hdo
    ean: "VÁŠ_EAN_KÓD"
```

### Pokročilá konfigurace (konkrétní signál)

```yaml
sensor:
  - platform: cez_hdo
    ean: "VÁŠ_EAN_KÓD"
    signal: "a3b4dp06"  # Konkrétní signál

binary_sensor:
  - platform: cez_hdo
    ean: "VÁŠ_EAN_KÓD"
    signal: "a3b4dp06"  # Konkrétní signál
```

## 🔍 Jak najít váš signál

1. **Zavolejte service:**
   ```yaml
   action: cez_hdo.list_signals
   data:
     ean: "VAŠE_EAN_ČÍSLO"
   ```

2. **Podívejte se do logů Home Assistant** - service vypíše všechny dostupné signály (úroveň WARNING)
   - **Settings** → **System** → **Logs**
   - Výsledky budou viditelné ihned jako WARNING zprávy
   - Hledejte záznamy s `📡 Dostupné signály` nebo `🎯 Signal:`

3. **Vyberte signál** podle vašich potřeb:
   - `a3b4dp01`, `a3b4dp02` - obvykle základní HDO signály (dlouhé období)
   - `a3b4dp06` - často kratší období nebo speciální tarify

## ⚙️ Logika výběru signálu

- **Bez `signal` parametru:** Použije se **první nalezený** signál pro daný den
- **S `signal` parametrem:** Hledá konkrétní signál, pokud neexistuje, fallback na první
- **Automatické fallback:** Pokud zadaný signál neexistuje, systém se vrátí k prvnímu dostupnému

## 🎯 Příklady použití

### Zjištění dostupných signálů

```yaml
# V Home Assistant Developer Tools -> Services
action: cez_hdo.list_signals
data:
  ean: "VÁŠ_EAN_KÓD"
```

### Konfigurace pro konkrétní signál
```yaml
# configuration.yaml
sensor:
  - platform: cez_hdo
    ean: "VÁŠ_EAN_KÓD"
    signal: "a3b4dp06"
```

## 🔧 Services dostupné v integraci

| Service | Popis | Parametry |
|---------|--------|-----------|
| `cez_hdo.list_signals` | Zobrazí dostupné signály pro EAN | `ean` (povinný) |
| `cez_hdo.reload_frontend_card` | Obnoví frontend kartu | žádné |

## 📝 Poznámky

- Service `list_signals` vypisuje informace do logů Home Assistant
- Pokud není specifikován `signal`, používá se první dostupný
- Různé signály mohou mít různé časové rozvrhy
- Doporučujeme použít service k objevení všech dostupných signálů před konfigurací

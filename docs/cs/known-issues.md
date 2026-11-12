# 🐛 Známé problémy

Tento soubor obsahuje seznam známých problémů a jejich stav řešení.

---

## Aktuální problémy (v3.3.1)

### 1. Automatické obnovení může selhat při nedostupnosti OCR nebo API

**Stav:** ⚠️ Závislost na externích službách

**Popis:** Automatické obnovení používá OCR pro řešení CAPTCHA a závisí na dostupnosti OCR služby i API ČEZ Distribuce.
Při výpadku nebo omezení požadavků se data nemusí obnovit včas; jejich platnost je 6 dní.

**Řešení:** Spusťte **Manuálně obnovit** na Lovelace kartě, zadejte CAPTCHA a vyberte signál. Dosud uložená data zůstanou dostupná, pokud ruční obnova selže.
Vlastní OCR.space API klíč v nastavení integrace obejde limity sdíleného demo klíče, viz [OCR API klíč](user-guide.md#ocr-api-klíč).

### 2. Kompatibilita s Home Assistant 2026.02+ (v3.1.0)

**Stav:** ✅ Vyřešeno v v3.1.1

**Popis:** V Home Assistant 2026.02+ byla změněna struktura `LovelaceData`.
Objekt již nemá atribut `mode`, což způsobovalo chybu při spuštění integrace:
`'LovelaceData' object has no attribute 'mode'`

**Řešení:** Nová detekce storage režimu pomocí kontroly typu resources kolekce.

**Sledování:** [#62](https://github.com/Cmajda/ha_cez_distribuce/issues/62)

---

### 3. CAPTCHA ochrana API ČEZ Distribuce

**Stav:** ✅ Vyřešeno v v3.1.0

**Popis:** ČEZ Distribuce zavedl CAPTCHA ochranu na svém API, což způsobovalo
nefunkčnost integrace pro nové instalace.

**Řešení:** Integrace zobrazuje CAPTCHA během konfigurace a ukládá přijatá data do cache.
Automatické obnovení se pokouší řešit CAPTCHA pomocí OCR; data lze obnovit také
tlačítkem **Manuálně obnovit** na Lovelace kartě.

**Sledování platnosti:** Nové senzory `data_valid`, `days_until_expiry`,
`data_age_days` a `data_valid_until` umožňují sledovat platnost dat
a vytvářet automatizace pro upozornění.

---

### 4. Služba set_prices nerozeznává zařízení

**Stav:** ⚠️ Známé omezení

**Popis:** Služba `cez_hdo.set_prices` (volatelná přes Nástroje pro vývojáře → Služby)
nastavuje ceny pro všechny instance integrace. Nelze rozlišit, kterému
zařízení se mají ceny nastavit.

**Dočasné řešení:** Pro změnu cen použijte Options Flow v nastavení integrace
(Nastavení → Zařízení a služby → ČEZ HDO → Konfigurovat).

**Plánované řešení:** Přidání parametru `device_id` nebo `entry_id` do služby
pro rozlišení konkrétního zařízení.

---

## Archiv vyřešených problémů (v3.0.0-RC.1)

> **Stav:** Všechny problémy z v3.0.0-RC.1 byly vyřešeny v RC.2.

### Priorita 1 - Kritické

### ~~1. Senzory se neaktualizují v reálném čase~~ ✅

**Stav:** ✅ Vyřešeno

**Popis:** Stav senzorů času a binárních senzorů aktivních tarifů se mění
pouze při restartu Home Assistant. Refresh dat musí být častější
(ideálně 1-2 sec pro countdown), odděleně od stahování dat z API.

**Řešení:** Přidán samostatný interval pro přepočet stavu (5 sekund),
nezávislý na stahování dat z API (1 hodina).

**Nahlásili:** @micjon, @pokornyIt

---

### ~~2. UI karta není zaregistrována~~ ✅

**Stav:** ✅ Není bug

**Popis:** Frontend karta není zaregistrována v Lovelace, ačkoliv v logu
je uvedeno že zaregistrována je.

**Řešení:** Nutný refresh prohlížeče (Ctrl+F5 nebo Cmd+Shift+R) po restartu HA.

**Nahlásil:** @pokornyIt

---

### ~~3. Nelze změnit ceny VT/NT po nastavení~~ ✅

**Stav:** ✅ Není bug

**Popis:** Po počátečním nastavení integrace nejde změnit ceny VT/NT.
Options flow nefunguje nebo není dostupný.

**Řešení:** Postup pro změnu cen:
Settings → Devices & Services → ČEZ HDO → Configure (ozubené kolo) →
proklikat kroky → poslední krok je nastavení cen.

Dokumentováno v [user-guide.md](user-guide.md#-nastavení-cen).

**Nahlásil:** @pokornyIt

---

### ~~4. EAN v logu - citlivá hodnota~~ ✅

**Stav:** ✅ Vyřešeno

**Popis:** EAN kód se zobrazuje v logu v plném znění. Pokud je to citlivá
hodnota, měl by být maskován (např. `859182400600xxxxx`).

**Řešení:** Přidány helper funkce `mask_ean()` a `ean_suffix()` v `const.py`.
EAN je nyní maskován v logu jako `***...XXXXXX` (zobrazeno posledních 6 číslic).
Názvy cache/price souborů používají pouze suffix EAN (posledních 6 číslic).

**Nahlásil:** @pokornyIt

---

## Priorita 2 - Střední

### ~~5. Více signálů pro jeden EAN - neintuitvní názvy entit~~ ✅

**Stav:** ✅ Vyřešeno

**Popis:** Pokud EAN má více signálů:

1. Jaké jméno bude mít device při přidání více signálů?
2. Názvy entit jsou neintuitvní (např. `binary_sensor.cez_hdo_nizky_tarif_aktivni_1`)

**Řešení:** Přidán nový krok v config flow pro zadání přípony entit.

- Výchozí přípona: `{EAN4}_{signál}` (např. `7606_a1b4dp04`)
- **Uživatel může zadat vlastní příponu** (např. `chalupa`, `byt`, `dum`)
- Entity mají ID: `sensor.cez_hdo_lowtariffstart_{pripona}`
- Device: `ČEZ HDO 967606 (a1b4dp04)`
- Stejné EAN lze přidat vícekrát s různými signály

**Nahlásil:** @pokornyIt

---

### ~~6. Debug log obsahuje emoji ikonu~~ ✅

**Stav:** ✅ Vyřešeno

**Popis:** Debug log message obsahuje emoji ikonu (🔴), což může
způsobovat problémy v některých systémech.

```log
# Před (s emoji)
2026-01-30 09:25:45 DEBUG ... 🔴 IN HIGH TARIFF: 06:15:00-14:10:00

# Po (bez emoji)
2026-01-30 09:25:45 DEBUG ... [VT] IN HIGH TARIFF: 06:15:00-14:10:00
```

**Řešení:** Emoji nahrazeny textovými značkami `[NT]` a `[VT]`.

**Nahlásil:** @pokornyIt

---

## Vyřešené

- **Issue #1:** Senzory se neaktualizují v reálném čase
- **Issue #2:** UI karta není zaregistrována (nutný refresh prohlížeče)
- **Issue #3:** Nelze změnit ceny VT/NT (dokumentováno v user-guide.md)
- **Issue #4:** EAN v logu - maskován na posledních 6 číslic
- **Issue #5:** Více signálů pro EAN - device obsahuje název signálu
- **Issue #6:** Debug log obsahuje emoji ikonu

---

## Jak nahlásit problém

1. Zkontrolujte, zda problém již není v tomto seznamu
2. Vytvořte [GitHub Issue](https://github.com/Cmajda/ha_cez_distribuce/issues)
3. Přiložte diagnostiku (Nastavení → Zařízení → ČEZ HDO → ⋮ → Stáhnout diagnostiku)

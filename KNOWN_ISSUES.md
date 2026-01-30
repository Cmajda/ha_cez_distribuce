# 🐛 Známé problémy (v3.0.0-RC.1)

Tento soubor obsahuje seznam známých problémů a jejich stav řešení.

## Priorita 1 - Kritické

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

Dokumentováno v [user-guide.md](docs/user-guide.md#-nastavení-cen).

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

**Řešení:** Každý signál nyní vytváří vlastní device s názvem obsahujícím signál.

- Device: `ČEZ HDO 967606 (a1b4dp04)`
- Device ID zahrnuje signál: `{ean}_{signal}`
- Entity jsou seskupeny pod správný device podle signálu

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
3. Přiložte diagnostiku (Settings → Devices → ČEZ HDO → ⋮ → Download diagnostics)

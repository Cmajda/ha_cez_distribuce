# Přispívání (Contributing)

🇬🇧 [English version](CONTRIBUTING_EN.md)

Díky, že chceš přispět! Tento repozitář obsahuje **CEZ HDO – vlastní integraci pro Home Assistant**.

Používáme jednoduchý workflow vhodný pro malý tým: **`main` je vždy releasovatelný** a každá změna jde přes krátkodobou větev a Pull Request (PR).

---

## Obsah

- [Přispívání (Contributing)](#přispívání-contributing)
  - [Obsah](#obsah)
  - [Přehled workflow](#přehled-workflow)
  - [Pravidla pro branche](#pravidla-pro-branche)
    - [Pojmenování branchí](#pojmenování-branchí)
  - [Konvence pro názvy commitů a PR](#konvence-pro-názvy-commitů-a-pr)
    - [Formát](#formát)
    - [Povolené typy](#povolené-typy)
    - [Příklady](#příklady)
    - [Doporučení](#doporučení)
  - [Pull Requesty](#pull-requesty)
    - [Název PR](#název-pr)
    - [Očekávání pro PR](#očekávání-pro-pr)
  - [Pravidla merge](#pravidla-merge)
  - [Tagování a releasy](#tagování-a-releasy)
    - [Příkazy (příklad)](#příkazy-příklad)
  - [Když si nevíš rady](#když-si-nevíš-rady)

---

## Přehled workflow

1. (Volitelné) Vytvoř Issue popisující změnu.
2. Pro každou změnu vytvoř větev z `main`.
3. Commity dělej podle konvence níže.
4. Otevři Pull Request (PR) zpět do `main`.
5. PR musí projít CI a být schválen.
6. Merge proveď pomocí **Squash & merge**.
7. Po úspěšném merge **smaž zdrojovou větev**.
8. Podle potřeby vytvoř **ruční git tag**.

---

## Pravidla pro branche

- **`main` je vždy releasovatelný.**
- Přímé pushování do `main` není povoleno (pouze přes PR).
- Pro každou aktivitu vytvoř novou větev z `main`.
- Větve drž krátké a tematicky zaměřené.

### Pojmenování branchí

Používej jeden z těchto prefixů:

- `feature/<short-title>`
- `fix/<short-title>`
- `docs/<short-title>`
- `chore/<short-title>`

Pokud máš číslo Issue, můžeš ho do názvu zahrnout:

- `feature/123-add-new-sensor`
- `fix/87-handle-timeout`

Bez Issue:

- `feature/add-new-sensor`
- `docs/update-readme`

Názvy drž krátké, malými písmeny, slova odděluj `-`.

---

## Konvence pro názvy commitů a PR

Používáme jednoduchou variantu Conventional Commits.

### Formát

Commit zprávy piš vždy **anglicky** (typ i krátké shrnutí).

```plain
<type>: <short short imperative English summary>
```

### Povolené typy

- `feat:` – nová funkce / nová funkcionalita
- `fix:` – oprava chyby
- `docs:` – pouze dokumentace
- `chore:` – údržba / refaktor / tooling / formátování
- `test:` – pouze testy
- `ci:` – změny v CI pipeline

### Příklady

- `feat: add service to refresh data`
- `fix: handle API timeout during startup`
- `docs: clarify installation steps`
- `chore: reorganize config constants`
- `test: add unit tests for coordinator`

### Doporučení

- Používej přítomný čas (“add”, “fix”, “update”).
- Drž to krátké (ideálně do ~70 znaků).
- Pokud je to relevantní, odkaž na issue v popisu PR (např. `Closes #123`).

---

## Pull Requesty

### Název PR

Názvy PR musí dodržovat stejnou konvenci jako commity:

```plain
<type>: <short summary>
```

### Očekávání pro PR

- PR drž malé a dobře reviewovatelné (jedna logická změna).
- CI musí projít.
- Před merge je potřeba alespoň **1 schválení**.
- Pokud PR řeší Issue, odkaž na něj v popisu PR (např. `Closes #123`).

---

## Pravidla merge

- Vše do `main` jde přes PR.
- CI musí projít.
- Je potřeba alespoň **1 schválení**.
- Merge metoda je vždy **Squash & merge**.
- Po merge **smaž zdrojovou větev**.

---

## Tagování a releasy

Tagy vytváříme **ručně** a jsou **neměnné** (nikdy se nepřepisují / neposouvají).

- Používáme semantic versioning: `vMAJOR.MINOR.PATCH` (např. `v1.4.2`).
  - **PATCH** pro opravy chyb
  - **MINOR** pro zpětně kompatibilní nové funkce
  - **MAJOR** pro breaking changes

### Příkazy (příklad)

Vytvoření a push nového tagu pro aktuální `main` HEAD:

```bash
git checkout main
git pull

git tag v1.2.3
git push origin v1.2.3
```

---

## Když si nevíš rady

Pokud si nejsi jistý/á rozsahem, názvoslovím nebo tagováním, otevři draft PR co nejdřív a domluvte se přímo v něm.

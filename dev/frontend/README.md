# ČEZ HDO Card - Frontend

Zdrojový kód pro Lovelace kartu ČEZ HDO integrace.

## Požadavky

- Node.js 18+
- npm nebo yarn

## Instalace závislostí

```bash
cd dev/frontend
npm install
```

## Vývoj

Pro sledování změn a automatickou rekompilaci:

```bash
npm run dev
```

## Build

Pro produkční build (s minifikací a bez console.log):

```bash
npm run build:prod
```

Výsledný soubor bude v `dist/cez-hdo-card.js`.

## Deployment

Po buildu zkopírujte výsledný soubor do integrace:

```bash
cp dist/cez-hdo-card.js ../../custom_components/cez_hdo/frontend/
```

Nebo použijte deploy skript z kořenového adresáře:

```bash
cd ../../dev
./deploy.sh
```

## Struktura

```text
frontend/
├── src/
│   ├── index.ts           # Entry point
│   ├── cez-hdo-card.ts    # Hlavní komponenta karty
│   └── cez-hdo-card-editor.ts  # Vizuální editor konfigurace
├── dist/                  # Výstupní složka (generovaná)
├── package.json
├── tsconfig.json
└── rollup.config.mjs
```

## Poznámky k vývoji

- Karta používá [Lit](https://lit.dev/) framework (verze 3.x)
- TypeScript dekorátory vyžadují `experimentalDecorators: true`
- V produkčním buildu jsou automaticky odstraněny všechny `console.log` volání
- Editor používá nativní HA komponenty jako `ha-entity-picker`, `ha-switch`, atd.

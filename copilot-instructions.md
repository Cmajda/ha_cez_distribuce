# GitHub Copilot - Pracovní instrukce

## Terminálové příkazy
- **VŽDY používej** `isBackground: true` pro všechny `run_in_terminal` příkazy
- **NIKDY nekombinuj** background/foreground příkazy v jednom workflow
- Pro kontrolu výsledků také používej background procesy

## Development workflow pro ČEZ HDO
- Dev soubory jsou v `/dev/` struktuře
- Production soubory v `/custom_components/`
- Build skript: `./dev/deploy-dev.sh`
- Clean skript: `./dev/deploy-dev.sh clean`

## Použití
Na začátku každé konverzace mi pošlete:
"Přečti si copilot-instructions.md a řiď se těmito pravidly"
cd /home/cmajda/Projects/Doma/ha_cez_distribuce

# Vytvoř strukturu
sudo mkdir -p /mnt/ha-config/custom_components/cez_hdo
sudo mkdir -p /mnt/ha-config/custom_components/cez_hdo/frontend/dist

# Kopíruj pouze potřebné Python soubory
sudo cp custom_components/cez_hdo/*.py /mnt/ha-config/custom_components/cez_hdo/
sudo cp custom_components/cez_hdo/manifest.json /mnt/ha-config/custom_components/cez_hdo/

# Kopíruj pouze built frontend (bez node_modules)
sudo cp custom_components/cez_hdo/frontend/dist/* /mnt/ha-config/custom_components/cez_hdo/frontend/dist/
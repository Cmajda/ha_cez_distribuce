export interface TranslationStrings {
  lowTariff: string;
  highTariff: string;
  nt: string;
  vt: string;
  active: string;
  inactive: string;
  currency: string;
  currencyShort: string;
  ntStart: string;
  vtStart: string;
  ntEnd: string;
  vtEnd: string;
  ntRemaining: string;
  vtRemaining: string;
  currentPrice: string;
  hdoSchedule: string;
  scheduleNotAvailable: string;
  editorTitle: string;
  showTitle: string;
  showTariffStatus: string;
  showTariffPrices: string;
  showTimes: string;
  showDuration: string;
  showCurrentPrice: string;
  showHdoSchedule: string;
  showSchedulePrices: string;
  compactMode: string;
  ntActiveBinarySensor: string;
  vtActiveBinarySensor: string;
  ntStartSensor: string;
  ntEndSensor: string;
  ntRemainingSensor: string;
  vtStartSensor: string;
  vtEndSensor: string;
  vtRemainingSensor: string;
  hdoScheduleSensor: string;
  editorHint: string;
  manualRefresh: string;
  loadingCaptcha: string;
  captchaCode: string;
  refreshNow: string;
  newCaptcha: string;
  cancel: string;
  refreshSuccess: string;
  manualRefreshUnavailable: string;
}

const translations: Record<string, TranslationStrings> = {
  cs: {
    lowTariff: "Nízký tarif",
    highTariff: "Vysoký tarif",
    nt: "NT",
    vt: "VT",
    active: "Aktivní",
    inactive: "Neaktivní",
    currency: "Kč/kWh",
    currencyShort: "Kč",
    ntStart: "Začátek NT",
    vtStart: "Začátek VT",
    ntEnd: "Konec NT",
    vtEnd: "Konec VT",
    ntRemaining: "Zbývá NT",
    vtRemaining: "Zbývá VT",
    currentPrice: "Aktuální cena",
    hdoSchedule: "HDO rozvrh",
    scheduleNotAvailable: "Rozvrh není k dispozici",
    editorTitle: "Titulek",
    showTitle: "Zobrazit titulek",
    showTariffStatus: "Zobrazit stavy tarifů",
    showTariffPrices: "Zobrazit ceny u tarifů",
    showTimes: "Zobrazit časy (začátek/konec)",
    showDuration: "Zobrazit zbývající čas",
    showCurrentPrice: "Zobrazit aktuální cenu",
    showHdoSchedule: "Zobrazit HDO rozvrh",
    showSchedulePrices: "Zobrazit ceny v legendě rozvrhu",
    compactMode: "Kompaktní režim",
    ntActiveBinarySensor: "NT aktivní (binary_sensor)",
    vtActiveBinarySensor: "VT aktivní (binary_sensor)",
    ntStartSensor: "NT začátek (sensor)",
    ntEndSensor: "NT konec (sensor)",
    ntRemainingSensor: "NT zbývající čas (sensor)",
    vtStartSensor: "VT začátek (sensor)",
    vtEndSensor: "VT konec (sensor)",
    vtRemainingSensor: "VT zbývající čas (sensor)",
    hdoScheduleSensor: "HDO rozvrh (sensor)",
    editorHint: "Nakonfigurujte entity v nastavení karty",
    manualRefresh: "Manuálně obnovit",
    loadingCaptcha: "Načítám CAPTCHA…",
    captchaCode: "Opište kód z obrázku",
    refreshNow: "Obnovit data",
    newCaptcha: "Nový obrázek",
    cancel: "Zavřít",
    refreshSuccess: "Data byla úspěšně obnovena.",
    manualRefreshUnavailable:
      "Vyberte senzor rozvrhu pro tuto instanci ČEZ HDO.",
  },
  en: {
    lowTariff: "Low tariff",
    highTariff: "High tariff",
    nt: "LT",
    vt: "HT",
    active: "Active",
    inactive: "Inactive",
    currency: "CZK/kWh",
    currencyShort: "CZK",
    ntStart: "Low tariff starts",
    vtStart: "High tariff starts",
    ntEnd: "Low tariff ends",
    vtEnd: "High tariff ends",
    ntRemaining: "Low tariff remaining",
    vtRemaining: "High tariff remaining",
    currentPrice: "Current price",
    hdoSchedule: "HDO schedule",
    scheduleNotAvailable: "Schedule is not available",
    editorTitle: "Title",
    showTitle: "Show title",
    showTariffStatus: "Show tariff status",
    showTariffPrices: "Show tariff prices",
    showTimes: "Show times (start/end)",
    showDuration: "Show remaining time",
    showCurrentPrice: "Show current price",
    showHdoSchedule: "Show HDO schedule",
    showSchedulePrices: "Show prices in schedule legend",
    compactMode: "Compact mode",
    ntActiveBinarySensor: "Low tariff active (binary_sensor)",
    vtActiveBinarySensor: "High tariff active (binary_sensor)",
    ntStartSensor: "Low tariff start (sensor)",
    ntEndSensor: "Low tariff end (sensor)",
    ntRemainingSensor: "Low tariff remaining (sensor)",
    vtStartSensor: "High tariff start (sensor)",
    vtEndSensor: "High tariff end (sensor)",
    vtRemainingSensor: "High tariff remaining (sensor)",
    hdoScheduleSensor: "HDO schedule (sensor)",
    editorHint: "Configure entities in card settings",
    manualRefresh: "Refresh manually",
    loadingCaptcha: "Loading CAPTCHA…",
    captchaCode: "Enter the code from the image",
    refreshNow: "Refresh data",
    newCaptcha: "New image",
    cancel: "Close",
    refreshSuccess: "Data refreshed successfully.",
    manualRefreshUnavailable:
      "Select the schedule sensor for this ČEZ HDO instance.",
  },
  sk: {
    lowTariff: "Nízka tarifa",
    highTariff: "Vysoká tarifa",
    nt: "NT",
    vt: "VT",
    active: "Aktívna",
    inactive: "Neaktívna",
    currency: "Kč/kWh",
    currencyShort: "Kč",
    ntStart: "Začiatok NT",
    vtStart: "Začiatok VT",
    ntEnd: "Koniec NT",
    vtEnd: "Koniec VT",
    ntRemaining: "Zostáva NT",
    vtRemaining: "Zostáva VT",
    currentPrice: "Aktuálna cena",
    hdoSchedule: "HDO rozvrh",
    scheduleNotAvailable: "Rozvrh nie je k dispozícii",
    editorTitle: "Nadpis",
    showTitle: "Zobraziť nadpis",
    showTariffStatus: "Zobraziť stavy taríf",
    showTariffPrices: "Zobraziť ceny taríf",
    showTimes: "Zobraziť časy (začiatok/koniec)",
    showDuration: "Zobraziť zostávajúci čas",
    showCurrentPrice: "Zobraziť aktuálnu cenu",
    showHdoSchedule: "Zobraziť HDO rozvrh",
    showSchedulePrices: "Zobraziť ceny v legende rozvrhu",
    compactMode: "Kompaktný režim",
    ntActiveBinarySensor: "NT aktívna (binary_sensor)",
    vtActiveBinarySensor: "VT aktívna (binary_sensor)",
    ntStartSensor: "Začiatok NT (sensor)",
    ntEndSensor: "Koniec NT (sensor)",
    ntRemainingSensor: "Zostávajúci čas NT (sensor)",
    vtStartSensor: "Začiatok VT (sensor)",
    vtEndSensor: "Koniec VT (sensor)",
    vtRemainingSensor: "Zostávajúci čas VT (sensor)",
    hdoScheduleSensor: "HDO rozvrh (sensor)",
    editorHint: "Nakonfigurujte entity v nastavení karty",
    manualRefresh: "Manuálne obnoviť",
    loadingCaptcha: "Načítavam CAPTCHA…",
    captchaCode: "Prepíšte kód z obrázka",
    refreshNow: "Obnoviť údaje",
    newCaptcha: "Nový obrázok",
    cancel: "Zavrieť",
    refreshSuccess: "Údaje boli úspešne obnovené.",
    manualRefreshUnavailable:
      "Vyberte senzor rozvrhu pre túto inštanciu ČEZ HDO.",
  },
};

export function getLanguageFromHass(hass: {
  language?: string;
  locale?: { language?: string };
}): string {
  return (hass.locale?.language || hass.language || "en")
    .toLowerCase()
    .split(/[-_]/)[0];
}

export function getTranslations(language: string): TranslationStrings {
  return translations[language] || translations.en;
}

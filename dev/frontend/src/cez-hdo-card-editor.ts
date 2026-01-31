/**
 * ČEZ HDO Card Editor - Visual Configuration Editor
 *
 * Provides a visual configuration interface for the ČEZ HDO Card in Home Assistant.
 * Uses ha-selector for entity selection (HA native component).
 */

import { getTranslations, getLanguageFromHass, TranslationStrings } from './localization';

// Entity prefixes for dynamic discovery (new format: cez_hdo_{type}_{ean4}_{signal})
const ENTITY_PREFIXES: Record<string, { domain: string; prefix: string }> = {
  low_tariff: { domain: 'binary_sensor', prefix: 'cez_hdo_lowtariffactive_' },
  high_tariff: { domain: 'binary_sensor', prefix: 'cez_hdo_hightariffactive_' },
  low_start: { domain: 'sensor', prefix: 'cez_hdo_lowtariffstart_' },
  low_end: { domain: 'sensor', prefix: 'cez_hdo_lowtariffend_' },
  low_duration: { domain: 'sensor', prefix: 'cez_hdo_lowtariffduration_' },
  high_start: { domain: 'sensor', prefix: 'cez_hdo_hightariffstart_' },
  high_end: { domain: 'sensor', prefix: 'cez_hdo_hightariffend_' },
  high_duration: { domain: 'sensor', prefix: 'cez_hdo_hightariffduration_' },
  schedule: { domain: 'sensor', prefix: 'cez_hdo_schedule_' },
};

// Find all entities matching prefix (for multiple integrations)
function findAllEntitiesByPrefix(hass: HomeAssistant | undefined, key: string): string[] {
  if (!hass?.states) return [];
  const config = ENTITY_PREFIXES[key];
  if (!config) return [];

  const fullPrefix = `${config.domain}.${config.prefix}`;
  return Object.keys(hass.states).filter(id => id.startsWith(fullPrefix));
}

// Resolve entity - only auto-fill if exactly one device exists
function resolveDefaultForKey(hass: HomeAssistant | undefined, key: string): string | null {
  const allMatches = findAllEntitiesByPrefix(hass, key);
  // Only auto-fill if exactly one entity found (single device)
  if (allMatches.length === 1) {
    return allMatches[0];
  }
  // Multiple devices or none - don't auto-fill
  return null;
}

interface HomeAssistant {
  states: Record<string, { attributes?: { friendly_name?: string } }>;
  callService: (domain: string, service: string, data: Record<string, unknown>) => Promise<void>;
  language?: string;
  locale?: {
    language: string;
  };
}

interface CardConfig {
  title?: string;
  show_title?: boolean;
  show_tariff_status?: boolean;
  show_tariff_prices?: boolean;
  show_times?: boolean;
  show_duration?: boolean;
  show_price?: boolean;
  show_schedule?: boolean;
  show_schedule_prices?: boolean;
  compact_mode?: boolean;
  entities?: Record<string, string>;
}

export class CezHdoCardEditor extends HTMLElement {
  private _hass?: HomeAssistant;
  private _config: CardConfig = {};

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  set hass(hass: HomeAssistant) {
    this._hass = hass;
    // Update ha-selector components with new hass
    if (this.shadowRoot) {
      const selectors = this.shadowRoot.querySelectorAll('ha-selector');
      selectors.forEach((selector) => {
        (selector as any).hass = hass;
      });
    }
  }

  setConfig(config: CardConfig): void {
    this._config = config || {};
    this._render();
  }

  private _emitConfigChanged(): void {
    this.dispatchEvent(
      new CustomEvent('config-changed', {
        detail: { config: this._config },
        bubbles: true,
        composed: true,
      })
    );
  }

  private _setOption(key: string, value: unknown, skipRender = false): void {
    this._config = { ...this._config, [key]: value };
    this._emitConfigChanged();
    if (!skipRender) {
      this._render();
    }
  }

  private _setEntity(key: string, value: string): void {
    const entities = { ...(this._config.entities || {}) };
    if (!value) {
      delete entities[key];
    } else {
      entities[key] = value;
    }
    this._config = { ...this._config, entities };
    this._emitConfigChanged();
    // DO NOT call _render() here - it would cause re-render and lose focus
  }

  private _entityPicker(label: string, key: string, domains: string[]): HTMLElement {
    // Get configured value or dynamically resolve
    let current = (this._config.entities && this._config.entities[key]) || '';
    const resolved = resolveDefaultForKey(this._hass, key);
    const allMatches = findAllEntitiesByPrefix(this._hass, key);

    // If not explicitly configured, use dynamically found entity
    const displayValue = current || resolved || '';

    const wrap = document.createElement('div');
    wrap.className = 'entity-row';

    // Use ha-selector for entity picking (HA native component)
    const selector = document.createElement('ha-selector') as any;
    selector.hass = this._hass;
    selector.label = label;
    selector.selector = { entity: domains && domains.length ? { domain: domains } : {} };
    selector.value = displayValue;
    selector.addEventListener('value-changed', (ev: CustomEvent) => {
      this._setEntity(key, ev.detail.value);
    });
    wrap.appendChild(selector);

    // Show hint about auto-detected entity or need for selection
    if (!current && resolved) {
      // Single device - auto-filled
      const note = document.createElement('div');
      note.className = 'hint';
      note.textContent = 'Auto-detekováno';
      wrap.appendChild(note);
    } else if (!current && !resolved && allMatches.length > 1) {
      // Multiple devices - user must select
      const note = document.createElement('div');
      note.className = 'hint hint-warning';
      note.textContent = `Nalezeno ${allMatches.length} zařízení - vyberte entitu`;
      wrap.appendChild(note);
    } else if (!current && !resolved && allMatches.length === 0) {
      // No devices found
      const note = document.createElement('div');
      note.className = 'hint';
      note.textContent = 'Žádná ČEZ HDO entita nenalezena';
      wrap.appendChild(note);
    }

    return wrap;
  }

  private _render(): void {
    if (!this.shadowRoot || !this._hass) {
      if (this.shadowRoot) this.shadowRoot.innerHTML = '';
      return;
    }

    // Get translations based on HA language
    const lang = getLanguageFromHass(this._hass);
    const t = getTranslations(lang);

    const title = this._config.title ?? '';
    const showTimes = this._config.show_times !== false;
    const showDuration = this._config.show_duration !== false;
    const compactMode = this._config.compact_mode === true;

    this.shadowRoot.innerHTML = `
      <style>
        .wrap {
          display: flex;
          flex-direction: column;
          gap: 12px;
          padding: 4px 0;
        }
        .entity-row {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        .entity-row ha-selector {
          display: block;
        }
        .hint {
          font-size: 12px;
          opacity: 0.8;
        }
        .hint-warning {
          color: var(--warning-color, #ff9800);
          font-weight: 500;
        }
      </style>
      <div class="wrap"></div>
    `;

    const wrap = this.shadowRoot.querySelector('.wrap');
    if (!wrap) return;

    // Title field
    const titleField = document.createElement('ha-textfield') as any;
    titleField.label = t.editorTitle;
    titleField.value = title;
    titleField.addEventListener('input', (ev: Event) => {
      this._config = { ...this._config, title: (ev.target as HTMLInputElement).value };
    });
    titleField.addEventListener('change', (ev: Event) => {
      this._config = { ...this._config, title: (ev.target as HTMLInputElement).value };
      this._emitConfigChanged();
    });
    wrap.appendChild(titleField);

    // Toggle helper - skipRender for smooth UX
    const mkToggle = (label: string, key: string, checked: boolean): HTMLElement => {
      const form = document.createElement('ha-formfield') as any;
      form.label = label;
      const sw = document.createElement('ha-switch') as any;
      sw.checked = checked;
      sw.addEventListener('change', () => this._setOption(key, sw.checked, true));
      form.appendChild(sw);
      return form;
    };

    wrap.appendChild(mkToggle(t.showTitle, 'show_title', this._config.show_title !== false));
    wrap.appendChild(mkToggle(t.showTariffStatus, 'show_tariff_status', this._config.show_tariff_status !== false));
    wrap.appendChild(mkToggle(t.showTariffPrices, 'show_tariff_prices', this._config.show_tariff_prices === true));
    wrap.appendChild(mkToggle(t.showTimes, 'show_times', showTimes));
    wrap.appendChild(mkToggle(t.showDuration, 'show_duration', showDuration));
    wrap.appendChild(mkToggle(t.showCurrentPrice, 'show_price', this._config.show_price !== false));
    wrap.appendChild(mkToggle(t.showHdoSchedule, 'show_schedule', this._config.show_schedule === true));
    wrap.appendChild(mkToggle(t.showSchedulePrices, 'show_schedule_prices', this._config.show_schedule_prices === true));
    wrap.appendChild(mkToggle(t.compactMode, 'compact_mode', compactMode));

    // Entity pickers using ha-selector
    wrap.appendChild(this._entityPicker(t.ntActiveBinarySensor, 'low_tariff', ['binary_sensor']));
    wrap.appendChild(this._entityPicker(t.vtActiveBinarySensor, 'high_tariff', ['binary_sensor']));
    wrap.appendChild(this._entityPicker(t.ntStartSensor, 'low_start', ['sensor']));
    wrap.appendChild(this._entityPicker(t.ntEndSensor, 'low_end', ['sensor']));
    wrap.appendChild(this._entityPicker(t.ntRemainingSensor, 'low_duration', ['sensor']));
    wrap.appendChild(this._entityPicker(t.vtStartSensor, 'high_start', ['sensor']));
    wrap.appendChild(this._entityPicker(t.vtEndSensor, 'high_end', ['sensor']));
    wrap.appendChild(this._entityPicker(t.vtRemainingSensor, 'high_duration', ['sensor']));
    wrap.appendChild(this._entityPicker(t.hdoScheduleSensor, 'schedule', ['sensor']));

    const hint = document.createElement('div');
    hint.className = 'hint';
    hint.textContent = t.editorHint;
    wrap.appendChild(hint);
  }
}

// Register the editor
if (!customElements.get('cez-hdo-card-editor')) {
  customElements.define('cez-hdo-card-editor', CezHdoCardEditor);
}

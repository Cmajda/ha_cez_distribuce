/**
 * ČEZ HDO Card Editor - Visual Configuration Editor
 * 
 * Provides a visual configuration interface for the ČEZ HDO Card in Home Assistant.
 * Uses ha-selector for entity selection (HA native component).
 */

// Default entity candidates
const DEFAULT_ENTITY_CANDIDATES: Record<string, string[]> = {
  low_tariff: ['binary_sensor.cez_hdo_nizky_tarif_aktivni'],
  high_tariff: ['binary_sensor.cez_hdo_vysoky_tarif_aktivni'],
  low_start: ['sensor.cez_hdo_nizky_tarif_zacatek'],
  low_end: ['sensor.cez_hdo_nizky_tarif_konec'],
  low_duration: ['sensor.cez_hdo_nizky_tarif_zbyva'],
  high_start: ['sensor.cez_hdo_vysoky_tarif_zacatek'],
  high_end: ['sensor.cez_hdo_vysoky_tarif_konec'],
  high_duration: ['sensor.cez_hdo_vysoky_tarif_zbyva'],
  schedule: ['sensor.cez_hdo_rozvrh'],
};

const DEFAULT_ENTITIES: Record<string, string> = {
  low_tariff: DEFAULT_ENTITY_CANDIDATES.low_tariff[0],
  high_tariff: DEFAULT_ENTITY_CANDIDATES.high_tariff[0],
  low_start: DEFAULT_ENTITY_CANDIDATES.low_start[0],
  low_end: DEFAULT_ENTITY_CANDIDATES.low_end[0],
  low_duration: DEFAULT_ENTITY_CANDIDATES.low_duration[0],
  high_start: DEFAULT_ENTITY_CANDIDATES.high_start[0],
  high_end: DEFAULT_ENTITY_CANDIDATES.high_end[0],
  high_duration: DEFAULT_ENTITY_CANDIDATES.high_duration[0],
  schedule: DEFAULT_ENTITY_CANDIDATES.schedule[0],
};

interface HomeAssistant {
  states: Record<string, { attributes?: { friendly_name?: string } }>;
  callService: (domain: string, service: string, data: Record<string, unknown>) => Promise<void>;
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
  low_tariff_price?: number;
  high_tariff_price?: number;
  entities?: Record<string, string>;
}

function resolveDefaultForKey(hass: HomeAssistant | undefined, key: string): string {
  if (!hass) return DEFAULT_ENTITIES[key];
  const candidates = DEFAULT_ENTITY_CANDIDATES[key] || [DEFAULT_ENTITIES[key]];
  for (const cand of candidates) {
    if (hass.states && hass.states[cand]) return cand;
  }
  return DEFAULT_ENTITIES[key];
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

  private _setPriceOption(key: string, value: number): void {
    // Only store value locally, don't emit (emit on blur/change)
    this._config = { ...this._config, [key]: value };
  }

  private _emitPriceChange(key: string, value: number): void {
    this._config = { ...this._config, [key]: value };
    this._emitConfigChanged();

    // Call set_prices service to persist prices to backend
    if (this._hass) {
      const lowPrice = key === 'low_tariff_price' ? value : (this._config.low_tariff_price || 0);
      const highPrice = key === 'high_tariff_price' ? value : (this._config.high_tariff_price || 0);
      
      this._hass.callService('cez_hdo', 'set_prices', {
        low_tariff_price: lowPrice,
        high_tariff_price: highPrice,
      });
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
    const current = (this._config.entities && this._config.entities[key]) || '';
    const wrap = document.createElement('div');
    wrap.className = 'entity-row';

    // Use ha-selector for entity picking (HA native component)
    const selector = document.createElement('ha-selector') as any;
    selector.hass = this._hass;
    selector.label = label;
    selector.selector = { entity: domains && domains.length ? { domain: domains } : {} };
    selector.value = current;
    selector.addEventListener('value-changed', (ev: CustomEvent) => {
      this._setEntity(key, ev.detail.value);
    });
    wrap.appendChild(selector);

    // Show default entity hint if field is empty
    if (!current) {
      const resolved = resolveDefaultForKey(this._hass, key);
      const note = document.createElement('div');
      note.className = 'hint';
      if (resolved) {
        const exists = !!(this._hass?.states && this._hass.states[resolved]);
        note.textContent = exists ? `Použito: ${resolved}` : `Výchozí: ${resolved} (nenalezeno)`;
      }
      wrap.appendChild(note);
    }

    return wrap;
  }

  private _render(): void {
    if (!this.shadowRoot || !this._hass) {
      if (this.shadowRoot) this.shadowRoot.innerHTML = '';
      return;
    }

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
      </style>
      <div class="wrap"></div>
    `;

    const wrap = this.shadowRoot.querySelector('.wrap');
    if (!wrap) return;

    // Title field
    const titleField = document.createElement('ha-textfield') as any;
    titleField.label = 'Titulek';
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

    wrap.appendChild(mkToggle('Zobrazit titulek', 'show_title', this._config.show_title !== false));
    wrap.appendChild(mkToggle('Zobrazit stavy tarifů', 'show_tariff_status', this._config.show_tariff_status !== false));
    wrap.appendChild(mkToggle('Zobrazit ceny u tarifů', 'show_tariff_prices', this._config.show_tariff_prices === true));
    wrap.appendChild(mkToggle('Zobrazit časy (začátek/konec)', 'show_times', showTimes));
    wrap.appendChild(mkToggle('Zobrazit zbývající čas', 'show_duration', showDuration));
    wrap.appendChild(mkToggle('Zobrazit aktuální cenu', 'show_price', this._config.show_price !== false));
    wrap.appendChild(mkToggle('Zobrazit HDO rozvrh', 'show_schedule', this._config.show_schedule === true));
    wrap.appendChild(mkToggle('Zobrazit ceny v legendě rozvrhu', 'show_schedule_prices', this._config.show_schedule_prices === true));
    wrap.appendChild(mkToggle('Kompaktní režim', 'compact_mode', compactMode));

    // Price fields - input only stores locally, change/blur emits
    const lowPriceField = document.createElement('ha-textfield') as any;
    lowPriceField.label = 'Cena NT (Kč/kWh)';
    lowPriceField.type = 'number';
    lowPriceField.step = '0.01';
    lowPriceField.value = this._config.low_tariff_price || '';
    lowPriceField.addEventListener('input', (ev: Event) => {
      this._setPriceOption('low_tariff_price', parseFloat((ev.target as HTMLInputElement).value) || 0);
    });
    lowPriceField.addEventListener('change', (ev: Event) => {
      this._emitPriceChange('low_tariff_price', parseFloat((ev.target as HTMLInputElement).value) || 0);
    });
    wrap.appendChild(lowPriceField);

    const highPriceField = document.createElement('ha-textfield') as any;
    highPriceField.label = 'Cena VT (Kč/kWh)';
    highPriceField.type = 'number';
    highPriceField.step = '0.01';
    highPriceField.value = this._config.high_tariff_price || '';
    highPriceField.addEventListener('input', (ev: Event) => {
      this._setPriceOption('high_tariff_price', parseFloat((ev.target as HTMLInputElement).value) || 0);
    });
    highPriceField.addEventListener('change', (ev: Event) => {
      this._emitPriceChange('high_tariff_price', parseFloat((ev.target as HTMLInputElement).value) || 0);
    });
    wrap.appendChild(highPriceField);

    // Entity pickers using ha-selector
    wrap.appendChild(this._entityPicker('NT aktivní (binary_sensor)', 'low_tariff', ['binary_sensor']));
    wrap.appendChild(this._entityPicker('VT aktivní (binary_sensor)', 'high_tariff', ['binary_sensor']));
    wrap.appendChild(this._entityPicker('NT začátek (sensor)', 'low_start', ['sensor']));
    wrap.appendChild(this._entityPicker('NT konec (sensor)', 'low_end', ['sensor']));
    wrap.appendChild(this._entityPicker('NT zbývá (sensor)', 'low_duration', ['sensor']));
    wrap.appendChild(this._entityPicker('VT začátek (sensor)', 'high_start', ['sensor']));
    wrap.appendChild(this._entityPicker('VT konec (sensor)', 'high_end', ['sensor']));
    wrap.appendChild(this._entityPicker('VT zbývá (sensor)', 'high_duration', ['sensor']));
    wrap.appendChild(this._entityPicker('HDO rozvrh (sensor)', 'schedule', ['sensor']));

    const hint = document.createElement('div');
    hint.className = 'hint';
    hint.textContent = 'Entity jsou předvyplněny automaticky. Změňte pouze pokud máte více instancí integrace.';
    wrap.appendChild(hint);
  }
}

// Register the editor
if (!customElements.get('cez-hdo-card-editor')) {
  customElements.define('cez-hdo-card-editor', CezHdoCardEditor);
}

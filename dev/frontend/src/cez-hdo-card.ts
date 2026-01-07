import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant, LovelaceCard, LovelaceCardConfig } from './types';

export interface CezHdoCardConfig extends LovelaceCardConfig {
  type: 'custom:cez-hdo-card';
  title?: string;
  show_times?: boolean;
  show_duration?: boolean;
  compact_mode?: boolean;
  entities?: {
    low_tariff?: string;
    high_tariff?: string;
    low_start?: string;
    low_end?: string;
    low_duration?: string;
    high_start?: string;
    high_end?: string;
    high_duration?: string;
  };
}

interface CezHdoData {
  lowTariffActive: boolean;
  highTariffActive: boolean;
  lowTariffStart: string;
  lowTariffEnd: string;
  lowTariffDuration: string;
  highTariffStart: string;
  highTariffEnd: string;
  highTariffDuration: string;
  ntAktualniZacatek?: string;
  ntAktualniKonec?: string;
  ntDalsiZacatek?: string;
  ntDalsiKonec?: string;
  vtAktualniZacatek?: string;
  vtAktualniKonec?: string;
  vtDalsiZacatek?: string;
  vtDalsiKonec?: string;
}

export class CezHdoCard extends LitElement implements LovelaceCard {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private config!: CezHdoCardConfig;
  @state() private hdoData: CezHdoData | null = null;

  public static getConfigElement() {
    return document.createElement('cez-hdo-card-editor');
  }

  public static getStubConfig(): CezHdoCardConfig {
    return {
      type: 'custom:cez-hdo-card',
      title: 'ČEZ HDO Status',
      show_times: true,
      show_duration: true,
      compact_mode: false,
      entities: {
        low_tariff: 'binary_sensor.cez_hdo_lowtariffactive',
        high_tariff: 'binary_sensor.cez_hdo_hightariffactive',
        low_start: 'sensor.cez_hdo_lowtariffstart',
        low_end: 'sensor.cez_hdo_lowtariffend',
        low_duration: 'sensor.cez_hdo_lowtariffduration',
        high_start: 'sensor.cez_hdo_hightariffstart',
        high_end: 'sensor.cez_hdo_hightariffend',
        high_duration: 'sensor.cez_hdo_hightariffduration'
      }
    };
  }

  public setConfig(config: CezHdoCardConfig): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }

    // Debug: Log the received config
    console.log('ČEZ HDO Card config:', config);

    // Validate entities configuration with more lenient check
    if (!config.entities || typeof config.entities !== 'object') {
      throw new Error(`ČEZ HDO Card vyžaduje konfiguraci entities. Příklad:

entities:
  low_tariff: binary_sensor.cez_hdo_lowtariffactive
  high_tariff: binary_sensor.cez_hdo_hightariffactive
  low_start: sensor.cez_hdo_lowtariffstart
  low_end: sensor.cez_hdo_lowtariffend
  low_duration: sensor.cez_hdo_lowtariffduration
  high_start: sensor.cez_hdo_hightariffstart
  high_end: sensor.cez_hdo_hightariffend
  high_duration: sensor.cez_hdo_hightariffduration`);
    }

    this.config = {
      show_header: true,
      show_current_state: true,
      show_schedule: true,
      theme: 'auto',
      ...config,
    };
  }

  public getCardSize(): number {
    return 3;
  }

  protected shouldUpdate(changedProps: PropertyValues): boolean {
    if (changedProps.has('config')) {
      return true;
    }

    if (changedProps.has('hass')) {
      const oldHass = changedProps.get('hass') as HomeAssistant | undefined;
      if (!oldHass) return true;

      // Check if any CEZ HDO entities have changed
      const cezEntities = Object.keys(this.hass.states).filter(id =>
        id.startsWith('binary_sensor.cez_hdo_') ||
        id.startsWith('sensor.cez_hdo_')
      );

      return cezEntities.some(entityId =>
        oldHass.states[entityId] !== this.hass.states[entityId]
      );
    }

    return false;
  }

  protected updated(changedProps: PropertyValues): void {
    super.updated(changedProps);
    if (changedProps.has('hass') || changedProps.has('config')) {
      this.updateHdoData();
    }
  }

  private updateHdoData(): void {
    if (!this.hass) return;

    const getEntityValue = (entityId: string): string => {
      const entity = this.hass.states[entityId];
      return entity ? entity.state : 'unavailable';
    };

    // Získat entity z hlavní entity (např. cez_hdo), kde jsou nové atributy
    const cezHdoEntity = Object.values(this.hass.states).find(
      (e: any) => e.entity_id && e.entity_id.startsWith('sensor.cez_hdo') && e.attributes && (
        'nt_aktualni_zacatek' in e.attributes || 'nt_dalsi_zacatek' in e.attributes
      )
    ) as any;

    this.hdoData = {
      lowTariffActive: getEntityValue('binary_sensor.cez_hdo_lowtariffactive') === 'on',
      highTariffActive: getEntityValue('binary_sensor.cez_hdo_hightariffactive') === 'on',
      lowTariffStart: getEntityValue('sensor.cez_hdo_lowtariffstart'),
      lowTariffEnd: getEntityValue('sensor.cez_hdo_lowtariffend'),
      lowTariffDuration: getEntityValue('sensor.cez_hdo_lowtariffduration'),
      highTariffStart: getEntityValue('sensor.cez_hdo_hightariffstart'),
      highTariffEnd: getEntityValue('sensor.cez_hdo_hightariffend'),
      highTariffDuration: getEntityValue('sensor.cez_hdo_hightariffduration'),
      ntAktualniZacatek: cezHdoEntity?.attributes?.nt_aktualni_zacatek ?? '',
      ntAktualniKonec: cezHdoEntity?.attributes?.nt_aktualni_konec ?? '',
      ntDalsiZacatek: cezHdoEntity?.attributes?.nt_dalsi_zacatek ?? '',
      ntDalsiKonec: cezHdoEntity?.attributes?.nt_dalsi_konec ?? '',
      vtAktualniZacatek: cezHdoEntity?.attributes?.vt_aktualni_zacatek ?? '',
      vtAktualniKonec: cezHdoEntity?.attributes?.vt_aktualni_konec ?? '',
      vtDalsiZacatek: cezHdoEntity?.attributes?.vt_dalsi_zacatek ?? '',
      vtDalsiKonec: cezHdoEntity?.attributes?.vt_dalsi_konec ?? '',
    };
  }

  private renderHeader() {
    if (!this.config.show_header) return '';

    return html`
      <div class="card-header">
        <h3>${this.config.title || 'ČEZ HDO'}</h3>
      </div>
    `;
  }

  private renderCurrentState() {
    if (!this.config.show_current_state || !this.hdoData) return '';

    const isLowTariff = this.hdoData.lowTariffActive;
    const isHighTariff = this.hdoData.highTariffActive;

    return html`
      <div class="current-state">
        <div class="state-indicator ${isLowTariff ? 'low-active' : isHighTariff ? 'high-active' : 'inactive'}">
          <ha-icon
            icon="${isLowTariff ? 'mdi:flash' : isHighTariff ? 'mdi:flash-outline' : 'mdi:flash-off'}"
          ></ha-icon>
          <span class="state-text">
            ${isLowTariff ? 'Nízký tarif' : isHighTariff ? 'Vysoký tarif' : 'Neaktivní'}
          </span>
        </div>

        ${isLowTariff ? html`
          <div class="duration-info">
            <span>Zbývá: ${this.formatDuration(this.hdoData.lowTariffDuration)}</span>
          </div>
        ` : ''}

        ${isHighTariff ? html`
          <div class="duration-info">
            <span>Zbývá: ${this.formatDuration(this.hdoData.highTariffDuration)}</span>
          </div>
        ` : ''}
      </div>
    `;
  }

  private renderSchedule() {
    if (!this.config.show_schedule || !this.hdoData) return '';

    return html`
      <div class="schedule">
        <h4>Aktuální a následující intervaly</h4>

        <div class="schedule-item low-tariff">
          <ha-icon icon="mdi:flash"></ha-icon>
          <span class="tariff-label">Aktuální NT:</span>
          <span class="time-range">
            ${this.formatTime(this.hdoData.ntAktualniZacatek)} - ${this.formatTime(this.hdoData.ntAktualniKonec)}
          </span>
        </div>
        <div class="schedule-item low-tariff">
          <ha-icon icon="mdi:flash"></ha-icon>
          <span class="tariff-label">Následující NT:</span>
          <span class="time-range">
            ${this.formatTime(this.hdoData.ntDalsiZacatek)} - ${this.formatTime(this.hdoData.ntDalsiKonec)}
          </span>
        </div>
        <div class="schedule-item high-tariff">
          <ha-icon icon="mdi:flash-outline"></ha-icon>
          <span class="tariff-label">Aktuální VT:</span>
          <span class="time-range">
            ${this.formatTime(this.hdoData.vtAktualniZacatek)} - ${this.formatTime(this.hdoData.vtAktualniKonec)}
          </span>
        </div>
        <div class="schedule-item high-tariff">
          <ha-icon icon="mdi:flash-outline"></ha-icon>
          <span class="tariff-label">Následující VT:</span>
          <span class="time-range">
            ${this.formatTime(this.hdoData.vtDalsiZacatek)} - ${this.formatTime(this.hdoData.vtDalsiKonec)}
          </span>
        </div>
      </div>
    `;
  }

  private formatTime(timeStr: string): string {
    if (!timeStr || timeStr === 'unavailable') return '--:--';
    return timeStr;
  }

  private formatDuration(durationStr: string): string {
    if (!durationStr || durationStr === 'unavailable') return '--:--';

    // Parse timedelta string like "1:23:45" or "0:15:30"
    const parts = durationStr.split(':');
    if (parts.length === 3) {
      const hours = parseInt(parts[0]);
      const minutes = parseInt(parts[1]);

      if (hours > 0) {
        return `${hours}h ${minutes}m`;
      } else {
        return `${minutes}m`;
      }
    }

    return durationStr;
  }

  protected render() {
    if (!this.config || !this.hass) {
      return html``;
    }

    return html`
      <ha-card>
        ${this.renderHeader()}
        <div class="card-content">
          ${this.renderCurrentState()}
          ${this.renderSchedule()}
        </div>
      </ha-card>
    `;
  }

  static get styles() {
    return css`
      :host {
        display: block;
      }

      ha-card {
        padding: 16px;
      }

      .card-header {
        margin-bottom: 16px;
      }

      .card-header h3 {
        margin: 0;
        font-size: 1.2em;
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .current-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 24px;
        padding: 16px;
        border-radius: 8px;
        background: var(--card-background-color);
      }

      .state-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.1em;
        font-weight: 500;
      }

      .state-indicator.low-active {
        color: var(--success-color, #4caf50);
      }

      .state-indicator.high-active {
        color: var(--warning-color, #ff9800);
      }

      .state-indicator.inactive {
        color: var(--disabled-text-color);
      }

      .duration-info {
        margin-top: 8px;
        font-size: 0.9em;
        color: var(--secondary-text-color);
      }

      .schedule {
        margin-top: 16px;
      }

      .schedule h4 {
        margin: 0 0 12px 0;
        font-size: 1em;
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .schedule-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        padding: 8px;
        border-radius: 6px;
        background: var(--secondary-background-color);
      }

      .schedule-item.low-tariff {
        border-left: 3px solid var(--success-color, #4caf50);
      }

      .schedule-item.high-tariff {
        border-left: 3px solid var(--warning-color, #ff9800);
      }

      .tariff-label {
        font-weight: 500;
        min-width: 80px;
      }

      .time-range {
        margin-left: auto;
        font-family: monospace;
        color: var(--secondary-text-color);
      }

      ha-icon {
        --mdc-icon-size: 20px;
      }
    `;
  }
}

// Safe registration - only register if not already defined
if (!customElements.get('cez-hdo-card')) {
  customElements.define('cez-hdo-card', CezHdoCard);
  console.info('✅ ČEZ HDO Card registered successfully');
} else {
  console.info('ℹ️ ČEZ HDO Card already registered, skipping');
}

// Register the card
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: 'cez-hdo-card',
  name: 'ČEZ HDO Card',
  description: 'Zobrazuje informace o HDO tarifech ČEZ Distribuce'
});

console.info(
  `%c  CEZ-HDO-CARD %c  Version 2.0.4  `,
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray',
);

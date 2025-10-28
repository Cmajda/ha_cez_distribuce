import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

interface CezHdoCardConfig {
  type: 'custom:cez-hdo-card';
  title?: string;
  entities: {
    low_tariff?: string;
    high_tariff?: string;
    low_start?: string;
    low_end?: string;
    low_duration?: string;
    high_start?: string;
    high_end?: string;
    high_duration?: string;
  };
  colors?: {
    low_tariff?: string;
    high_tariff?: string;
    background?: string;
    text?: string;
  };
  show_duration?: boolean;
  show_times?: boolean;
  compact_mode?: boolean;
}

@customElement('cez-hdo-card')
export class CezHdoCard extends LitElement {
  @property({ attribute: false }) public hass: any;
  @state() private config!: CezHdoCardConfig;

  static styles = css`
    :host {
      display: block;
    }

    ha-card {
      padding: 16px;
      background: var(--card-background-color, var(--ha-card-background));
      border-radius: var(--ha-card-border-radius, 12px);
      box-shadow: var(--ha-card-box-shadow, 0 2px 4px rgba(0,0,0,0.1));
    }

    .card-header {
      font-size: 24px;
      font-weight: 500;
      margin-bottom: 16px;
      color: var(--primary-text-color);
    }

    .status-container {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
    }

    .status-item {
      flex: 1;
      padding: 12px;
      border-radius: 8px;
      text-align: center;
      transition: all 0.3s ease;
    }

    .status-item.active {
      transform: scale(1.02);
      box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    .status-item.low-tariff {
      background: var(--low-tariff-color, #4CAF50);
      color: white;
    }

    .status-item.high-tariff {
      background: var(--high-tariff-color, #FF5722);
      color: white;
    }

    .status-item.inactive {
      background: var(--disabled-color, #cccccc);
      color: var(--secondary-text-color);
    }

    .status-title {
      font-weight: 600;
      font-size: 14px;
      margin-bottom: 4px;
    }

    .status-value {
      font-size: 12px;
      opacity: 0.9;
    }

    .details-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
    }

    .detail-item {
      padding: 8px 12px;
      background: var(--secondary-background-color, rgba(0,0,0,0.05));
      border-radius: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .detail-label {
      font-size: 12px;
      color: var(--secondary-text-color);
    }

    .detail-value {
      font-size: 14px;
      font-weight: 500;
      color: var(--primary-text-color);
    }

    .compact .status-container {
      margin-bottom: 8px;
    }

    .compact .status-item {
      padding: 8px;
    }

    .compact .details-container {
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
  `;

  setConfig(config: CezHdoCardConfig): void {
    console.log('CezHdoCard setConfig called with:', config);
    
    // If entities are missing, auto-fill with default configuration
    if (!config.entities) {
      console.log('Entities missing, auto-filling with default configuration');
      const defaultConfig = {
        entities: {
          low_tariff: 'binary_sensor.cez_hdo_lowtariffactive',
          high_tariff: 'binary_sensor.cez_hdo_hightariffactive',
          low_start: 'sensor.cez_hdo_lowtariffstart',
          low_end: 'sensor.cez_hdo_lowtariffend',
          low_duration: 'sensor.cez_hdo_lowtariffduration',
          high_start: 'sensor.cez_hdo_hightariffstart',
          high_end: 'sensor.cez_hdo_hightariffend',
          high_duration: 'sensor.cez_hdo_hightariffduration'
        },
        title: 'ČEZ HDO Status',
        show_times: true,
        show_duration: true,
        compact_mode: false
      };
      config = { ...defaultConfig, ...config };
      console.log('Auto-filled config:', config);
    }
    
    console.log('Config validation passed');
    this.config = config;
  }

  private getEntityState(entityId?: string): string {
    if (!entityId || !this.hass) return 'unavailable';
    const entity = this.hass.states[entityId];
    return entity ? entity.state : 'unavailable';
  }

  private isEntityOn(entityId?: string): boolean {
    return this.getEntityState(entityId) === 'on';
  }

  render() {
    if (!this.config || !this.hass) {
      return html`<ha-card>Loading...</ha-card>`;
    }

    const { entities } = this.config;
    const lowTariffActive = this.isEntityOn(entities.low_tariff);
    const highTariffActive = this.isEntityOn(entities.high_tariff);
    
    const lowStart = this.getEntityState(entities.low_start);
    const lowEnd = this.getEntityState(entities.low_end);
    const lowDuration = this.getEntityState(entities.low_duration);
    const highStart = this.getEntityState(entities.high_start);
    const highEnd = this.getEntityState(entities.high_end);
    const highDuration = this.getEntityState(entities.high_duration);

    const title = this.config.title || 'ČEZ HDO';
    const showTimes = this.config.show_times !== false;
    const showDuration = this.config.show_duration !== false;
    const compactMode = this.config.compact_mode === true;

    return html`
      <ha-card class="${compactMode ? 'compact' : ''}">
        ${title ? html`<div class="card-header">${title}</div>` : ''}
        
        <div class="status-container">
          <div class="status-item ${lowTariffActive ? 'active low-tariff' : 'inactive'}">
            <div class="status-title">Nízký tarif</div>
            <div class="status-value">${lowTariffActive ? 'Aktivní' : 'Neaktivní'}</div>
          </div>
          <div class="status-item ${highTariffActive ? 'active high-tariff' : 'inactive'}">
            <div class="status-title">Vysoký tarif</div>
            <div class="status-value">${highTariffActive ? 'Aktivní' : 'Neaktivní'}</div>
          </div>
        </div>

        ${showTimes || showDuration ? html`
          <div class="details-container">
            ${showTimes ? html`
              <div class="detail-item">
                <span class="detail-label">NT začátek</span>
                <span class="detail-value">${lowStart}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">NT konec</span>
                <span class="detail-value">${lowEnd}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT začátek</span>
                <span class="detail-value">${highStart}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT konec</span>
                <span class="detail-value">${highEnd}</span>
              </div>
            ` : ''}
            ${showDuration ? html`
              <div class="detail-item">
                <span class="detail-label">NT zbývá</span>
                <span class="detail-value">${lowDuration}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT zbývá</span>
                <span class="detail-value">${highDuration}</span>
              </div>
            ` : ''}
          </div>
        ` : ''}
      </ha-card>
    `;
  }
}

// Register the card
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: 'cez-hdo-card',
  name: 'ČEZ HDO Card',
  description: 'Custom card for ČEZ HDO integration',
  preview: true,
});

console.info("ČEZ HDO Card v1.1.0 loaded successfully");
/**
 * ČEZ HDO Card - Custom Lovelace Card for Home Assistant
 * 
 * Displays HDO (Hromadné Dálkové Ovládání) tariff information from ČEZ Distribuce.
 * 
 * @version 3.0.0
 * @author ČEZ HDO Integration Contributors
 */

import { LitElement, html, css, CSSResultGroup } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

// Type definitions
interface HassEntity {
  state: string;
  attributes: Record<string, unknown>;
}

interface HomeAssistant {
  states: Record<string, HassEntity>;
  callService: (domain: string, service: string, data: Record<string, unknown>) => Promise<void>;
}

interface EntityConfig {
  low_tariff?: string;
  high_tariff?: string;
  low_start?: string;
  low_end?: string;
  low_duration?: string;
  high_start?: string;
  high_end?: string;
  high_duration?: string;
  schedule?: string;
}

interface CardConfig {
  type: string;
  title?: string;
  entities?: EntityConfig;
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
}

interface ScheduleItem {
  start: string;
  end: string;
  tariff: string;
}

// Default entity mappings
const DEFAULT_ENTITIES: Required<EntityConfig> = {
  low_tariff: 'binary_sensor.cez_hdo_nizky_tarif_aktivni',
  high_tariff: 'binary_sensor.cez_hdo_vysoky_tarif_aktivni',
  low_start: 'sensor.cez_hdo_nizky_tarif_zacatek',
  low_end: 'sensor.cez_hdo_nizky_tarif_konec',
  low_duration: 'sensor.cez_hdo_nizky_tarif_zbyva',
  high_start: 'sensor.cez_hdo_vysoky_tarif_zacatek',
  high_end: 'sensor.cez_hdo_vysoky_tarif_konec',
  high_duration: 'sensor.cez_hdo_vysoky_tarif_zbyva',
  schedule: 'sensor.cez_hdo_rozvrh',
};

@customElement('cez-hdo-card')
export class CezHdoCard extends LitElement {
  @property({ attribute: false }) hass!: HomeAssistant;
  @state() private config!: CardConfig;

  static getConfigElement(): HTMLElement {
    return document.createElement('cez-hdo-card-editor');
  }

  static getStubConfig(): CardConfig {
    return {
      type: 'custom:cez-hdo-card',
      title: 'ČEZ HDO Status',
      show_times: true,
      show_duration: true,
      compact_mode: false,
      entities: { ...DEFAULT_ENTITIES },
    };
  }

  setConfig(config: CardConfig): void {
    if (!config.entities) {
      config = {
        entities: { ...DEFAULT_ENTITIES },
        title: 'ČEZ HDO Status',
        show_times: true,
        show_duration: true,
        compact_mode: false,
        ...config,
      };
    }
    this.config = config;
  }

  private getEntityState(entityId: string | undefined): string {
    if (!entityId || !this.hass) return 'unavailable';
    const entity = this.hass.states[entityId];
    return entity ? entity.state : 'unavailable';
  }

  private isEntityOn(entityId: string | undefined): boolean {
    return this.getEntityState(entityId) === 'on';
  }

  render() {
    if (!this.config || !this.hass) {
      return html`<ha-card>Loading...</ha-card>`;
    }

    const { entities } = this.config;
    if (!entities) {
      return html`<ha-card>No entities configured</ha-card>`;
    }

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
    const showPrice = this.config.show_price !== false;
    const lowTariffPrice = this.config.low_tariff_price || 0;
    const highTariffPrice = this.config.high_tariff_price || 0;
    const currentPrice = lowTariffActive ? lowTariffPrice : highTariffPrice;
    const showTariffPrices = this.config.show_tariff_prices === true;
    const showTitle = this.config.show_title !== false;
    const showTariffStatus = this.config.show_tariff_status !== false;

    return html`
      <ha-card class="${compactMode ? 'compact' : ''}">
        ${title && showTitle ? html`<div class="card-header">${title}</div>` : ''}

        ${showTariffStatus ? html`
          <div class="status-container">
            <div class="status-item ${lowTariffActive ? 'active low-tariff' : 'inactive'}">
              <div class="status-title">Nízký tarif</div>
              <div class="status-value">${lowTariffActive ? 'Aktivní' : 'Neaktivní'}</div>
              ${showTariffPrices && lowTariffPrice > 0 ? html`<div class="status-price">${lowTariffPrice} Kč/kWh</div>` : ''}
            </div>
            <div class="status-item ${highTariffActive ? 'active high-tariff' : 'inactive'}">
              <div class="status-title">Vysoký tarif</div>
              <div class="status-value">${highTariffActive ? 'Aktivní' : 'Neaktivní'}</div>
              ${showTariffPrices && highTariffPrice > 0 ? html`<div class="status-price">${highTariffPrice} Kč/kWh</div>` : ''}
            </div>
          </div>
        ` : ''}

        ${showTimes || showDuration ? html`
          <div class="details-container">
            ${showTimes ? html`
              <div class="detail-item">
                <span class="detail-label">NT začátek</span>
                <span class="detail-value">${lowStart}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT začátek</span>
                <span class="detail-value">${highStart}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">NT konec</span>
                <span class="detail-value">${lowEnd}</span>
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

        ${showPrice ? html`
          <div class="price-container">
            <div class="price-item ${lowTariffActive ? 'active' : ''}">
              <span class="price-label">Aktuální cena</span>
              <span class="price-value">${currentPrice} Kč/kWh</span>
              <span class="price-tariff">${lowTariffActive ? 'Nízký tarif' : 'Vysoký tarif'}</span>
            </div>
          </div>
        ` : ''}

        ${this._renderSchedule()}
      </ha-card>
    `;
  }

  private _renderSchedule() {
    if (!this.config.show_schedule) return html``;
    
    const scheduleEntity = this.config.entities?.schedule || 'sensor.cez_hdo_rozvrh';
    const scheduleState = this.hass.states[scheduleEntity];
    
    if (!scheduleState || !scheduleState.attributes.schedule) {
      return html`<div class="schedule-error">Rozvrh není k dispozici</div>`;
    }

    const schedule = scheduleState.attributes.schedule as ScheduleItem[];
    const days: Record<string, { label: string; items: ScheduleItem[] }> = {};

    // Group by days - use local date (not UTC)
    schedule.forEach((item) => {
      const start = new Date(item.start);
      const year = start.getFullYear();
      const month = String(start.getMonth() + 1).padStart(2, '0');
      const day = String(start.getDate()).padStart(2, '0');
      const dayKey = `${year}-${month}-${day}`;
      const dayLabel = start.toLocaleDateString('cs-CZ', { weekday: 'short', day: '2-digit', month: '2-digit' });
      
      if (!days[dayKey]) {
        days[dayKey] = { label: dayLabel, items: [] };
      }
      days[dayKey].items.push(item);
    });

    const sortedDays = Object.keys(days).sort();

    const ntPrice = this.config.low_tariff_price || 0;
    const vtPrice = this.config.high_tariff_price || 0;
    const showSchedulePrices = this.config.show_schedule_prices === true && (ntPrice > 0 || vtPrice > 0);

    return html`
      <div class="schedule-container">
        <div class="schedule-header">
          <span class="schedule-title">HDO rozvrh</span>
          <div class="schedule-legend">
            <span class="legend-item nt">
              <span class="legend-color"></span>NT${showSchedulePrices ? html` <span class="legend-price">${ntPrice} Kč</span>` : ''}
            </span>
            <span class="legend-item vt">
              <span class="legend-color"></span>VT${showSchedulePrices ? html` <span class="legend-price">${vtPrice} Kč</span>` : ''}
            </span>
          </div>
        </div>
        <div class="schedule-time-axis">
          <span>0:00</span><span>6:00</span><span>12:00</span><span>18:00</span><span>24:00</span>
        </div>
        ${sortedDays.map((dayKey) => {
          const day = days[dayKey];
          return html`
            <div class="schedule-row">
              <div class="schedule-day-label">${day.label}</div>
              <div class="schedule-bar">
                ${day.items.map((item) => {
                  const start = new Date(item.start);
                  const end = new Date(item.end);
                  const startHour = start.getHours() + start.getMinutes() / 60;
                  let endHour = end.getHours() + end.getMinutes() / 60;
                  if (endHour === 0) endHour = 24;
                  const left = (startHour / 24) * 100;
                  const width = ((endHour - startHour) / 24) * 100;
                  const startStr = start.toLocaleTimeString('cs-CZ', { hour: '2-digit', minute: '2-digit' });
                  const endStr = end.toLocaleTimeString('cs-CZ', { hour: '2-digit', minute: '2-digit' });
                  return html`
                    <div 
                      class="schedule-block ${item.tariff.toLowerCase()}"
                      style="left:${left}%;width:${width}%"
                      title="${startStr}-${endStr}"
                    >
                      ${width > 8 ? html`<span class="block-time">${startStr}-${endStr}</span>` : ''}
                    </div>
                  `;
                })}
              </div>
            </div>
          `;
        })}
      </div>
    `;
  }

  static get styles(): CSSResultGroup {
    return css`
      :host {
        display: block;
      }

      ha-card {
        padding: 16px;
        background: var(--card-background-color, var(--ha-card-background));
        border-radius: var(--ha-card-border-radius, 12px);
        box-shadow: var(--ha-card-box-shadow, 0 2px 4px rgba(0, 0, 0, 0.1));
      }

      .card-header {
        font-size: 24px;
        font-weight: 500;
        margin-bottom: 8px;
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
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      }

      .status-item.low-tariff {
        background: var(--low-tariff-color, #4caf50);
        color: white;
      }

      .status-item.high-tariff {
        background: var(--high-tariff-color, #ff5722);
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

      .status-price {
        font-size: 11px;
        font-weight: 500;
        opacity: 0.85;
        margin-top: 4px;
        padding-top: 4px;
        border-top: 1px solid rgba(255, 255, 255, 0.3);
      }

      .details-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
      }

      .detail-item {
        padding: 8px 12px;
        background: var(--secondary-background-color, rgba(0, 0, 0, 0.05));
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

      .price-container {
        margin-top: 16px;
        padding: 12px;
        background: linear-gradient(135deg, var(--primary-color, #03a9f4) 0%, var(--accent-color, #00bcd4) 100%);
        border-radius: 8px;
        text-align: center;
      }

      .price-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        color: white;
      }

      .price-label {
        font-size: 12px;
        opacity: 0.9;
      }

      .price-value {
        font-size: 24px;
        font-weight: 700;
      }

      .price-tariff {
        font-size: 11px;
        opacity: 0.8;
        text-transform: uppercase;
      }

      .compact .price-container {
        margin-top: 8px;
        padding: 8px;
      }

      .compact .price-value {
        font-size: 18px;
      }

      /* Schedule styles */
      .schedule-container {
        margin-top: 16px;
        padding: 12px;
        background: var(--secondary-background-color, rgba(0, 0, 0, 0.05));
        border-radius: 8px;
      }

      .schedule-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      }

      .schedule-title {
        font-weight: 600;
        font-size: 14px;
        color: var(--primary-text-color);
      }

      .schedule-legend {
        display: flex;
        gap: 12px;
        font-size: 11px;
      }

      .legend-item {
        display: flex;
        align-items: center;
        gap: 4px;
      }

      .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 2px;
      }

      .legend-item.nt .legend-color {
        background: var(--low-tariff-color, #4caf50);
      }

      .legend-item.vt .legend-color {
        background: var(--high-tariff-color, #ff5722);
      }

      .legend-price {
        font-weight: 500;
        opacity: 0.8;
      }

      .schedule-time-axis {
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        color: var(--secondary-text-color);
        margin-bottom: 4px;
        padding-left: 60px;
      }

      .schedule-row {
        display: flex;
        align-items: center;
        margin-bottom: 4px;
      }

      .schedule-day-label {
        width: 55px;
        font-size: 11px;
        color: var(--primary-text-color);
        flex-shrink: 0;
      }

      .schedule-bar {
        flex: 1;
        height: 24px;
        background: var(--divider-color, #e0e0e0);
        border-radius: 4px;
        position: relative;
        overflow: hidden;
      }

      .schedule-block {
        position: absolute;
        top: 0;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 2px;
        transition: opacity 0.2s;
      }

      .schedule-block.nt {
        background: var(--low-tariff-color, #4caf50);
      }

      .schedule-block.vt {
        background: var(--high-tariff-color, #ff5722);
      }

      .schedule-block:hover {
        opacity: 0.85;
      }

      .block-time {
        font-size: 9px;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding: 0 2px;
      }

      .schedule-error {
        padding: 12px;
        text-align: center;
        color: var(--secondary-text-color);
        font-size: 12px;
      }

      .compact .schedule-container {
        margin-top: 8px;
        padding: 8px;
      }

      .compact .schedule-bar {
        height: 18px;
      }

      .compact .block-time {
        display: none;
      }
    `;
  }
}

// Register the card
if (!customElements.get('cez-hdo-card')) {
  customElements.define('cez-hdo-card', CezHdoCard);
}

// Register in customCards array for HACS/Lovelace
declare global {
  interface Window {
    customCards?: Array<{ type: string; name: string; description: string; preview?: boolean }>;
  }
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'cez-hdo-card',
  name: 'ČEZ HDO Card',
  description: 'Custom card for ČEZ HDO integration',
  preview: true,
});



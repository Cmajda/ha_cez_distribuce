import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant, LovelaceCardEditor } from './types';
import { CezHdoCardConfig } from './cez-hdo-card';

@customElement('cez-hdo-card-editor')
export class CezHdoCardEditor extends LitElement implements LovelaceCardEditor {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private config!: CezHdoCardConfig;

  public setConfig(config: CezHdoCardConfig): void {
    this.config = { ...config };
  }

  private valueChanged(ev: CustomEvent): void {
    if (!this.config || !this.hass) {
      return;
    }

    const target = ev.target as any;
    const configValue = target.configValue;
    
    if (this.config[configValue] === target.value) {
      return;
    }

    const newConfig = { ...this.config };
    
    if (target.checked !== undefined) {
      newConfig[configValue] = target.checked;
    } else {
      newConfig[configValue] = target.value;
    }

    const event = new CustomEvent('config-changed', {
      detail: { config: newConfig },
      bubbles: true,
      composed: true
    });
    
    this.dispatchEvent(event);
  }

  protected render() {
    if (!this.hass || !this.config) {
      return html``;
    }

    return html`
      <div class="card-config">
        <div class="option">
          <ha-textfield
            label="Název karty"
            .value=${this.config.title || ''}
            .configValue=${'title'}
            @input=${this.valueChanged}
          ></ha-textfield>
        </div>

        <div class="option">
          <ha-formfield label="Zobrazit hlavičku">
            <ha-switch
              .checked=${this.config.show_header !== false}
              .configValue=${'show_header'}
              @change=${this.valueChanged}
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="option">
          <ha-formfield label="Zobrazit aktuální stav">
            <ha-switch
              .checked=${this.config.show_current_state !== false}
              .configValue=${'show_current_state'}
              @change=${this.valueChanged}
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="option">
          <ha-formfield label="Zobrazit rozvrh">
            <ha-switch
              .checked=${this.config.show_schedule !== false}
              .configValue=${'show_schedule'}
              @change=${this.valueChanged}
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="option">
          <ha-select
            label="Téma"
            .value=${this.config.theme || 'auto'}
            .configValue=${'theme'}
            @selected=${this.valueChanged}
          >
            <mwc-list-item value="auto">Automatické</mwc-list-item>
            <mwc-list-item value="light">Světlé</mwc-list-item>
            <mwc-list-item value="dark">Tmavé</mwc-list-item>
          </ha-select>
        </div>
      </div>
    `;
  }

  static get styles() {
    return css`
      .card-config {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .option {
        display: flex;
        align-items: center;
      }

      ha-textfield {
        width: 100%;
      }

      ha-formfield {
        width: 100%;
      }

      ha-select {
        width: 100%;
      }
    `;
  }
}
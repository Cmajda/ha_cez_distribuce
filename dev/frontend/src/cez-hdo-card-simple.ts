import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('cez-hdo-card')
export class CezHdoCard extends LitElement {
  @property({ attribute: false }) public hass: any;

  static styles = css`
    :host {
      display: block;
      padding: 16px;
      background: var(--ha-card-background, var(--card-background-color, white));
      border-radius: var(--ha-card-border-radius, 12px);
      box-shadow: var(--ha-card-box-shadow, 0 2px 4px rgba(0,0,0,0.1));
    }
  `;

  render() {
    return html`
      <div>
        <h2>ČEZ HDO Card</h2>
        <p>Test card is working!</p>
      </div>
    `;
  }
}

// Register the card with window for Home Assistant
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: 'cez-hdo-card',
  name: 'ČEZ HDO Card',
  description: 'Custom card for ČEZ HDO integration'
});

console.info('ČEZ HDO Card loaded successfully');

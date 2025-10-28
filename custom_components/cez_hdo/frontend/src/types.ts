export interface HomeAssistant {
  states: { [entity_id: string]: HassEntity };
  services: HassServices;
  config: HassConfig;
  themes: any;
  selectedTheme: any;
  panels: any;
  panelUrl: string;
  language: string;
  selectedLanguage?: string;
  resources: any;
  localize: (key: string, ...args: any[]) => string;
  translationMetadata: any;
  suspendWhenHidden: boolean;
  enableShortcuts: boolean;
  vibrate: boolean;
  dockedSidebar: "docked" | "always_hidden" | "auto";
  defaultPanel: string;
  moreInfoEntityId: string;
  user?: CurrentUser;
  callService: (domain: string, service: string, serviceData?: any, target?: any) => Promise<any>;
  callApi: <T>(method: "GET" | "POST" | "PUT" | "DELETE", path: string, parameters?: any) => Promise<T>;
  fetchWithAuth: (path: string, init?: any) => Promise<Response>;
  sendWS: (msg: any) => void;
  callWS: <T>(msg: any) => Promise<T>;
}

export interface HassEntity {
  entity_id: string;
  state: string;
  last_changed: string;
  last_updated: string;
  attributes: { [key: string]: any };
  context: {
    id: string;
    parent_id?: string;
    user_id?: string;
  };
}

export interface HassServices {
  [domain: string]: {
    [service: string]: {
      description?: string;
      fields?: any;
    };
  };
}

export interface HassConfig {
  latitude: number;
  longitude: number;
  elevation: number;
  unit_system: {
    length: string;
    mass: string;
    temperature: string;
    volume: string;
  };
  location_name: string;
  time_zone: string;
  components: string[];
  config_dir: string;
  whitelist_external_dirs: string[];
  allowlist_external_dirs: string[];
  allowlist_external_urls: string[];
  version: string;
  config_source: string;
  safe_mode: boolean;
  state: "NOT_RUNNING" | "STARTING" | "RUNNING" | "STOPPING" | "FINAL_WRITE";
  external_url?: string;
  internal_url?: string;
}

export interface CurrentUser {
  id: string;
  name: string;
  is_owner: boolean;
  is_admin: boolean;
  credentials: any[];
  mfa_modules: any[];
}

export interface LovelaceCard {
  hass?: HomeAssistant;
  setConfig(config: LovelaceCardConfig): void;
  getCardSize?(): number;
}

export interface LovelaceCardConfig {
  type: string;
  [key: string]: any;
}

export interface LovelaceCardEditor extends LovelaceCard {
  setConfig(config: LovelaceCardConfig): void;
}

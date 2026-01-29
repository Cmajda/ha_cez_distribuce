function t(t,e,i,s){var n,o=arguments.length,r=o<3?e:null===s?s=Object.getOwnPropertyDescriptor(e,i):s;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,i,s);else for(var a=t.length-1;a>=0;a--)(n=t[a])&&(r=(o<3?n(r):o>3?n(e,i,r):n(e,i))||r);return o>3&&r&&Object.defineProperty(e,i,r),r}"function"==typeof SuppressedError&&SuppressedError;const e=globalThis,i=e.ShadowRoot&&(void 0===e.ShadyCSS||e.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s=Symbol(),n=new WeakMap;let o=class{constructor(t,e,i){if(this._$cssResult$=!0,i!==s)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(i&&void 0===t){const i=void 0!==e&&1===e.length;i&&(t=n.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&n.set(e,t))}return t}toString(){return this.cssText}};const r=(t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new o(i,t,s)},a=i?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new o("string"==typeof t?t:t+"",void 0,s))(e)})(t):t,{is:c,defineProperty:h,getOwnPropertyDescriptor:l,getOwnPropertyNames:d,getOwnPropertySymbols:p,getPrototypeOf:u}=Object,_=globalThis,f=_.trustedTypes,g=f?f.emptyScript:"",v=_.reactiveElementPolyfillSupport,m=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?g:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},$=(t,e)=>!c(t,e),b={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:$};Symbol.metadata??=Symbol("metadata"),_.litPropertyMetadata??=new WeakMap;let w=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=b){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&h(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:n}=l(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const o=s?.call(this);n?.call(this,e),this.requestUpdate(t,o,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??b}static _$Ei(){if(this.hasOwnProperty(m("elementProperties")))return;const t=u(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(m("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(m("properties"))){const t=this.properties,e=[...d(t),...p(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(a(t))}else void 0!==t&&e.push(a(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((t,s)=>{if(i)t.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const i of s){const s=document.createElement("style"),n=e.litNonce;void 0!==n&&s.setAttribute("nonce",n),s.textContent=i.cssText,t.appendChild(s)}})(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const n=(void 0!==i.converter?.toAttribute?i.converter:y).toAttribute(e,i.type);this._$Em=t,null==n?this.removeAttribute(s):this.setAttribute(s,n),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),n="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=s;const o=n.fromAttribute(e,t.type);this[s]=o??this._$Ej?.get(s)??o,this._$Em=null}}requestUpdate(t,e,i,s=!1,n){if(void 0!==t){const o=this.constructor;if(!1===s&&(n=this[t]),i??=o.getPropertyOptions(t),!((i.hasChanged??$)(n,e)||i.useDefault&&i.reflect&&n===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:n},o){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),!0!==n||void 0!==o)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};w.elementStyles=[],w.shadowRootOptions={mode:"open"},w[m("elementProperties")]=new Map,w[m("finalized")]=new Map,v?.({ReactiveElement:w}),(_.reactiveElementVersions??=[]).push("2.1.2");const x=globalThis,E=t=>t,A=x.trustedTypes,k=A?A.createPolicy("lit-html",{createHTML:t=>t}):void 0,C="$lit$",z=`lit$${Math.random().toFixed(9).slice(2)}$`,S="?"+z,P=`<${S}>`,O=document,T=()=>O.createComment(""),H=t=>null===t||"object"!=typeof t&&"function"!=typeof t,N=Array.isArray,U="[ \t\n\f\r]",M=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,R=/-->/g,D=/>/g,L=RegExp(`>|${U}(?:([^\\s"'>=/]+)(${U}*=${U}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),j=/'/g,Z=/"/g,V=/^(?:script|style|textarea|title)$/i,I=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),W=Symbol.for("lit-noChange"),B=Symbol.for("lit-nothing"),q=new WeakMap,K=O.createTreeWalker(O,129);function F(t,e){if(!N(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==k?k.createHTML(e):e}const J=(t,e)=>{const i=t.length-1,s=[];let n,o=2===e?"<svg>":3===e?"<math>":"",r=M;for(let e=0;e<i;e++){const i=t[e];let a,c,h=-1,l=0;for(;l<i.length&&(r.lastIndex=l,c=r.exec(i),null!==c);)l=r.lastIndex,r===M?"!--"===c[1]?r=R:void 0!==c[1]?r=D:void 0!==c[2]?(V.test(c[2])&&(n=RegExp("</"+c[2],"g")),r=L):void 0!==c[3]&&(r=L):r===L?">"===c[0]?(r=n??M,h=-1):void 0===c[1]?h=-2:(h=r.lastIndex-c[2].length,a=c[1],r=void 0===c[3]?L:'"'===c[3]?Z:j):r===Z||r===j?r=L:r===R||r===D?r=M:(r=L,n=void 0);const d=r===L&&t[e+1].startsWith("/>")?" ":"";o+=r===M?i+P:h>=0?(s.push(a),i.slice(0,h)+C+i.slice(h)+z+d):i+z+(-2===h?e:d)}return[F(t,o+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class Y{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let n=0,o=0;const r=t.length-1,a=this.parts,[c,h]=J(t,e);if(this.el=Y.createElement(c,i),K.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=K.nextNode())&&a.length<r;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(C)){const e=h[o++],i=s.getAttribute(t).split(z),r=/([.?@])?(.*)/.exec(e);a.push({type:1,index:n,name:r[2],strings:i,ctor:"."===r[1]?et:"?"===r[1]?it:"@"===r[1]?st:tt}),s.removeAttribute(t)}else t.startsWith(z)&&(a.push({type:6,index:n}),s.removeAttribute(t));if(V.test(s.tagName)){const t=s.textContent.split(z),e=t.length-1;if(e>0){s.textContent=A?A.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],T()),K.nextNode(),a.push({type:2,index:++n});s.append(t[e],T())}}}else if(8===s.nodeType)if(s.data===S)a.push({type:2,index:n});else{let t=-1;for(;-1!==(t=s.data.indexOf(z,t+1));)a.push({type:7,index:n}),t+=z.length-1}n++}}static createElement(t,e){const i=O.createElement("template");return i.innerHTML=t,i}}function G(t,e,i=t,s){if(e===W)return e;let n=void 0!==s?i._$Co?.[s]:i._$Cl;const o=H(e)?void 0:e._$litDirective$;return n?.constructor!==o&&(n?._$AO?.(!1),void 0===o?n=void 0:(n=new o(t),n._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=n:i._$Cl=n),void 0!==n&&(e=G(t,n._$AS(t,e.values),n,s)),e}class Q{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??O).importNode(e,!0);K.currentNode=s;let n=K.nextNode(),o=0,r=0,a=i[0];for(;void 0!==a;){if(o===a.index){let e;2===a.type?e=new X(n,n.nextSibling,this,t):1===a.type?e=new a.ctor(n,a.name,a.strings,this,t):6===a.type&&(e=new nt(n,this,t)),this._$AV.push(e),a=i[++r]}o!==a?.index&&(n=K.nextNode(),o++)}return K.currentNode=O,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class X{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=B,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=G(this,t,e),H(t)?t===B||null==t||""===t?(this._$AH!==B&&this._$AR(),this._$AH=B):t!==this._$AH&&t!==W&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>N(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==B&&H(this._$AH)?this._$AA.nextSibling.data=t:this.T(O.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=Y.createElement(F(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new Q(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=q.get(t.strings);return void 0===e&&q.set(t.strings,e=new Y(t)),e}k(t){N(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const n of t)s===e.length?e.push(i=new X(this.O(T()),this.O(T()),this,this.options)):i=e[s],i._$AI(n),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=E(t).nextSibling;E(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class tt{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,n){this.type=1,this._$AH=B,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=n,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=B}_$AI(t,e=this,i,s){const n=this.strings;let o=!1;if(void 0===n)t=G(this,t,e,0),o=!H(t)||t!==this._$AH&&t!==W,o&&(this._$AH=t);else{const s=t;let r,a;for(t=n[0],r=0;r<n.length-1;r++)a=G(this,s[i+r],e,r),a===W&&(a=this._$AH[r]),o||=!H(a)||a!==this._$AH[r],a===B?t=B:t!==B&&(t+=(a??"")+n[r+1]),this._$AH[r]=a}o&&!s&&this.j(t)}j(t){t===B?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class et extends tt{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===B?void 0:t}}class it extends tt{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==B)}}class st extends tt{constructor(t,e,i,s,n){super(t,e,i,s,n),this.type=5}_$AI(t,e=this){if((t=G(this,t,e,0)??B)===W)return;const i=this._$AH,s=t===B&&i!==B||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,n=t!==B&&(i===B||s);s&&this.element.removeEventListener(this.name,this,i),n&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class nt{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){G(this,t)}}const ot=x.litHtmlPolyfillSupport;ot?.(Y,X),(x.litHtmlVersions??=[]).push("3.3.2");const rt=globalThis;class at extends w{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let n=s._$litPart$;if(void 0===n){const t=i?.renderBefore??null;s._$litPart$=n=new X(e.insertBefore(T(),t),t,void 0,i??{})}return n._$AI(t),n})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return W}}at._$litElement$=!0,at.finalized=!0,rt.litElementHydrateSupport?.({LitElement:at});const ct=rt.litElementPolyfillSupport;ct?.({LitElement:at}),(rt.litElementVersions??=[]).push("4.2.2");const ht={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:$},lt=(t=ht,e,i)=>{const{kind:s,metadata:n}=i;let o=globalThis.litPropertyMetadata.get(n);if(void 0===o&&globalThis.litPropertyMetadata.set(n,o=new Map),"setter"===s&&((t=Object.create(t)).wrapped=!0),o.set(i.name,t),"accessor"===s){const{name:s}=i;return{set(i){const n=e.get.call(this);e.set.call(this,i),this.requestUpdate(s,n,t,!0,i)},init(e){return void 0!==e&&this.C(s,void 0,t,e),e}}}if("setter"===s){const{name:s}=i;return function(i){const n=this[s];e.call(this,i),this.requestUpdate(s,n,t,!0,i)}}throw Error("Unsupported decorator location: "+s)};function dt(t){return(e,i)=>"object"==typeof i?lt(t,e,i):((t,e,i)=>{const s=e.hasOwnProperty(i);return e.constructor.createProperty(i,t),s?Object.getOwnPropertyDescriptor(e,i):void 0})(t,e,i)}const pt={low_tariff:"binary_sensor.cez_hdo_nizky_tarif_aktivni",high_tariff:"binary_sensor.cez_hdo_vysoky_tarif_aktivni",low_start:"sensor.cez_hdo_nizky_tarif_zacatek",low_end:"sensor.cez_hdo_nizky_tarif_konec",low_duration:"sensor.cez_hdo_nizky_tarif_zbyva",high_start:"sensor.cez_hdo_vysoky_tarif_zacatek",high_end:"sensor.cez_hdo_vysoky_tarif_konec",high_duration:"sensor.cez_hdo_vysoky_tarif_zbyva",schedule:"sensor.cez_hdo_rozvrh"};let ut=class extends at{static getConfigElement(){return document.createElement("cez-hdo-card-editor")}static getStubConfig(){return{type:"custom:cez-hdo-card",title:"ČEZ HDO Status",show_times:!0,show_duration:!0,compact_mode:!1,entities:{...pt}}}setConfig(t){t.entities||(t={entities:{...pt},title:"ČEZ HDO Status",show_times:!0,show_duration:!0,compact_mode:!1,...t}),this.config=t}getEntityState(t){if(!t||!this.hass)return"unavailable";const e=this.hass.states[t];return e?e.state:"unavailable"}isEntityOn(t){return"on"===this.getEntityState(t)}render(){if(!this.config||!this.hass)return I`<ha-card>Loading...</ha-card>`;const{entities:t}=this.config;if(!t)return I`<ha-card>No entities configured</ha-card>`;const e=this.isEntityOn(t.low_tariff),i=this.isEntityOn(t.high_tariff),s=this.getEntityState(t.low_start),n=this.getEntityState(t.low_end),o=this.getEntityState(t.low_duration),r=this.getEntityState(t.high_start),a=this.getEntityState(t.high_end),c=this.getEntityState(t.high_duration),h=this.config.title||"ČEZ HDO",l=!1!==this.config.show_times,d=!1!==this.config.show_duration,p=!0===this.config.compact_mode,u=!1!==this.config.show_price,_=this.config.low_tariff_price||0,f=this.config.high_tariff_price||0,g=e?_:f,v=!0===this.config.show_tariff_prices,m=!1!==this.config.show_title,y=!1!==this.config.show_tariff_status;return I`
      <ha-card class="${p?"compact":""}">
        ${m?I`<div class="card-header">${h}</div>`:""}

        ${y?I`
          <div class="status-container">
            <div class="status-item ${e?"active low-tariff":"inactive"}">
              <div class="status-title">Nízký tarif</div>
              <div class="status-value">${e?"Aktivní":"Neaktivní"}</div>
              ${v&&_>0?I`<div class="status-price">${_} Kč/kWh</div>`:""}
            </div>
            <div class="status-item ${i?"active high-tariff":"inactive"}">
              <div class="status-title">Vysoký tarif</div>
              <div class="status-value">${i?"Aktivní":"Neaktivní"}</div>
              ${v&&f>0?I`<div class="status-price">${f} Kč/kWh</div>`:""}
            </div>
          </div>
        `:""}

        ${l||d?I`
          <div class="details-container">
            ${l?I`
              <div class="detail-item">
                <span class="detail-label">NT začátek</span>
                <span class="detail-value">${s}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT začátek</span>
                <span class="detail-value">${r}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">NT konec</span>
                <span class="detail-value">${n}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT konec</span>
                <span class="detail-value">${a}</span>
              </div>
            `:""}
            ${d?I`
              <div class="detail-item">
                <span class="detail-label">NT zbývá</span>
                <span class="detail-value">${o}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT zbývá</span>
                <span class="detail-value">${c}</span>
              </div>
            `:""}
          </div>
        `:""}

        ${u?I`
          <div class="price-container">
            <div class="price-item ${e?"active":""}">
              <span class="price-label">Aktuální cena</span>
              <span class="price-value">${g} Kč/kWh</span>
              <span class="price-tariff">${e?"Nízký tarif":"Vysoký tarif"}</span>
            </div>
          </div>
        `:""}

        ${this._renderSchedule()}
      </ha-card>
    `}_renderSchedule(){if(!this.config.show_schedule)return I``;const t=this.config.entities?.schedule||"sensor.cez_hdo_rozvrh",e=this.hass.states[t];if(!e||!e.attributes.schedule)return I`<div class="schedule-error">Rozvrh není k dispozici</div>`;const i=e.attributes.schedule,s={};i.forEach(t=>{const e=new Date(t.start),i=`${e.getFullYear()}-${String(e.getMonth()+1).padStart(2,"0")}-${String(e.getDate()).padStart(2,"0")}`,n=e.toLocaleDateString("cs-CZ",{weekday:"short",day:"2-digit",month:"2-digit"});s[i]||(s[i]={label:n,items:[]}),s[i].items.push(t)});const n=Object.keys(s).sort(),o=this.config.low_tariff_price||0,r=this.config.high_tariff_price||0,a=!0===this.config.show_schedule_prices&&(o>0||r>0);return I`
      <div class="schedule-container">
        <div class="schedule-header">
          <span class="schedule-title">HDO rozvrh</span>
          <div class="schedule-legend">
            <span class="legend-item nt">
              <span class="legend-color"></span>NT${a?I` <span class="legend-price">${o} Kč</span>`:""}
            </span>
            <span class="legend-item vt">
              <span class="legend-color"></span>VT${a?I` <span class="legend-price">${r} Kč</span>`:""}
            </span>
          </div>
        </div>
        <div class="schedule-time-axis">
          <span>0:00</span><span>6:00</span><span>12:00</span><span>18:00</span><span>24:00</span>
        </div>
        ${n.map(t=>{const e=s[t];return I`
            <div class="schedule-row">
              <div class="schedule-day-label">${e.label}</div>
              <div class="schedule-bar">
                ${e.items.map(t=>{const e=new Date(t.start),i=new Date(t.end),s=e.getHours()+e.getMinutes()/60;let n=i.getHours()+i.getMinutes()/60;0===n&&(n=24);const o=s/24*100,r=(n-s)/24*100,a=e.toLocaleTimeString("cs-CZ",{hour:"2-digit",minute:"2-digit"}),c=i.toLocaleTimeString("cs-CZ",{hour:"2-digit",minute:"2-digit"});return I`
                    <div 
                      class="schedule-block ${t.tariff.toLowerCase()}"
                      style="left:${o}%;width:${r}%"
                      title="${a}-${c}"
                    >
                      ${r>8?I`<span class="block-time">${a}-${c}</span>`:""}
                    </div>
                  `})}
              </div>
            </div>
          `})}
      </div>
    `}static get styles(){return r`
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
    `}};t([dt({attribute:!1})],ut.prototype,"hass",void 0),t([function(t){return dt({...t,state:!0,attribute:!1})}()],ut.prototype,"config",void 0),ut=t([(t=>(e,i)=>{void 0!==i?i.addInitializer(()=>{customElements.define(t,e)}):customElements.define(t,e)})("cez-hdo-card")],ut),customElements.get("cez-hdo-card")||customElements.define("cez-hdo-card",ut),window.customCards=window.customCards||[],window.customCards.push({type:"cez-hdo-card",name:"ČEZ HDO Card",description:"Custom card for ČEZ HDO integration",preview:!0});const _t={low_tariff:["binary_sensor.cez_hdo_nizky_tarif_aktivni"],high_tariff:["binary_sensor.cez_hdo_vysoky_tarif_aktivni"],low_start:["sensor.cez_hdo_nizky_tarif_zacatek"],low_end:["sensor.cez_hdo_nizky_tarif_konec"],low_duration:["sensor.cez_hdo_nizky_tarif_zbyva"],high_start:["sensor.cez_hdo_vysoky_tarif_zacatek"],high_end:["sensor.cez_hdo_vysoky_tarif_konec"],high_duration:["sensor.cez_hdo_vysoky_tarif_zbyva"],schedule:["sensor.cez_hdo_rozvrh"]},ft={low_tariff:_t.low_tariff[0],high_tariff:_t.high_tariff[0],low_start:_t.low_start[0],low_end:_t.low_end[0],low_duration:_t.low_duration[0],high_start:_t.high_start[0],high_end:_t.high_end[0],high_duration:_t.high_duration[0],schedule:_t.schedule[0]};class gt extends HTMLElement{constructor(){super(),this._config={},this.attachShadow({mode:"open"})}set hass(t){if(this._hass=t,this.shadowRoot){this.shadowRoot.querySelectorAll("ha-selector").forEach(e=>{e.hass=t})}}setConfig(t){this._config=t||{},this._render()}_emitConfigChanged(){this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:this._config},bubbles:!0,composed:!0}))}_setOption(t,e,i=!1){this._config={...this._config,[t]:e},this._emitConfigChanged(),i||this._render()}_setPriceOption(t,e){this._config={...this._config,[t]:e}}_emitPriceChange(t,e){if(this._config={...this._config,[t]:e},this._emitConfigChanged(),this._hass){const i="low_tariff_price"===t?e:this._config.low_tariff_price||0,s="high_tariff_price"===t?e:this._config.high_tariff_price||0;this._hass.callService("cez_hdo","set_prices",{low_tariff_price:i,high_tariff_price:s})}}_setEntity(t,e){const i={...this._config.entities||{}};e?i[t]=e:delete i[t],this._config={...this._config,entities:i},this._emitConfigChanged()}_entityPicker(t,e,i){const s=this._config.entities&&this._config.entities[e]||"",n=document.createElement("div");n.className="entity-row";const o=document.createElement("ha-selector");if(o.hass=this._hass,o.label=t,o.selector={entity:i&&i.length?{domain:i}:{}},o.value=s,o.addEventListener("value-changed",t=>{this._setEntity(e,t.detail.value)}),n.appendChild(o),!s){const t=function(t,e){if(!t)return ft[e];const i=_t[e]||[ft[e]];for(const e of i)if(t.states&&t.states[e])return e;return ft[e]}(this._hass,e),i=document.createElement("div");if(i.className="hint",t){const e=!(!this._hass?.states||!this._hass.states[t]);i.textContent=e?`Použito: ${t}`:`Výchozí: ${t} (nenalezeno)`}n.appendChild(i)}return n}_render(){if(!this.shadowRoot||!this._hass)return void(this.shadowRoot&&(this.shadowRoot.innerHTML=""));const t=this._config.title??"",e=!1!==this._config.show_times,i=!1!==this._config.show_duration,s=!0===this._config.compact_mode;this.shadowRoot.innerHTML='\n      <style>\n        .wrap {\n          display: flex;\n          flex-direction: column;\n          gap: 12px;\n          padding: 4px 0;\n        }\n        .entity-row {\n          display: flex;\n          flex-direction: column;\n          gap: 6px;\n        }\n        .entity-row ha-selector {\n          display: block;\n        }\n        .hint {\n          font-size: 12px;\n          opacity: 0.8;\n        }\n      </style>\n      <div class="wrap"></div>\n    ';const n=this.shadowRoot.querySelector(".wrap");if(!n)return;const o=document.createElement("ha-textfield");o.label="Titulek",o.value=t,o.addEventListener("input",t=>{this._config={...this._config,title:t.target.value}}),o.addEventListener("change",t=>{this._config={...this._config,title:t.target.value},this._emitConfigChanged()}),n.appendChild(o);const r=(t,e,i)=>{const s=document.createElement("ha-formfield");s.label=t;const n=document.createElement("ha-switch");return n.checked=i,n.addEventListener("change",()=>this._setOption(e,n.checked,!0)),s.appendChild(n),s};n.appendChild(r("Zobrazit titulek","show_title",!1!==this._config.show_title)),n.appendChild(r("Zobrazit stavy tarifů","show_tariff_status",!1!==this._config.show_tariff_status)),n.appendChild(r("Zobrazit ceny u tarifů","show_tariff_prices",!0===this._config.show_tariff_prices)),n.appendChild(r("Zobrazit časy (začátek/konec)","show_times",e)),n.appendChild(r("Zobrazit zbývající čas","show_duration",i)),n.appendChild(r("Zobrazit aktuální cenu","show_price",!1!==this._config.show_price)),n.appendChild(r("Zobrazit HDO rozvrh","show_schedule",!0===this._config.show_schedule)),n.appendChild(r("Zobrazit ceny v legendě rozvrhu","show_schedule_prices",!0===this._config.show_schedule_prices)),n.appendChild(r("Kompaktní režim","compact_mode",s));const a=document.createElement("ha-textfield");a.label="Cena NT (Kč/kWh)",a.type="number",a.step="0.01",a.value=this._config.low_tariff_price||"",a.addEventListener("input",t=>{this._setPriceOption("low_tariff_price",parseFloat(t.target.value)||0)}),a.addEventListener("change",t=>{this._emitPriceChange("low_tariff_price",parseFloat(t.target.value)||0)}),n.appendChild(a);const c=document.createElement("ha-textfield");c.label="Cena VT (Kč/kWh)",c.type="number",c.step="0.01",c.value=this._config.high_tariff_price||"",c.addEventListener("input",t=>{this._setPriceOption("high_tariff_price",parseFloat(t.target.value)||0)}),c.addEventListener("change",t=>{this._emitPriceChange("high_tariff_price",parseFloat(t.target.value)||0)}),n.appendChild(c),n.appendChild(this._entityPicker("NT aktivní (binary_sensor)","low_tariff",["binary_sensor"])),n.appendChild(this._entityPicker("VT aktivní (binary_sensor)","high_tariff",["binary_sensor"])),n.appendChild(this._entityPicker("NT začátek (sensor)","low_start",["sensor"])),n.appendChild(this._entityPicker("NT konec (sensor)","low_end",["sensor"])),n.appendChild(this._entityPicker("NT zbývá (sensor)","low_duration",["sensor"])),n.appendChild(this._entityPicker("VT začátek (sensor)","high_start",["sensor"])),n.appendChild(this._entityPicker("VT konec (sensor)","high_end",["sensor"])),n.appendChild(this._entityPicker("VT zbývá (sensor)","high_duration",["sensor"])),n.appendChild(this._entityPicker("HDO rozvrh (sensor)","schedule",["sensor"]));const h=document.createElement("div");h.className="hint",h.textContent="Entity jsou předvyplněny automaticky. Změňte pouze pokud máte více instancí integrace.",n.appendChild(h)}}customElements.get("cez-hdo-card-editor")||customElements.define("cez-hdo-card-editor",gt);console.info("ČEZ HDO Card v2.2.0 loaded successfully");

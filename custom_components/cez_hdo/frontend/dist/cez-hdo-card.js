/*! For license information please see cez-hdo-card.js.LICENSE.txt */
(()=>{"use strict";const t=globalThis,e=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s=Symbol(),i=new WeakMap;class o{constructor(t,e,i){if(this._$cssResult$=!0,i!==s)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const s=this.t;if(e&&void 0===t){const e=void 0!==s&&1===s.length;e&&(t=i.get(s)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&i.set(s,t))}return t}toString(){return this.cssText}}const r=(s,i)=>{if(e)s.adoptedStyleSheets=i.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const e of i){const i=document.createElement("style"),o=t.litNonce;void 0!==o&&i.setAttribute("nonce",o),i.textContent=e.cssText,s.appendChild(i)}},n=e?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const s of t.cssRules)e+=s.cssText;return(t=>new o("string"==typeof t?t:t+"",void 0,s))(e)})(t):t,{is:a,defineProperty:h,getOwnPropertyDescriptor:l,getOwnPropertyNames:c,getOwnPropertySymbols:d,getPrototypeOf:p}=Object,u=globalThis,f=u.trustedTypes,_=f?f.emptyScript:"",$=u.reactiveElementPolyfillSupport,g=(t,e)=>t,v={toAttribute(t,e){switch(e){case Boolean:t=t?_:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let s=t;switch(e){case Boolean:s=null!==t;break;case Number:s=null===t?null:Number(t);break;case Object:case Array:try{s=JSON.parse(t)}catch(t){s=null}}return s}},m=(t,e)=>!a(t,e),y={attribute:!0,type:String,converter:v,reflect:!1,useDefault:!1,hasChanged:m};Symbol.metadata??=Symbol("metadata"),u.litPropertyMetadata??=new WeakMap;class A extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=y){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const s=Symbol(),i=this.getPropertyDescriptor(t,s,e);void 0!==i&&h(this.prototype,t,i)}}static getPropertyDescriptor(t,e,s){const{get:i,set:o}=l(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:i,set(e){const r=i?.call(this);o?.call(this,e),this.requestUpdate(t,r,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??y}static _$Ei(){if(this.hasOwnProperty(g("elementProperties")))return;const t=p(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(g("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(g("properties"))){const t=this.properties,e=[...c(t),...d(t)];for(const s of e)this.createProperty(s,t[s])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,s]of e)this.elementProperties.set(t,s)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const s=this._$Eu(t,e);void 0!==s&&this._$Eh.set(s,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const s=new Set(t.flat(1/0).reverse());for(const t of s)e.unshift(n(t))}else void 0!==t&&e.push(n(t));return e}static _$Eu(t,e){const s=e.attribute;return!1===s?void 0:"string"==typeof s?s:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const s of e.keys())this.hasOwnProperty(s)&&(t.set(s,this[s]),delete this[s]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return r(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,s){this._$AK(t,s)}_$ET(t,e){const s=this.constructor.elementProperties.get(t),i=this.constructor._$Eu(t,s);if(void 0!==i&&!0===s.reflect){const o=(void 0!==s.converter?.toAttribute?s.converter:v).toAttribute(e,s.type);this._$Em=t,null==o?this.removeAttribute(i):this.setAttribute(i,o),this._$Em=null}}_$AK(t,e){const s=this.constructor,i=s._$Eh.get(t);if(void 0!==i&&this._$Em!==i){const t=s.getPropertyOptions(i),o="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:v;this._$Em=i;const r=o.fromAttribute(e,t.type);this[i]=r??this._$Ej?.get(i)??r,this._$Em=null}}requestUpdate(t,e,s){if(void 0!==t){const i=this.constructor,o=this[t];if(s??=i.getPropertyOptions(t),!((s.hasChanged??m)(o,e)||s.useDefault&&s.reflect&&o===this._$Ej?.get(t)&&!this.hasAttribute(i._$Eu(t,s))))return;this.C(t,e,s)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:s,reflect:i,wrapped:o},r){s&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,r??e??this[t]),!0!==o||void 0!==r)||(this._$AL.has(t)||(this.hasUpdated||s||(e=void 0),this._$AL.set(t,e)),!0===i&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,s]of t){const{wrapped:t}=s,i=this[e];!0!==t||this._$AL.has(e)||void 0===i||this.C(e,void 0,s,i)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}}A.elementStyles=[],A.shadowRootOptions={mode:"open"},A[g("elementProperties")]=new Map,A[g("finalized")]=new Map,$?.({ReactiveElement:A}),(u.reactiveElementVersions??=[]).push("2.1.1");const b=globalThis,E=b.trustedTypes,w=E?E.createPolicy("lit-html",{createHTML:t=>t}):void 0,S="$lit$",x=`lit$${Math.random().toFixed(9).slice(2)}$`,C="?"+x,P=`<${C}>`,O=document,U=()=>O.createComment(""),H=t=>null===t||"object"!=typeof t&&"function"!=typeof t,T=Array.isArray,k="[ \t\n\f\r]",N=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,z=/-->/g,M=/>/g,R=RegExp(`>|${k}(?:([^\\s"'>=/]+)(${k}*=${k}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),D=/'/g,j=/"/g,L=/^(?:script|style|textarea|title)$/i,B=t=>(e,...s)=>({_$litType$:t,strings:e,values:s}),I=B(1),V=(B(2),B(3),Symbol.for("lit-noChange")),q=Symbol.for("lit-nothing"),W=new WeakMap,Z=O.createTreeWalker(O,129);function F(t,e){if(!T(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==w?w.createHTML(e):e}const J=(t,e)=>{const s=t.length-1,i=[];let o,r=2===e?"<svg>":3===e?"<math>":"",n=N;for(let e=0;e<s;e++){const s=t[e];let a,h,l=-1,c=0;for(;c<s.length&&(n.lastIndex=c,h=n.exec(s),null!==h);)c=n.lastIndex,n===N?"!--"===h[1]?n=z:void 0!==h[1]?n=M:void 0!==h[2]?(L.test(h[2])&&(o=RegExp("</"+h[2],"g")),n=R):void 0!==h[3]&&(n=R):n===R?">"===h[0]?(n=o??N,l=-1):void 0===h[1]?l=-2:(l=n.lastIndex-h[2].length,a=h[1],n=void 0===h[3]?R:'"'===h[3]?j:D):n===j||n===D?n=R:n===z||n===M?n=N:(n=R,o=void 0);const d=n===R&&t[e+1].startsWith("/>")?" ":"";r+=n===N?s+P:l>=0?(i.push(a),s.slice(0,l)+S+s.slice(l)+x+d):s+x+(-2===l?e:d)}return[F(t,r+(t[s]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),i]};class K{constructor({strings:t,_$litType$:e},s){let i;this.parts=[];let o=0,r=0;const n=t.length-1,a=this.parts,[h,l]=J(t,e);if(this.el=K.createElement(h,s),Z.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(i=Z.nextNode())&&a.length<n;){if(1===i.nodeType){if(i.hasAttributes())for(const t of i.getAttributeNames())if(t.endsWith(S)){const e=l[r++],s=i.getAttribute(t).split(x),n=/([.?@])?(.*)/.exec(e);a.push({type:1,index:o,name:n[2],strings:s,ctor:"."===n[1]?tt:"?"===n[1]?et:"@"===n[1]?st:Y}),i.removeAttribute(t)}else t.startsWith(x)&&(a.push({type:6,index:o}),i.removeAttribute(t));if(L.test(i.tagName)){const t=i.textContent.split(x),e=t.length-1;if(e>0){i.textContent=E?E.emptyScript:"";for(let s=0;s<e;s++)i.append(t[s],U()),Z.nextNode(),a.push({type:2,index:++o});i.append(t[e],U())}}}else if(8===i.nodeType)if(i.data===C)a.push({type:2,index:o});else{let t=-1;for(;-1!==(t=i.data.indexOf(x,t+1));)a.push({type:7,index:o}),t+=x.length-1}o++}}static createElement(t,e){const s=O.createElement("template");return s.innerHTML=t,s}}function G(t,e,s=t,i){if(e===V)return e;let o=void 0!==i?s._$Co?.[i]:s._$Cl;const r=H(e)?void 0:e._$litDirective$;return o?.constructor!==r&&(o?._$AO?.(!1),void 0===r?o=void 0:(o=new r(t),o._$AT(t,s,i)),void 0!==i?(s._$Co??=[])[i]=o:s._$Cl=o),void 0!==o&&(e=G(t,o._$AS(t,e.values),o,i)),e}class Q{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:s}=this._$AD,i=(t?.creationScope??O).importNode(e,!0);Z.currentNode=i;let o=Z.nextNode(),r=0,n=0,a=s[0];for(;void 0!==a;){if(r===a.index){let e;2===a.type?e=new X(o,o.nextSibling,this,t):1===a.type?e=new a.ctor(o,a.name,a.strings,this,t):6===a.type&&(e=new it(o,this,t)),this._$AV.push(e),a=s[++n]}r!==a?.index&&(o=Z.nextNode(),r++)}return Z.currentNode=O,i}p(t){let e=0;for(const s of this._$AV)void 0!==s&&(void 0!==s.strings?(s._$AI(t,s,e),e+=s.strings.length-2):s._$AI(t[e])),e++}}class X{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,s,i){this.type=2,this._$AH=q,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=s,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=G(this,t,e),H(t)?t===q||null==t||""===t?(this._$AH!==q&&this._$AR(),this._$AH=q):t!==this._$AH&&t!==V&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>T(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==q&&H(this._$AH)?this._$AA.nextSibling.data=t:this.T(O.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:s}=t,i="number"==typeof s?this._$AC(t):(void 0===s.el&&(s.el=K.createElement(F(s.h,s.h[0]),this.options)),s);if(this._$AH?._$AD===i)this._$AH.p(e);else{const t=new Q(i,this),s=t.u(this.options);t.p(e),this.T(s),this._$AH=t}}_$AC(t){let e=W.get(t.strings);return void 0===e&&W.set(t.strings,e=new K(t)),e}k(t){T(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let s,i=0;for(const o of t)i===e.length?e.push(s=new X(this.O(U()),this.O(U()),this,this.options)):s=e[i],s._$AI(o),i++;i<e.length&&(this._$AR(s&&s._$AB.nextSibling,i),e.length=i)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=t.nextSibling;t.remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class Y{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,s,i,o){this.type=1,this._$AH=q,this._$AN=void 0,this.element=t,this.name=e,this._$AM=i,this.options=o,s.length>2||""!==s[0]||""!==s[1]?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=q}_$AI(t,e=this,s,i){const o=this.strings;let r=!1;if(void 0===o)t=G(this,t,e,0),r=!H(t)||t!==this._$AH&&t!==V,r&&(this._$AH=t);else{const i=t;let n,a;for(t=o[0],n=0;n<o.length-1;n++)a=G(this,i[s+n],e,n),a===V&&(a=this._$AH[n]),r||=!H(a)||a!==this._$AH[n],a===q?t=q:t!==q&&(t+=(a??"")+o[n+1]),this._$AH[n]=a}r&&!i&&this.j(t)}j(t){t===q?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class tt extends Y{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===q?void 0:t}}class et extends Y{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==q)}}class st extends Y{constructor(t,e,s,i,o){super(t,e,s,i,o),this.type=5}_$AI(t,e=this){if((t=G(this,t,e,0)??q)===V)return;const s=this._$AH,i=t===q&&s!==q||t.capture!==s.capture||t.once!==s.once||t.passive!==s.passive,o=t!==q&&(s===q||i);i&&this.element.removeEventListener(this.name,this,s),o&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class it{constructor(t,e,s){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=s}get _$AU(){return this._$AM._$AU}_$AI(t){G(this,t)}}const ot=b.litHtmlPolyfillSupport;ot?.(K,X),(b.litHtmlVersions??=[]).push("3.3.1");const rt=globalThis;class nt extends A{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,s)=>{const i=s?.renderBefore??e;let o=i._$litPart$;if(void 0===o){const t=s?.renderBefore??null;i._$litPart$=o=new X(e.insertBefore(U(),t),t,void 0,s??{})}return o._$AI(t),o})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return V}}nt._$litElement$=!0,nt.finalized=!0,rt.litElementHydrateSupport?.({LitElement:nt});const at=rt.litElementPolyfillSupport;at?.({LitElement:nt}),(rt.litElementVersions??=[]).push("4.2.1");const ht={attribute:!0,type:String,converter:v,reflect:!1,hasChanged:m},lt=(t=ht,e,s)=>{const{kind:i,metadata:o}=s;let r=globalThis.litPropertyMetadata.get(o);if(void 0===r&&globalThis.litPropertyMetadata.set(o,r=new Map),"setter"===i&&((t=Object.create(t)).wrapped=!0),r.set(s.name,t),"accessor"===i){const{name:i}=s;return{set(s){const o=e.get.call(this);e.set.call(this,s),this.requestUpdate(i,o,t)},init(e){return void 0!==e&&this.C(i,void 0,t,e),e}}}if("setter"===i){const{name:i}=s;return function(s){const o=this[i];e.call(this,s),this.requestUpdate(i,o,t)}}throw Error("Unsupported decorator location: "+i)};function ct(t){return(e,s)=>"object"==typeof s?lt(t,e,s):((t,e,s)=>{const i=e.hasOwnProperty(s);return e.constructor.createProperty(s,t),i?Object.getOwnPropertyDescriptor(e,s):void 0})(t,e,s)}var dt=function(t,e,s,i){var o,r=arguments.length,n=r<3?e:null===i?i=Object.getOwnPropertyDescriptor(e,s):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(t,e,s,i);else for(var a=t.length-1;a>=0;a--)(o=t[a])&&(n=(r<3?o(n):r>3?o(e,s,n):o(e,s))||n);return r>3&&n&&Object.defineProperty(e,s,n),n};class pt extends nt{setConfig(t){console.log("CezHdoCard setConfig called with:",t),t.entities||(console.log("Entities missing, auto-filling with default configuration"),t={entities:{low_tariff:"binary_sensor.cez_hdo_lowtariffactive",high_tariff:"binary_sensor.cez_hdo_hightariffactive",low_start:"sensor.cez_hdo_lowtariffstart",low_end:"sensor.cez_hdo_lowtariffend",low_duration:"sensor.cez_hdo_lowtariffduration",high_start:"sensor.cez_hdo_hightariffstart",high_end:"sensor.cez_hdo_hightariffend",high_duration:"sensor.cez_hdo_hightariffduration"},title:"ČEZ HDO Status",show_times:!0,show_duration:!0,compact_mode:!1,...t},console.log("Auto-filled config:",t)),console.log("Config validation passed"),this.config=t}getEntityState(t){if(!t||!this.hass)return"unavailable";const e=this.hass.states[t];return e?e.state:"unavailable"}isEntityOn(t){return"on"===this.getEntityState(t)}render(){if(!this.config||!this.hass)return I`<ha-card>Loading...</ha-card>`;const{entities:t}=this.config,e=this.isEntityOn(t.low_tariff),s=this.isEntityOn(t.high_tariff),i=this.getEntityState(t.low_start),o=this.getEntityState(t.low_end),r=this.getEntityState(t.low_duration),n=this.getEntityState(t.high_start),a=this.getEntityState(t.high_end),h=this.getEntityState(t.high_duration),l=this.config.title||"ČEZ HDO",c=!1!==this.config.show_times,d=!1!==this.config.show_duration,p=!0===this.config.compact_mode,u=!1!==this.config.show_price,f=this.config.low_tariff_price||0,_=this.config.high_tariff_price||0,$=e?f:_,g=!0===this.config.show_tariff_prices;return I`
      <ha-card class="${p?"compact":""}">
        ${l?I`<div class="card-header">${l}</div>`:""}

        <div class="status-container">
          <div class="status-item ${e?"active low-tariff":"inactive"}">
            <div class="status-title">Nízký tarif</div>
            <div class="status-value">${e?"Aktivní":"Neaktivní"}</div>
            ${g&&f>0?I`<div class="status-price">${f} Kč/kWh</div>`:""}
          </div>
          <div class="status-item ${s?"active high-tariff":"inactive"}">
            <div class="status-title">Vysoký tarif</div>
            <div class="status-value">${s?"Aktivní":"Neaktivní"}</div>
            ${g&&_>0?I`<div class="status-price">${_} Kč/kWh</div>`:""}
          </div>
        </div>

        ${c||d?I`
          <div class="details-container">
            ${c?I`
              <div class="detail-item">
                <span class="detail-label">NT začátek</span>
                <span class="detail-value">${i}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT začátek</span>
                <span class="detail-value">${n}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">NT konec</span>
                <span class="detail-value">${o}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT konec</span>
                <span class="detail-value">${a}</span>
              </div>
            `:""}
            ${d?I`
              <div class="detail-item">
                <span class="detail-label">NT zbývá</span>
                <span class="detail-value">${r}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">VT zbývá</span>
                <span class="detail-value">${h}</span>
              </div>
            `:""}
          </div>
        `:""}

        ${u?I`
          <div class="price-container">
            <div class="price-item ${e?"active":""}">
              <span class="price-label">Aktuální cena</span>
              <span class="price-value">${$} Kč/kWh</span>
              <span class="price-tariff">${e?"Nízký tarif":"Vysoký tarif"}</span>
            </div>
          </div>
        `:""}

        ${this._renderSchedule()}
      </ha-card>
    `}

  _renderSchedule(){
    if(!this.config.show_schedule) return I``;
    const scheduleEntity=this.config.entities?.schedule||"sensor.cez_hdo_rozvrh";
    const scheduleState=this.hass.states[scheduleEntity];
    if(!scheduleState||!scheduleState.attributes.schedule) return I`<div class="schedule-error">Rozvrh není k dispozici</div>`;

    const schedule=scheduleState.attributes.schedule;
    const days={};

    // Seskupit podle dnů
    schedule.forEach(item=>{
      const start=new Date(item.start);
      const dayKey=start.toISOString().split("T")[0];
      const dayLabel=start.toLocaleDateString("cs-CZ",{weekday:"short",day:"2-digit",month:"2-digit"});
      if(!days[dayKey]) days[dayKey]={label:dayLabel,items:[]};
      days[dayKey].items.push(item);
    });

    const sortedDays=Object.keys(days).sort();

    return I`
      <div class="schedule-container">
        <div class="schedule-header">
          <span class="schedule-title">HDO rozvrh</span>
          <div class="schedule-legend">
            <span class="legend-item nt"><span class="legend-color"></span>NT</span>
            <span class="legend-item vt"><span class="legend-color"></span>VT</span>
          </div>
        </div>
        <div class="schedule-time-axis">
          <span>0:00</span><span>6:00</span><span>12:00</span><span>18:00</span><span>24:00</span>
        </div>
        ${sortedDays.map(dayKey=>{
          const day=days[dayKey];
          return I`
            <div class="schedule-row">
              <div class="schedule-day-label">${day.label}</div>
              <div class="schedule-bar">
                ${day.items.map(item=>{
                  const start=new Date(item.start);
                  const end=new Date(item.end);
                  const startHour=start.getHours()+start.getMinutes()/60;
                  let endHour=end.getHours()+end.getMinutes()/60;
                  if(endHour===0) endHour=24;
                  const left=(startHour/24)*100;
                  const width=((endHour-startHour)/24)*100;
                  const startStr=start.toLocaleTimeString("cs-CZ",{hour:"2-digit",minute:"2-digit"});
                  const endStr=end.toLocaleTimeString("cs-CZ",{hour:"2-digit",minute:"2-digit"});
                  return I`
                    <div class="schedule-block ${item.tariff.toLowerCase()}"
                         style="left:${left}%;width:${width}%"
                         title="${startStr}-${endStr}">
                      ${width>8?I`<span class="block-time">${startStr}-${endStr}</span>`:""}
                    </div>
                  `;
                })}
              </div>
            </div>
          `;
        })}
      </div>
    `;
  }}pt.styles=((t,...e)=>{const i=1===t.length?t[0]:e.reduce((e,s,i)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+t[i+1],t[0]);return new o(i,t,s)})`
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

    .status-price {
      font-size: 11px;
      font-weight: 500;
      opacity: 0.85;
      margin-top: 4px;
      padding-top: 4px;
      border-top: 1px solid rgba(255,255,255,0.3);
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
      background: var(--secondary-background-color, rgba(0,0,0,0.05));
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
      background: var(--low-tariff-color, #4CAF50);
    }

    .legend-item.vt .legend-color {
      background: var(--high-tariff-color, #FF5722);
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
      background: var(--low-tariff-color, #4CAF50);
    }

    .schedule-block.vt {
      background: var(--high-tariff-color, #FF5722);
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
  `,dt([ct({attribute:!1})],pt.prototype,"hass",void 0),dt([ct({state:!0,attribute:!1})],pt.prototype,"config",void 0),customElements.get("cez-hdo-card")||customElements.define("cez-hdo-card",pt),window.customCards=window.customCards||[],window.customCards.push({type:"cez-hdo-card",name:"ČEZ HDO Card",description:"Custom card for ČEZ HDO integration",preview:!0}),console.info("ČEZ HDO Card v2.1.0 loaded successfully")})();

// --- Runtime patch: editor + entity konfigurace v UI (Lovelace) ---
// Soubor je buildnutý/minifikovaný; patch děláme bezpečně až po registraci custom elementu.
(function(){
  // Výchozí entity podle aktuálních názvů integrace (CZ).
  const DEFAULT_ENTITY_CANDIDATES={
    low_tariff:[
      "binary_sensor.cez_hdo_nizky_tarif_aktivni"
    ],
    high_tariff:[
      "binary_sensor.cez_hdo_vysoky_tarif_aktivni"
    ],
    low_start:[
      "sensor.cez_hdo_nizky_tarif_zacatek"
    ],
    low_end:[
      "sensor.cez_hdo_nizky_tarif_konec"
    ],
    low_duration:[
      "sensor.cez_hdo_nizky_tarif_zbyva"
    ],
    high_start:[
      "sensor.cez_hdo_vysoky_tarif_zacatek"
    ],
    high_end:[
      "sensor.cez_hdo_vysoky_tarif_konec"
    ],
    high_duration:[
      "sensor.cez_hdo_vysoky_tarif_zbyva"
    ],
    schedule:[
      "sensor.cez_hdo_rozvrh"
    ]
  };

  const DEFAULT_ENTITIES={
    low_tariff:DEFAULT_ENTITY_CANDIDATES.low_tariff[0],
    high_tariff:DEFAULT_ENTITY_CANDIDATES.high_tariff[0],
    low_start:DEFAULT_ENTITY_CANDIDATES.low_start[0],
    low_end:DEFAULT_ENTITY_CANDIDATES.low_end[0],
    low_duration:DEFAULT_ENTITY_CANDIDATES.low_duration[0],
    high_start:DEFAULT_ENTITY_CANDIDATES.high_start[0],
    high_end:DEFAULT_ENTITY_CANDIDATES.high_end[0],
    high_duration:DEFAULT_ENTITY_CANDIDATES.high_duration[0],
    schedule:DEFAULT_ENTITY_CANDIDATES.schedule[0]
  };

  function resolveEntityIdSuffix(hass,entityId){
    const states=hass.states||{};
    if(states[entityId]) return entityId;
    const parts=String(entityId).split(".");
    if(parts.length!==2) return entityId;
    const domain=parts[0];
    const objectId=parts[1];
    const prefix=`${domain}.${objectId}_`;
    let best=null;
    let bestNum=Number.POSITIVE_INFINITY;
    for(const id of Object.keys(states)){
      if(!id.startsWith(prefix)) continue;
      const suffix=id.slice(prefix.length);
      const num=parseInt(suffix,10);
      if(Number.isFinite(num)&&num<bestNum){
        bestNum=num;
        best=id;
      }
    }
    return best||entityId;
  }

  function resolveEntityId(hass,entityId){
    if(!hass||!entityId) return entityId;
    const states=hass.states||{};

    // 1) Přesná shoda
    if(states[entityId]) return entityId;

    // 2) Sufix pro původní
    const resolvedSelf=resolveEntityIdSuffix(hass,entityId);
    return resolvedSelf;
  }

  function resolveDefaultForKey(hass,key){
    if(!hass) return DEFAULT_ENTITIES[key];
    const candidates=DEFAULT_ENTITY_CANDIDATES[key]||[DEFAULT_ENTITIES[key]];
    for(const cand of candidates){
      const resolved=resolveEntityIdSuffix(hass,cand);
      if(hass.states&&hass.states[resolved]) return resolved;
    }
    return resolveEntityId(hass,DEFAULT_ENTITIES[key]);
  }

  function ensureEditorDefined(){
    if(customElements.get("cez-hdo-card-editor")) return;

    class CezHdoCardEditor extends HTMLElement{
      constructor(){
        super();
        this.attachShadow({mode:"open"});
        this._config={};
        this._datalistIds={};
      }
      set hass(hass){
        this._hass=hass;
      }
      setConfig(config){
        this._config=config||{};
        this._render();
      }
      _emitConfigChanged(){
        this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:this._config},bubbles:true,composed:true}));
      }
      _setPriceOption(key,value){
        // Pro cenová pole: pouze uloží hodnotu, neemituje změnu (ta se emituje při blur)
        this._config={...this._config,[key]:value};
      }
      _emitPriceChange(key,value){
        // Emituje změnu ceny - volá se při opuštění pole (blur/change)
        this._config={...this._config,[key]:value};
        this._emitConfigChanged();
      }
      _setOption(key,value,skipRender=false){
        this._config={...this._config,[key]:value};
        this._emitConfigChanged();
        // Při změně cenových polí nepřekresluj (zachovej focus)
        if(!skipRender){
          this._render();
        }
      }
      _setEntity(key,value){
        const entities={...(this._config.entities||{})};
        if(!value) delete entities[key];
        else entities[key]=value;
        this._config={...this._config,entities};
        this._emitConfigChanged();
        this._render();
      }
      _entityPicker(label,key,domains){
        const current=(this._config.entities&&this._config.entities[key])||"";
        const wrap=document.createElement("div");
        wrap.className="entity-row";

        const activateOnce=(()=>{
          let activated=false;
          return (el,input)=>{
            if(activated) return;
            activated=true;
            el.style.display="";
            input.style.display="none";
          };
        })();

        // 1) Vždy-funkční našeptávač přes <datalist> (bez závislosti na HA komponentách)
        if(!this._datalistIds[key]){
          this._datalistIds[key]=`cez-hdo-entities-${key}-${Math.random().toString(16).slice(2)}`;
        }
        const listId=this._datalistIds[key];

        const input=document.createElement("input");
        input.className="entity-input";
        input.type="text";
        input.value=current;
        input.placeholder=label;
        input.setAttribute("list",listId);
        input.addEventListener("input",(ev)=>this._setEntity(key,(ev.target.value||"").trim()));

        const datalist=document.createElement("datalist");
        datalist.id=listId;
        const wanted=new Set(domains||[]);
        const states=this._hass?.states||{};
        for(const entityId of Object.keys(states)){
          const domain=entityId.split(".")[0];
          if(wanted.size && !wanted.has(domain)) continue;
          const opt=document.createElement("option");
          opt.value=entityId;
          const friendly=states[entityId]?.attributes?.friendly_name;
          if(friendly) opt.label=friendly;
          datalist.appendChild(opt);
        }

        wrap.appendChild(input);
        wrap.appendChild(datalist);

        // Pokud je pole prázdné, ukaž jakou výchozí entitu karta použije (včetně _2/_3).
        if(!current){
          const resolved=resolveDefaultForKey(this._hass,key);
          const note=document.createElement("div");
          note.className="hint";
          if(resolved){
            const exists=!!(this._hass?.states&&this._hass.states[resolved]);
            note.textContent=exists?`Použito: ${resolved}`:`Výchozí: ${resolved} (nenalezeno)`;
          }
          wrap.appendChild(note);
        }

        customElements.whenDefined("ha-selector").then(()=>{
          const selector=document.createElement("ha-selector");
          selector.style.display="none";
          selector.hass=this._hass;
          selector.label=label;
          selector.selector={entity:(domains&&domains.length)?{domain:domains}:{}};
          selector.value=(this._config.entities&&this._config.entities[key])||"";
          selector.addEventListener("value-changed",(ev)=>this._setEntity(key,ev.detail.value));
          wrap.appendChild(selector);
          activateOnce(selector,input);
        }).catch(()=>{});

        return wrap;
      }
      _render(){
        if(!this.shadowRoot||!this._hass){
          if(this.shadowRoot) this.shadowRoot.innerHTML="";
          return;
        }

        const title=this._config.title??"";
        const show_times=this._config.show_times!==false;
        const show_duration=this._config.show_duration!==false;
        const compact_mode=this._config.compact_mode===true;

        this.shadowRoot.innerHTML=`
          <style>
            .wrap{display:flex;flex-direction:column;gap:12px;padding:4px 0;}
            .entity-row{display:flex;flex-direction:column;gap:6px;}
            .entity-row ha-selector{display:block;}
            .entity-input{padding:10px 12px;border-radius:8px;border:1px solid var(--divider-color);background:var(--card-background-color, var(--ha-card-background));color:var(--primary-text-color);}
            .entity-input:focus{outline:none;border-color:var(--primary-color);}
            .hint{font-size:12px;opacity:.8;}
          </style>
          <div class="wrap"></div>
        `;

        const wrap=this.shadowRoot.querySelector(".wrap");
        const titleField=document.createElement("ha-textfield");
        titleField.label="Titulek";
        titleField.value=title;
        titleField.addEventListener("input",(ev)=>this._setOption("title",ev.target.value));
        wrap.appendChild(titleField);

        const mkToggle=(label,key,checked)=>{
          const form=document.createElement("ha-formfield");
          form.label=label;
          const sw=document.createElement("ha-switch");
          sw.checked=checked;
          sw.addEventListener("change",()=>this._setOption(key,sw.checked));
          form.appendChild(sw);
          return form;
        };
        wrap.appendChild(mkToggle("Zobrazit časy (začátek/konec)","show_times",show_times));
        wrap.appendChild(mkToggle("Zobrazit zbývající čas","show_duration",show_duration));
        wrap.appendChild(mkToggle("Zobrazit aktuální cenu","show_price",this._config.show_price!==false));
        wrap.appendChild(mkToggle("Zobrazit ceny u tarifů","show_tariff_prices",this._config.show_tariff_prices===true));
        wrap.appendChild(mkToggle("Zobrazit HDO rozvrh","show_schedule",this._config.show_schedule===true));
        wrap.appendChild(mkToggle("Kompaktní režim","compact_mode",compact_mode));

        // Cenová pole - input pouze lokálně ukládá, change/blur emituje změnu
        const lowPriceField=document.createElement("ha-textfield");
        lowPriceField.label="Cena NT (Kč/kWh)";
        lowPriceField.type="number";
        lowPriceField.step="0.01";
        lowPriceField.value=this._config.low_tariff_price||"";
        lowPriceField.addEventListener("input",(ev)=>this._setPriceOption("low_tariff_price",parseFloat(ev.target.value)||0));
        lowPriceField.addEventListener("change",(ev)=>this._emitPriceChange("low_tariff_price",parseFloat(ev.target.value)||0));
        wrap.appendChild(lowPriceField);

        const highPriceField=document.createElement("ha-textfield");
        highPriceField.label="Cena VT (Kč/kWh)";
        highPriceField.type="number";
        highPriceField.step="0.01";
        highPriceField.value=this._config.high_tariff_price||"";
        highPriceField.addEventListener("input",(ev)=>this._setPriceOption("high_tariff_price",parseFloat(ev.target.value)||0));
        highPriceField.addEventListener("change",(ev)=>this._emitPriceChange("high_tariff_price",parseFloat(ev.target.value)||0));
        wrap.appendChild(highPriceField);

        wrap.appendChild(this._entityPicker("NT aktivní (binary_sensor)","low_tariff",["binary_sensor"]));
        wrap.appendChild(this._entityPicker("VT aktivní (binary_sensor)","high_tariff",["binary_sensor"]));
        wrap.appendChild(this._entityPicker("NT začátek (sensor)","low_start",["sensor"]));
        wrap.appendChild(this._entityPicker("NT konec (sensor)","low_end",["sensor"]));
        wrap.appendChild(this._entityPicker("NT zbývá (sensor)","low_duration",["sensor"]));
        wrap.appendChild(this._entityPicker("VT začátek (sensor)","high_start",["sensor"]));
        wrap.appendChild(this._entityPicker("VT konec (sensor)","high_end",["sensor"]));
        wrap.appendChild(this._entityPicker("VT zbývá (sensor)","high_duration",["sensor"]));
        wrap.appendChild(this._entityPicker("HDO rozvrh (sensor)","schedule",["sensor"]));

        const hint=document.createElement("div");
        hint.className="hint";
        hint.textContent="Tip: Když necháš nějaké pole prázdné, karta použije výchozí entity (pokud existují).";
        wrap.appendChild(hint);
      }
    }

    customElements.define("cez-hdo-card-editor",CezHdoCardEditor);
  }

  customElements.whenDefined("cez-hdo-card").then(()=>{
    const patchCard=()=>{
      ensureEditorDefined();
      const Card=customElements.get("cez-hdo-card");
      if(!Card||Card.__cezHdoPatched) return;
      Card.__cezHdoPatched=true;

      // UI editor pro Lovelace
      Card.getConfigElement=()=>document.createElement("cez-hdo-card-editor");
      // Při první instalaci rovnou předvyplň defaulty (uživatel může smazat → použijí se defaulty znovu).
      Card.getStubConfig=()=>({
        type:"custom:cez-hdo-card",
        title:"ČEZ HDO Status",
        show_times:true,
        show_duration:true,
        compact_mode:false,
        entities:{...DEFAULT_ENTITIES}
      });

      // Normalizace konfigurace: mapování starých klíčů nt_/vt_ + doplnění defaultů
      const originalSetConfig=Card.prototype.setConfig;
      const originalGetEntityState=Card.prototype.getEntityState;

      Card.prototype.getEntityState=function(entityId){
        const resolved=resolveEntityId(this.hass,entityId);
        return originalGetEntityState.call(this,resolved);
      };

      // Uložíme předchozí ceny pro detekci změn
      Card.prototype._prevLowPrice=undefined;
      Card.prototype._prevHighPrice=undefined;

      Card.prototype.setConfig=function(config){
        const cfg=config||{};
        const ent=(cfg.entities||{});
        const mapped={
          low_tariff:ent.low_tariff||ent.nt_binary||ent.nt_active||ent.low_tariff_active,
          high_tariff:ent.high_tariff||ent.vt_binary||ent.vt_active||ent.high_tariff_active,
          low_start:ent.low_start||ent.nt_start,
          low_end:ent.low_end||ent.nt_end,
          low_duration:ent.low_duration||ent.nt_remaining,
          high_start:ent.high_start||ent.vt_start,
          high_end:ent.high_end||ent.vt_end,
          high_duration:ent.high_duration||ent.vt_remaining
        };
        const entities={...DEFAULT_ENTITIES};
        for(const k of Object.keys(mapped)) if(mapped[k]) entities[k]=mapped[k];
        const normalized={
          title:"ČEZ HDO Status",
          show_times:true,
          show_duration:true,
          compact_mode:false,
          ...cfg,
          entities
        };

        // Zkontroluj, zda se ceny změnily
        const newLow=normalized.low_tariff_price||0;
        const newHigh=normalized.high_tariff_price||0;
        const pricesChanged=(this._prevLowPrice!==newLow||this._prevHighPrice!==newHigh);

        // Uložíme aktuální ceny pro příští porovnání
        this._prevLowPrice=newLow;
        this._prevHighPrice=newHigh;

        const result=originalSetConfig.call(this,normalized);

        // Synchronizuj ceny se senzorem pouze pokud se změnily a máme hass
        if(pricesChanged&&(newLow>0||newHigh>0)){
          // Počkáme na hass pokud není k dispozici
          const syncPrices=()=>{
            if(!this.hass){
              setTimeout(syncPrices,100);
              return;
            }
            console.log("CezHdoCard: Calling set_prices with NT="+newLow+", VT="+newHigh);
            this.hass.callService("cez_hdo","set_prices",{
              low_tariff_price:newLow,
              high_tariff_price:newHigh
            }).then(()=>console.log("CezHdoCard: set_prices called successfully")).catch(err=>console.warn("CezHdoCard: Failed to sync prices:",err));
          };
          syncPrices();
        }
        return result;
      };
    };

    // Patchni okamžitě, ať stihneme i první setConfig při přidání karty.
    patchCard();
    customElements.whenDefined("cez-hdo-card").then(patchCard);
  });
})();

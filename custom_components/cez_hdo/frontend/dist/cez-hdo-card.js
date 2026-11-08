function t(t,e,s,i){var a,n=arguments.length,r=n<3?e:null===i?i=Object.getOwnPropertyDescriptor(e,s):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)r=Reflect.decorate(t,e,s,i);else for(var o=t.length-1;o>=0;o--)(a=t[o])&&(r=(n<3?a(r):n>3?a(e,s,r):a(e,s))||r);return n>3&&r&&Object.defineProperty(e,s,r),r}"function"==typeof SuppressedError&&SuppressedError;const e=globalThis,s=e.ShadowRoot&&(void 0===e.ShadyCSS||e.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),a=new WeakMap;let n=class{constructor(t,e,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(s&&void 0===t){const s=void 0!==e&&1===e.length;s&&(t=a.get(e)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),s&&a.set(e,t))}return t}toString(){return this.cssText}};const r=(t,...e)=>{const s=1===t.length?t[0]:e.reduce((e,s,i)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+t[i+1],t[0]);return new n(s,t,i)},o=s?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const s of t.cssRules)e+=s.cssText;return(t=>new n("string"==typeof t?t:t+"",void 0,i))(e)})(t):t,{is:h,defineProperty:c,getOwnPropertyDescriptor:l,getOwnPropertyNames:d,getOwnPropertySymbols:p,getPrototypeOf:u}=Object,f=globalThis,g=f.trustedTypes,_=g?g.emptyScript:"",m=f.reactiveElementPolyfillSupport,v=(t,e)=>t,y={toAttribute(t,e){switch(e){case Boolean:t=t?_:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let s=t;switch(e){case Boolean:s=null!==t;break;case Number:s=null===t?null:Number(t);break;case Object:case Array:try{s=JSON.parse(t)}catch(t){s=null}}return s}},b=(t,e)=>!h(t,e),$={attribute:!0,type:String,converter:y,reflect:!1,useDefault:!1,hasChanged:b};Symbol.metadata??=Symbol("metadata"),f.litPropertyMetadata??=new WeakMap;let w=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=$){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const s=Symbol(),i=this.getPropertyDescriptor(t,s,e);void 0!==i&&c(this.prototype,t,i)}}static getPropertyDescriptor(t,e,s){const{get:i,set:a}=l(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:i,set(e){const n=i?.call(this);a?.call(this,e),this.requestUpdate(t,n,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??$}static _$Ei(){if(this.hasOwnProperty(v("elementProperties")))return;const t=u(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(v("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(v("properties"))){const t=this.properties,e=[...d(t),...p(t)];for(const s of e)this.createProperty(s,t[s])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,s]of e)this.elementProperties.set(t,s)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const s=this._$Eu(t,e);void 0!==s&&this._$Eh.set(s,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const s=new Set(t.flat(1/0).reverse());for(const t of s)e.unshift(o(t))}else void 0!==t&&e.push(o(t));return e}static _$Eu(t,e){const s=e.attribute;return!1===s?void 0:"string"==typeof s?s:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const s of e.keys())this.hasOwnProperty(s)&&(t.set(s,this[s]),delete this[s]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((t,i)=>{if(s)t.adoptedStyleSheets=i.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const s of i){const i=document.createElement("style"),a=e.litNonce;void 0!==a&&i.setAttribute("nonce",a),i.textContent=s.cssText,t.appendChild(i)}})(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,s){this._$AK(t,s)}_$ET(t,e){const s=this.constructor.elementProperties.get(t),i=this.constructor._$Eu(t,s);if(void 0!==i&&!0===s.reflect){const a=(void 0!==s.converter?.toAttribute?s.converter:y).toAttribute(e,s.type);this._$Em=t,null==a?this.removeAttribute(i):this.setAttribute(i,a),this._$Em=null}}_$AK(t,e){const s=this.constructor,i=s._$Eh.get(t);if(void 0!==i&&this._$Em!==i){const t=s.getPropertyOptions(i),a="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:y;this._$Em=i;const n=a.fromAttribute(e,t.type);this[i]=n??this._$Ej?.get(i)??n,this._$Em=null}}requestUpdate(t,e,s,i=!1,a){if(void 0!==t){const n=this.constructor;if(!1===i&&(a=this[t]),s??=n.getPropertyOptions(t),!((s.hasChanged??b)(a,e)||s.useDefault&&s.reflect&&a===this._$Ej?.get(t)&&!this.hasAttribute(n._$Eu(t,s))))return;this.C(t,e,s)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:s,reflect:i,wrapped:a},n){s&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,n??e??this[t]),!0!==a||void 0!==n)||(this._$AL.has(t)||(this.hasUpdated||s||(e=void 0),this._$AL.set(t,e)),!0===i&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,s]of t){const{wrapped:t}=s,i=this[e];!0!==t||this._$AL.has(e)||void 0===i||this.C(e,void 0,s,i)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};w.elementStyles=[],w.shadowRootOptions={mode:"open"},w[v("elementProperties")]=new Map,w[v("finalized")]=new Map,m?.({ReactiveElement:w}),(f.reactiveElementVersions??=[]).push("2.1.2");const S=globalThis,x=t=>t,E=S.trustedTypes,A=E?E.createPolicy("lit-html",{createHTML:t=>t}):void 0,C="$lit$",R=`lit$${Math.random().toFixed(9).slice(2)}$`,k="?"+R,z=`<${k}>`,T=document,P=()=>T.createComment(""),H=t=>null===t||"object"!=typeof t&&"function"!=typeof t,O=Array.isArray,N="[ \t\n\f\r]",M=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,U=/-->/g,D=/>/g,Z=RegExp(`>|${N}(?:([^\\s"'>=/]+)(${N}*=${N}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),L=/'/g,j=/"/g,I=/^(?:script|style|textarea|title)$/i,B=(t=>(e,...s)=>({_$litType$:t,strings:e,values:s}))(1),V=Symbol.for("lit-noChange"),K=Symbol.for("lit-nothing"),W=new WeakMap,q=T.createTreeWalker(T,129);function F(t,e){if(!O(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==A?A.createHTML(e):e}const J=(t,e)=>{const s=t.length-1,i=[];let a,n=2===e?"<svg>":3===e?"<math>":"",r=M;for(let e=0;e<s;e++){const s=t[e];let o,h,c=-1,l=0;for(;l<s.length&&(r.lastIndex=l,h=r.exec(s),null!==h);)l=r.lastIndex,r===M?"!--"===h[1]?r=U:void 0!==h[1]?r=D:void 0!==h[2]?(I.test(h[2])&&(a=RegExp("</"+h[2],"g")),r=Z):void 0!==h[3]&&(r=Z):r===Z?">"===h[0]?(r=a??M,c=-1):void 0===h[1]?c=-2:(c=r.lastIndex-h[2].length,o=h[1],r=void 0===h[3]?Z:'"'===h[3]?j:L):r===j||r===L?r=Z:r===U||r===D?r=M:(r=Z,a=void 0);const d=r===Z&&t[e+1].startsWith("/>")?" ":"";n+=r===M?s+z:c>=0?(i.push(o),s.slice(0,c)+C+s.slice(c)+R+d):s+R+(-2===c?e:d)}return[F(t,n+(t[s]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),i]};class Y{constructor({strings:t,_$litType$:e},s){let i;this.parts=[];let a=0,n=0;const r=t.length-1,o=this.parts,[h,c]=J(t,e);if(this.el=Y.createElement(h,s),q.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(i=q.nextNode())&&o.length<r;){if(1===i.nodeType){if(i.hasAttributes())for(const t of i.getAttributeNames())if(t.endsWith(C)){const e=c[n++],s=i.getAttribute(t).split(R),r=/([.?@])?(.*)/.exec(e);o.push({type:1,index:a,name:r[2],strings:s,ctor:"."===r[1]?et:"?"===r[1]?st:"@"===r[1]?it:tt}),i.removeAttribute(t)}else t.startsWith(R)&&(o.push({type:6,index:a}),i.removeAttribute(t));if(I.test(i.tagName)){const t=i.textContent.split(R),e=t.length-1;if(e>0){i.textContent=E?E.emptyScript:"";for(let s=0;s<e;s++)i.append(t[s],P()),q.nextNode(),o.push({type:2,index:++a});i.append(t[e],P())}}}else if(8===i.nodeType)if(i.data===k)o.push({type:2,index:a});else{let t=-1;for(;-1!==(t=i.data.indexOf(R,t+1));)o.push({type:7,index:a}),t+=R.length-1}a++}}static createElement(t,e){const s=T.createElement("template");return s.innerHTML=t,s}}function G(t,e,s=t,i){if(e===V)return e;let a=void 0!==i?s._$Co?.[i]:s._$Cl;const n=H(e)?void 0:e._$litDirective$;return a?.constructor!==n&&(a?._$AO?.(!1),void 0===n?a=void 0:(a=new n(t),a._$AT(t,s,i)),void 0!==i?(s._$Co??=[])[i]=a:s._$Cl=a),void 0!==a&&(e=G(t,a._$AS(t,e.values),a,i)),e}class Q{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:s}=this._$AD,i=(t?.creationScope??T).importNode(e,!0);q.currentNode=i;let a=q.nextNode(),n=0,r=0,o=s[0];for(;void 0!==o;){if(n===o.index){let e;2===o.type?e=new X(a,a.nextSibling,this,t):1===o.type?e=new o.ctor(a,o.name,o.strings,this,t):6===o.type&&(e=new at(a,this,t)),this._$AV.push(e),o=s[++r]}n!==o?.index&&(a=q.nextNode(),n++)}return q.currentNode=T,i}p(t){let e=0;for(const s of this._$AV)void 0!==s&&(void 0!==s.strings?(s._$AI(t,s,e),e+=s.strings.length-2):s._$AI(t[e])),e++}}class X{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,s,i){this.type=2,this._$AH=K,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=s,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=G(this,t,e),H(t)?t===K||null==t||""===t?(this._$AH!==K&&this._$AR(),this._$AH=K):t!==this._$AH&&t!==V&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>O(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==K&&H(this._$AH)?this._$AA.nextSibling.data=t:this.T(T.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:s}=t,i="number"==typeof s?this._$AC(t):(void 0===s.el&&(s.el=Y.createElement(F(s.h,s.h[0]),this.options)),s);if(this._$AH?._$AD===i)this._$AH.p(e);else{const t=new Q(i,this),s=t.u(this.options);t.p(e),this.T(s),this._$AH=t}}_$AC(t){let e=W.get(t.strings);return void 0===e&&W.set(t.strings,e=new Y(t)),e}k(t){O(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let s,i=0;for(const a of t)i===e.length?e.push(s=new X(this.O(P()),this.O(P()),this,this.options)):s=e[i],s._$AI(a),i++;i<e.length&&(this._$AR(s&&s._$AB.nextSibling,i),e.length=i)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=x(t).nextSibling;x(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class tt{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,s,i,a){this.type=1,this._$AH=K,this._$AN=void 0,this.element=t,this.name=e,this._$AM=i,this.options=a,s.length>2||""!==s[0]||""!==s[1]?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=K}_$AI(t,e=this,s,i){const a=this.strings;let n=!1;if(void 0===a)t=G(this,t,e,0),n=!H(t)||t!==this._$AH&&t!==V,n&&(this._$AH=t);else{const i=t;let r,o;for(t=a[0],r=0;r<a.length-1;r++)o=G(this,i[s+r],e,r),o===V&&(o=this._$AH[r]),n||=!H(o)||o!==this._$AH[r],o===K?t=K:t!==K&&(t+=(o??"")+a[r+1]),this._$AH[r]=o}n&&!i&&this.j(t)}j(t){t===K?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class et extends tt{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===K?void 0:t}}class st extends tt{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==K)}}class it extends tt{constructor(t,e,s,i,a){super(t,e,s,i,a),this.type=5}_$AI(t,e=this){if((t=G(this,t,e,0)??K)===V)return;const s=this._$AH,i=t===K&&s!==K||t.capture!==s.capture||t.once!==s.once||t.passive!==s.passive,a=t!==K&&(s===K||i);i&&this.element.removeEventListener(this.name,this,s),a&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class at{constructor(t,e,s){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=s}get _$AU(){return this._$AM._$AU}_$AI(t){G(this,t)}}const nt=S.litHtmlPolyfillSupport;nt?.(Y,X),(S.litHtmlVersions??=[]).push("3.3.3");const rt=globalThis;class ot extends w{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,s)=>{const i=s?.renderBefore??e;let a=i._$litPart$;if(void 0===a){const t=s?.renderBefore??null;i._$litPart$=a=new X(e.insertBefore(P(),t),t,void 0,s??{})}return a._$AI(t),a})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return V}}ot._$litElement$=!0,ot.finalized=!0,rt.litElementHydrateSupport?.({LitElement:ot});const ht=rt.litElementPolyfillSupport;ht?.({LitElement:ot}),(rt.litElementVersions??=[]).push("4.2.2");const ct={attribute:!0,type:String,converter:y,reflect:!1,hasChanged:b},lt=(t=ct,e,s)=>{const{kind:i,metadata:a}=s;let n=globalThis.litPropertyMetadata.get(a);if(void 0===n&&globalThis.litPropertyMetadata.set(a,n=new Map),"setter"===i&&((t=Object.create(t)).wrapped=!0),n.set(s.name,t),"accessor"===i){const{name:i}=s;return{set(s){const a=e.get.call(this);e.set.call(this,s),this.requestUpdate(i,a,t,!0,s)},init(e){return void 0!==e&&this.C(i,void 0,t,e),e}}}if("setter"===i){const{name:i}=s;return function(s){const a=this[i];e.call(this,s),this.requestUpdate(i,a,t,!0,s)}}throw Error("Unsupported decorator location: "+i)};function dt(t){return(e,s)=>"object"==typeof s?lt(t,e,s):((t,e,s)=>{const i=e.hasOwnProperty(s);return e.constructor.createProperty(s,t),i?Object.getOwnPropertyDescriptor(e,s):void 0})(t,e,s)}function pt(t){return dt({...t,state:!0,attribute:!1})}const ut={cs:{lowTariff:"Nízký tarif",highTariff:"Vysoký tarif",nt:"NT",vt:"VT",active:"Aktivní",inactive:"Neaktivní",currency:"Kč/kWh",currencyShort:"Kč",ntStart:"Začátek NT",vtStart:"Začátek VT",ntEnd:"Konec NT",vtEnd:"Konec VT",ntRemaining:"Zbývá NT",vtRemaining:"Zbývá VT",currentPrice:"Aktuální cena",hdoSchedule:"HDO rozvrh",scheduleNotAvailable:"Rozvrh není k dispozici",editorTitle:"Titulek",showTitle:"Zobrazit titulek",showTariffStatus:"Zobrazit stavy tarifů",showTariffPrices:"Zobrazit ceny u tarifů",showTimes:"Zobrazit časy (začátek/konec)",showDuration:"Zobrazit zbývající čas",showCurrentPrice:"Zobrazit aktuální cenu",showManualRefresh:"Zobrazit manuální obnovu",showHdoSchedule:"Zobrazit HDO rozvrh",showSchedulePrices:"Zobrazit ceny v legendě rozvrhu",compactMode:"Kompaktní režim",ntActiveBinarySensor:"NT aktivní (binary_sensor)",vtActiveBinarySensor:"VT aktivní (binary_sensor)",ntStartSensor:"NT začátek (sensor)",ntEndSensor:"NT konec (sensor)",ntRemainingSensor:"NT zbývající čas (sensor)",vtStartSensor:"VT začátek (sensor)",vtEndSensor:"VT konec (sensor)",vtRemainingSensor:"VT zbývající čas (sensor)",hdoScheduleSensor:"HDO rozvrh (sensor)",editorHint:"Nakonfigurujte entity v nastavení karty",manualRefresh:"Manuálně obnovit",loadingCaptcha:"Načítám CAPTCHA…",captchaCode:"Opište kód z obrázku",signalLabel:"HDO signál",loadSignals:"Načíst signály",refreshNow:"Obnovit data",newCaptcha:"Nový obrázek",cancel:"Zavřít",refreshSuccess:"Data byla úspěšně obnovena.",manualRefreshUnavailable:"Vyberte senzor rozvrhu pro tuto instanci ČEZ HDO.",lastUpdated:"Data aktualizována",lastUpdatedUnknown:"neznámý čas"},en:{lowTariff:"Low tariff",highTariff:"High tariff",nt:"LT",vt:"HT",active:"Active",inactive:"Inactive",currency:"CZK/kWh",currencyShort:"CZK",ntStart:"Low tariff starts",vtStart:"High tariff starts",ntEnd:"Low tariff ends",vtEnd:"High tariff ends",ntRemaining:"Low tariff remaining",vtRemaining:"High tariff remaining",currentPrice:"Current price",hdoSchedule:"HDO schedule",scheduleNotAvailable:"Schedule is not available",editorTitle:"Title",showTitle:"Show title",showTariffStatus:"Show tariff status",showTariffPrices:"Show tariff prices",showTimes:"Show times (start/end)",showDuration:"Show remaining time",showCurrentPrice:"Show current price",showManualRefresh:"Show manual refresh",showHdoSchedule:"Show HDO schedule",showSchedulePrices:"Show prices in schedule legend",compactMode:"Compact mode",ntActiveBinarySensor:"Low tariff active (binary_sensor)",vtActiveBinarySensor:"High tariff active (binary_sensor)",ntStartSensor:"Low tariff start (sensor)",ntEndSensor:"Low tariff end (sensor)",ntRemainingSensor:"Low tariff remaining (sensor)",vtStartSensor:"High tariff start (sensor)",vtEndSensor:"High tariff end (sensor)",vtRemainingSensor:"High tariff remaining (sensor)",hdoScheduleSensor:"HDO schedule (sensor)",editorHint:"Configure entities in card settings",manualRefresh:"Refresh manually",loadingCaptcha:"Loading CAPTCHA…",captchaCode:"Enter the code from the image",signalLabel:"HDO signal",loadSignals:"Load signals",refreshNow:"Refresh data",newCaptcha:"New image",cancel:"Close",refreshSuccess:"Data refreshed successfully.",manualRefreshUnavailable:"Select the schedule sensor for this ČEZ HDO instance.",lastUpdated:"Data updated",lastUpdatedUnknown:"unknown time"},sk:{lowTariff:"Nízka tarifa",highTariff:"Vysoká tarifa",nt:"NT",vt:"VT",active:"Aktívna",inactive:"Neaktívna",currency:"Kč/kWh",currencyShort:"Kč",ntStart:"Začiatok NT",vtStart:"Začiatok VT",ntEnd:"Koniec NT",vtEnd:"Koniec VT",ntRemaining:"Zostáva NT",vtRemaining:"Zostáva VT",currentPrice:"Aktuálna cena",hdoSchedule:"HDO rozvrh",scheduleNotAvailable:"Rozvrh nie je k dispozícii",editorTitle:"Nadpis",showTitle:"Zobraziť nadpis",showTariffStatus:"Zobraziť stavy taríf",showTariffPrices:"Zobraziť ceny taríf",showTimes:"Zobraziť časy (začiatok/koniec)",showDuration:"Zobraziť zostávajúci čas",showCurrentPrice:"Zobraziť aktuálnu cenu",showManualRefresh:"Zobraziť manuálne obnovenie",showHdoSchedule:"Zobraziť HDO rozvrh",showSchedulePrices:"Zobraziť ceny v legende rozvrhu",compactMode:"Kompaktný režim",ntActiveBinarySensor:"NT aktívna (binary_sensor)",vtActiveBinarySensor:"VT aktívna (binary_sensor)",ntStartSensor:"Začiatok NT (sensor)",ntEndSensor:"Koniec NT (sensor)",ntRemainingSensor:"Zostávajúci čas NT (sensor)",vtStartSensor:"Začiatok VT (sensor)",vtEndSensor:"Koniec VT (sensor)",vtRemainingSensor:"Zostávajúci čas VT (sensor)",hdoScheduleSensor:"HDO rozvrh (sensor)",editorHint:"Nakonfigurujte entity v nastavení karty",manualRefresh:"Manuálne obnoviť",loadingCaptcha:"Načítavam CAPTCHA…",captchaCode:"Prepíšte kód z obrázka",signalLabel:"HDO signál",loadSignals:"Načítať signály",refreshNow:"Obnoviť údaje",newCaptcha:"Nový obrázok",cancel:"Zavrieť",refreshSuccess:"Údaje boli úspešne obnovené.",manualRefreshUnavailable:"Vyberte senzor rozvrhu pre túto inštanciu ČEZ HDO.",lastUpdated:"Údaje aktualizované",lastUpdatedUnknown:"neznámy čas"}};function ft(t){return(t.locale?.language||t.language||"en").toLowerCase().split(/[-_]/)[0]}function gt(t){return ut[t]||ut.en}const _t={low_tariff:{domain:"binary_sensor",prefix:"cez_hdo_lowtariffactive_"},high_tariff:{domain:"binary_sensor",prefix:"cez_hdo_hightariffactive_"},low_start:{domain:"sensor",prefix:"cez_hdo_lowtariffstart_"},low_end:{domain:"sensor",prefix:"cez_hdo_lowtariffend_"},low_duration:{domain:"sensor",prefix:"cez_hdo_lowtariffduration_"},high_start:{domain:"sensor",prefix:"cez_hdo_hightariffstart_"},high_end:{domain:"sensor",prefix:"cez_hdo_hightariffend_"},high_duration:{domain:"sensor",prefix:"cez_hdo_hightariffduration_"},schedule:{domain:"sensor",prefix:"cez_hdo_schedule_"}},mt={low_tariff:"",high_tariff:"",low_start:"",low_end:"",low_duration:"",high_start:"",high_end:"",high_duration:"",schedule:""};let vt=class extends ot{constructor(){super(...arguments),this._manualRefreshOpen=!1,this._manualRefreshBusy=!1,this._manualRefreshMessage="",this._captchaId="",this._captchaImage="",this._captchaCode="",this._availableSignals=[],this._selectedSignal="",this._manualRefreshStep="captcha",this._manualRefreshSucceeded=!1,this._manualRefreshEntityId=""}static getConfigElement(){return document.createElement("cez-hdo-card-editor")}static getStubConfig(){return{type:"custom:cez-hdo-card",title:"ČEZ HDO Status",show_times:!0,show_duration:!0,compact_mode:!1,entities:{...mt}}}setConfig(t){t.entities||(t={entities:{},title:"ČEZ HDO Status",show_times:!0,show_duration:!0,compact_mode:!1,...t}),this.config=t}findAllEntitiesByPrefix(t){if(!this.hass?.states)return[];const e=_t[t];if(!e)return[];const s=`${e.domain}.${e.prefix}`;return Object.keys(this.hass.states).filter(t=>t.startsWith(s))}resolveEntity(t){const e=this.config.entities?.[t];if(e&&this.hass?.states[e])return e;const s=this.findAllEntitiesByPrefix(t);if(1===s.length)return s[0];const i=mt[t];return i&&this.hass?.states[i]?i:void 0}getEntityState(t){if(!t||!this.hass)return"unavailable";const e=this.hass.states[t];return e?e.state:"unavailable"}isEntityOn(t){return"on"===this.getEntityState(t)}getPricesFromSensor(){const t=this.resolveEntity("schedule"),e=t?this.hass?.states[t]:void 0;if(e?.attributes){const t=e.attributes.low_tariff_price,s=e.attributes.high_tariff_price;return{low:"number"==typeof t?t:0,high:"number"==typeof s?s:0}}return{low:0,high:0}}render(){if(!this.config||!this.hass)return B`<ha-card>Loading...</ha-card>`;const t=ft(this.hass),e=gt(t),s={low_tariff:this.resolveEntity("low_tariff"),high_tariff:this.resolveEntity("high_tariff"),low_start:this.resolveEntity("low_start"),low_end:this.resolveEntity("low_end"),low_duration:this.resolveEntity("low_duration"),high_start:this.resolveEntity("high_start"),high_end:this.resolveEntity("high_end"),high_duration:this.resolveEntity("high_duration"),schedule:this.resolveEntity("schedule")},i=this.isEntityOn(s.low_tariff),a=this.isEntityOn(s.high_tariff),n=this.getEntityState(s.low_start),r=this.getEntityState(s.low_end),o=this.getEntityState(s.low_duration),h=this.getEntityState(s.high_start),c=this.getEntityState(s.high_end),l=this.getEntityState(s.high_duration),d=this.config.title||"ČEZ HDO",p=!1!==this.config.show_times,u=!1!==this.config.show_duration,f=!0===this.config.compact_mode,g=!1!==this.config.show_manual_refresh,_=!1!==this.config.show_price,m=this.getPricesFromSensor(),v=m.low,y=m.high,b=i?v:y,$=!0===this.config.show_tariff_prices,w=!1!==this.config.show_title,S=!1!==this.config.show_tariff_status,x=s.schedule?this.hass.states[s.schedule]:void 0,E=x?.attributes.last_update,A=this._formatLastUpdated(E,t);return B`
      <ha-card class="${f?"compact":""}">
        ${w?B`<div class="card-header">${d}</div>`:""}
        ${S?B`
              <div class="status-container">
                <div
                  class="status-item ${i?"active low-tariff":"inactive"}"
                >
                  <div class="status-title">${e.lowTariff}</div>
                  <div class="status-value">
                    ${i?e.active:e.inactive}
                  </div>
                  ${$&&v>0?B`<div class="status-price">
                        ${v} ${e.currency}
                      </div>`:""}
                </div>
                <div
                  class="status-item ${a?"active high-tariff":"inactive"}"
                >
                  <div class="status-title">${e.highTariff}</div>
                  <div class="status-value">
                    ${a?e.active:e.inactive}
                  </div>
                  ${$&&y>0?B`<div class="status-price">
                        ${y} ${e.currency}
                      </div>`:""}
                </div>
              </div>
            `:""}
        ${p||u?B`
              <div class="details-container">
                ${p?B`
                      <div class="detail-item">
                        <span class="detail-label">${e.ntStart}</span>
                        <span class="detail-value">${n}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">${e.vtStart}</span>
                        <span class="detail-value">${h}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">${e.ntEnd}</span>
                        <span class="detail-value">${r}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">${e.vtEnd}</span>
                        <span class="detail-value">${c}</span>
                      </div>
                    `:""}
                ${u?B`
                      <div class="detail-item">
                        <span class="detail-label">${e.ntRemaining}</span>
                        <span class="detail-value">${o}</span>
                      </div>
                      <div class="detail-item">
                        <span class="detail-label">${e.vtRemaining}</span>
                        <span class="detail-value">${l}</span>
                      </div>
                    `:""}
              </div>
            `:""}
        ${_?B`
              <div class="price-container">
                <div class="price-item ${i?"active":""}">
                  <span class="price-label">${e.currentPrice}</span>
                  <span class="price-value">${b} ${e.currency}</span>
                  <span class="price-tariff"
                    >${i?e.lowTariff:e.highTariff}</span
                  >
                </div>
              </div>
            `:""}
        ${this._renderSchedule(e)}
        ${g?B`<div class="manual-refresh">
              <button
                class="manual-refresh-button"
                ?disabled=${!s.schedule||this._manualRefreshBusy}
                @click=${()=>this._openManualRefresh(s.schedule)}
              >
                <ha-icon icon="mdi:refresh"></ha-icon>
                ${e.manualRefresh}
              </button>
              <span class="manual-refresh-last-updated">
                ${e.lastUpdated}: ${A??e.lastUpdatedUnknown}
              </span>
              ${s.schedule?"":B`<div class="manual-refresh-message">
                    ${e.manualRefreshUnavailable}
                  </div>`}
            </div>`:""}
        ${this._manualRefreshOpen?B`
              <ha-dialog
                class="manual-refresh-dialog"
                .open=${this._manualRefreshOpen}
                .headerTitle=${e.manualRefresh}
                .width=${"medium"}
                @closed=${this._closeManualRefresh}
              >
                <form
                  id="manual-refresh-form"
                  class="manual-refresh-form"
                  @submit=${this._submitManualRefresh}
                >
                  ${"captcha"===this._manualRefreshStep&&this._captchaImage?B`<img
                        class="captcha-image"
                        src="data:image/png;base64,${this._captchaImage}"
                        alt="CAPTCHA"
                      />`:""}
                  ${"captcha"===this._manualRefreshStep&&this._manualRefreshBusy&&!this._captchaImage?B`<div class="manual-refresh-message">
                        ${e.loadingCaptcha}
                      </div>`:""}
                  ${this._manualRefreshMessage?B`<div class="manual-refresh-message">
                        ${this._manualRefreshMessage}
                      </div>`:""}
                  ${this._manualRefreshMessage||"captcha"!==this._manualRefreshStep?"":B`
                        <label class="captcha-label">
                          ${e.captchaCode}
                          <input
                            class="captcha-input"
                            type="text"
                            autocomplete="off"
                            maxlength="12"
                            .value=${this._captchaCode}
                            ?disabled=${this._manualRefreshBusy||!this._captchaImage||"captcha"!==this._manualRefreshStep}
                            @input=${t=>{this._captchaCode=t.target.value}}
                          />
                        </label>
                      `}
                  ${this._manualRefreshMessage||"signal"!==this._manualRefreshStep?"":B`
                        <label class="captcha-label">
                          ${e.signalLabel}
                          <ha-selector
                            .hass=${this.hass}
                            .selector=${{select:{options:this._availableSignals.map(t=>({label:t,value:t}))}}}
                            .value=${this._selectedSignal}
                            ?disabled=${this._manualRefreshBusy}
                            @value-changed=${t=>{this._selectedSignal=t.detail.value}}
                          ></ha-selector>
                        </label>
                      `}
                </form>
                <div slot="footer" class="manual-refresh-actions">
                  ${this._manualRefreshMessage&&!this._manualRefreshSucceeded?B`
                        <button
                          type="button"
                          class="manual-refresh-cancel"
                          @click=${()=>this._openManualRefresh(this._manualRefreshEntityId)}
                        >
                          ${e.newCaptcha}
                        </button>
                      `:""}
                  ${this._manualRefreshMessage?"":B`
                        <button
                          type="submit"
                          form="manual-refresh-form"
                          class="manual-refresh-button"
                          ?disabled=${this._manualRefreshBusy||("captcha"===this._manualRefreshStep?!this._captchaCode.trim():!this._selectedSignal)}
                        >
                          ${this._manualRefreshBusy?e.loadingCaptcha:"captcha"===this._manualRefreshStep?e.loadSignals:e.refreshNow}
                        </button>
                      `}
                  <button
                    type="button"
                    class="manual-refresh-cancel"
                    ?disabled=${this._manualRefreshBusy}
                    @click=${this._closeManualRefresh}
                  >
                    ${e.cancel}
                  </button>
                </div>
              </ha-dialog>
            `:""}
      </ha-card>
    `}async _openManualRefresh(t){if(t){this._manualRefreshEntityId=t,this._manualRefreshOpen=!0,this._manualRefreshBusy=!0,this._manualRefreshMessage="",this._captchaCode="",this._captchaImage="",this._availableSignals=[],this._selectedSignal="",this._manualRefreshStep="captcha",this._manualRefreshSucceeded=!1;try{const e=await this.hass.callWS({type:"cez_hdo/manual_refresh/captcha",entity_id:t});this._captchaId=e.captcha_id,this._captchaImage=e.image_base64}catch(t){this._manualRefreshMessage=this._getErrorMessage(t,"CAPTCHA se nepodařilo načíst")}finally{this._manualRefreshBusy=!1}}}_formatLastUpdated(t,e){if("string"!=typeof t)return;const s=new Date(t);if(Number.isNaN(s.getTime()))return;const i="cs"===e?"cs-CZ":"sk"===e?"sk-SK":"en-US";return s.toLocaleString(i,{dateStyle:"short",timeStyle:"short"})}async _submitManualRefresh(t){if(t.preventDefault(),this._captchaId&&this._manualRefreshEntityId&&("captcha"!==this._manualRefreshStep||this._captchaCode.trim())&&("signal"!==this._manualRefreshStep||this._selectedSignal)){this._manualRefreshBusy=!0,this._manualRefreshMessage="";try{if("captcha"===this._manualRefreshStep){const t=await this.hass.callWS({type:"cez_hdo/manual_refresh/submit",entity_id:this._manualRefreshEntityId,captcha_id:this._captchaId,captcha_code:this._captchaCode.trim()});this._availableSignals=t.available_signals,this._selectedSignal=t.configured_signal??t.available_signals[0]??"",this._captchaImage="",this._captchaCode="",this._manualRefreshStep="signal"}else await this.hass.callWS({type:"cez_hdo/manual_refresh/select_signal",entity_id:this._manualRefreshEntityId,captcha_id:this._captchaId,signal:this._selectedSignal}),this._captchaId="",this._captchaImage="",this._captchaCode="",this._availableSignals=[],this._selectedSignal="",this._manualRefreshMessage=gt(ft(this.hass)).refreshSuccess,this._manualRefreshSucceeded=!0}catch(t){this._manualRefreshMessage=this._getErrorMessage(t,"Obnovu se nepodařilo dokončit"),this._manualRefreshSucceeded=!1,"captcha"===this._manualRefreshStep&&(this._captchaId="",this._captchaImage="",this._captchaCode="")}finally{this._manualRefreshBusy=!1}}}_getErrorMessage(t,e){if(t instanceof Error&&t.message)return t.message;if("object"==typeof t&&null!==t&&"message"in t){const e=t.message;if("string"==typeof e&&e.trim())return e}return e}_closeManualRefresh(){this._manualRefreshOpen=!1,this._manualRefreshMessage="",this._captchaId="",this._captchaImage="",this._captchaCode="",this._manualRefreshSucceeded=!1}_renderSchedule(t){if(!this.config.show_schedule)return B``;const e=this.resolveEntity("schedule"),s=e?this.hass.states[e]:void 0;if(!s||!s.attributes.schedule)return B`<div class="schedule-error">${t.scheduleNotAvailable}</div>`;const i=s.attributes.schedule,a={},n=ft(this.hass),r="cs"===n?"cs-CZ":"sk"===n?"sk-SK":"en-US";i.forEach(t=>{const e=new Date(t.start),s=`${e.getFullYear()}-${String(e.getMonth()+1).padStart(2,"0")}-${String(e.getDate()).padStart(2,"0")}`,i=e.toLocaleDateString(r,{weekday:"short",day:"2-digit",month:"2-digit"});a[s]||(a[s]={label:i,items:[]}),a[s].items.push(t)});const o=Object.keys(a).sort(),h=this.getPricesFromSensor(),c=h.low,l=h.high,d=!0===this.config.show_schedule_prices&&(c>0||l>0);return B`
      <div class="schedule-container">
        <div class="schedule-header">
          <span class="schedule-title">${t.hdoSchedule}</span>
          <div class="schedule-legend">
            <span class="legend-item nt">
              <span class="legend-color"></span>${t.nt}${d?B` <span class="legend-price"
                    >${c} ${t.currencyShort}</span
                  >`:""}
            </span>
            <span class="legend-item vt">
              <span class="legend-color"></span>${t.vt}${d?B` <span class="legend-price"
                    >${l} ${t.currencyShort}</span
                  >`:""}
            </span>
          </div>
        </div>
        <div class="schedule-time-axis">
          <span>0:00</span><span>6:00</span><span>12:00</span><span>18:00</span
          ><span>24:00</span>
        </div>
        ${o.map(t=>{const e=a[t];return B`
            <div class="schedule-row">
              <div class="schedule-day-label">${e.label}</div>
              <div class="schedule-bar">
                ${e.items.map(t=>{const e=new Date(t.start),s=new Date(t.end),i=e.getHours()+e.getMinutes()/60;let a=s.getHours()+s.getMinutes()/60;0===a&&(a=24);const n=i/24*100,o=(a-i)/24*100,h=e.toLocaleTimeString(r,{hour:"2-digit",minute:"2-digit"}),c=s.toLocaleTimeString(r,{hour:"2-digit",minute:"2-digit"});return B`
                    <div
                      class="schedule-block ${t.tariff.toLowerCase()}"
                      style="left:${n}%;width:${o}%"
                      title="${h}-${c}"
                    >
                      ${o>8?B`<span class="block-time"
                            >${h}-${c}</span
                          >`:""}
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
        background: linear-gradient(
          135deg,
          var(--primary-color, #03a9f4) 0%,
          var(--accent-color, #00bcd4) 100%
        );
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

      .manual-refresh {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 16px;
      }

      .manual-refresh-button,
      .manual-refresh-cancel {
        min-height: 40px;
        padding: 0 14px;
        border: 0;
        border-radius: 6px;
        cursor: pointer;
        font: inherit;
      }

      .manual-refresh-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        min-height: 32px;
        padding: 0 10px;
        background: var(--primary-color);
        color: var(--text-primary-color, white);
        font-size: 13px;
      }

      .manual-refresh-button ha-icon {
        --mdc-icon-size: 16px;
      }

      .manual-refresh-last-updated {
        color: var(--secondary-text-color);
        font-size: 12px;
      }

      .manual-refresh-button:disabled,
      .manual-refresh-cancel:disabled {
        cursor: not-allowed;
        opacity: 0.6;
      }

      .manual-refresh-cancel {
        background: var(--secondary-background-color);
        color: var(--primary-text-color);
      }

      .manual-refresh-form {
        display: grid;
        gap: 12px;
        max-width: 420px;
        margin-top: 12px;
        padding: 12px;
        border: 1px solid var(--divider-color);
        border-radius: 6px;
      }

      .manual-refresh-dialog {
        width: min(420px, calc(100vw - 48px));
        max-height: calc(100vh - 48px);
        overflow: auto;
        padding: 0;
        border: 0;
        border-radius: 6px;
        background: var(--card-background-color);
        color: var(--primary-text-color);
        box-shadow: var(--ha-card-box-shadow, 0 8px 24px rgba(0, 0, 0, 0.24));
      }

      .manual-refresh-dialog::backdrop {
        background: rgba(0, 0, 0, 0.42);
      }

      .captcha-image {
        width: min(100%, 300px);
        height: auto;
        image-rendering: auto;
      }

      .captcha-label {
        display: grid;
        gap: 6px;
        color: var(--primary-text-color);
        font-size: 14px;
      }

      .captcha-input {
        min-height: 40px;
        padding: 0 10px;
        border: 1px solid var(--divider-color);
        border-radius: 4px;
        background: var(--card-background-color);
        color: var(--primary-text-color);
        font: inherit;
      }

      .manual-refresh-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }

      .manual-refresh-message {
        color: var(--secondary-text-color);
        font-size: 13px;
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
    `}};t([dt({attribute:!1})],vt.prototype,"hass",void 0),t([pt()],vt.prototype,"config",void 0),t([pt()],vt.prototype,"_manualRefreshOpen",void 0),t([pt()],vt.prototype,"_manualRefreshBusy",void 0),t([pt()],vt.prototype,"_manualRefreshMessage",void 0),t([pt()],vt.prototype,"_captchaId",void 0),t([pt()],vt.prototype,"_captchaImage",void 0),t([pt()],vt.prototype,"_captchaCode",void 0),t([pt()],vt.prototype,"_availableSignals",void 0),t([pt()],vt.prototype,"_selectedSignal",void 0),t([pt()],vt.prototype,"_manualRefreshStep",void 0),t([pt()],vt.prototype,"_manualRefreshSucceeded",void 0),vt=t([(t=>(e,s)=>{void 0!==s?s.addInitializer(()=>{customElements.define(t,e)}):customElements.define(t,e)})("cez-hdo-card")],vt),customElements.get("cez-hdo-card")||customElements.define("cez-hdo-card",vt),window.customCards=window.customCards||[],window.customCards.push({type:"cez-hdo-card",name:"ČEZ HDO Card",description:"Custom card for ČEZ HDO integration",preview:!0});const yt={low_tariff:{domain:"binary_sensor",prefix:"cez_hdo_lowtariffactive_"},high_tariff:{domain:"binary_sensor",prefix:"cez_hdo_hightariffactive_"},low_start:{domain:"sensor",prefix:"cez_hdo_lowtariffstart_"},low_end:{domain:"sensor",prefix:"cez_hdo_lowtariffend_"},low_duration:{domain:"sensor",prefix:"cez_hdo_lowtariffduration_"},high_start:{domain:"sensor",prefix:"cez_hdo_hightariffstart_"},high_end:{domain:"sensor",prefix:"cez_hdo_hightariffend_"},high_duration:{domain:"sensor",prefix:"cez_hdo_hightariffduration_"},schedule:{domain:"sensor",prefix:"cez_hdo_schedule_"}};function bt(t,e){if(!t?.states)return[];const s=yt[e];if(!s)return[];const i=`${s.domain}.${s.prefix}`;return Object.keys(t.states).filter(t=>t.startsWith(i))}class $t extends HTMLElement{constructor(){super(),this._config={},this.attachShadow({mode:"open"})}set hass(t){if(this._hass=t,this.shadowRoot){this.shadowRoot.querySelectorAll("ha-selector").forEach(e=>{e.hass=t})}}setConfig(t){this._config=t||{},this._render()}_emitConfigChanged(){this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:this._config},bubbles:!0,composed:!0}))}_setOption(t,e,s=!1){this._config={...this._config,[t]:e},this._emitConfigChanged(),s||this._render()}_setEntity(t,e){const s={...this._config.entities||{}};e?s[t]=e:delete s[t],this._config={...this._config,entities:s},this._emitConfigChanged()}_entityPicker(t,e,s){let i=this._config.entities&&this._config.entities[e]||"";const a=function(t,e){const s=bt(t,e);return 1===s.length?s[0]:null}(this._hass,e),n=bt(this._hass,e),r=i||a||"",o=document.createElement("div");o.className="entity-row";const h=document.createElement("ha-selector");if(h.hass=this._hass,h.label=t,h.selector={entity:s&&s.length?{domain:s}:{}},h.value=r,h.addEventListener("value-changed",t=>{this._setEntity(e,t.detail.value)}),o.appendChild(h),!i&&a){const t=document.createElement("div");t.className="hint",t.textContent="Auto-detekováno",o.appendChild(t)}else if(!i&&!a&&n.length>1){const t=document.createElement("div");t.className="hint hint-warning",t.textContent=`Nalezeno ${n.length} zařízení - vyberte entitu`,o.appendChild(t)}else if(!i&&!a&&0===n.length){const t=document.createElement("div");t.className="hint",t.textContent="Žádná ČEZ HDO entita nenalezena",o.appendChild(t)}return o}_render(){if(!this.shadowRoot||!this._hass)return void(this.shadowRoot&&(this.shadowRoot.innerHTML=""));const t=gt(ft(this._hass)),e=this._config.title??"",s=!1!==this._config.show_times,i=!1!==this._config.show_duration,a=!0===this._config.compact_mode;this.shadowRoot.innerHTML='\n      <style>\n        .wrap {\n          display: flex;\n          flex-direction: column;\n          gap: 12px;\n          padding: 4px 0;\n        }\n        .toggle-row {\n          display: flex;\n          align-items: center;\n          gap: 12px;\n          min-height: 32px;\n          color: var(--primary-text-color);\n          font-size: 14px;\n        }\n        .entity-row {\n          display: flex;\n          flex-direction: column;\n          gap: 6px;\n        }\n        .entity-row ha-selector {\n          display: block;\n        }\n        .hint {\n          font-size: 12px;\n          opacity: 0.8;\n        }\n        .hint-warning {\n          color: var(--warning-color, #ff9800);\n          font-weight: 500;\n        }\n      </style>\n      <div class="wrap"></div>\n    ';const n=this.shadowRoot.querySelector(".wrap");if(!n)return;const r=document.createElement("ha-textfield");r.label=t.editorTitle,r.value=e,r.addEventListener("input",t=>{this._config={...this._config,title:t.target.value}}),r.addEventListener("change",t=>{this._config={...this._config,title:t.target.value},this._emitConfigChanged()}),n.appendChild(r);const o=(t,e,s)=>{const i=document.createElement("div");i.className="toggle-row";const a=document.createElement("ha-switch");a.checked=s,a.setAttribute("aria-label",t),a.addEventListener("change",()=>this._setOption(e,a.checked,!0));const n=document.createElement("span");return n.textContent=t,i.appendChild(a),i.appendChild(n),i};n.appendChild(o(t.showTitle,"show_title",!1!==this._config.show_title)),n.appendChild(o(t.showTariffStatus,"show_tariff_status",!1!==this._config.show_tariff_status)),n.appendChild(o(t.showTariffPrices,"show_tariff_prices",!0===this._config.show_tariff_prices)),n.appendChild(o(t.showTimes,"show_times",s)),n.appendChild(o(t.showDuration,"show_duration",i)),n.appendChild(o(t.showCurrentPrice,"show_price",!1!==this._config.show_price)),n.appendChild(o(t.showManualRefresh,"show_manual_refresh",!1!==this._config.show_manual_refresh)),n.appendChild(o(t.showHdoSchedule,"show_schedule",!0===this._config.show_schedule)),n.appendChild(o(t.showSchedulePrices,"show_schedule_prices",!0===this._config.show_schedule_prices)),n.appendChild(o(t.compactMode,"compact_mode",a)),n.appendChild(this._entityPicker(t.ntActiveBinarySensor,"low_tariff",["binary_sensor"])),n.appendChild(this._entityPicker(t.vtActiveBinarySensor,"high_tariff",["binary_sensor"])),n.appendChild(this._entityPicker(t.ntStartSensor,"low_start",["sensor"])),n.appendChild(this._entityPicker(t.ntEndSensor,"low_end",["sensor"])),n.appendChild(this._entityPicker(t.ntRemainingSensor,"low_duration",["sensor"])),n.appendChild(this._entityPicker(t.vtStartSensor,"high_start",["sensor"])),n.appendChild(this._entityPicker(t.vtEndSensor,"high_end",["sensor"])),n.appendChild(this._entityPicker(t.vtRemainingSensor,"high_duration",["sensor"])),n.appendChild(this._entityPicker(t.hdoScheduleSensor,"schedule",["sensor"]));const h=document.createElement("div");h.className="hint",h.textContent=t.editorHint,n.appendChild(h)}}customElements.get("cez-hdo-card-editor")||customElements.define("cez-hdo-card-editor",$t);console.info("ČEZ HDO Card v3.3.0 loaded successfully");

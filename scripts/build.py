import json, os, re, urllib.parse

EXT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'extension')

BASE_VARIABLES = r'''/* ==========================================================================
   Discord Classic Dark — True 1:1 Discord Desktop Replica for TeamSpeak 6
   ========================================================================== */

:root,
::before,
::after {
  /* ── Discord Classic Dark Tokens ── */
  --dc-bg-primary: #36393f;
  --dc-bg-secondary: #2f3136;
  --dc-bg-secondary-alt: #292b2f;
  --dc-bg-tertiary: #202225;
  --dc-bg-floating: #18191c;
  --dc-channel-input: #40444b;
  --dc-hover: rgba(79, 84, 92, 0.32);
  --dc-selected: rgba(79, 84, 92, 0.6);

  --dc-blurple: #5865f2;
  --dc-blurple-hover: #4752c4;
  --dc-green: #3ba55c;
  --dc-green-ring: #43b581;
  --dc-yellow: #faa61a;
  --dc-red: #ed4245;
  --dc-link: #00aff4;

  --dc-text-normal: #dcddde;
  --dc-text-muted: #72767d;
  --dc-channels-default: #8e9297;
  --dc-interactive-normal: #b9bbbe;
  --dc-header-primary: #ffffff;

  /* ── Header Geometry (Discord 22px titlebar + 48px channel header) ── */
  --tsv-header-window-bar-height: 22px !important;
  --tsv-header-content-header-height: 48px !important;

  /* ── Typography ── */
  --tsv-font-family: "gg sans", "Segoe UI", "Noto Sans", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif !important;
  --tsv-font-family-monospace: Consolas, "gg mono", ui-monospace, monospace !important;
  --tsv-font-color: #dcddde !important;
  --tsv-preview-font-color: #dcddde !important;
  --tsv-font-color-invert: #202225 !important;
  --tsv-contrast-font-color: #ffffff !important;
  --tsv-item-title-color: #dcddde !important;
  --tsv-item-subtitle-color: #8e9297 !important;
  --tsv-font-subtitle-color: #8e9297 !important;
  --tsv-item-accessory-color: #72767d !important;
  --tsv-disabled-color: #6d7179 !important;
  --tsv-connection-client-font-color: #8e9297 !important;
  --ts-contact-typing-color: #dcddde !important;
  --ts-secondary-font-color: #8e9297 !important;
  --ts-third-font-color: #ffffff !important;
  --font-color-button-white: #ffffff !important;

  /* ── Accents ── */
  --tsv-tint: #5865f2 !important;
  --tsv-tint2: #7289da !important;
  --tsv-tint-light: #99aab5 !important;
  --tsv-on-tint: #ffffff !important;
  --default-tsv-tint: #5865f2 !important;
  --tsv-highlight-color: #5865f2 !important;
  --ts-menu-action-color: #00aff4 !important;
  --ts-primary-accent-color: #5865f2 !important;
  --card-outline: #5865f2 !important;
  --highlight-outline-color: rgba(88, 101, 242, 0.45) !important;

  /* ── Surfaces ── */
  --tsv-bg: #36393f !important;
  --tsv-shaded-bg: #2f3136 !important;
  --tsv-contrast-bg: #202225 !important;
  --tsv-contrast-strong-bg: #18191c !important;
  --strong-bg: #202225 !important;
  --tsv-deviant-bg: #292b2f !important;
  --tsv-window-color: #202225 !important;
  --tsv-header-bg: #36393f !important;
  --ts-new-header-bg: #202225 !important;
  --tsv-header-toolbar-bg: #202225 !important;
  --tsv-header-font-color: #ffffff !important;
  --tsv-shaded-header-bg: #2f3136 !important;
  --tsv-shaded-header-font-color: #ffffff !important;
  --tsv-footer-bg: #292b2f !important;
  --tsv-shaded-footer-bg: #292b2f !important;
  --tsv-bar-bg: #292b2f !important;
  --tsv-shaded-bar-bg: #292b2f !important;
  --tsv-settings-bg: #2f3136 !important;
  --tsv-preview-bg: #2f3136 !important;
  --tsv-homebase-bg: #2f3136 !important;
  --tsv-homebase-transparent-bg: rgba(47, 49, 54, 0.92) !important;
  --tsv-dashboard-add-contact-bg: #292b2f !important;
  --card-background: #2f3136 !important;
  --card-hover-background: #34373c !important;
  --card-background-inverted: #292b2f !important;
  --ts-select-bg: #202225 !important;
  --settings-highlight-bg: rgba(79, 84, 92, 0.32) !important;

  /* ── Selections & Borders ── */
  --tsv-item-selection: rgba(79, 84, 92, 0.32) !important;
  --tsv-shaded-item-selection: rgba(79, 84, 92, 0.48) !important;
  --tsv-shaded-bg-selection: rgba(88, 101, 242, 0.25) !important;
  --tsv-separation-border-color: rgba(255, 255, 255, 0.06) !important;
  --tsv-separation-border: 1px solid rgba(255, 255, 255, 0.06) !important;
  --tsv-separation-border-strong-color: #202225 !important;
  --tsv-separation-border-thick: 1px solid rgba(255, 255, 255, 0.06) !important;
  --horizontal-separator-color: rgba(255, 255, 255, 0.06) !important;
  --horizontal-separator-width: 1px !important;
  --presence-separator-presence: #292b2f !important;

  /* ── Flattened Tree & Sidebar Variables (NO gradients) ── */
  --tsv-side-bar-bg-gradient-bottom: #202225 !important;
  --tsv-main-bg-gradient-start: #2f3136 !important;
  --tsv-main-bg-gradient-end: #2f3136 !important;
  --tsv-servertree-bg-gradient: #2f3136 !important;
  --tsv-servertree-blur-tint: transparent !important;
  --ts-tree-channel-bg-start: transparent !important;
  --ts-tree-channel-bg-end: transparent !important;
  --ts-tree-badges-bg: #202225 !important;
  --ts-tree-item-hover-bg-color: rgba(79, 84, 92, 0.32) !important;
  --tsv-server-header-gradient-start: #2f3136 !important;
  --tsv-server-header-gradient-end: #2f3136 !important;
  --tsv-view-header-gradient-start: #2f3136 !important;
  --tsv-view-header-gradient-end: #2f3136 !important;
  --tsv-view-header-bg: #2f3136 !important;
  --tsv-unrelated-activity-header-bg: #36393f !important;
  --tsv-unrelated-activity-header-controls-bg: #2f3136 !important;
  --tsv-unrelated-activity-seperator-color: #202225 !important;
  --tsv-server-info-topic-bg: #2f3136 !important;
  --spacer-bg-gradient-from: transparent !important;
  --spacer-bg-gradient-to: transparent !important;

  /* ── Tabs & Branding ── */
  --tsv-tab-content: #36393f !important;
  --tsv-tab-item-active: #393c43 !important;
  --tsv-tab-item-single-font-color: #8e9297 !important;
  --tsv-highlight-header-bg: #202225 !important;
  --tsv-highlight-header-honeycomb-bg: #202225 !important;
  --tsv-highlight-header-font-color: #ffffff !important;
  --tsv-content-branding-bg: #2f3136 !important;
  --tsv-content-branding-fancy-gradient-start: #5865f2 !important;
  --tsv-content-branding-fancy-gradient-end: #4752c4 !important;
  --tsv-content-branding-fancy-bg: #5865f2 !important;
  --tsv-content-branding-fancy-bg-linear: #5865f2 !important;
  --tsv-content-branding-pinned-bg: #5865f2 !important;
  --tsv-content-branding-servers-bg-gradient-stop-1: #202225 !important;
  --tsv-content-branding-servers-bg-gradient-stop-2: #2f3136 !important;
  --tsv-content-branding-servers-bg-gradient-stop-3: #5865f2 !important;

  /* ── Icons ── */
  --tsv-icon-base: #b9bbbe !important;
  --tsv-icon-tint: #ffffff !important;
  --tsv-icon-tint2: #5865f2 !important;
  --tsv-icon-base-contrast: #ffffff !important;
  --tsv-icon-folder: #8e9297 !important;
  --tsv-icon-shaded-bg: #292b2f !important;
  --tsv-icon-channel-bg: transparent !important;
  --tsv-icon-channel-shade1: #8e9297 !important;
  --tsv-icon-channel-shade2: #72767d !important;
  --tsv-icon-channel-shade3: #b9bbbe !important;
  --tsv-icon-online: #3ba55c !important;
  --tsv-icon-away: #faa61a !important;
  --tsv-icon-error: #ed4245 !important;
  --tsv-icon-subtitle: #8e9297 !important;

  /* ── Chat Colors ── */
  --ts-chat-background-color: #36393f !important;
  --tsv-chat-remote-bg: transparent !important;
  --tsv-chat-self-bg: transparent !important;
  --tsv-chat-self-bg-transparent: transparent !important;
  --tsv-chat-self-bg-pending: transparent !important;
  --tsv-chat-self-bg-pending-transparent: transparent !important;
  --tsv-chat-remote-font-color: #dcddde !important;
  --tsv-chat-self-font-color: #dcddde !important;
  --tsv-chat-deleted-bg: rgba(237, 66, 69, 0.1) !important;
  --tsv-chat-deleted-font-color: #ed4245 !important;
  --tsv-chat-link-color: #00aff4 !important;
  --tsv-chat-mention-bg: rgba(250, 166, 26, 0.1) !important;
  --ts-chat-mention-bg-opacity: 0.1 !important;
  --ts-chat-system-message-bg: transparent !important;
  --ts-chat-system-message-text-color: #8e9297 !important;
  --ts-chat-system-highlight-text-color: #ffffff !important;
  --ts-chat-system-secured-text-color: #3ba55c !important;
  --tsv-chat-widget-bg: #2f3136 !important;
  --tsv-chat-placeholder-element-bg-1: #40444b !important;
  --tsv-chat-placeholder-element-bg-2: #36393f !important;
  --tsv-chat-placeholder-element-bg-3: #4f545c !important;
  --tsv-spoiler-background-color: #202225 !important;

  /* ── Controls & Buttons ── */
  --tsv-button-bg: #4f545c !important;
  --tsv-button-hover-bg: #5d6269 !important;
  --tsv-button-filled-bg: #5865f2 !important;
  --tsv-button-filled-destructive-bg: #ed4245 !important;
  --tsv-button-filled-destructive-hover-bg: #c03537 !important;
  --tsv-button-filled-disabled-bg: #4752c4 !important;
  --hero-button-background: #5865f2 !important;
  --hero-button-border: none !important;
  --tsv-slider-track-bg: #4f545c !important;
  --tsv-toggle-bg: #72767d !important;
  --ts-toggle-bg-color: #72767d !important;
  --ts-toggle-checked-bg-color: #3ba55c !important;
  --tsv-control-handle-bg: #ffffff !important;
  --tsv-control-handle-active-bg: #5865f2 !important;
  --tsv-slider-vad-color: #3ba55c !important;

  /* ── Context Menu ── */
  --ts-context-menu-background: #18191c !important;
  --tsv-context-menu-border: 1px solid rgba(255, 255, 255, 0.04) !important;
  --tsv-context-menu-item-selection: #5865f2 !important;
  --ts-context-menu-font-color: #b9bbbe !important;
  --ts-context-menu-icon-tint-color: #b9bbbe !important;
  --tsv-context-menu-disabled-color: #4f545c !important;
  --tsv-context-menu-error-color: #ed4245 !important;

  /* ── Scrollbar ── */
  --tsv-scrollbar-bg: #202225 !important;
  --tsv-scrollbar-chunks--bg-1: #5865f2 !important;
  --tsv-scrollbar-chunks--bg-2: #4f545c !important;

  /* ── Presence & Talking ── */
  --tsv-online-color: #3ba55c !important;
  --tsv-accept-color: #3ba55c !important;
  --tsv-accept-dark-color: #2d7d46 !important;
  --tsv-accept-light-color: #43b581 !important;
  --tsv-away-color: #faa61a !important;
  --tsv-error-color: #ed4245 !important;
  --tsv-error-light-color: #f37b7d !important;
  --presence-online: #3ba55c !important;
  --presence-away: #faa61a !important;
  --presence-dnd: #ed4245 !important;

  --tsv-client-silent--gradient-start: #2f3136 !important;
  --tsv-client-silent--gradient-stop: #2f3136 !important;
  --tsv-client-silent--outline: transparent !important;
  --tsv-client-talking--gradient-start: #43b581 !important;
  --tsv-client-talking--gradient-stop: #43b581 !important;
  --tsv-client-talking--outline: #43b581 !important;
  --tsv-client-whisper-talking--outline: #ed4245 !important;
  --tsv-client-commander-talking--outline: #faa61a !important;

  /* ── Radii ── */
  --tsv-border-radius-small: 3px !important;
  --tsv-border-radius: 4px !important;
  --tsv-border-radius-large: 8px !important;
  --tsv-border-radius-xlarge: 8px !important;
  --tsv-border-radius-xxlarge: 8px !important;
  --tsv-border-radius-xxxlarge: 8px !important;
  --tsv-shade: rgba(255, 255, 255, 0.04) !important;
  --tsv-shadow-color: rgba(0, 0, 0, 0.24) !important;
  --graph-layer-bg: #4f545c !important;
  --tsv-favorite-fill: #faa61a !important;
  --tsv-favorite-stroke: #292b2f !important;
}

/* Crisp Discord Font Rendering */
html,
body,
#app {
  font-family: var(--tsv-font-family) !important;
  font-weight: 400 !important;
  -webkit-font-smoothing: antialiased !important;
  -webkit-text-stroke: 0 !important;
  background-color: #202225 !important;
}

/* Remove ALL TS6 hexagon masks so server icons & user avatars are clean circles */
.tsv-avatar {
  mask-image: none !important;
  -webkit-mask-image: none !important;
  border-radius: 50% !important;
}

/* Hide decorative hexes & promo clutter (keep interactive controls intact!) */
.ts-start-community-banner,
.ts-background-hexes-container,
.ts-activities-placeholder,
.ts-connection-selector,
.tsv-activity-main .tsv-header > .tsv-window-bar::after,
.tsv-header .tsv-central-toolbar-buttons::before,
.tsv-central-toolbar-buttons .tsv-tool-button:not(:last-child)::after,
.ts-server-informative-buttons::before,
.ts-server-informative-buttons .tsv-tool-button:not(:last-child)::after {
  display: none !important;
}

/* Contain & transform neutrality so anchored docking across columns works seamlessly */
.tsv-window,
.tsv-view.tsv-activity,
.tsv-activity-main,
.tsv-sidebar,
.tsv-window-bar,
.tsv-sidebar > .tsv-footer,
.tsv-activity-main .tsv-header {
  contain: none !important;
  transform: none !important;
}
.tsv-activity-main .tsv-header,
.tsv-window-bar {
  overflow: visible !important;
}
.tsv-activity-main .tsv-window-bar {
  position: static !important;
  z-index: auto !important;
}
.tsv-tool-buttons::before {
  display: none !important;
}
'''

ICON_REPLACEMENT_CSS = r'''/* ==========================================================================
   Discord Custom Monochrome Vector Icons (replaces 3D TS cubes & audio icons)
   ========================================================================== */

/* Channel tree: banner handling moved to CHANNEL_NO_BANNERS_CSS / CHANNEL_BANNERS_CSS */

/* Channel tree icons: swap default 3D TS cubes for Discord Speaker (🔊) / Lock */
.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-server-tree-icon.channel:not(:has(.tsv-avatar)) {
  position: relative !important;
  width: 20px !important;
  height: 20px !important;
  min-width: 20px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  transform: none !important;
  margin-right: 6px !important;
}

.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-server-tree-icon.channel:not(:has(.tsv-avatar)) svg {
  opacity: 0 !important;
}

.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-server-tree-icon.channel:not(:has(.tsv-avatar))::after {
  content: "";
  position: absolute;
  width: 18px;
  height: 18px;
  background-color: #8e9297;
  -webkit-mask-image: url("icons/discord-voice.svg");
  mask-image: url("icons/discord-voice.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
}

.ts-server-tree-item-leaf.channel:not(.spacer).has-password .tsv-server-tree-icon.channel:not(:has(.tsv-avatar))::after {
  -webkit-mask-image: url("icons/discord-voice-locked.svg");
  mask-image: url("icons/discord-voice-locked.svg");
}

.ts-server-tree-item-leaf.channel:not(.spacer):hover .tsv-server-tree-icon.channel:not(:has(.tsv-avatar))::after {
  background-color: #dcddde;
}

.ts-server-tree-item-leaf.channel:not(.spacer).tsv-selected .tsv-server-tree-icon.channel:not(:has(.tsv-avatar))::after,
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-active .tsv-server-tree-icon.channel:not(:has(.tsv-avatar))::after {
  background-color: #ffffff;
}

/* Custom server channel icons: hide the 3D silver cube behind custom CS2/Dota icons */
.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-server-tree-icon.channel:has(.tsv-avatar) svg[name^="channel-"] {
  opacity: 0 !important;
}

/* Right chat header channel icon -> Discord # hashtag SVG (and crisp 20x20 custom channel avatars) */
.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack {
  width: 24px !important;
  height: 24px !important;
  min-width: 24px !important;
  margin-right: 8px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack .tsv-avatar {
  width: 22px !important;
  height: 22px !important;
  min-width: 22px !important;
  min-height: 22px !important;
  border-radius: 50% !important;
  background: transparent !important;
}
.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack:not(:has(.tsv-avatar)) {
  position: relative !important;
}

.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack:not(:has(.tsv-avatar)) svg {
  opacity: 0 !important;
}

.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack:not(:has(.tsv-avatar))::after {
  content: "";
  position: absolute;
  inset: 0;
  background-color: #8e9297;
  -webkit-mask-image: url("icons/discord-hash.svg");
  mask-image: url("icons/discord-hash.svg");
  -webkit-mask-size: 22px 22px;
  mask-size: 22px 22px;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
}

/* Hide 3D TS cube inside chat/detail header icon-stack when channel icon is present;
   show # hashtag ONLY on channel headers without a custom loaded avatar image (preserve Server/Client/DM/Group icons!) */
.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack:has(svg[name^="channel"]) svg {
  opacity: 0 !important;
}
.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack:has(svg[name^="channel"]):not(:has(.tsv-avatar img[src])) {
  position: relative !important;
}
.tsv-activity-detail .tsv-content-header-bar .tsv-content-header-item .tsv-icon-stack:has(svg[name^="channel"]):not(:has(.tsv-avatar img[src]))::after {
  content: "";
  position: absolute;
  inset: 0;
  background-color: #8e9297;
  -webkit-mask-image: url("icons/discord-hash.svg");
  mask-image: url("icons/discord-hash.svg");
  -webkit-mask-size: 22px 22px;
  mask-size: 22px 22px;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  pointer-events: none;
}

/* Mic & Headphones (Speaker) & Settings Discord SVG icons */
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name^="microphone"]),
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name^="speaker"]),
.tsv-footer .tsv-action-subtle[data-v-step="2"]:has(svg[name="settings"]) {
  position: relative !important;
}

.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name^="microphone"]) svg,
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name^="speaker"]) svg,
.tsv-footer .tsv-action-subtle[data-v-step="2"]:has(svg[name="settings"]) svg {
  opacity: 0 !important;
}

.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="microphone"])::after,
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="microphone-slash"])::after,
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="speaker"])::after,
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="speaker-slash"])::after,
.tsv-footer .tsv-action-subtle[data-v-step="2"]:has(svg[name="settings"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 20px;
  height: 20px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}

.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="microphone"])::after {
  -webkit-mask-image: url("icons/discord-mic.svg");
  mask-image: url("icons/discord-mic.svg");
}
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="microphone-slash"])::after,
.tsv-central-toolbar-buttons .tsv-tool-button.active .tsv-tool-button-icon-container:has(svg[name^="microphone"])::after {
  -webkit-mask-image: url("icons/discord-mic-muted.svg");
  mask-image: url("icons/discord-mic-muted.svg");
  background-color: #ed4245 !important;
}

.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="speaker"])::after {
  -webkit-mask-image: url("icons/discord-deafen.svg");
  mask-image: url("icons/discord-deafen.svg");
}
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="speaker-slash"])::after,
.tsv-central-toolbar-buttons .tsv-tool-button.active .tsv-tool-button-icon-container:has(svg[name^="speaker"])::after {
  -webkit-mask-image: url("icons/discord-deafen-muted.svg");
  mask-image: url("icons/discord-deafen-muted.svg");
  background-color: #ed4245 !important;
}

.tsv-footer .tsv-action-subtle[data-v-step="2"]:has(svg[name="settings"])::after {
  -webkit-mask-image: url("icons/discord-settings.svg");
  mask-image: url("icons/discord-settings.svg");
  width: 19px;
  height: 19px;
}

.tsv-central-toolbar-buttons .tsv-tool-button:hover .tsv-tool-button-icon-container::after,
.tsv-footer .tsv-action-subtle[data-v-step="2"]:hover::after {
  background-color: #dcddde;
}

/* Outbound Screenshare ("демка") live & paused toolbar icon + clean single badge */
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="mode-streaming"]) {
  position: relative !important;
  width: 20px !important;
  height: 20px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="mode-streaming"]) svg {
  opacity: 0 !important;
}
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="mode-streaming"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 20px;
  height: 20px;
  transform: translate(-50%, -50%);
  background-color: #ed4245;
  -webkit-mask-image: url("icons/discord-screen.svg");
  mask-image: url("icons/discord-screen.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-central-toolbar-buttons .tsv-tool-button:hover .tsv-tool-button-icon-container:has(svg[name="mode-streaming"])::after {
  background-color: #ff6b6d;
}
.tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="pause"]) svg {
  width: 16px !important;
  height: 16px !important;
  color: #b9bbbe !important;
  fill: currentColor !important;
  opacity: 1 !important;
}
.tsv-central-toolbar-buttons .tsv-tool-button:hover .tsv-tool-button-icon-container:has(svg[name="pause"]) svg {
  color: #ffffff !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="pause"]) svg,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="pause"]) svg,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="pause"]) svg,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-icon-container:has(svg[name="pause"]) svg {
  width: 13px !important;
  height: 13px !important;
}
.tsv-central-toolbar-buttons .tsv-tool-button .tsv-badge-count {
  top: 1px !important;
  right: 1px !important;
  bottom: auto !important;
  left: auto !important;
  min-width: 14px !important;
  height: 14px !important;
  line-height: 12px !important;
  font-size: 9px !important;
  padding: 0 3px !important;
  transform: none !important;
  border: 1px solid #292b2f !important;
  box-sizing: border-box !important;
  z-index: 3 !important;
  pointer-events: none !important;
}
.tsv-central-toolbar-buttons .tsv-tool-button .tsv-badge-count::after,
.ts-stream-view-settings .tsv-badge-count::after {
  display: none !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button .tsv-badge-count,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button .tsv-badge-count,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button .tsv-badge-count,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button .tsv-badge-count {
  top: -1px !important;
  right: -2px !important;
  min-width: 11px !important;
  height: 11px !important;
  line-height: 11px !important;
  font-size: 8px !important;
  padding: 0 2px !important;
  border: none !important;
}

/* Status Bar & Away Discord Monochrome SVG replacements */
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="channel-create"]),
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="video-screen"]),
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-status"]),
.ts-server-status-bar .ts-connection-info-button,
.tsv-activity-main .tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"]) {
  position: relative !important;
  width: 18px !important;
  height: 18px !important;
  padding: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="channel-create"]) svg,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="video-screen"]) svg,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-status"]) svg,
.ts-server-status-bar .ts-connection-info-button svg,
.tsv-activity-main .tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"]) svg {
  opacity: 0 !important;
}

.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="channel-create"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="video-screen"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-status"])::after,
.ts-server-status-bar .ts-connection-info-button::after,
.tsv-activity-main .tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 17px;
  height: 17px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}

.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="channel-create"])::after {
  -webkit-mask-image: url("icons/discord-plus.svg");
  mask-image: url("icons/discord-plus.svg");
  background-color: #dcddde;
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="video-screen"])::after {
  -webkit-mask-image: url("icons/discord-screen.svg");
  mask-image: url("icons/discord-screen.svg");
  background-color: #3ba55c;
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-status"])::after,
.ts-server-status-bar .ts-connection-info-button::after {
  -webkit-mask-image: url("icons/discord-signal.svg");
  mask-image: url("icons/discord-signal.svg");
  background-color: #43b581;
}
.ts-server-status-bar .ts-connection-info-button.bar1-quality2::after,
.ts-server-status-bar .ts-connection-info-button.bar2-quality2::after {
  background-color: #faa61a;
}
.ts-server-status-bar .ts-connection-info-button.bar1-quality1::after,
.ts-server-status-bar .ts-connection-info-button.bar2-quality1::after {
  background-color: #ed4245;
}
.ts-server-status-bar .ts-connection-info-button.bar1-quality0::after {
  background-color: #72767d;
}
.ts-server-status-bar .tsv-tool-button.tsv-is-disabled .tsv-tool-button-icon-container::after {
  background-color: var(--tsv-disabled-color) !important;
  opacity: 0.55;
}
.tsv-activity-main .tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"])::after {
  -webkit-mask-image: url("icons/discord-away.svg");
  mask-image: url("icons/discord-away.svg");
  background-color: #b9bbbe;
}
.tsv-activity-main .tsv-central-toolbar .tsv-tool-button.active .tsv-tool-button-icon-container:has(svg[name^="away"])::after {
  background-color: #faa61a;
}
.ts-server-status-bar .tsv-tool-button:hover .tsv-tool-button-icon-container::after,
.ts-server-status-bar .tsv-tool-button:hover .ts-connection-info-button::after,
.tsv-activity-main .tsv-central-toolbar .tsv-tool-button:hover .tsv-tool-button-icon-container::after {
  filter: brightness(1.18);
}

/* Additional Status Bar icons (Events, Talk Power Requests, Whispers, Recording) */
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-events"]),
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-moderation-events"]),
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-whispers"]),
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="whisper"]),
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="status-recording"]) {
  position: relative !important;
  width: 18px !important;
  height: 18px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-events"]) svg,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-moderation-events"]) svg,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-whispers"]) svg,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="whisper"]) svg,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="status-recording"]) svg {
  opacity: 0 !important;
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-events"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-moderation-events"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-whispers"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="whisper"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="status-recording"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 16px;
  height: 16px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-events"])::after {
  -webkit-mask-image: url("icons/discord-events.svg");
  mask-image: url("icons/discord-events.svg");
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-moderation-events"])::after {
  -webkit-mask-image: url("icons/discord-users.svg");
  mask-image: url("icons/discord-users.svg");
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="connection-whispers"])::after,
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="whisper"])::after {
  -webkit-mask-image: url("icons/discord-mic.svg");
  mask-image: url("icons/discord-mic.svg");
}
.ts-server-status-bar .tsv-tool-button-icon-container:has(svg[name="status-recording"])::after {
  -webkit-mask-image: url("icons/discord-record.svg");
  mask-image: url("icons/discord-record.svg");
  background-color: #ed4245;
}

/* Server Header & Right Chat Header Monochrome Discord Icons */
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark"]),
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark-home"]),
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="channel-show-chat"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="info"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-info"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="notifications"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="folder"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-files"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse-left"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="server-info-users"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="search"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-events"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-chat"]),
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="item-leave"]) {
  position: relative !important;
  width: 24px !important;
  height: 24px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="info"]),
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-info"]),
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-chat"]),
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-files"]),
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-events"]) {
  position: relative !important;
  width: 28px !important;
  min-width: 28px !important;
  height: 26px !important;
  padding: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark"]) svg,
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark-home"]) svg,
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="channel-show-chat"]) svg,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="info"]) svg,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-info"]) svg,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-chat"]) svg,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-files"]) svg,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-events"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="info"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-info"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="notifications"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="folder"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-files"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse-left"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="server-info-users"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="search"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-events"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-chat"]) svg,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="item-leave"]) svg {
  opacity: 0 !important;
}
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark"])::after,
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark-home"])::after,
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="channel-show-chat"])::after,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="info"])::before,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-info"])::before,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-chat"])::before,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-files"])::before,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-events"])::before,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="info"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-info"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="notifications"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="folder"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-files"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse-left"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="server-info-users"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="search"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-events"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-chat"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="item-leave"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 18px;
  height: 18px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
  transition: background-color 0.1s ease;
}
.ts-server-header .tsv-tool-button:hover .tsv-tool-button-icon-container::after,
.tsv-content-header-bar .tsv-tool-button:hover .tsv-tool-button-icon-container::after,
.tsv-content-header-bar .tsv-segmented-button:hover::before,
.tsv-content-header-bar .tsv-segmented-button.active::before {
  background-color: #ffffff;
}
.ts-server-header .tsv-tool-button.active .tsv-tool-button-icon-container:has(svg[name^="bookmark"])::after {
  background-color: #5865f2;
}
.tsv-content-header-bar .tsv-tool-button.tsv-is-disabled .tsv-tool-button-icon-container::after {
  background-color: var(--tsv-disabled-color) !important;
  opacity: 0.55;
}
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark"])::after,
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="bookmark-home"])::after {
  -webkit-mask-image: url("icons/discord-bookmark.svg");
  mask-image: url("icons/discord-bookmark.svg");
}
.ts-server-header .tsv-tool-button-icon-container:has(svg[name="channel-show-chat"])::after,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-chat"])::before,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-chat"])::after {
  -webkit-mask-image: url("icons/discord-chat.svg");
  mask-image: url("icons/discord-chat.svg");
}
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="info"])::before,
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-info"])::before,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="info"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-info"])::after {
  -webkit-mask-image: url("icons/discord-info.svg");
  mask-image: url("icons/discord-info.svg");
}
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="notifications"])::after {
  -webkit-mask-image: url("icons/discord-bell.svg");
  mask-image: url("icons/discord-bell.svg");
}
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-files"])::before,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="folder"])::after,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-files"])::after {
  -webkit-mask-image: url("icons/discord-folder.svg");
  mask-image: url("icons/discord-folder.svg");
}
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse"])::after {
  -webkit-mask-image: url("icons/discord-chevron.svg");
  mask-image: url("icons/discord-chevron.svg");
  transform: translate(-50%, -50%) rotate(-90deg);
}
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="window-collapse-left"])::after {
  -webkit-mask-image: url("icons/discord-chevron.svg");
  mask-image: url("icons/discord-chevron.svg");
  transform: translate(-50%, -50%) rotate(90deg);
}
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="server-info-users"])::after {
  -webkit-mask-image: url("icons/discord-users.svg");
  mask-image: url("icons/discord-users.svg");
}
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="search"])::after {
  -webkit-mask-image: url("icons/discord-search.svg");
  mask-image: url("icons/discord-search.svg");
}
.tsv-content-header-bar .tsv-segmented-button:has(svg[name="mode-events"])::before,
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="mode-events"])::after {
  -webkit-mask-image: url("icons/discord-events.svg");
  mask-image: url("icons/discord-events.svg");
}
.tsv-content-header-bar .tsv-tool-button-icon-container:has(svg[name="item-leave"])::after {
  -webkit-mask-image: url("icons/discord-close.svg");
  mask-image: url("icons/discord-close.svg");
}

/* Chat Input Actions (Emoji, Upload +/Attach, Send) -> Discord Vector Icons */
.ts-chat-input-container-actions .ts-chat-emoji-button,
.ts-chat-input-container-actions .ts-chat-image-button,
.ts-chat-input-container-actions .ts-chat-send-button {
  position: relative !important;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: transparent !important;
  border-radius: 4px !important;
  padding: 0 !important;
}
.ts-chat-input-container-actions .ts-chat-emoji-button svg,
.ts-chat-input-container-actions .ts-chat-image-button svg,
.ts-chat-input-container-actions .ts-chat-send-button svg {
  opacity: 0 !important;
}
.ts-chat-input-container-actions .ts-chat-emoji-button::after,
.ts-chat-input-container-actions .ts-chat-image-button::after,
.ts-chat-input-container-actions .ts-chat-send-button::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 20px;
  height: 20px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
  transition: background-color 0.1s ease;
}
.ts-chat-input-container-actions .ts-chat-emoji-button::after {
  -webkit-mask-image: url("icons/discord-emoji.svg");
  mask-image: url("icons/discord-emoji.svg");
}
.ts-chat-input-container-actions .ts-chat-image-button::after {
  -webkit-mask-image: url("icons/discord-attach.svg");
  mask-image: url("icons/discord-attach.svg");
}
.ts-chat-input-container-actions .ts-chat-send-button::after {
  -webkit-mask-image: url("icons/discord-send.svg");
  mask-image: url("icons/discord-send.svg");
  width: 18px;
  height: 18px;
}
.ts-chat-input-container-actions .ts-chat-emoji-button:hover::after,
.ts-chat-input-container-actions .ts-chat-image-button:hover::after {
  background-color: #dcddde;
}
.ts-chat-input-container-actions .ts-chat-send-button:not(.disabled):hover::after {
  background-color: #5865f2;
}

/* Server Tree Voice Participant Mute/Deafen/Away Badges (aligned right cleanly like Discord!) */
.ts-server-tree-item-node-content.client {
  position: relative !important;
}
.ts-server-tree-item-node-content .tsv-server-tree-icon.client,
.ts-server-tree-item-node-content .ts-server-tree-icon.client {
  width: 24px !important;
  height: 24px !important;
  min-width: 24px !important;
  min-height: 24px !important;
  border-radius: 50% !important;
  box-shadow: none !important;
  margin-right: 8px !important;
}
.ts-server-tree-item-node-content .tsv-server-tree-icon.client .tsv-avatar,
.ts-server-tree-item-node-content .ts-server-tree-icon.client .tsv-avatar {
  width: 24px !important;
  height: 24px !important;
  border-radius: 50% !important;
}
.ts-server-tree-item-node-content .tsv-server-tree-icon.client.talking,
.ts-server-tree-item-node-content .ts-server-tree-icon.client.talking {
  box-shadow: 0 0 0 2px #43b581 !important;
  border-radius: 50% !important;
}
.ts-server-tree-item-node-content .mute-indicator {
  position: relative !important;
  order: 4 !important;
  margin: 0 2px 0 auto !important;
  padding: 0 !important;
  background: transparent !important;
  width: 16px !important;
  height: 16px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}
.ts-server-tree-item-node-content .mute-indicator svg {
  opacity: 0 !important;
}
.ts-server-tree-item-node-content .mute-indicator::after {
  content: "";
  position: absolute;
  inset: 0;
  margin: auto;
  width: 15px;
  height: 15px;
  background-color: #8e9297;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.ts-server-tree-item-node-content .mute-indicator.input-muted::after {
  -webkit-mask-image: url("icons/discord-mic-muted.svg");
  mask-image: url("icons/discord-mic-muted.svg");
  background-color: #8e9297;
}
.ts-server-tree-item-node-content .mute-indicator.output-muted::after {
  -webkit-mask-image: url("icons/discord-deafen-muted.svg");
  mask-image: url("icons/discord-deafen-muted.svg");
  background-color: #8e9297;
}
.ts-server-tree-item-node-content .mute-indicator.away::after {
  -webkit-mask-image: url("icons/discord-away.svg");
  mask-image: url("icons/discord-away.svg");
  background-color: #faa61a;
}
.ts-server-tree-item-node-content .mute-indicator:has(svg[name="input-muted-local"])::after {
  -webkit-mask-image: url("icons/discord-mic-muted.svg");
  mask-image: url("icons/discord-mic-muted.svg");
  background-color: #ed4245;
}
'''

DOCK_AND_LAYOUT_CSS = r'''/* ==========================================================================
   Core Discord Layout, Moved Buttons, Channel Tree, Flat Chat, Controls
   ========================================================================== */

/* Top window bar (#202225, 22px across the window) */
.tsv-window {
  background: #202225 !important;
}

.tsv-window-bar,
.tsv-highlight.tsv-header {
  background: #202225 !important;
  border-bottom: none !important;
}

.tsv-window-bar {
  height: 22px !important;
  min-height: 22px !important;
  max-height: 22px !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

/* Keep window minimize / maximize / close compact inside 22px top bar */
.tsv-window-controls {
  height: 22px !important;
  align-items: center !important;
}
.tsv-window-controls .tsv-bar-item {
  height: 22px !important;
  min-height: 22px !important;
  padding: 0 10px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  --tsv-icon-base: #b9bbbe !important;
}
.tsv-window-controls .tsv-bar-item:hover {
  background: rgba(79, 84, 92, 0.4) !important;
  --tsv-icon-base: #ffffff !important;
}

/* Collapse Column 2's top header to ONLY the 22px window drag strip & flatten Dashboard backdrop */
.tsv-activity-main > .tsv-header:has(.tsv-window-bar):not(:has(.tsv-content-header-bar)) {
  flex-basis: 22px !important;
  min-height: 22px !important;
  max-height: 22px !important;
  height: 22px !important;
  background: #202225 !important;
  border-bottom: none !important;
}
.tsv-activity-main > .tsv-header::before,
.tsv-activity-main > .tsv-header .tsv-header-backdrop {
  display: none !important;
  background: #202225 !important;
}
.tsv-window-bar > .tsv-bar-item:first-child:has(> .tsv-icon:empty) {
  display: none !important;
}

/* When NOT in server split view (Home/Settings/Slideover/Fullscreen) OR in split view: keep Away + top-bar controls cleanly inside 22px #202225 top bar! */
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-central-toolbar,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-central-toolbar,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-central-toolbar,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-central-toolbar,
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-central-toolbar {
  height: 22px !important;
  min-height: 22px !important;
  max-height: 22px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 2px !important;
  padding: 0 6px !important;
  margin: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-buttons,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-buttons,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-buttons,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-buttons,
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-tool-buttons:not(.tsv-central-toolbar-buttons) {
  height: 20px !important;
  min-height: 20px !important;
  padding: 0 !important;
  margin: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 2px !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]),
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]),
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]),
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]),
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) {
  width: 22px !important;
  height: 20px !important;
  min-width: 22px !important;
  min-height: 20px !important;
  max-height: 20px !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 3px !important;
  background: transparent !important;
  box-shadow: none !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-button,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-button,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-button,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-button {
  height: 20px !important;
  min-height: 20px !important;
  max-height: 20px !important;
  min-width: 22px !important;
  padding: 0 3px !important;
  margin: 0 !important;
  border-radius: 3px !important;
  background: transparent !important;
  box-shadow: none !important;
  position: relative !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-button:hover,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-button:hover,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-button:hover,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-button:hover,
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]):hover {
  background: rgba(79, 84, 92, 0.45) !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-button-icon-container,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-button-icon-container,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-button-icon-container,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-button-icon-container,
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-icon-container {
  width: 16px !important;
  height: 16px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-button-icon-container::after,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-button-icon-container::after,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-button-icon-container::after,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-button-icon-container::after,
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-icon-container::after {
  width: 14px !important;
  height: 14px !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-context-menu-toggle,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-context-menu-toggle,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-context-menu-toggle,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-context-menu-toggle,
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-window-bar .tsv-tool-button:has(svg[name^="away"]) .tsv-tool-button-context-menu-toggle {
  display: none !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-context-menu-toggle,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-context-menu-toggle,
.tsv-window:has(.tsv-settings) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-context-menu-toggle,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-window-bar .tsv-central-toolbar-buttons .tsv-tool-button-context-menu-toggle {
  width: 10px !important;
  height: 16px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin-left: 1px !important;
}
/* Dashboard Popular Servers Search Input ("IP / домен / никнейм сервера") — prevent placeholder clipping */
.tsv-dashboard-servers .server-search-input-wrapper,
.tsv-dashboard-servers .server-search-input,
.tsv-dashboard-servers #server-addr {
  min-width: min(360px, 100%) !important;
  width: min(360px, 100%) !important;
  max-width: 100% !important;
}
.tsv-dashboard-servers #server-addr {
  background: #202225 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 6px !important;
}

/* Give Dashboard Away button its crisp moon SVG even on Home/Settings top bar */
.tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"]) {
  position: relative !important;
  width: 16px !important;
  height: 16px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"]) svg {
  opacity: 0 !important;
}
.tsv-central-toolbar .tsv-tool-button-icon-container:has(svg[name^="away"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 14px;
  height: 14px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-image: url("icons/discord-away.svg");
  mask-image: url("icons/discord-away.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-central-toolbar .tsv-tool-button.active .tsv-tool-button-icon-container:has(svg[name^="away"])::after {
  background-color: #faa61a;
}

/* ==========================================================================
   MOVE BUTTONS TO EXACT DISCORD POSITIONS (CSS Anchor Positioning in Chrome 146)
   Targets split view: Column 2 (Server Tree) + Column 3 (Chat / Server Info)
   ========================================================================== */

/* Define --dc-rail-edge BEFORE .tsv-sidebar > .tsv-footer in DOM so Anchor Positioning resolves in Chrome 146! */
.tsv-sidebar-header {
  anchor-name: --dc-rail-edge;
}

/* Lock Column 2 to authentic Discord 256px Channel Sidebar width in split view & anchor it (exclude slideover & fullscreen screenshare!) */
.tsv-window:has(.tsv-activity-detail):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-activity-main:not(.tsv-activity-slideover) {
  anchor-name: --dc-channel-col;
  flex: 0 0 256px !important;
  width: 256px !important;
  min-width: 240px !important;
  max-width: 256px !important;
}

/* Reserve exact 52px bottom space inside Column 2 so Voice Status bar sits right above User Dock */
.tsv-window:has(.tsv-activity-detail):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-activity-main:not(.tsv-activity-slideover) > .tsv-body {
  padding-bottom: 52px !important;
}

/* Move NotificationsOverlay ("Insufficient talk power") cleanly above Voice + User Dock & keep bottom tree rows clickable */
.tsv-activity-main .ts-server-tree-wrapper .ts-server-tree-content-spacer-top,
.tsv-activity-main .ts-server-tree-wrapper .ts-server-tree-content-spacer-top.has-notifications {
  height: 0 !important;
  padding-top: 0 !important;
  margin: 0 !important;
}
.tsv-activity-main:not(.tsv-activity-slideover):has(.ts-server-status-bar) .ts-notifications-overlay {
  top: auto !important;
  bottom: 98px !important;
  padding: 0 6px !important;
  z-index: 30 !important;
}
.tsv-activity-main.tsv-activity-slideover:has(.ts-server-status-bar) .ts-notifications-overlay {
  top: auto !important;
  bottom: 50px !important;
  padding: 0 6px !important;
  z-index: 30 !important;
}
.tsv-activity-main:not(:has(.ts-server-status-bar)) .ts-notifications-overlay {
  top: auto !important;
  bottom: 8px !important;
  padding: 0 6px !important;
  z-index: 30 !important;
}
.tsv-activity-main:has(.ts-notifications-overlay .ts-notification) .ts-server-tree-wrapper .scroller {
  padding-bottom: 48px !important;
}
.tsv-activity-main .ts-notification {
  background: #202225 !important;
  border-left: 2px solid #faa61a !important;
  border-radius: 4px !important;
  padding: 4px 8px !important;
  min-height: 28px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35) !important;
}

/* 1) Teleport Column 1 Footer (TSPresenceV Avatar/Name + Settings Gear) -> Bottom of Column 2 (#292b2f, 52px) */
/* Anchored to --dc-rail-edge (prior sibling!) so Chrome 146 resolves left: anchor(right) cleanly in DOM order! */
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer {
  position: fixed !important;
  position-anchor: --dc-rail-edge !important;
  left: anchor(right) !important;
  right: auto !important;
  bottom: 0 !important;
  top: auto !important;
  width: 255px !important;
  height: 52px !important;
  min-height: 52px !important;
  max-height: 52px !important;
  background: #292b2f !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
  padding: 0 !important;
  margin: 0 !important;
  z-index: 45 !important;
  display: flex !important;
  justify-content: center !important;
}

.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer::before {
  display: none !important;
}

.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer > .tsv-bar {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  width: 100% !important;
  height: 52px !important;
  padding: 0 8px !important;
  gap: 0 !important;
  flex-wrap: nowrap !important;
}

/* Profile item on the left side of the 52px dock (leave exact room on right for Mic + Headphones + [Screenshare] + Settings) */
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer > .tsv-bar > .tsv-loading-no-delay {
  flex: 1 1 auto !important;
  min-width: 0 !important;
  max-width: calc(100% - 106px) !important;
  justify-content: flex-start !important;
  padding: 0 !important;
  margin: 0 !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)):has(.tsv-central-toolbar-buttons .tsv-tool-button:nth-child(3)) .tsv-sidebar > .tsv-footer > .tsv-bar > .tsv-loading-no-delay {
  max-width: calc(100% - 140px) !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)):has(.tsv-central-toolbar-buttons .tsv-tool-button:nth-child(4)) .tsv-sidebar > .tsv-footer > .tsv-bar > .tsv-loading-no-delay {
  max-width: calc(100% - 174px) !important;
}

.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item {
  width: 100% !important;
  min-height: 38px !important;
  padding: 3px 6px 3px 4px !important;
  margin: 0 !important;
  border-radius: 4px !important;
  justify-content: flex-start !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item:hover {
  background: rgba(79, 84, 92, 0.35) !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item .tsv-item-container {
  justify-content: flex-start !important;
  padding: 0 !important;
  margin: 0 !important;
}
.tsv-sidebar > .tsv-footer .tsv-item .tsv-item-content {
  gap: 8px !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item .tsv-item-content {
  justify-content: flex-start !important;
  gap: 8px !important;
  margin: 0 !important;
}
.tsv-sidebar > .tsv-footer .tsv-item .tsv-item-text {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  margin-left: 0 !important;
  text-align: left !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item .tsv-icon-primary,
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item .tsv-avatar {
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  min-height: 32px !important;
  border-radius: 50% !important;
  flex-shrink: 0 !important;
}

/* Crisp Discord 10px status badge dot on bottom dock avatar */
.tsv-sidebar > .tsv-footer .tsv-icon-primary,
.tsv-sidebar > .tsv-footer .tsv-icon-stack {
  overflow: visible !important;
  position: relative !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .has-presence {
  --presence-width: 10px !important;
  --presence-border-width: 2px !important;
  --presence-outline-color: #292b2f !important;
}
.tsv-sidebar > .tsv-footer .has-presence.available {
  --presence-color: #3ba55c !important;
}
.tsv-sidebar > .tsv-footer .has-presence.away {
  --presence-color: #faa61a !important;
}
.tsv-sidebar > .tsv-footer .has-presence.dnd {
  --presence-color: #ed4245 !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item-content:has(.available) .tsv-icon-primary::after,
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-icon-stack.has-presence.available::after {
  content: "";
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #3ba55c;
  border: 2px solid #292b2f;
  box-sizing: border-box;
  pointer-events: none;
  z-index: 8;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item-content:has(.away) .tsv-icon-primary::after,
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-icon-stack.has-presence.away::after {
  content: "";
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #faa61a;
  border: 2px solid #292b2f;
  box-sizing: border-box;
  pointer-events: none;
  z-index: 8;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-item-content:has(.dnd) .tsv-icon-primary::after,
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-icon-stack.has-presence.dnd::after {
  content: "";
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ed4245;
  border: 2px solid #292b2f;
  box-sizing: border-box;
  pointer-events: none;
  z-index: 8;
}
.tsv-sidebar > .tsv-footer .tsv-item-title {
  font-size: 13px !important;
  font-weight: 600 !important;
  color: #ffffff !important;
  line-height: 16px !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}
.tsv-sidebar > .tsv-footer .tsv-item-subtitle {
  font-size: 11px !important;
  color: #b9bbbe !important;
  line-height: 13px !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}
.tsv-sidebar > .tsv-footer .ts-has-server-presence,
.tsv-sidebar > .tsv-footer .ts-server-presence-loading,
.tsv-sidebar > .tsv-footer .tsv-reveal-on-hover,
.ts-has-server-presence,
.ts-server-presence-loading {
  display: none !important;
}

/* Settings Gear pinned far-right of 52px dock */
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-sidebar > .tsv-footer .tsv-action-subtle[data-v-step="2"] {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 4px !important;
  flex: 0 0 32px !important;
  cursor: pointer !important;
}
.tsv-sidebar > .tsv-footer .tsv-action-subtle[data-v-step="2"]:hover {
  background: rgba(79, 84, 92, 0.4) !important;
}

/* 2) Teleport Mic, Headphones & optional Screenshare (.tsv-central-toolbar-buttons) -> Right beside Settings in 52px dock! */
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons {
  position: fixed !important;
  position-anchor: --dc-channel-col !important;
  left: calc(anchor(right) - 109px) !important;
  bottom: calc(anchor(bottom) + 10px) !important;
  top: auto !important;
  right: auto !important;
  width: 66px !important;
  height: 32px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 2px !important;
  padding: 0 !important;
  margin: 0 !important;
  z-index: 60 !important;
  pointer-events: auto !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons:has(.tsv-tool-button:nth-child(3)) {
  left: calc(anchor(right) - 143px) !important;
  width: 100px !important;
}
.tsv-window:has(.tsv-activity-detail):has(.tsv-activity-main:not(.tsv-activity-slideover)):not(:has(.tsv-settings)):not(:has(.screenshare-fullscreen-host.is-active)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons:has(.tsv-tool-button:nth-child(4)) {
  left: calc(anchor(right) - 177px) !important;
  width: 134px !important;
}

.tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons .tsv-tool-button {
  width: 32px !important;
  height: 32px !important;
  min-width: 32px !important;
  max-width: 32px !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  cursor: pointer !important;
}

.tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons .tsv-tool-button:hover {
  background: rgba(79, 84, 92, 0.4) !important;
}

.tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons .tsv-tool-button-icon-container {
  width: 22px !important;
  height: 22px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
}

/* Show audio-device selector chevron discretely only on button hover so 32x32 spacing never shifts */
.tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons .tsv-tool-button-context-menu-toggle {
  position: absolute !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 10px !important;
  height: 10px !important;
  opacity: 0 !important;
  pointer-events: none !important;
  transition: opacity 0.12s ease !important;
}
.tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar-buttons .tsv-tool-button:hover .tsv-tool-button-context-menu-toggle {
  opacity: 0.9 !important;
  pointer-events: auto !important;
}

/* Away button duplicate definition removed — positioned cleanly above right edge */
.tsv-activity-main:not(.tsv-activity-slideover) .tsv-central-toolbar > .tsv-tool-buttons:not(.tsv-central-toolbar-buttons) .tsv-tool-button-context-menu-toggle {
  display: none !important;
}

/* Settings View Bottom Clearance when open (never cut off bottom items) */
.tsv-window:has(.tsv-settings) .tsv-settings {
  padding-bottom: 8px !important;
}

/* ==========================================================================
   Column 2: Channel Sidebar (#2f3136) + Voice Status Bar (#292b2f)
   ========================================================================== */
.tsv-window:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover),
.tsv-window:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-body,
.tsv-window:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) .tsv-body-background,
.ts-server-tree-item-root,
.ts-server-tree-wrapper {
  background: #2f3136 !important;
}

.tsv-window:has(.tsv-activity-detail):not(:has(.tsv-settings)) .tsv-activity-main:not(.tsv-activity-slideover) {
  border-right: 1px solid #202225 !important;
}

.ts-server-header {
  background: #2f3136 !important;
  border-bottom: 1px solid #26282c !important;
  box-shadow: 0 1px 0 rgba(4, 4, 5, 0.2), 0 1.5px 0 rgba(6, 6, 7, 0.05), 0 2px 0 rgba(4, 4, 5, 0.05) !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  height: 48px !important;
  min-height: 48px !important;
  max-height: 48px !important;
}

.ts-server-header .tsv-view-banner {
  --top-spacing: 0px !important;
  --total-banner-height: 47px !important;
  min-height: 47px !important;
  max-height: 47px !important;
  height: 47px !important;
  margin: 0 !important;
  padding: 0 14px 0 16px !important;
  border-radius: 0 !important;
  background: #2f3136 !important;
  cursor: pointer !important;
  position: relative !important;
}
.ts-server-header .tsv-view-banner:hover {
  background: rgba(79, 84, 92, 0.24) !important;
}

/* Discord Server Name down-chevron at rest; show TS Bookmark / Chat icons smoothly on hover! */
.ts-server-header .tsv-view-banner::after {
  content: "";
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  background-color: #dcddde;
  -webkit-mask-image: url("icons/discord-chevron.svg");
  mask-image: url("icons/discord-chevron.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
  transition: opacity 0.12s ease;
}
.ts-server-header:hover .tsv-view-banner::after,
.ts-server-header:focus-within .tsv-view-banner::after,
.ts-server-header .tsv-view-banner:has(.tsv-view-accessory .tsv-badge-count)::after,
.ts-server-header .tsv-view-banner:has(.tsv-view-accessory .active)::after {
  opacity: 0;
}
.ts-server-header .tsv-view-banner .tsv-view-accessory {
  opacity: 0 !important;
  transition: opacity 0.12s ease !important;
}
.ts-server-header:hover .tsv-view-banner .tsv-view-accessory,
.ts-server-header:focus-within .tsv-view-banner .tsv-view-accessory,
.ts-server-header .tsv-view-banner .tsv-view-accessory:has(.tsv-badge-count),
.ts-server-header .tsv-view-banner .tsv-view-accessory:has(.active) {
  opacity: 1 !important;
}

/* Hide blurry banner image & bulky hex server avatar in channel header so "SKOOOOOOOOO" fits cleanly! */
.ts-server-header .tsv-view-banner .tsv-view-background,
.ts-server-header .tsv-view-banner .tsv-view-image {
  display: none !important;
}

.ts-server-header .tsv-view-banner .tsv-view-content,
.ts-server-header .tsv-view-banner .tsv-view-accessory {
  margin-top: 0 !important;
  align-self: center !important;
}

.ts-server-header .tsv-view-banner .tsv-view-content {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  line-height: 20px !important;
  min-width: 0 !important;
  flex: 1 1 auto !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}
.ts-server-header .tsv-view-banner .tsv-view-content .tsv-text-truncate {
  display: block !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
}
.ts-server-header .tsv-view-banner .tsv-view-accessory {
  flex-shrink: 0 !important;
}

/* Channel header accessory icons ([Bookmark] [Server Chat]) -> crisp Discord subtle icons */
.ts-server-header .tsv-view-accessory .tsv-tool-button {
  --tsv-icon-base: #b9bbbe !important;
  opacity: 0.85 !important;
}
.ts-server-header .tsv-view-accessory .tsv-tool-button:hover {
  --tsv-icon-base: #ffffff !important;
  opacity: 1 !important;
}

/* Server tree scrolling */
.ts-server-tree-wrapper .scroller {
  padding-left: 2px !important;
  padding-right: 4px !important;
}

/* Category Headers / Spacers — Clean Discord Category Typography (respects TS [cspacer] centering without fake chevrons) */
.ts-server-tree-item-leaf.spacer {
  margin-top: 8px !important;
  height: 24px !important;
}
.ts-server-tree-item-leaf.spacer .tsv-item-highlight,
.ts-server-tree-item-leaf.spacer .tsv-item-highlight-extra,
.ts-server-tree-item-leaf.spacer .ts-server-tree-item-background-no-image,
.ts-server-tree-item-leaf.spacer .ts-server-tree-item-background-image {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  opacity: 0 !important;
}
.ts-server-tree-item-leaf.spacer .ts-server-tree-item-node-content {
  padding-left: 8px !important;
  padding-right: 8px !important;
  justify-content: center !important;
}
.ts-server-tree-item-leaf.spacer > .ts-server-tree-item-node .ts-server-tree-item-text {
  color: #8e9297 !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.04em !important;
  font-style: normal !important;
  text-align: left !important;
  padding-left: 4px !important;
  padding-right: 4px !important;
  position: relative !important;
  display: block !important;
  line-height: 16px !important;
}
.ts-server-tree-item-leaf.spacer > .ts-server-tree-item-node .ts-server-tree-item-text.centered {
  text-align: center !important;
}
.ts-server-tree-item-leaf.spacer > .ts-server-tree-item-node .ts-server-tree-item-text.right {
  text-align: right !important;
}
.ts-server-tree-item-leaf.spacer > .ts-server-tree-item-node .ts-server-tree-item-text::before {
  display: none !important;
  content: none !important;
}
.ts-server-tree-item-leaf.spacer:hover > .ts-server-tree-item-node .ts-server-tree-item-text {
  color: #dcddde !important;
}

/* Channels: Flat Discord Rows */
.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-item-highlight,
.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-item-highlight-extra,
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-no-image {
  border-radius: 4px !important;
  top: 1px !important;
  bottom: 1px !important;
  left: 6px !important;
  right: 6px !important;
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  transition: background-color 0.08s ease !important;
}

.ts-server-tree-item-leaf.channel:not(.spacer):hover .tsv-item-highlight,
.ts-server-tree-item-leaf.channel:not(.spacer):hover .ts-server-tree-item-background-no-image {
  background: rgba(79, 84, 92, 0.32) !important;
  opacity: 1 !important;
  top: 1px !important;
  bottom: 1px !important;
  left: 6px !important;
  right: 6px !important;
}

.ts-server-tree-item-leaf.channel:not(.spacer).tsv-selected .tsv-item-highlight,
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-active .tsv-item-highlight,
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-selected .ts-server-tree-item-background-no-image,
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-active .ts-server-tree-item-background-no-image {
  background: rgba(79, 84, 92, 0.6) !important;
  opacity: 1 !important;
  top: 1px !important;
  bottom: 1px !important;
  left: 6px !important;
  right: 6px !important;
}

.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-text {
  color: #8e9297 !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  text-shadow: none !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer):hover .ts-server-tree-item-text {
  color: #dcddde !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-selected .ts-server-tree-item-text,
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-active .ts-server-tree-item-text {
  color: #ffffff !important;
  font-weight: 600 !important;
}

.ts-server-tree-channel-info {
  color: #72767d !important;
  font-size: 12px !important;
  margin-left: 2px !important;
}

.ts-server-tree-item-leaf.channel:not(.spacer) .tsv-item-accessory {
  color: #72767d !important;
  --tsv-icon-base: #72767d !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer):hover .tsv-item-accessory {
  color: #b9bbbe !important;
  --tsv-icon-base: #b9bbbe !important;
}

/* Voice Channel Participants: circular avatars + solid #43b581 green speaking ring */
.ts-server-tree-item-leaf.client .tsv-item-highlight {
  border-radius: 4px !important;
  top: 1px !important;
  bottom: 1px !important;
  left: 16px !important;
  right: 6px !important;
  border: none !important;
}
.ts-server-tree-item-leaf.client:hover .tsv-item-highlight {
  background: rgba(79, 84, 92, 0.28) !important;
  opacity: 1 !important;
}
.ts-server-tree-item-leaf.client.tsv-selected .tsv-item-highlight,
.ts-server-tree-item-leaf.client.tsv-active .tsv-item-highlight {
  background: rgba(79, 84, 92, 0.5) !important;
  opacity: 1 !important;
}
.ts-server-tree-item-leaf.client .ts-server-tree-item-text {
  color: #8e9297 !important;
  font-size: 14px !important;
  font-weight: 500 !important;
}
.ts-server-tree-item-leaf.client:hover .ts-server-tree-item-text,
.ts-server-tree-item-leaf.client.self .ts-server-tree-item-text {
  color: #dcddde !important;
}
.ts-server-tree-item-node-content.channel {
  padding-left: 10px !important;
  padding-right: 8px !important;
}
.ts-server-tree-item-node-content.client {
  padding-left: 26px !important;
  padding-right: 8px !important;
}

.ts-server-tree-icon.client,
.ts-server-tree-icon.client:not(.compact) {
  width: 24px !important;
  height: 24px !important;
  min-width: 24px !important;
  min-height: 24px !important;
  border-radius: 50% !important;
  box-shadow: none !important;
  margin-right: 8px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}
.ts-server-tree-icon.client .tsv-avatar {
  width: 24px !important;
  height: 24px !important;
  min-width: 24px !important;
  min-height: 24px !important;
  border-radius: 50% !important;
}
.ts-server-tree-icon.client .ts-server-tree-client-talking {
  display: none !important;
}
.ts-server-tree-icon.client.talking {
  box-shadow: 0 0 0 2px #43b581 !important;
  border-radius: 50% !important;
}
.ts-server-tree-item-leaf.client:has(.talking) .ts-server-tree-item-text {
  color: #ffffff !important;
  font-weight: 600 !important;
}

/* Server Status Bar -> Discord Voice Controls Bar directly above 52px User Dock */
.tsv-activity-main .tsv-footer:has(.ts-server-status-bar) {
  background: #292b2f !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
  min-height: 44px !important;
  height: 44px !important;
  flex-basis: 44px !important;
}
.tsv-activity-main .tsv-footer::before {
  display: none !important;
}
.ts-server-status-bar {
  background: #292b2f !important;
  padding: 0 8px !important;
  height: 44px !important;
  min-height: 44px !important;
  max-height: 44px !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  flex-wrap: nowrap !important;
}
.ts-server-status-bar .tsv-tool-buttons {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 3px !important;
  flex-wrap: nowrap !important;
  min-width: 0 !important;
}
.ts-server-status-bar .tsv-flex-grow {
  min-width: 2px !important;
}
.ts-server-status-bar .tsv-tool-button {
  background: #36393f !important;
  border-radius: 4px !important;
  height: 28px !important;
  min-width: 26px !important;
  padding: 0 5px !important;
  margin: 0 !important;
  flex-shrink: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #dcddde !important;
  --tsv-icon-base: #b9bbbe !important;
  --tsv-icon-tint: #b9bbbe !important;
}
.ts-server-status-bar .tsv-tool-button:hover {
  background: #40444b !important;
  color: #ffffff !important;
  --tsv-icon-base: #ffffff !important;
  --tsv-icon-tint: #ffffff !important;
}
/* Keep informative buttons flush-right cleanly inside Voice strip */
.tsv-view.tsv-activity:has(.tsv-activity-detail):not(:has(.tsv-settings)) .ts-server-informative-buttons {
  margin-right: 0 !important;
}
/* Discord green tint for screenshare / constructive button */
.ts-server-status-constructive-buttons .tsv-tool-button.tsv-font-attention {
  --tsv-icon-base: #3ba55c !important;
  --tsv-icon-tint: #3ba55c !important;
  color: #dcddde !important;
}
.ts-server-status-constructive-buttons .tsv-tool-button.tinted.filled {
  background: #36393f !important;
  --tsv-icon-base: #dcddde !important;
  --tsv-icon-tint2: #dcddde !important;
  color: #dcddde !important;
}

/* ==========================================================================
   Column 3: Main Chat & Detail View (#36393f) — Flat Discord Messages
   ========================================================================== */
.tsv-activity-detail,
.tsv-activity-detail .tsv-body,
.tsv-activity-detail .tsv-body-background,
.ts-chat,
.ts-chat-view,
.ts-chat-container {
  background: #36393f !important;
  --body-bg: #36393f;
  --body-bg-contrast: #2f3136;
}

.tsv-activity-detail .tsv-header,
.tsv-activity-detail .tsv-header::before,
.tsv-activity-detail .tsv-header-backdrop {
  background-color: #36393f !important;
}
.tsv-activity-detail .tsv-header {
  border-bottom: none !important;
}

.tsv-activity-detail .tsv-content-header-bar {
  height: 48px !important;
  min-height: 48px !important;
  max-height: 48px !important;
  background: #36393f !important;
  border-bottom: 1px solid #26282c !important;
  box-shadow: 0 1px 0 rgba(4, 4, 5, 0.2), 0 1.5px 0 rgba(6, 6, 7, 0.05) !important;
  padding: 0 12px !important;
}

.tsv-content-header-item {
  font-size: 16px !important;
  font-weight: 700 !important;
  color: #ffffff !important;
}

.tsv-header-bar-below-tools .tsv-content-header-item,
.tsv-header .tsv-tool-button {
  --tsv-icon-base: #b9bbbe !important;
}
.tsv-header-bar-below-tools .tsv-content-header-item:hover,
.tsv-header .tsv-tool-button:hover {
  --tsv-icon-base: #dcddde !important;
}

/* Segmented control (Info / Chat toggle) -> crisp flat Discord pills */
.tsv-content-header-bar .tsv-segmented-control {
  background: #292b2f !important;
  border-radius: 4px !important;
  padding: 2px !important;
  gap: 2px !important;
}
.tsv-content-header-bar .tsv-segmented-button {
  padding: 0 8px !important;
  min-height: 26px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: #b9bbbe !important;
  border-radius: 3px !important;
}
.tsv-content-header-bar .tsv-segmented-button.active {
  background: #40444b !important;
  color: #ffffff !important;
  border-radius: 3px !important;
}

/* Flat Discord Messages (NO BUBBLES, aligned 40px round avatars!) */
.ts-chat-room-event-detailed {
  padding-left: 16px !important;
  padding-right: 16px !important;
  padding-top: 2px !important;
  padding-bottom: 2px !important;
  --tsv-timestamp-width: 56px !important;
  --tsv-chat-link-color: #00aff4 !important;
  transition: background-color 0.05s ease !important;
}

.ts-chat-room-event-detailed.group-start {
  margin-top: 14px !important;
  padding-top: 4px !important;
}

.ts-chat-room-event-detailed:not(.is-system):hover {
  background-color: rgba(4, 4, 5, 0.07) !important;
}

.ts-chat-room-event-detailed .ts-chat-room-event-bubble,
.ts-chat-room-event-detailed.ownclient .ts-chat-room-event-bubble,
.ts-chat-room-event-detailed:not(.ts-currently-referencing) .ts-chat-room-event-bubble {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin-right: 0 !important;
  color: #dcddde !important;
}
.ts-chat-room-event-detailed .ts-chat-room-event-bubble::before {
  display: none !important;
  content: none !important;
}

.ts-chat-room-event-detailed.isPending .ts-chat-room-event-bubble:not(.deleted) {
  background: transparent !important;
  color: #8e9297 !important;
}
.ts-chat-room-event-detailed.isError .ts-chat-room-event-bubble:not(.deleted) {
  background: transparent !important;
  color: #ed4245 !important;
}

.ts-chat-room-event-detailed:has(.self-mention),
.ts-chat-room-event-detailed.has-self-mention {
  background-color: rgba(250, 166, 26, 0.1) !important;
  box-shadow: inset 2px 0 0 #faa61a !important;
}
.ts-chat-room-event-detailed .ts-chat-room-event-bubble.self-mention {
  background: transparent !important;
}

.ts-chat-room-event-detailed.ts-currently-referencing,
.ts-chat-room-event-detailed.ts-chat-room-event-selected {
  background-color: rgba(88, 101, 242, 0.12) !important;
  box-shadow: inset 2px 0 0 #5865f2 !important;
}
.ts-chat-room-event-detailed.ts-currently-referencing .ts-chat-room-event-bubble {
  background: transparent !important;
}

/* 40px Circular Avatar (exact 40x40 square aspect + rounded 50%) */
.ts-chat-room-event-detailed .ts-chat-room-event-sender-avatar-wrapper {
  width: 40px !important;
  height: 40px !important;
  margin-right: 16px !important;
  flex-shrink: 0 !important;
}
.ts-chat-room-event-detailed .ts-chat-room-event-sender-avatar {
  width: 40px !important;
  height: 40px !important;
  min-width: 40px !important;
  min-height: 40px !important;
  border-radius: 50% !important;
  margin: 2px 0 0 0 !important;
  overflow: visible !important;
  --tsv-icon-scale: 1.8 !important;
}
.ts-chat-room-event-detailed .ts-chat-room-event-sender-avatar .tsv-avatar {
  width: 40px !important;
  height: 40px !important;
  min-width: 40px !important;
  min-height: 40px !important;
  border-radius: 50% !important;
}
.ts-chat-room-event-detailed.group-start {
  min-height: 48px !important;
}

.ts-chat-room-event-detailed .ts-chat-message-header {
  height: 22px !important;
  line-height: 22px !important;
  margin-bottom: 2px !important;
  margin-top: 0 !important;
}

.ts-chat-room-event-detailed .ts-chat-message-sender-name {
  font-size: 15px !important;
  font-weight: 500 !important;
  line-height: 22px !important;
}
.ts-chat-room-event-detailed .ts-chat-message-sender-name:hover {
  text-decoration: underline !important;
  opacity: 1 !important;
}

.ts-chat-room-event-detailed .ts-timestamp {
  color: #72767d !important;
  font-size: 12px !important;
  font-weight: 400 !important;
  text-transform: none !important;
  margin-left: 8px !important;
}

.ts-chat-room-event-detailed .ts-chat-room-event-body {
  margin-top: 0 !important;
  margin-bottom: 1px !important;
  padding-left: 0 !important;
}

.ts-chat-room-event-detailed:not(.is-system):hover .ts-chat-room-event-timestamp {
  background: transparent !important;
  color: #72767d !important;
  font-size: 11px !important;
}

.ts-chat-room-event-detailed .ts-chat-message-content {
  font-size: 15px !important;
  line-height: 1.375rem !important;
  color: #dcddde !important;
}

.ts-chat-room-event-detailed .ts-chat-room-event-bubble a {
  color: #00aff4 !important;
  text-decoration: none !important;
}
.ts-chat-room-event-detailed .ts-chat-room-event-bubble a:hover {
  text-decoration: underline !important;
}

.ts-parsed-text-content .md-mention {
  background: rgba(88, 101, 242, 0.3) !important;
  color: #dee0fc !important;
  border-radius: 3px !important;
  padding: 0 2px !important;
  font-weight: 500 !important;
}
.ts-parsed-text-content .md-mention:hover {
  background: #5865f2 !important;
  color: #ffffff !important;
}

.cm-editor.md-dark,
.offline-preview.md-dark {
  --_md-bg: #2f3136 !important;
  --_md-fg: #dcddde !important;
  --_md-accent: #5865f2 !important;
  --_md-muted: #72767d !important;
  --_md-surface: #2f3136 !important;
  --_md-border: #202225 !important;
  --_md-link: #00aff4 !important;
  --_md-inline-code-bg: #2f3136 !important;
  --_md-inline-code-fg: #dcddde !important;
  --_md-blockquote-fg: #dcddde !important;
  --_md-blockquote-border: #4f545c !important;
  --_md-code-bg: #2f3136 !important;
  --_md-code-bg-alt: #2f3136 !important;
  --_md-code-fg: #b9bbbe !important;
  --_md-code-border: #202225 !important;
  --_md-code-lineno: #72767d !important;
  --_md-table-border: #202225 !important;
  --_md-table-header-bg: #292b2f !important;
  --_md-table-hover-bg: #34373c !important;
}

.ts-parsed-text-content .md-codeblock,
.ts-parsed-text-content pre {
  background: #2f3136 !important;
  border: 1px solid #202225 !important;
  border-radius: 4px !important;
}
.ts-parsed-text-content .md-spoiler:not([visible]) {
  background-color: #202225 !important;
}

/* System messages: horizontal flex row with timestamp neatly aligned */
.ts-chat-room-event-detailed.is-system .ts-chat-message-system-body {
  background: transparent !important;
  border-radius: 0 !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 10px !important;
  padding: 2px 0 !important;
}
.ts-chat-room-event-detailed.is-system .ts-chat-message-system-time {
  color: #72767d !important;
  font-size: 11px !important;
  margin: 0 !important;
  order: 2 !important;
  margin-left: auto !important;
}
.ts-chat-room-event-detailed.is-system .ts-chat-message-system-body-contents {
  color: #8e9297 !important;
  font-size: 14px !important;
  order: 1 !important;
}
.ts-chat-room-event-detailed.is-system .ts-chat-message-system-body-contents strong {
  color: #ffffff !important;
  font-weight: 500 !important;
}

.ts-chat-day-start {
  color: #72767d !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
  margin: 16px 16px 4px 16px !important;
  padding-top: 8px !important;
}

.ts-chat-message-attachment .ts-chat-message-attachment-inner,
.ts-chat-message-attachment-myts-file {
  background: #2f3136 !important;
  border: 1px solid #202225 !important;
  border-radius: 8px !important;
}

.ts-chat-quick-actions::before {
  background-color: #36393f !important;
  border: 1px solid #202225 !important;
  border-radius: 4px !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.24) !important;
  opacity: 1 !important;
}

/* ==========================================================================
   Chat Input Box (#40444b, clean Discord look)
   ========================================================================== */
.ts-chat-input-container {
  background-color: #40444b !important;
  border: none !important;
  border-radius: 8px !important;
  box-shadow: none !important;
  margin: 0 16px 16px 16px !important;
  width: calc(100% - 32px) !important;
  min-width: calc(100% - 32px) !important;
  max-width: calc(100% - 32px) !important;
  align-self: stretch !important;
  box-sizing: border-box !important;
  --body-bg: #40444b !important;
  --body-bg-contrast: #2f3136 !important;
}
.ts-chat-input-container.focus,
.ts-chat-input-container:focus-within,
.ts-chat-input-container:hover {
  border: none !important;
  box-shadow: none !important;
  background-color: #40444b !important;
}
.ts-chat-input-container-content,
.ts-chat-input-container-inner {
  background-color: transparent !important;
  --ts-chat-background-color: #40444b !important;
  text-align: left !important;
}
.ts-chat-input-container-content {
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: center !important;
  width: 100% !important;
}
.ts-chat-input-container-content-inner {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: flex-start !important;
  width: 100% !important;
  padding: 10px 12px 10px 16px !important;
  min-height: 44px !important;
  box-sizing: border-box !important;
}
.ts-chat-input-container-actions {
  margin: 0 0 0 8px !important;
  height: 28px !important;
  align-items: center !important;
}
.ts-chat-input-container-inner,
.ts-chat-input-container-content-inner > .tsv-flex-grow {
  flex: 1 1 auto !important;
  min-width: 0 !important;
}
.ts-chat-input-container .ts-chat-input-textarea-inner,
.ts-chat-input-container .ts-chat-input-textarea-inner-editor,
.ts-chat-input-container .cm-editor,
.ts-chat-input-container .cm-scroller,
.ts-chat-input-container .cm-content,
.ts-chat-input-container .cm-line {
  background: transparent !important;
  color: #dcddde !important;
  text-align: left !important;
}
.ts-chat-input-container .cm-placeholder,
.ts-chat-input-container .ts-chat-input-textarea-inner-editor.is-empty::before {
  color: #72767d !important;
  text-align: left !important;
  left: 0 !important;
}

/* Collapse TS6 formatting bar (.ts-chat-input-edit-toolbar) cleanly unless text is selected -> 1:1 Discord input box! */
.ts-chat-input-container .ts-chat-input-toolbar,
.ts-chat-input-container .ts-chat-input-edit-toolbar {
  background: #2f3136 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
  border-radius: 8px 8px 0 0 !important;
  max-height: 0 !important;
  min-height: 0 !important;
  height: 0 !important;
  padding: 0 10px !important;
  margin: 0 !important;
  border-bottom-width: 0 !important;
  overflow: hidden !important;
  opacity: 0 !important;
  transition: max-height 0.14s ease, height 0.14s ease, opacity 0.14s ease !important;
}
.ts-chat-input-container:has(.cm-selectionBackground) .ts-chat-input-toolbar,
.ts-chat-input-container:has(.cm-selectionBackground) .ts-chat-input-edit-toolbar,
.ts-chat-input-container .ts-chat-input-edit-toolbar:hover {
  max-height: 36px !important;
  height: 30px !important;
  padding: 3px 10px !important;
  border-bottom-width: 1px !important;
  opacity: 1 !important;
}

.ts-chat-input-container-actions * {
  --tsv-icon-base: #b9bbbe !important;
}
.ts-chat-input-container-actions *:hover {
  --tsv-icon-base: #dcddde !important;
}
.ts-chat-input-container-actions .ts-chat-send-button .tsv-icon-base-fill,
.ts-chat-input-container-actions .ts-chat-send-button .tsv-icon-base-stroke {
  fill: #b9bbbe !important;
}
.ts-chat-input-container-actions .ts-chat-send-button:not(.disabled):hover .tsv-icon-base-fill,
.ts-chat-input-container-actions .ts-chat-send-button:not(.disabled):hover .tsv-icon-base-stroke {
  fill: #5865f2 !important;
}

/* ==========================================================================
   Voice / Video Grid (Discord Stage) & Context Menus, Modals, Badges
   ========================================================================== */
.video-stream:not(.is-fullscreen) {
  background-color: #18191c !important;
  border: 2px solid transparent !important;
  border-radius: 8px !important;
  outline: none !important;
}
.video-stream:not(.is-fullscreen).show-outline,
.video-stream:not(.is-fullscreen):not(.setup-stream__preview).active {
  border-color: #43b581 !important;
  box-shadow: inset 0 0 0 1px #43b581 !important;
}
.video-stream:not(.is-fullscreen):not(.setup-stream__preview):hover {
  border-color: #4f545c !important;
}

.tsv-badge-count {
  background: #ed4245 !important;
  color: #ffffff !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  padding: 0 4px !important;
  min-width: 16px !important;
  height: 16px !important;
  line-height: 16px !important;
  text-align: center !important;
}

::-webkit-scrollbar {
  width: 8px !important;
  height: 8px !important;
}
.ts-server-tree-wrapper ::-webkit-scrollbar {
  width: 4px !important;
}
.ts-server-tree-wrapper ::-webkit-scrollbar-track {
  background: transparent !important;
}
::-webkit-scrollbar-track {
  background: #2e3338 !important;
  border-radius: 4px !important;
}
::-webkit-scrollbar-thumb,
.ts-chunk-scroll-track__thumb {
  background: #202225 !important;
  border-radius: 4px !important;
}

.tsv-context-menu,
.ts-context-menu,
.ts-false-context-menu,
.ts-presence-menu {
  background: #18191c !important;
  border-radius: 4px !important;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.24) !important;
}
.tsv-context-menu .tsv-item:hover .tsv-item-highlight,
.tsv-context-menu .tsv-item.tsv-selected .tsv-item-highlight,
.tsv-context-menu .tsv-item.focused .tsv-item-highlight,
.ts-context-menu .tsv-item:hover .tsv-item-highlight,
.ts-context-menu .tsv-item.tsv-selected .tsv-item-highlight,
.ts-context-menu .tsv-item.focused .tsv-item-highlight,
.ts-false-context-menu .tsv-item:hover .tsv-item-highlight,
.ts-false-context-menu .tsv-item.tsv-selected .tsv-item-highlight,
.ts-false-context-menu .tsv-item.focused .tsv-item-highlight {
  background: #5865f2 !important;
  border-radius: 2px !important;
}
.ts-context-menu .ts-context-menu-action:hover,
.ts-false-context-menu .ts-context-menu-action:hover {
  background: #5865f2 !important;
  color: #ffffff !important;
}
.tsv-context-menu .tsv-item:hover .tsv-item-text,
.tsv-context-menu .tsv-item.tsv-selected .tsv-item-text,
.tsv-context-menu .tsv-item.focused .tsv-item-text,
.ts-context-menu .tsv-item:hover .tsv-item-text,
.ts-context-menu .tsv-item.tsv-selected .tsv-item-text,
.ts-context-menu .tsv-item.focused .tsv-item-text,
.ts-false-context-menu .tsv-item:hover .tsv-item-text,
.ts-false-context-menu .tsv-item.tsv-selected .tsv-item-text,
.ts-false-context-menu .tsv-item.focused .tsv-item-text {
  color: #ffffff !important;
}
.tsv-context-menu .tsv-item:hover,
.tsv-context-menu .tsv-item.tsv-selected,
.tsv-context-menu .tsv-item.focused,
.ts-context-menu .tsv-item:hover,
.ts-context-menu .tsv-item.tsv-selected,
.ts-context-menu .tsv-item.focused,
.ts-false-context-menu .tsv-item:hover,
.ts-false-context-menu .tsv-item.tsv-selected,
.ts-false-context-menu .tsv-item.focused {
  --tsv-icon-base: #ffffff !important;
  --tsv-icon-tint: #ffffff !important;
}

.tsv-button-filled,
.tsv-button-hero {
  background: #5865f2 !important;
  border-radius: 3px !important;
  border: none !important;
  color: #ffffff !important;
  box-shadow: none !important;
  animation: none !important;
}
.tsv-button-filled:hover,
.tsv-button-hero:hover {
  background: #4752c4 !important;
}
.tsv-button-filled.tsv-is-destructive {
  background: #ed4245 !important;
}
.tsv-button-filled.tsv-is-destructive:hover {
  background: #c03537 !important;
}

.ts-toggle {
  border-radius: 14px !important;
}
.ts-toggle.checked {
  background: #3ba55c !important;
  border-color: #3ba55c !important;
}
.ts-toggle-inner.checked::after {
  background: #ffffff !important;
}

.tsv-modal-overlay .tsv-modal-container {
  background: #36393f !important;
  border-radius: 5px !important;
  box-shadow: 0 0 0 1px rgba(32, 34, 37, 0.6), 0 2px 10px 0 rgba(0, 0, 0, 0.2) !important;
}
.tsv-settings-categories.not-in-sidebar {
  background: #2f3136 !important;
}
.tsv-settings-categories.not-in-sidebar .tsv-item.tsv-selected {
  background: rgba(79, 84, 92, 0.6) !important;
  border-radius: 4px !important;
  --tsv-icon-base: #ffffff !important;
  --tsv-icon-fill: #ffffff !important;
}
.tsv-activity-detail .tsv-search-input::placeholder {
  color: #72767d !important;
  font-size: 14px !important;
}
*:focus-visible {
  outline: 2px solid #00aff4 !important;
  outline-offset: 1px !important;
}
'''

GUILD_RAIL_CSS = r'''/* ==========================================================================
   72px Discord Guild Rail (Zero Z.< / (+) / (slash) Artifacts!)
   ========================================================================== */
.sidebar-pane-layout,
.tsv-sidebar {
  flex: 0 0 72px !important;
  width: 72px !important;
  min-width: 72px !important;
  max-width: 72px !important;
  background: #202225 !important;
  border-right: none !important;
}

.tsv-sidebar .tsv-body-background,
.tsv-sidebar .tsv-sidebar-content {
  background: #202225 !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
  overflow-x: hidden !important;
  scrollbar-width: none !important;
}
.tsv-sidebar .tsv-sidebar-content::-webkit-scrollbar {
  display: none !important;
}

/* Header: crisp 22px "DISCORD" strip + 48x48 Discord Clyde Home/Search button + divider pill */
.tsv-sidebar-header {
  background: #202225 !important;
  padding: 0 !important;
  border-bottom: none !important;
  position: relative !important;
}

.tsv-sidebar-header .tsv-title-bar {
  height: 22px !important;
  min-height: 22px !important;
  max-height: 22px !important;
  padding: 0 22px 0 8px !important;
  justify-content: flex-start !important;
  align-items: center !important;
  position: relative !important;
}

/* Notifications bell button top-right of 22px DISCORD header — always accessible, clean subtle Discord icon */
.tsv-sidebar-header .tsv-title-bar .tsv-action[data-v-step="3"] {
  position: absolute !important;
  right: 5px !important;
  top: 3px !important;
  opacity: 0.72 !important;
  width: 16px !important;
  height: 16px !important;
  min-width: 16px !important;
  padding: 0 !important;
  z-index: 4 !important;
  cursor: pointer !important;
}
.tsv-sidebar-header .tsv-title-bar .tsv-action[data-v-step="3"]:hover {
  opacity: 1 !important;
}
.tsv-sidebar-header .tsv-title-bar .tsv-action[data-v-step="3"] .tsv-magnify {
  position: relative !important;
  width: 14px !important;
  height: 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-sidebar-header .tsv-title-bar .tsv-action[data-v-step="3"] svg {
  opacity: 0 !important;
}
.tsv-sidebar-header .tsv-title-bar .tsv-action[data-v-step="3"] .tsv-magnify::after {
  content: "";
  position: absolute;
  width: 13px;
  height: 13px;
  background-color: #8e9297;
  -webkit-mask-image: url("icons/discord-bell.svg");
  mask-image: url("icons/discord-bell.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-sidebar-header .tsv-title-bar .tsv-action[data-v-step="3"]:hover .tsv-magnify::after {
  background-color: #ffffff;
}

.tsv-sidebar .ts-title-logo {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  width: auto !important;
  padding: 0 !important;
  margin: 0 !important;
}
.tsv-sidebar .ts-title-logo > * {
  display: none !important;
}
.tsv-sidebar .ts-title-logo::after {
  content: "DISCORD";
  font-family: var(--tsv-font-family);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: #72767d;
  line-height: 1;
  pointer-events: none;
}

/* Search row -> Discord Clyde 48x48 circular Home / Quick Switcher button */
.tsv-sidebar-header > .tsv-bar:not(.tsv-title-bar) {
  min-height: 56px !important;
  padding: 4px 0 8px 0 !important;
  justify-content: center !important;
  position: relative !important;
}

/* Iconic 32px x 2px Discord divider line below Home icon */
.tsv-sidebar-header > .tsv-bar:not(.tsv-title-bar)::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 2px;
  background: #2f3136;
  border-radius: 1px;
  pointer-events: none;
}

.tsv-sidebar .tsv-search-bar {
  width: 48px !important;
  height: 48px !important;
  min-width: 48px !important;
  max-width: 48px !important;
  min-height: 48px !important;
  margin: 0 auto !important;
  padding: 0 !important;
  border-radius: 50% !important;
  background: #36393f !important;
  border: none !important;
  box-shadow: none !important;
  position: relative !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  transition: border-radius 0.15s ease, background-color 0.15s ease !important;
}

.tsv-sidebar .tsv-search-bar:hover,
.tsv-sidebar .tsv-search-bar.tsv-active {
  border-radius: 16px !important;
  background: #5865f2 !important;
}

/* Hide any built-in children visually EXCEPT keep clickable search input & collapsed menu toggle functional! */
.tsv-sidebar:not(.tsv-sidebar-collapsed) .tsv-search-bar > *:not(.tsv-search-input) {
  display: none !important;
}
.tsv-sidebar .tsv-search-bar .tsv-search-input {
  position: absolute !important;
  inset: 0 !important;
  width: 48px !important;
  height: 48px !important;
  opacity: 0 !important;
  cursor: pointer !important;
  z-index: 5 !important;
}

.tsv-sidebar .tsv-search-bar::after {
  content: "";
  width: 28px;
  height: 28px;
  background-color: #dcddde;
  -webkit-mask-image: url("icons/discord-logo.svg");
  mask-image: url("icons/discord-logo.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
  transition: background-color 0.15s ease !important;
}
.tsv-sidebar .tsv-search-bar:hover::after,
.tsv-sidebar .tsv-search-bar.tsv-active::after {
  background-color: #ffffff;
}

/* Hide ONLY text-clutter ("З.<", "К.<", "Г...", empty "Нет чатов" placeholder, promo text) — NEVER hide clickable controls! */
.tsv-sidebar .tsv-search-bar:focus-within .tsv-search-input,
.tsv-sidebar .tsv-search-bar.tsv-active .tsv-search-input,
.tsv-sidebar .tsv-search-bar .tsv-search-input:focus {
  position: fixed !important;
  inset: auto !important;
  left: 78px !important;
  top: 26px !important;
  width: 310px !important;
  height: 36px !important;
  opacity: 1 !important;
  background: #202225 !important;
  border: 1px solid #5865f2 !important;
  border-radius: 6px !important;
  padding: 0 12px !important;
  color: #ffffff !important;
  font-size: 13px !important;
  cursor: text !important;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.45) !important;
  z-index: 1001 !important;
}

/* Keep Quick-Switcher / Location Navigator dropdown full readable width when opened! */
.tsv-sidebar .tsv-location-navigator {
  position: fixed !important;
  left: 78px !important;
  top: 68px !important;
  width: 310px !important;
  max-height: 70vh !important;
  background: #18191c !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 6px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
  padding: 6px !important;
  z-index: 999 !important;
}
.tsv-sidebar .tsv-location-response {
  position: fixed !important;
  left: 78px !important;
  top: 68px !important;
  width: 310px !important;
  background: #18191c !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 6px !important;
  padding: 8px 12px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
  z-index: 999 !important;
}
.tsv-sidebar .tsv-location-navigator .tsv-item-text {
  display: block !important;
  font-size: 13px !important;
  color: #dcddde !important;
}
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item {
  width: 100% !important;
  min-height: 34px !important;
  height: 34px !important;
  padding: 0 8px !important;
  margin: 1px 0 !important;
  justify-content: flex-start !important;
  border-radius: 4px !important;
}
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item:hover {
  background: #40444b !important;
}
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-action-primary,
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item-container,
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item-content {
  width: 100% !important;
  min-width: 0 !important;
  max-width: none !important;
  flex: 1 1 auto !important;
  height: 34px !important;
  min-height: 34px !important;
  justify-content: flex-start !important;
  gap: 8px !important;
}
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item .tsv-icon-primary,
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item .tsv-avatar {
  width: 22px !important;
  height: 22px !important;
  min-width: 22px !important;
  min-height: 22px !important;
  border-radius: 50% !important;
  background: transparent !important;
}
.tsv-sidebar .tsv-location-navigator .tsv-activities .tsv-item::after {
  display: none !important;
}

.tsv-sidebar .tsv-sidebar-tab-header,
.tsv-sidebar .tsv-sidebar-tab-header-title,
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item,
.tsv-sidebar .tsv-tabs-slim .tsv-flex-grow,
.tsv-sidebar .tsv-tabs-slim .tsv-bar-item-title-container,
.tsv-sidebar .tsv-tabs-slim .ts-expander,
.tsv-sidebar .ts-resources-group-drop-indicator,
.tsv-sidebar .resources-section-container .ts-matrix-status,
.tsv-sidebar .resources-section-container .ts-room-join-cell-loading,
.tsv-sidebar .resources-section-container li:has(svg[name="empty"]),
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="empty"]),
.tsv-sidebar .ts-join-community__text,
.tsv-sidebar .ts-bookmarks-hidden,
.tsv-sidebar .tsv-item-card,
.tsv-sidebar .tsv-item-active-indicator,
.tsv-sidebar .ts-resize-handle,
.tsv-sidebar .tsv-resize-area-container .tsv-resize-handle,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item-text {
  display: none !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-extended-expander-click-area {
  display: flex !important;
  justify-content: center !important;
  width: 72px !important;
  flex: 0 0 auto !important;
  padding: 0 !important;
  margin: 0 !important;
  cursor: default !important;
}

/* Make the whole 72px Guild Rail scroll smoothly as one unified column */
.tsv-sidebar .ts-resources-group-fixed-size,
.tsv-sidebar .ts-resources-group-fixed-size .tsv-resize-area-container,
.tsv-sidebar .resources-section-container {
  height: auto !important;
  max-height: none !important;
  min-height: 0 !important;
  flex: 0 0 auto !important;
  overflow: visible !important;
}

/* Hover close/disconnect badge on connected server circles — compact accessory box (matches native TS6 flow) + opacity toggle so left-click ALWAYS hits TSButton! */
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory {
  position: absolute !important;
  right: 8px !important;
  top: 0 !important;
  width: auto !important;
  height: auto !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  display: flex !important;
  flex-direction: row-reverse !important;
  align-items: center !important;
  gap: 2px !important;
  pointer-events: auto !important;
  -webkit-app-region: no-drag !important;
  z-index: 50 !important;
}
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-button:has(svg[name="item-close"]),
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"]) {
  display: inline-flex !important;
  opacity: 0 !important;
  position: relative !important;
  width: 18px !important;
  height: 18px !important;
  min-width: 18px !important;
  min-height: 18px !important;
  max-width: 18px !important;
  max-height: 18px !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 50% !important;
  background: #18191c !important;
  border: 2px solid #202225 !important;
  color: #b9bbbe !important;
  align-items: center !important;
  justify-content: center !important;
  box-sizing: border-box !important;
  cursor: pointer !important;
  pointer-events: auto !important;
  -webkit-app-region: no-drag !important;
  z-index: 51 !important;
  transition: opacity 0.1s ease, background-color 0.1s ease !important;
}
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:hover .tsv-item-accessory .tsv-button:has(svg[name="item-close"]),
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:hover .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"]),
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:focus-within .tsv-item-accessory .tsv-button:has(svg[name="item-close"]),
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:focus-within .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"]) {
  opacity: 1 !important;
}
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-button:has(svg[name="item-close"]):hover,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"]):hover {
  opacity: 1 !important;
  background: #ed4245 !important;
  color: #ffffff !important;
}
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-button:has(svg[name="item-close"]) *,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"]) * {
  pointer-events: none !important;
}
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-button:has(svg[name="item-close"]) svg,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"]) svg {
  opacity: 0 !important;
}
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-button:has(svg[name="item-close"])::after,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-accessory .tsv-action-subtle:has(svg[name="item-close"])::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 10px;
  height: 10px;
  transform: translate(-50%, -50%);
  background-color: currentColor;
  -webkit-mask-image: url("icons/discord-close.svg");
  mask-image: url("icons/discord-close.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none !important;
}

/* Discover Communities / Join Community button -> sleek 48x48 Discord Green Compass below server list! */
.tsv-sidebar .ts-join-community {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 2px 0 8px 0 !important;
  margin: 0 !important;
  width: 72px !important;
}
.tsv-sidebar .ts-join-community button,
.tsv-sidebar .ts-join-community .tsv-button {
  width: 48px !important;
  height: 48px !important;
  min-width: 48px !important;
  max-width: 48px !important;
  min-height: 48px !important;
  padding: 0 !important;
  margin: 0 auto !important;
  border-radius: 50% !important;
  background: #36393f !important;
  border: none !important;
  box-shadow: none !important;
  position: relative !important;
  font-size: 0 !important;
  color: transparent !important;
  transition: border-radius 0.15s ease, background-color 0.15s ease !important;
}
.tsv-sidebar .ts-join-community button *,
.tsv-sidebar .ts-join-community .tsv-button * {
  display: none !important;
}
.tsv-sidebar .ts-join-community button::after,
.tsv-sidebar .ts-join-community .tsv-button::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 24px;
  height: 24px;
  transform: translate(-50%, -50%);
  background-color: #3ba55c;
  -webkit-mask-image: url("icons/discord-compass.svg");
  mask-image: url("icons/discord-compass.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
  transition: background-color 0.15s ease;
}
.tsv-sidebar .ts-join-community button:hover,
.tsv-sidebar .ts-join-community .tsv-button:hover {
  border-radius: 16px !important;
  background: #3ba55c !important;
}
.tsv-sidebar .ts-join-community button:hover::after,
.tsv-sidebar .ts-join-community .tsv-button:hover::after {
  background-color: #ffffff;
}

/* Strip .tsv-tabs-slim chrome so Bookmarks/Rooms header action buttons sit cleanly in 72px rail */
.tsv-sidebar .tsv-tabs-slim::before,
.tsv-sidebar .ts-resources-group-fixed-size::before {
  display: none !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-bar-item:first-of-type,
.tsv-sidebar .resources-section-container ul {
  margin: 0 !important;
  padding: 0 !important;
  width: 72px !important;
}
.tsv-sidebar .tsv-tabs-slim {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  min-height: 0 !important;
  height: auto !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-sidebar-header-accessories {
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 4px !important;
  padding: 4px 12px !important;
  margin: 0 !important;
  width: 72px !important;
  box-sizing: border-box !important;
}
.tsv-sidebar .tsv-sidebar-header-accessories > div {
  display: flex !important;
  justify-content: center !important;
  width: auto !important;
  padding: 0 !important;
  margin: 0 !important;
}
.tsv-sidebar .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) > div:has(svg[name="add"]) {
  width: 72px !important;
  order: -3 !important;
  margin-bottom: 4px !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory {
  width: 40px !important;
  height: 40px !important;
  border-radius: 50% !important;
  background: #36393f !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  cursor: pointer !important;
  transition: border-radius 0.15s ease, background-color 0.15s ease !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory svg {
  opacity: 0 !important;
  pointer-events: none !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 17px;
  height: 17px;
  transform: translate(-50%, -50%);
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
  transition: background-color 0.15s ease;
}

/* Bookmarks "+ New Server / Bookmark" -> DISCORD GREEN (+) 48x48 CIRCLE directly under server list! */
.tsv-sidebar .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) > div:has(svg[name="search-hexagon"]) {
  order: -1 !important;
}
.tsv-sidebar .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"]) {
  width: 48px !important;
  height: 48px !important;
  background: #36393f !important;
}
.tsv-sidebar .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"])::after {
  width: 22px;
  height: 22px;
  background-color: #3ba55c;
  -webkit-mask-image: url("icons/discord-plus.svg");
  mask-image: url("icons/discord-plus.svg");
}
.tsv-sidebar .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"]):hover {
  border-radius: 16px !important;
  background: #3ba55c !important;
}
.tsv-sidebar .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"]):hover::after {
  background-color: #ffffff;
}

/* Server Discovery & Chat Discovery ("search-hexagon") -> Sleek Search Circle */
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="search-hexagon"])::after {
  -webkit-mask-image: url("icons/discord-search.svg");
  mask-image: url("icons/discord-search.svg");
  background-color: #b9bbbe;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="search-hexagon"]):hover {
  border-radius: 14px !important;
  background: #3ba55c !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="search-hexagon"]):hover::after {
  background-color: #ffffff;
}

/* Bookmark New Folder ("folder-action") */
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="folder-action"])::after {
  -webkit-mask-image: url("icons/discord-folder-add.svg");
  mask-image: url("icons/discord-folder-add.svg");
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="folder-action"]):hover {
  border-radius: 12px !important;
  background: #5865f2 !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="folder-action"]):hover::after {
  background-color: #ffffff;
}

/* Group Chats Create ("add" without folder-action sibling) -> Distinct Chat Bubble icon */
.tsv-sidebar .tsv-sidebar-header-accessories:not(:has(svg[name="folder-action"])) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"])::after {
  -webkit-mask-image: url("icons/discord-chat.svg");
  mask-image: url("icons/discord-chat.svg");
}
.tsv-sidebar .tsv-sidebar-header-accessories:not(:has(svg[name="folder-action"])) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"]):hover {
  border-radius: 12px !important;
  background: #5865f2 !important;
}
.tsv-sidebar .tsv-sidebar-header-accessories:not(:has(svg[name="folder-action"])) .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"]):hover::after {
  background-color: #ffffff;
}

/* Contacts Add & Join Group Chat cells -> Sleek 40x40 centered Discord circular icon buttons (never override input editor!) */
.tsv-sidebar .resources-section-container ul:has(svg[name="chat-contact-add"]),
.tsv-sidebar .resources-section-container ul:has(svg[name="contact-add"]) {
  width: 72px !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)),
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  padding: 3px 0 !important;
  margin: 0 !important;
  width: 72px !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-action-primary,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-action-primary {
  width: 40px !important;
  height: 40px !important;
  flex: 0 0 40px !important;
  flex-grow: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin: 0 auto !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-container,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-item-container {
  width: 40px !important;
  min-width: 40px !important;
  max-width: 40px !important;
  height: 40px !important;
  min-height: 40px !important;
  flex: 0 0 40px !important;
  flex-grow: 0 !important;
  padding: 0 !important;
  margin: 0 auto !important;
  justify-content: center !important;
  align-items: center !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-item-content {
  width: 40px !important;
  min-width: 40px !important;
  max-width: 40px !important;
  height: 40px !important;
  flex: 0 0 40px !important;
  flex-grow: 0 !important;
  border-radius: 50% !important;
  background: #36393f !important;
  justify-content: center !important;
  align-items: center !important;
  padding: 0 !important;
  margin: 0 !important;
  position: relative !important;
  cursor: pointer !important;
  transition: border-radius 0.15s ease, background-color 0.15s ease !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) svg,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) svg,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-icon,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-icon {
  position: absolute !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content::after {
  content: "";
  position: absolute;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%) !important;
  width: 17px;
  height: 17px;
  background-color: #b9bbbe;
  -webkit-mask-image: url("icons/discord-chat-add.svg");
  mask-image: url("icons/discord-chat-add.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-sidebar .resources-section-container .tsv-resources-group:has(svg[name="contacts"]):not(:has(svg[name="groups"])) .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content::after,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-item-content::after {
  content: "";
  position: absolute;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%) !important;
  width: 17px;
  height: 17px;
  background-color: #b9bbbe;
  -webkit-mask-image: url("icons/discord-user-add.svg");
  mask-image: url("icons/discord-user-add.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)):hover .tsv-item-content,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)):hover .tsv-item-content {
  border-radius: 12px !important;
  background: #5865f2 !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)):hover .tsv-item-content::after,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)):hover .tsv-item-content::after {
  background-color: #ffffff;
}

/* Inline Create Bookmark / Folder / Join Chat input popout outside 72px rail (never match User Dock or Edit Drawer!) */
.tsv-sidebar .resources-section-container ul .tsv-item:has(input):not(.ts-sidebar-tab-sub-panel *),
.tsv-sidebar .resources-section-container .ts-bookmark-entry:has(input):not(.ts-sidebar-tab-sub-panel *),
.tsv-sidebar .resources-section-container .ts-bookmark-folder-box:has(input):not(.ts-sidebar-tab-sub-panel *) {
  position: fixed !important;
  left: 78px !important;
  width: 268px !important;
  min-width: 268px !important;
  height: 42px !important;
  min-height: 42px !important;
  background: #18191c !important;
  border: 1px solid #5865f2 !important;
  border-radius: 6px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.55) !important;
  padding: 4px 10px !important;
  margin: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  z-index: 1002 !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-action-primary,
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-item-container,
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-item-content {
  width: 100% !important;
  min-width: 0 !important;
  max-width: none !important;
  height: 32px !important;
  min-height: 32px !important;
  flex: 1 1 auto !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: flex-start !important;
  gap: 8px !important;
  padding: 0 !important;
  margin: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-icon-primary,
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-icon:not(.ts-text-input-box .tsv-icon),
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-avatar {
  width: 18px !important;
  height: 18px !important;
  min-width: 18px !important;
  min-height: 18px !important;
  margin: 0 4px 0 2px !important;
  border-radius: 0 !important;
  background: transparent !important;
  position: static !important;
  opacity: 1 !important;
  pointer-events: none !important;
  flex: 0 0 18px !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) svg:not(.ts-text-input-box svg) {
  width: 18px !important;
  height: 18px !important;
  opacity: 1 !important;
  position: static !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-item-content::after {
  display: none !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .ts-text-input-box {
  position: relative !important;
  inset: auto !important;
  left: auto !important;
  right: auto !important;
  flex: 1 1 auto !important;
  width: auto !important;
  height: 28px !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .ts-text-input-box .ts-input:not(.ts-input-preview) {
  position: relative !important;
  inset: auto !important;
  width: 100% !important;
  height: 28px !important;
  padding: 0 24px 0 4px !important;
  color: #ffffff !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input) .tsv-item-text {
  display: block !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel {
  position: fixed !important;
  left: 78px !important;
  top: 76px !important;
  width: 286px !important;
  max-height: 75vh !important;
  overflow-y: auto !important;
  background: #18191c !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 8px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.55) !important;
  padding: 10px !important;
  z-index: 1002 !important;
}

/* Remove extra box backgrounds in ResourcesGroup */
.tsv-sidebar .tsv-activities .tsv-item-group::before,
.tsv-sidebar .tsv-activities .tsv-item .tsv-item-highlight {
  display: none !important;
}

/* Guild Icons (.tsv-activities .tsv-item ONLY — never random items or Quick Switcher!) */
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) {
  padding-top: 6px !important;
}

.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item {
  width: 72px !important;
  min-height: 54px !important;
  height: 54px !important;
  padding: 0 !important;
  margin: 2px 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  cursor: pointer !important;
}

.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-action-primary,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-container,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-item-content {
  width: 48px !important;
  min-width: 48px !important;
  max-width: 48px !important;
  height: 48px !important;
  min-height: 48px !important;
  flex: 0 0 48px !important;
  flex-grow: 0 !important;
  padding: 0 !important;
  margin: 0 auto !important;
  justify-content: center !important;
  align-items: center !important;
}

/* Neutralize TS6 .tsv-sidebar-detailed negative icon-primary offset (-6px) across the 72px rail */
.tsv-sidebar :where(.tsv-activities:not(.tsv-location-navigator .tsv-activities), .resources-section-container) :where(.tsv-icon-primary, .tsv-icon-stack, .tsv-avatar) {
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-icon-primary,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item .tsv-avatar {
  width: 48px !important;
  height: 48px !important;
  min-width: 48px !important;
  min-height: 48px !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  border-radius: 50% !important;
  background: #36393f !important;
  overflow: hidden !important;
  transition: border-radius 0.15s ease, background-color 0.15s ease !important;
}

.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:hover .tsv-icon-primary,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:hover .tsv-avatar,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item.tsv-selected .tsv-icon-primary,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item.tsv-selected .tsv-avatar,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item.tsv-active .tsv-icon-primary,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item.tsv-active .tsv-avatar {
  border-radius: 16px !important;
}

/* White pill indicator ONLY on actual guild items (.tsv-activities .tsv-item) */
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item:hover::after {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  background: #ffffff;
  border-radius: 0 4px 4px 0;
  pointer-events: none;
  z-index: 5;
}

.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item.tsv-selected::after,
.tsv-sidebar .tsv-activities:not(.tsv-location-navigator .tsv-activities) .tsv-item.tsv-active::after {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 40px;
  background: #ffffff;
  border-radius: 0 4px 4px 0;
  pointer-events: none;
  z-index: 5;
}

/* Bookmark entries, folders & real contacts/chats -> crisp 48x48 centered guild / DM circles in 72px rail */
.tsv-sidebar .resources-section-container .tsv-item-text,
.tsv-sidebar .resources-section-container .tsv-item-accessory {
  display: none !important;
}
.tsv-sidebar .resources-section-container {
  padding-top: 2px !important;
  border-top: none !important;
  width: 72px !important;
  position: relative !important;
}
.tsv-sidebar .resources-section-container::before {
  content: "";
  display: block;
  width: 32px;
  height: 2px;
  background: #2f3136;
  border-radius: 1px;
  margin: 0 auto 6px auto;
}
.tsv-sidebar .resources-section-container ul.bookmarks,
.tsv-sidebar .resources-section-container .ts-bookmarks-root > div {
  margin: 0 !important;
  padding: 0 !important;
  width: 72px !important;
}
.tsv-sidebar :where(.ts-bookmark-entry, .ts-bookmark-folder-box, .resources-section-container .tsv-item:not(:has(svg[name="empty"])):not(:has(svg[name="chat-contact-add"])):not(:has(svg[name="contact-add"]))):not(:has(input)) {
  width: 72px !important;
  min-height: 54px !important;
  padding: 0 !important;
  margin: 2px 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: relative !important;
  cursor: pointer !important;
}
.tsv-sidebar :where(.ts-bookmark-entry, .ts-bookmark-folder-box, .resources-section-container .tsv-item:not(:has(svg[name="empty"])):not(:has(svg[name="chat-contact-add"])):not(:has(svg[name="contact-add"]))):not(:has(input)) :where(.tsv-action-primary, .tsv-item-container, .tsv-item-content) {
  width: 48px !important;
  min-width: 48px !important;
  max-width: 48px !important;
  height: 48px !important;
  min-height: 48px !important;
  flex: 0 0 48px !important;
  flex-grow: 0 !important;
  padding: 0 !important;
  margin: 0 auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-sidebar .ts-bookmark-entry .tsv-item-highlight,
.tsv-sidebar .ts-bookmark-folder-box .tsv-item-highlight,
.tsv-sidebar .resources-section-container .tsv-item .tsv-item-highlight {
  display: none !important;
}
.tsv-sidebar :where(.ts-bookmark-entry, .ts-bookmark-folder-box, .resources-section-container .tsv-item:not(:has(svg[name="chat-contact-add"])):not(:has(svg[name="contact-add"]))):not(:has(input)) :where(.tsv-icon-primary, .tsv-avatar) {
  width: 48px !important;
  height: 48px !important;
  min-width: 48px !important;
  min-height: 48px !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  border-radius: 50% !important;
  background: #36393f !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: hidden !important;
  transition: border-radius 0.15s ease !important;
}
.tsv-sidebar .ts-bookmark-folder-box:not(:has(input)) .tsv-item-content {
  position: relative !important;
}
.tsv-sidebar .ts-bookmark-folder-box:not(:has(input)) svg {
  opacity: 0 !important;
}
.tsv-sidebar .ts-bookmark-folder-box:not(:has(input)) .tsv-item-content::after {
  content: "";
  position: absolute;
  width: 22px;
  height: 22px;
  background-color: #b9bbbe;
  -webkit-mask-image: url("icons/discord-folder.svg");
  mask-image: url("icons/discord-folder.svg");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-sidebar :where(.ts-bookmark-entry, .ts-bookmark-folder-box, .resources-section-container .tsv-item:not(:has(svg[name="chat-contact-add"])):not(:has(svg[name="contact-add"]))):hover :where(.tsv-icon-primary, .tsv-avatar) {
  border-radius: 16px !important;
}
.tsv-sidebar :where(.ts-bookmark-entry, .ts-bookmark-folder-box, .resources-section-container .tsv-item:not(:has(svg[name="chat-contact-add"])):not(:has(svg[name="contact-add"]))):not(:has(input)):hover::after {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  background: #ffffff;
  border-radius: 0 4px 4px 0;
  pointer-events: none;
}

/* Fallback if .tsv-sidebar > .tsv-footer is NOT teleported (Home / Settings / Slideover / Fullscreen Screenshare; flat non-nested :has()!) */
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer {
  background: #202225 !important;
  height: auto !important;
  min-height: 0 !important;
  max-height: none !important;
  flex-basis: auto !important;
  padding: 8px 0 10px 0 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
  align-items: center !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer::before,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer::before,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer::before,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer::before {
  display: none !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-bar,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-bar,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-bar,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-bar {
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  height: auto !important;
  min-height: 0 !important;
  padding: 0 !important;
  gap: 8px !important;
  width: 100% !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-bar-item,
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-item,
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-item-container,
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-item-content,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-bar-item,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-item,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-item-container,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-item-content,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-bar-item,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-item,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-item-container,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-item-content,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-bar-item,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-item,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-item-container,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-item-content {
  padding: 0 !important;
  margin: 0 !important;
  width: auto !important;
  min-width: 0 !important;
  justify-content: center !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-icon-primary,
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-avatar,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-icon-primary,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-avatar,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-icon-primary,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-avatar,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-icon-primary,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-avatar {
  width: 36px !important;
  height: 36px !important;
  min-width: 36px !important;
  min-height: 36px !important;
  border-radius: 50% !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-action-subtle[data-v-step="2"],
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-action-subtle[data-v-step="2"],
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-action-subtle[data-v-step="2"],
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-action-subtle[data-v-step="2"] {
  width: 36px !important;
  height: 36px !important;
  border-radius: 50% !important;
  background: #2f3136 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-window:not(:has(.tsv-activity-detail)) .tsv-sidebar > .tsv-footer .tsv-item-text,
.tsv-window:not(:has(.tsv-activity-main:not(.tsv-activity-slideover))) .tsv-sidebar > .tsv-footer .tsv-item-text,
.tsv-window:has(.tsv-settings) .tsv-sidebar > .tsv-footer .tsv-item-text,
.tsv-window:has(.screenshare-fullscreen-host.is-active) .tsv-sidebar > .tsv-footer .tsv-item-text {
  display: none !important;
}

/* Default "Discord Dark" keeps Add Server (+), Discover, Bookmarks & Chats accessible in the 72px rail! */
'''

# Channel Banner Variants Toggle
CHANNEL_NO_BANNERS_CSS = r'''/* Channel tree: flat Discord rows without photo banners */
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-image,
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-image-full,
.ts-server-tree-item-has-banner .tsv-item-accessory::before {
  display: none !important;
}
'''

CHANNEL_BANNERS_CSS = r'''/* Channel tree: preserve server channel background art cleanly inside Discord rows! */
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-image-full {
  display: none !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-image {
  display: flex !important;
  border-radius: 4px !important;
  top: 1px !important;
  bottom: 1px !important;
  left: 6px !important;
  right: 6px !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  width: auto !important;
  opacity: 0.78 !important;
  overflow: hidden !important;
  z-index: 0 !important;
  background: #2f3136 !important;
  transition: opacity 0.15s ease, box-shadow 0.15s ease !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer):hover .ts-server-tree-item-background-image {
  opacity: 0.96 !important;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.14) !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-selected .ts-server-tree-item-background-image,
.ts-server-tree-item-leaf.channel:not(.spacer).tsv-active .ts-server-tree-item-background-image {
  opacity: 1 !important;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.24), inset 3px 0 0 #ffffff !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-image img {
  width: 100% !important;
  max-width: 100% !important;
  height: 100% !important;
  left: 0 !important;
  margin-left: 0 !important;
  object-fit: cover !important;
  object-position: center !important;
  -webkit-mask-image: none !important;
  mask-image: none !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-background-image-blur {
  background: linear-gradient(90deg, rgba(47, 49, 54, 0.96) 0%, rgba(47, 49, 54, 0.72) 45%, rgba(47, 49, 54, 0.22) 100%) !important;
  width: 100% !important;
  left: 0 !important;
  right: 0 !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-node {
  position: relative !important;
  z-index: 2 !important;
}
.ts-server-tree-item-leaf.channel:not(.spacer) .ts-server-tree-item-text {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.65) !important;
}
'''

PURE_RAIL_EXTRA = r'''
/* Minimalist "Guild Rail" variant: hides Contacts, Group Chats, Folder-Create, and duplicate search-hexagon
   when connected, while ALWAYS keeping saved voice servers (.ts-bookmark-entry), Green (+) Add Server,
   inline :has(input) creation popouts, and Green Discover Compass clickable and accessible! */
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .ts-bookmarks-hidden,
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .tsv-resources-group:has(svg[name="contacts"]):not(:has(svg[name="bookmark-edit"])),
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .tsv-resources-group:has(svg[name="groups"]):not(:has(svg[name="bookmark-edit"])),
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)),
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)),
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .ts-chat-room-item:not(:has(input)),
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) > div:has(svg[name="search-hexagon"]),
.tsv-sidebar:has(.tsv-activities:not(.is-empty)) .resources-section-container .tsv-sidebar-header-accessories:has(svg[name="folder-action"]) > div:has(svg[name="folder-action"]) {
  display: none !important;
}
'''

WIDE_NAV_CSS = r'''/* ==========================================================================
   Wide Navigation Left Sidebar Variant (#202225) — Keeps Bookmarks/Contacts readable
   ========================================================================== */
.tsv-sidebar,
.tsv-sidebar .tsv-body-background {
  background: #202225 !important;
  --body-bg: #202225;
  --body-bg-contrast: #2f3136;
}
.tsv-sidebar {
  border-right: none !important;
}
.tsv-activity-main {
  border-left: 1px solid #18191c !important;
}
.tsv-sidebar ul {
  margin: 0 !important;
  padding: 0 !important;
  list-style: none !important;
}

.tsv-sidebar-header .tsv-title-bar {
  min-height: 22px !important;
  height: 22px !important;
  padding: 0 10px !important;
  justify-content: flex-start !important;
  gap: 8px !important;
}

.ts-title-logo {
  position: relative !important;
  display: flex !important;
  align-items: center !important;
  padding-left: 0 !important;
}
.ts-title-logo > * {
  display: none !important;
}
.ts-title-logo::after {
  content: "DISCORD";
  font-family: var(--tsv-font-family);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: #8e9297;
  line-height: 1;
}

.tsv-sidebar .tsv-search-bar,
.tsv-sidebar .tsv-location-bar {
  background: #18191c !important;
  border-radius: 4px !important;
  border: none !important;
  box-shadow: none !important;
  min-height: 28px !important;
  padding: 0 8px !important;
}
.tsv-sidebar .tsv-search-bar .tsv-search-input {
  text-align: left !important;
  width: 100% !important;
}
.tsv-sidebar .tsv-search-bar .tsv-search-input::placeholder {
  color: #72767d !important;
  font-size: 13px !important;
}

.tsv-sidebar-tab-header-title,
.tsv-tabs-slim .tsv-bar-item-title {
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.04em !important;
  color: #8e9297 !important;
}

.tsv-activities .tsv-item-group::before {
  display: none !important;
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="empty"]) {
  --tsv-icon-base: #4f545c !important;
  color: #72767d !important;
}
.tsv-sidebar .resources-section-container .tsv-item.tinted {
  --tsv-icon-base: #b9bbbe !important;
  color: #b9bbbe !important;
}
.tsv-activities .tsv-item {
  min-height: 40px !important;
  padding: 4px 12px 4px 14px !important;
  overflow: visible !important;
}
.tsv-activities .tsv-item .tsv-item-highlight {
  left: 8px !important;
  right: 8px !important;
}
.tsv-activities .tsv-item-container {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
  gap: 8px !important;
}
.tsv-activities .tsv-item-content {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 8px !important;
  flex-wrap: nowrap !important;
  min-width: 0 !important;
}
.tsv-activities .tsv-item-text {
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  text-align: left !important;
}
.tsv-activities .tsv-item:hover .tsv-item-highlight {
  background: #2f3136 !important;
  border-radius: 6px !important;
}
.tsv-activities .tsv-item.tsv-selected .tsv-item-highlight,
.tsv-activities .tsv-item.tsv-active .tsv-item-highlight {
  background: #36393f !important;
  border-radius: 6px !important;
}
.tsv-activities .tsv-item.tsv-selected::after,
.tsv-activities .tsv-item.tsv-active::after {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: #ffffff;
  border-radius: 0 4px 4px 0;
  pointer-events: none;
}
.tsv-activities .tsv-item .tsv-icon-primary,
.tsv-activities .tsv-item .tsv-avatar {
  border-radius: 50% !important;
  width: 24px !important;
  height: 24px !important;
  min-width: 24px !important;
  min-height: 24px !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  flex-shrink: 0 !important;
}
.tsv-activities .tsv-item-active-indicator,
.tsv-sidebar .tsv-item-active-indicator {
  display: none !important;
}
/* Clean up empty state & header accessories in Wide Nav */
.tsv-sidebar .tsv-tabs-slim {
  padding: 0 6px !important;
  align-items: center !important;
  gap: 2px !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-bar-item:first-of-type {
  margin-left: 0 !important;
  min-width: 0 !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-sidebar-header-accessories {
  margin-right: 0 !important;
  gap: 2px !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item .tsv-magnify {
  position: relative !important;
  width: 14px !important;
  height: 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item .tsv-magnify svg {
  opacity: 0 !important;
}
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item .tsv-magnify::after {
  content: "";
  position: absolute;
  width: 13px;
  height: 13px;
  background-color: #8e9297;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item .tsv-magnify:has(svg[name="bookmark-edit"])::after {
  -webkit-mask-image: url("icons/discord-bookmark.svg");
  mask-image: url("icons/discord-bookmark.svg");
}
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item .tsv-magnify:has(svg[name="contacts"])::after {
  -webkit-mask-image: url("icons/discord-users.svg");
  mask-image: url("icons/discord-users.svg");
}
.tsv-sidebar .tsv-tabs-slim .tsv-tab-item .tsv-magnify:has(svg[name="groups"])::after {
  -webkit-mask-image: url("icons/discord-chat.svg");
  mask-image: url("icons/discord-chat.svg");
}
.tsv-sidebar .tsv-sidebar-header-accessories {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 4px !important;
  padding: 0 !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory {
  position: relative !important;
  width: 20px !important;
  height: 20px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 4px !important;
  cursor: pointer !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory svg,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) svg,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) svg,
.tsv-sidebar .tsv-title-bar .tsv-action[data-v-step="3"] svg {
  opacity: 0 !important;
  pointer-events: none !important;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory::after,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-item-content::after,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content::after,
.tsv-sidebar .tsv-title-bar .tsv-action[data-v-step="3"] .tsv-magnify::after {
  content: "";
  position: absolute;
  width: 14px;
  height: 14px;
  background-color: #b9bbbe;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-size: contain;
  mask-size: contain;
  pointer-events: none;
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="search-hexagon"])::after {
  -webkit-mask-image: url("icons/discord-search.svg");
  mask-image: url("icons/discord-search.svg");
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="folder-action"])::after {
  -webkit-mask-image: url("icons/discord-folder-add.svg");
  mask-image: url("icons/discord-folder-add.svg");
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:has(svg[name="add"])::after {
  -webkit-mask-image: url("icons/discord-plus.svg");
  mask-image: url("icons/discord-plus.svg");
  background-color: #3ba55c;
}
.tsv-sidebar .tsv-title-bar .tsv-action[data-v-step="3"] .tsv-magnify {
  position: relative !important;
  width: 14px !important;
  height: 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.tsv-sidebar .tsv-title-bar .tsv-action[data-v-step="3"] .tsv-magnify::after {
  -webkit-mask-image: url("icons/discord-bell.svg");
  mask-image: url("icons/discord-bell.svg");
}
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-item-content,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content {
  position: relative !important;
  gap: 8px !important;
}
.tsv-sidebar .resources-section-container .tsv-resources-group:has(svg[name="contacts"]):not(:has(svg[name="groups"])) .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content::after,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="contact-add"]):not(:has(input)) .tsv-item-content::after {
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  -webkit-mask-image: url("icons/discord-user-add.svg");
  mask-image: url("icons/discord-user-add.svg");
}
.tsv-sidebar .resources-section-container .tsv-resources-group:has(svg[name="groups"]) .tsv-item:has(svg[name="chat-contact-add"]):not(:has(input)) .tsv-item-content::after {
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  -webkit-mask-image: url("icons/discord-chat-add.svg");
  mask-image: url("icons/discord-chat-add.svg");
}
.tsv-sidebar .ts-sidebar-tab-sub-panel-accessory:hover {
  background: rgba(79, 84, 92, 0.4) !important;
}
.tsv-sidebar .resources-section-container .tsv-item-active-indicator,
.tsv-sidebar .resources-section-container .tsv-item:has(svg[name="empty"]) {
  display: none !important;
}
.tsv-sidebar .tsv-footer .tsv-item-text {
  margin-left: 8px !important;
}
.tsv-sidebar .ts-join-community {
  padding: 4px 10px 8px 10px !important;
  margin: 0 !important;
}
.tsv-sidebar .ts-join-community__text {
  display: none !important;
}
.tsv-sidebar .ts-join-community button,
.tsv-sidebar .ts-join-community .tsv-button {
  width: 100% !important;
  background: #292b2f !important;
  color: #dcddde !important;
  border: 1px solid rgba(255, 255, 255, 0.06) !important;
  border-radius: 4px !important;
  min-height: 30px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}
.tsv-sidebar .ts-join-community button:hover,
.tsv-sidebar .ts-join-community .tsv-button:hover {
  background: #3ba55c !important;
  color: #ffffff !important;
}
/* Inline Create Bookmark / Folder / Add Contact / Join Chat input row in Wide Nav (prevent icon overlap) */
.tsv-sidebar .resources-section-container ul .tsv-item:has(input):not(.ts-sidebar-tab-sub-panel *) {
  padding: 4px 8px !important;
  min-height: 36px !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input):not(.ts-sidebar-tab-sub-panel *) :where(.tsv-action-primary, .tsv-item-container, .tsv-item-content) {
  width: 100% !important;
  min-width: 0 !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 8px !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input):not(.ts-sidebar-tab-sub-panel *) :where(.tsv-icon-primary, .tsv-icon:not(.ts-text-input-box .tsv-icon), .tsv-avatar) {
  width: 18px !important;
  height: 18px !important;
  min-width: 18px !important;
  flex: 0 0 18px !important;
  position: static !important;
  margin: 0 !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input):not(.ts-sidebar-tab-sub-panel *) .ts-text-input-box {
  position: relative !important;
  inset: auto !important;
  left: auto !important;
  right: auto !important;
  flex: 1 1 auto !important;
  width: auto !important;
  min-width: 0 !important;
  height: 28px !important;
  background: #18191c !important;
  border: 1px solid #5865f2 !important;
  border-radius: 4px !important;
  padding: 0 6px !important;
}
.tsv-sidebar .resources-section-container ul .tsv-item:has(input):not(.ts-sidebar-tab-sub-panel *) .ts-text-input-box .ts-input:not(.ts-input-preview) {
  position: relative !important;
  inset: auto !important;
  width: 100% !important;
  height: 26px !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  color: #ffffff !important;
}
'''

variants = {
    'discord.css': BASE_VARIABLES + '\n' + GUILD_RAIL_CSS + '\n' + DOCK_AND_LAYOUT_CSS + '\n' + ICON_REPLACEMENT_CSS + '\n' + CHANNEL_NO_BANNERS_CSS,
    'discord-banners.css': BASE_VARIABLES + '\n' + GUILD_RAIL_CSS + '\n' + DOCK_AND_LAYOUT_CSS + '\n' + ICON_REPLACEMENT_CSS + '\n' + CHANNEL_BANNERS_CSS,
    'discord-rail.css': BASE_VARIABLES + '\n' + GUILD_RAIL_CSS + '\n' + PURE_RAIL_EXTRA + '\n' + DOCK_AND_LAYOUT_CSS + '\n' + ICON_REPLACEMENT_CSS + '\n' + CHANNEL_NO_BANNERS_CSS,
    'discord-rail-banners.css': BASE_VARIABLES + '\n' + GUILD_RAIL_CSS + '\n' + PURE_RAIL_EXTRA + '\n' + DOCK_AND_LAYOUT_CSS + '\n' + ICON_REPLACEMENT_CSS + '\n' + CHANNEL_BANNERS_CSS,
    'discord-wide.css': BASE_VARIABLES + '\n' + WIDE_NAV_CSS + '\n' + DOCK_AND_LAYOUT_CSS + '\n' + ICON_REPLACEMENT_CSS + '\n' + CHANNEL_NO_BANNERS_CSS,
    'discord-wide-banners.css': BASE_VARIABLES + '\n' + WIDE_NAV_CSS + '\n' + DOCK_AND_LAYOUT_CSS + '\n' + ICON_REPLACEMENT_CSS + '\n' + CHANNEL_BANNERS_CSS,
}

def inline_svg_urls(css_txt):
    cache = {}
    def repl(m):
        rel = m.group(1)
        if rel not in cache:
            svg_p = os.path.join(EXT_DIR, 'icons', rel.replace('/', os.sep))
            if not os.path.isfile(svg_p):
                raise FileNotFoundError(f"Missing SVG asset: {svg_p}")
            svg = open(svg_p, encoding='utf-8').read().strip()
            svg = re.sub(r'\s+', ' ', svg)
            # Ensure explicit opaque fill for external SVG mask images inside tsui://
            svg = svg.replace('currentColor', '#000000')
            cache[rel] = 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=':/=') + '")'
        return cache[rel]
    return re.sub(r'url\("icons/([^"]+)"\)', repl, css_txt)

for fname, raw_css in variants.items():
    css_txt = inline_svg_urls(raw_css)
    p = os.path.join(EXT_DIR, fname)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(css_txt)
    clean = re.sub(r'/[*].*?[*]/', '', css_txt, flags=re.S)
    o, c = clean.count('{'), clean.count('}')
    po, pc = clean.count('('), clean.count(')')
    print(f"Wrote {fname}: {len(css_txt)} bytes, braces {o}/{c} (ok={o==c}), parens {po}/{pc} (ok={po==pc})")

pkg = {
    "name": "Discord Classic Dark",
    "description": "1:1 Discord Desktop Dark replica for TeamSpeak 6 with moved bottom user dock, mic/deafen controls, 72px guild rail, flat chat, and monochrome Discord icons.",
    "version": "2.0.0",
    "identifier": "dev.custom.discord",
    "engines": {"teamspeak": 1},
    "repository": {
        "type": "git",
        "url": "https://github.com/Roskud/teamspeak6-discord-theme"
    },
    "image": "preview.svg",
    "license": "MIT",
    "author": "Roskud",
    "keywords": ["discord", "dark", "flat", "replica", "theme"],
    "content": {
        "themes": [
            {
                "name": "Discord Dark",
                "source": "discord.css",
                "apiVersion": 1,
                "image": "preview.svg"
            },
            {
                "name": "Discord Dark + Banners",
                "source": "discord-banners.css",
                "apiVersion": 1,
                "image": "preview.svg"
            },
            {
                "name": "Discord Rail",
                "source": "discord-rail.css",
                "apiVersion": 1,
                "image": "preview.svg"
            },
            {
                "name": "Discord Rail + Banners",
                "source": "discord-rail-banners.css",
                "apiVersion": 1,
                "image": "preview.svg"
            },
            {
                "name": "Discord Wide",
                "source": "discord-wide.css",
                "apiVersion": 1,
                "image": "preview.svg"
            },
            {
                "name": "Discord Wide + Banners",
                "source": "discord-wide-banners.css",
                "apiVersion": 1,
                "image": "preview.svg"
            }
        ]
    }
}

pkg_path = os.path.join(EXT_DIR, 'package.json')
with open(pkg_path, 'w', encoding='utf-8') as f:
    json.dump(pkg, f, indent=2)
    f.write('\n')
print("Wrote package.json")

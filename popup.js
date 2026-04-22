/**
 * popup.js — Anh Ngữ Việt Nam
 * Centralized popup system — all config from data.json
 * Entry popup (delay-based) + Exit intent popup (mouse leave)
 * Session-controlled: each shows once per session
 *
 * ★ Para activar/desactivar o modificar los popups,
 *   edita SOLO el campo "popup" en data.json.
 *   No necesitas tocar este archivo ni ningún HTML.
 */
(function () {
  'use strict';

  const STORAGE_KEY_ENTRY = 'anvn_popup_entry_shown';
  const STORAGE_KEY_EXIT  = 'anvn_popup_exit_shown';

  // ── Load popup config from data.json ─────────────────────────────
  async function loadPopupConfig() {
    try {
      const res = await fetch('data.json');
      const data = await res.json();
      return data.popup || null;
    } catch {
      return null;
    }
  }

  // ── Create popup DOM ─────────────────────────────────────────────
  function createPopup(id, config, type) {
    // Overlay
    const overlay = document.createElement('div');
    overlay.id = id;
    overlay.className = `popup-overlay popup-${type}`;
    overlay.setAttribute('aria-hidden', 'true');

    const isExit = type === 'exit';

    overlay.innerHTML = `
      <div class="popup-card ${isExit ? 'popup-card--exit' : 'popup-card--entry'}">
        <button class="popup-close" aria-label="Đóng">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
        ${isExit ? '<div class="popup-ribbon">MIỄN PHÍ</div>' : ''}
        <div class="popup-icon">${isExit ? '🎁' : '🏨'}</div>
        <h2 class="popup-title">${config.title}</h2>
        <p class="popup-subtitle">${config.subtitle}</p>
        <div class="popup-body">${config.body}</div>
        <a href="${config.cta_url}" class="popup-cta" target="_blank" rel="noopener noreferrer">
          ${config.cta_text}
        </a>
        <button class="popup-dismiss">${config.dismiss_text}</button>
      </div>
    `;

    document.body.appendChild(overlay);

    // Close handlers
    const close = () => {
      overlay.classList.remove('popup-visible');
      overlay.setAttribute('aria-hidden', 'true');
      setTimeout(() => overlay.remove(), 400);
    };

    overlay.querySelector('.popup-close').addEventListener('click', close);
    overlay.querySelector('.popup-dismiss').addEventListener('click', close);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });

    // Escape key
    const escHandler = (e) => {
      if (e.key === 'Escape') { close(); document.removeEventListener('keydown', escHandler); }
    };
    document.addEventListener('keydown', escHandler);

    return { overlay, show: () => {
      overlay.classList.add('popup-visible');
      overlay.setAttribute('aria-hidden', 'false');
    }};
  }

  // ── Entry popup (delay-based) ────────────────────────────────────
  function initEntryPopup(config) {
    if (!config.entry || !config.entry.enabled) return;
    if (sessionStorage.getItem(STORAGE_KEY_ENTRY)) return;

    const delay = config.entry.delay_ms || 4000;

    setTimeout(() => {
      // Don't show if exit popup is already visible
      if (document.querySelector('.popup-visible')) return;

      const { show } = createPopup('entryPopup', config.entry, 'entry');
      // Small delay for CSS transition
      requestAnimationFrame(() => requestAnimationFrame(show));
      sessionStorage.setItem(STORAGE_KEY_ENTRY, '1');
    }, delay);
  }

  // ── Exit intent popup (mouse leave) ──────────────────────────────
  function initExitPopup(config) {
    if (!config.exit || !config.exit.enabled) return;
    if (sessionStorage.getItem(STORAGE_KEY_EXIT)) return;

    let triggered = false;

    const handler = (e) => {
      // Only trigger when mouse leaves through top of viewport
      if (e.clientY > 10) return;
      if (triggered) return;
      // Don't show if entry popup is visible
      if (document.querySelector('.popup-visible')) return;

      triggered = true;
      document.removeEventListener('mouseout', handler);

      const { show } = createPopup('exitPopup', config.exit, 'exit');
      requestAnimationFrame(() => requestAnimationFrame(show));
      sessionStorage.setItem(STORAGE_KEY_EXIT, '1');
    };

    // Wait a bit before attaching exit intent (avoid false triggers on load)
    setTimeout(() => {
      document.addEventListener('mouseout', handler);
    }, 8000);
  }

  // ── Init ─────────────────────────────────────────────────────────
  async function init() {
    const config = await loadPopupConfig();
    if (!config) return;

    initEntryPopup(config);
    initExitPopup(config);
  }

  // Run after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

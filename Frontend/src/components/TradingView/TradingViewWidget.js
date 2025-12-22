// DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// NO IMPORT OVERRIDES | NO PATH ASSUMPTIONS | ABSOLUTE STRUCTURE COMPLIANCE

// NOTE:
// This file previously auto-instantiated a TradingView widget on import.
// That behavior is NO LONGER VALID.
//
// TradingViewController is now the SOLE widget mount owner.
// This file is preserved as a future helper/factory only.

export function createTradingViewWidget(config) {
  if (!window.TradingView || !window.TradingView.widget) {
    console.warn("[TradingViewWidget] TradingView library not loaded");
    return null;
  }

  if (!config || !config.container) {
    console.error("[TradingViewWidget] CANNOT INITIALIZE: config.container is missing.", config);
    return null;
  }

  console.log(`[TradingViewWidget] Constructor call for: "${config.container}"`);

  const widgetOptions = {
    autosize: true,
    symbol: config.symbol || "BINANCE:BTCUSDT",
    interval: config.interval || "15",
    timezone: "Etc/UTC",
    theme: "dark",
    style: "1",
    locale: "en",
    container_id: config.container,
    hide_top_toolbar: false,
    hide_legend: false,
    allow_symbol_change: true,
    debug: false
  };

  try {
    return new window.TradingView.widget(widgetOptions);
  } catch (err) {
    console.error("[TradingViewWidget] Constructor error:", err);
    return null;
  }
}

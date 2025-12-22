// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from 'react';
import './App.css';

import Header from './components/Header/Header';
import PerformancePanel from './components/Performance/PerformancePanel';
import WalletControls from './components/Wallet/WalletControls';
import ControlsSection from './components/Controls/ControlsSection';
import TradingViewChartSection from './components/TradingView/TradingViewChartSection';

function App() {
  return (
    <div className="App">
      <Header />

      <main className="App-main">
        <section className="App-row">
          <PerformancePanel />
        </section>

        <section className="App-row">
          <WalletControls />
        </section>

        <section className="App-row">
          <ControlsSection />
        </section>

        <section className="App-row">
          <TradingViewChartSection />
        </section>
      </main>
    </div>
  );
}

export default App;

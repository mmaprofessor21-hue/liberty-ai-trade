export default function WalletControlsPanel() {
  return (
    <div className="wallet-section wallet-controls">
      <div className="tc-button-group">
        <button data-intent="positive">CONNECT</button>
        <button data-intent="negative" disabled>DISCONNECT</button>
      </div>
    </div>
  );
}

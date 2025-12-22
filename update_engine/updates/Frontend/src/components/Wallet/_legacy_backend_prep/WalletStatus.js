export default function WalletStatus() {
  return (
    <div className="wallet-section wallet-status">
      <div className="wallet-status-grid">
        <div>
          <div className="wallet-status-label">BALANCE</div>
          <div className="wallet-status-value">—</div>
          <div className="wallet-status-label">ADDRESS</div>
          <div className="wallet-status-value">—</div>
        </div>
        <div>
          <div className="wallet-status-label">NETWORK</div>
          <div className="wallet-status-value">Solana</div>
          <div className="wallet-status-label">STATUS</div>
          <div className="wallet-status-value">DISCONNECTED</div>
        </div>
      </div>
    </div>
  );
}

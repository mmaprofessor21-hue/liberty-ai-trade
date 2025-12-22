/**
 * WALLET ADAPTER INTERFACE
 * ------------------------------------------------------------
 * This file defines the REQUIRED contract for any wallet backend.
 * UI components must never talk to the backend directly.
 *
 * Implementation examples:
 * - Solana RPC
 * - Phantom provider
 * - Mock adapter (for dev / tests)
 * ------------------------------------------------------------
 */

export const walletAdapterInterface = {
  // Connection lifecycle
  connect: async () => {
    throw new Error("walletAdapter.connect() not implemented");
  },

  disconnect: async () => {
    throw new Error("walletAdapter.disconnect() not implemented");
  },

  // Wallet identity
  getAddress: async () => {
    throw new Error("walletAdapter.getAddress() not implemented");
  },

  getNetwork: async () => {
    throw new Error("walletAdapter.getNetwork() not implemented");
  },

  // Account data
  getBalance: async () => {
    throw new Error("walletAdapter.getBalance() not implemented");
  },

  // Security / health
  getSecurityStatus: async () => {
    // Expected return shape:
    // { safe: boolean, reason?: string }
    throw new Error("walletAdapter.getSecurityStatus() not implemented");
  },

  // Funds
  requestDeposit: async () => {
    throw new Error("walletAdapter.requestDeposit() not implemented");
  },

  requestWithdraw: async () => {
    throw new Error("walletAdapter.requestWithdraw() not implemented");
  },

  // Data feeds
  getHoldings: async () => {
    throw new Error("walletAdapter.getHoldings() not implemented");
  },

  getTransactionHistory: async () => {
    throw new Error("walletAdapter.getTransactionHistory() not implemented");
  },

  // Optional live channel
  subscribe: (callback) => {
    // callback(payload)
    // return unsubscribe()
    throw new Error("walletAdapter.subscribe() not implemented");
  }
};

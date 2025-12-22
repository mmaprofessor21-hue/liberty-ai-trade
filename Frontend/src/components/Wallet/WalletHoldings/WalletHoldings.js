import React, { useState } from "react";
import "./WalletHoldings.css";

const MOCK_HOLDINGS = [
  { token: "SOL", symbol: "SOL", balance: 145.2, price: 142.50, value: 20691.00, allocation: 45, change: 5.2 },
  { token: "Bonk", symbol: "BONK", balance: 15000000, price: 0.000024, value: 360.00, allocation: 2, change: -12.4 },
  { token: "Jupiter", symbol: "JUP", balance: 5000, price: 1.12, value: 5600.00, allocation: 15, change: 1.1 },
  { token: "Pyth", symbol: "PYTH", balance: 2500, price: 0.65, value: 1625.00, allocation: 5, change: 0.5 },
  { token: "Raydium", symbol: "RAY", balance: 100, price: 1.85, value: 185.00, allocation: 1, change: -2.1 },
];

export default function WalletHoldings({ filter, isRefreshing }) {
  const [sortConfig, setSortConfig] = useState({ key: "value", direction: "desc" });

  // Filter
  const filteredData = MOCK_HOLDINGS.filter(item => {
    if (!filter) return true;
    const search = filter.toLowerCase();
    return (
      item.token.toLowerCase().includes(search) ||
      item.symbol.toLowerCase().includes(search)
    );
  });

  // Sort
  const sortedData = [...filteredData].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) {
      return sortConfig.direction === "ascending" ? -1 : 1;
    }
    if (a[sortConfig.key] > b[sortConfig.key]) {
      return sortConfig.direction === "ascending" ? 1 : -1;
    }
    return 0;
  });

  const requestSort = (key) => {
    let direction = "ascending";
    if (sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  const getSortIndicator = (name) => {
    if (sortConfig.key !== name) return " ";
    return sortConfig.direction === "ascending" ? " ▲" : " ▼";
  };

  return (
    <div className={`wallet-holdings-table ${isRefreshing ? "refreshing" : ""}`}>
      <table>
        <thead>
          <tr>
            <th onClick={() => requestSort("token")}>TOKEN {getSortIndicator("token")}</th>
            <th onClick={() => requestSort("balance")}>BALANCE {getSortIndicator("balance")}</th>
            <th onClick={() => requestSort("price")}>PRICE {getSortIndicator("price")}</th>
            <th onClick={() => requestSort("value")}>VALUE {getSortIndicator("value")}</th>
            <th onClick={() => requestSort("allocation")}>ALLOC % {getSortIndicator("allocation")}</th>
            <th onClick={() => requestSort("change")}>24H {getSortIndicator("change")}</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.length > 0 ? (
            sortedData.map((row, index) => (
              <tr key={index}>
                <td className="col-token">
                  <span className="token-symbol">{row.symbol}</span>
                  <span className="token-name">{row.token}</span>
                </td>
                <td>{row.balance.toLocaleString()}</td>
                <td>${row.price.toLocaleString()}</td>
                <td className="col-value">${row.value.toLocaleString()}</td>
                <td>
                  <div className="allocation-bar-wrap">
                    <div className="allocation-bar" style={{ width: `${row.allocation}%` }}></div>
                    <span>{row.allocation}%</span>
                  </div>
                </td>
                <td className={row.change >= 0 ? "positive" : "negative"}>
                  {row.change > 0 ? "+" : ""}{row.change}%
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" className="empty-state">No holdings found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

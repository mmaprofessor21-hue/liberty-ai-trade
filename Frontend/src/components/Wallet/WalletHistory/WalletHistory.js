import React, { useState } from "react";
import "./WalletHistory.css";

const MOCK_HISTORY = [
  { id: 1, time: "2024-05-20 14:30", action: "BUY", token: "SOL", amount: 1.5, price: 140.00, value: 210.00, status: "FILLED" },
  { id: 2, time: "2024-05-20 12:15", action: "SELL", token: "BONK", amount: 5000000, price: 0.000025, value: 125.00, status: "FILLED" },
  { id: 3, time: "2024-05-19 09:45", action: "BUY", token: "JUP", amount: 200, price: 1.10, value: 220.00, status: "FILLED" },
  { id: 4, time: "2024-05-18 16:20", action: "SELL", token: "SOL", amount: 0.5, price: 138.50, value: 69.25, status: "FILLED" },
  { id: 5, time: "2024-05-18 10:00", action: "BUY", token: "PYTH", amount: 1000, price: 0.60, value: 600.00, status: "FILLED" },
  { id: 6, time: "2024-05-17 11:30", action: "FAIL", token: "RAY", amount: 50, price: 1.80, value: 90.00, status: "FAILED" },
];

export default function WalletHistory({ filter, isRefreshing }) {
  const [sortConfig, setSortConfig] = useState({ key: "time", direction: "desc" });

  // Filter
  const filteredData = MOCK_HISTORY.filter(item => {
    if (!filter) return true;
    const search = filter.toLowerCase();

    // Check specific specific key words for filtering by type
    if (search === 'buy' || search === 'sell') {
      return item.action.toLowerCase() === search;
    }

    return (
      item.token.toLowerCase().includes(search) ||
      item.action.toLowerCase().includes(search) ||
      item.status.toLowerCase().includes(search)
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
    // Default time to descending first
    if (key === "time" && sortConfig.key !== "time") {
      direction = "descending";
    } else if (sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  const getSortIndicator = (name) => {
    if (sortConfig.key !== name) return " ";
    return sortConfig.direction === "ascending" ? " ▲" : " ▼";
  };

  const getStatusClass = (status) => {
    if (status === "FILLED") return "status-filled";
    if (status === "FAILED") return "status-failed";
    return "";
  };

  const getActionClass = (action) => {
    if (action === "BUY") return "action-buy";
    if (action === "SELL") return "action-sell";
    if (action === "FAIL") return "action-fail";
    return "";
  };

  return (
    <div className={`wallet-history-table ${isRefreshing ? "refreshing" : ""}`}>
      <table>
        <thead>
          <tr>
            <th onClick={() => requestSort("time")}>TIME {getSortIndicator("time")}</th>
            <th onClick={() => requestSort("action")}>ACTION {getSortIndicator("action")}</th>
            <th onClick={() => requestSort("token")}>TOKEN {getSortIndicator("token")}</th>
            <th onClick={() => requestSort("amount")}>AMOUNT {getSortIndicator("amount")}</th>
            <th onClick={() => requestSort("price")}>PRICE {getSortIndicator("price")}</th>
            <th onClick={() => requestSort("value")}>VALUE {getSortIndicator("value")}</th>
            <th onClick={() => requestSort("status")}>STATUS {getSortIndicator("status")}</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.length > 0 ? (
            sortedData.map((row) => (
              <tr key={row.id}>
                <td className="col-time">{row.time}</td>
                <td className={`col-action ${getActionClass(row.action)}`}>{row.action}</td>
                <td className="col-token">{row.token}</td>
                <td>{row.amount.toLocaleString()}</td>
                <td>${row.price.toLocaleString()}</td>
                <td>${row.value.toLocaleString()}</td>
                <td>
                  <span className={`status-badge ${getStatusClass(row.status)}`}>
                    {row.status}
                  </span>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="7" className="empty-state">No history found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

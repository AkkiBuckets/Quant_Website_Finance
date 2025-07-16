import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const [symbols, setSymbols] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [portfolioName, setPortfolioName] = useState("");
  const [userName, setUserName] = useState("");
  const [saveMessage, setSaveMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysisResult(null);
    setSaveMessage("");

    try {
      const response = await axios.post(
        "/api/analysis/",
        { symbols: symbols.split(",").map(s => s.trim().toUpperCase()) },
        { headers: { "Content-Type": "application/json" } }
      );
      setAnalysisResult(response.data);
    } catch (err) {
      setError("❌ Failed to fetch analysis. Check symbol(s) or server.");
    }

    setLoading(false);
  };

  const savePortfolio = async () => {
    if (!portfolioName || !analysisResult) {
      setSaveMessage("❌ Portfolio name and analysis required.");
      return;
    }

    try {
      await axios.post(
        "/api/save-portfolio/",
        {
          portfolio_name: portfolioName,
          user_name: userName,
          symbols: symbols.split(",").map(s => s.trim().toUpperCase()),
          expected_return: analysisResult.expected_return,
          std_deviation: analysisResult.std_deviation,
          sharpe_ratio: analysisResult.sharpe_ratio,
          treynor_ratio: analysisResult.treynor_ratio,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      setSaveMessage("✅ Portfolio logged successfully!");
    } catch (err) {
      setSaveMessage("❌ Failed to log portfolio.");
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 20, fontFamily: "Arial, sans-serif" }}>
      
      <div style={{ textAlign: "right", marginBottom: 10 }}>
        <a
          href="http://localhost:8000/admin/"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: "#facc15",
            fontWeight: "bold",
            textDecoration: "none",
            fontSize: 14,
            backgroundColor: "#1e293b",
            padding: "6px 12px",
            borderRadius: "6px",
            border: "1px solid #334155"
          }}
        >
          🔐 Admin Login
        </a>
      </div>

      <h1>📊 Quantitative Portfolio Analysis</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
        <label>
          🏷️ Stock Symbols (comma-separated):
          <input
            type="text"
            value={symbols}
            onChange={(e) => setSymbols(e.target.value)}
            required
            placeholder="e.g. AAPL,MSFT,GOOG"
            style={{ marginLeft: 10, padding: 5, fontSize: 16, width: "80%" }}
          />
        </label>
        <br />
        <button type="submit" style={{ marginTop: 15, padding: "10px 20px", fontSize: 16 }}>
          {loading ? "⏳ Analyzing..." : "📈 Run Analysis"}
        </button>
      </form>

      {error && <div style={{ color: "red" }}>{error}</div>}

      {analysisResult && (
        <div>
          <h2>📉 Results</h2>
          <ul>
            <li>📈 Expected Return: <strong>{analysisResult.expected_return}</strong></li>
            <li>📊 Std Deviation: <strong>{analysisResult.std_deviation}</strong></li>
            <li>⚖️ Sharpe Ratio: <strong>{analysisResult.sharpe_ratio}</strong></li>
            <li>📏 Treynor Ratio: <strong>{analysisResult.treynor_ratio}</strong></li>
          </ul>

          {analysisResult.graph && (
            <>
              <h3>📌 Efficient Frontier</h3>
              <img
                src={`data:image/png;base64,${analysisResult.graph}`}
                alt="Efficient Frontier"
                style={{ maxWidth: "100%", border: "1px solid #ccc", padding: 10 }}
              />
            </>
          )}

          <div style={{ marginTop: 40 }}>
            <h3>🗃️ Log This Portfolio to Central Database</h3>
            <input
              type="text"
              placeholder="Portfolio Name"
              value={portfolioName}
              onChange={(e) => setPortfolioName(e.target.value)}
              style={{ padding: 8, marginRight: 10, width: 250 }}
            />
            <input
              type="text"
              placeholder="Your Name (optional)"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              style={{ padding: 8, width: 250 }}
            />
            <br />
            <button style={{ marginTop: 15 }} onClick={savePortfolio}>
              🗃️ Log Portfolio to Central Database
            </button>
            {saveMessage && <div style={{ marginTop: 10 }}>{saveMessage}</div>}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

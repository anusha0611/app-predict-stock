import { useState } from "react";

function App() {
  const [stockSymbol, setStockSymbol] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!stockSymbol) {
      alert("Please enter a stock symbol");
      return;
    }

    setLoading(true);
    setPrediction(null);

    try {
      const response = await fetch("http://localhost:5003/predict/stock", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ symbol: stockSymbol }),
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data.predicted_price);
      } else {
        alert(data.error || "Prediction failed");
      }
    } catch (error) {
      alert("Error connecting to prediction service");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Stock Price Predictor</h1>

      <div className="flex space-x-2">
        <input
          type="text"
          value={stockSymbol}
          onChange={(e) => setStockSymbol(e.target.value)}
          placeholder="Enter stock symbol (e.g. AAPL)"
          className="p-2 border rounded w-64"
        />
        <button
          onClick={handlePredict}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Predict
        </button>
      </div>

      {loading && <p className="mt-4 text-gray-600">Loading prediction...</p>}

      {prediction && (
        <div className="mt-6 text-green-700 text-xl font-semibold">
          Predicted Price for {stockSymbol.toUpperCase()}: ${prediction}
        </div>
      )}
    </div>
  );
}

export default App;

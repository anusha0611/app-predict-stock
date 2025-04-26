import React, { useEffect, useState } from "react";
import { api } from "../../utils/api";

const StockList = () => {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    api.fetchStocks().then(setStocks);
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-2xl mb-4">Stocks</h2>
      <ul>
        {stocks.map((stock) => (
          <li key={stock.id} className="mb-2">
            {stock.symbol} - {stock.name}: ${stock.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StockList;

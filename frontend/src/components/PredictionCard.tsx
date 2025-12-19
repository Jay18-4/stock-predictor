import { useState, useEffect } from "react";
import { fetchPredictions } from "../api/client";
import StockPanel from "./StockPanel";

export default function PredictionCard({ latestData }: { latestData: any }) {
  const [predictionsData, setPredictionsData] = useState<{
    tickers: string[];
    predictions: number[];
    timestamp?: string;
  } | null>(null);

  useEffect(() => {
    const cached = localStorage.getItem("predictions");
    const predictionsTime = localStorage.getItem("predictions_time");
    const latestTime = localStorage.getItem("latest_data_time");

    if (cached && predictionsTime && latestTime && predictionsTime === latestTime) {
      setPredictionsData(JSON.parse(cached));
      return;
    }

    fetchPredictions().then((data) => {
      setPredictionsData(data);
      localStorage.setItem("predictions", JSON.stringify(data));
      localStorage.setItem("predictions_time", localStorage.getItem("latest_data_time") || "");
    });
  }, [latestData]);

  if (!predictionsData) return <div className="text-white">Loading predictions…</div>;

  return (
    <div className="grid gap-6">
      {latestData.stocks.map((stock: any) => {
        const index = predictionsData.tickers.indexOf(stock.ticker);
        const prediction = index !== -1 ? predictionsData.predictions[index] : null;

        return (
          <StockPanel
            key={stock.ticker}
            ticker={stock.ticker}
            data={{
              ...stock,
              predictionDirection:
                prediction === 1 ? "Up" : prediction === 0 ? "Down" : "N/A",
            }}
          />
        );
      })}
    </div>
  );
}


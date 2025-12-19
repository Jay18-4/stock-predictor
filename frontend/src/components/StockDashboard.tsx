import { useQuery } from "@tanstack/react-query";
import { fetchLatestData, fetchPredictions } from "../api/client";
import StockPanel from "./StockPanel";

export default function StockDashboard() {
  const { data: latestData, isLoading: loadingData } = useQuery({
    queryKey: ["latest-data"],
    queryFn: fetchLatestData,
    staleTime: 60_000,
  });

  const { data: predictionsData, isLoading: loadingPredictions } = useQuery({
    queryKey: ["predictions"],
    queryFn: fetchPredictions,
    staleTime: 60_000,
  });

  if (loadingData || loadingPredictions) return <div className="text-white">Loading…</div>;
  if (!latestData || !predictionsData) return <div className="text-red-500">Failed to load data</div>;

  return (
    <div className="grid gap-6">
      {latestData.stocks.map((stock: any) => {
        const ticker = stock.Ticker || stock.ticker;
        const index = predictionsData.tickers.indexOf(ticker);
        const predictionValue = index !== -1 ? predictionsData.predictions[index] : null;
        const predictionDirection =
          predictionValue === 1 ? "Up" :
          predictionValue === 0 ? "Down" : "N/A";

        return (
          <StockPanel
            key={ticker}
            ticker={ticker}
            stockData={stock}
            predData={{ predictionDirection }}
          />
        );
      })}
    </div>
  );
}


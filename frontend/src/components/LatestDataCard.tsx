import { useQuery } from "@tanstack/react-query";
import { fetchLatestData } from "../api/client";

import StockPanel from "./StockPanel";

export default function LatestDataCard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["latest-data"],
    queryFn: fetchLatestData,
    staleTime: 60_000,
  });

  if (isLoading) return <div className="text-white">Loading…</div>;
  if (error) return <div className="text-red-500">Failed to load</div>;


  return (
    <>
    <p className="text-[#00ff00] text-sm mb-2">
       Data as of {data.timestamp}
    </p>

    <div className="grid gap-6 bg-[#121212] p-6 rounded-lg">
      {data.stocks.map((stock: any) => (
        <StockPanel
          key={stock['Ticker']}
          ticker={stock['Ticker']} // the actual ticker string
          data={stock}         // the full stock object
        />
      ))}
    </div>
    </>
  );
}


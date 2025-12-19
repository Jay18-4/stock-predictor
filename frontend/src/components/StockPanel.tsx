import KpiCard from "./KpiCard";

type StockPanelProps = {
  ticker: string;
  stockData: any; // we’ll strongly type later
  predData: any; // we’ll strongly type later
};

export default function StockPanel({ ticker, stockData, predData }: StockPanelProps) {
  return (
    <>
    <div className="bg-[#1f1f1f] text-[#00ff00] hover:text-[#ffffff] rounded-lg p-5 border border-gray-700 shadow-lg">
      <h2 className="text-xl font-bold  mb-4">{ticker}</h2>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 ">
        <KpiCard label="Latest Price" value={stockData['Close']?? "—"} />
        <KpiCard label="Volume" value={stockData["Volume"] ?? "—"} />
        <KpiCard label="Ploarity Mean" value={stockData["pol_mean"] ?? 0} />
        <KpiCard label="Ploarity Sum" value={stockData["sum"] ?? 0} />
        <KpiCard label="Positive News" value={stockData["pos_count"] ?? 0} />
        <KpiCard label="Negative News" value={stockData["neg_count"] ?? 0} />
        <KpiCard label="Neutral News" value={stockData["new_count"] ?? 0} />
        <KpiCard label="Has News" value={stockData["gas_news"] ?? 0} />
      </div>

      {/* Chart placeholder */}
      <div className="h-48 rounded-lg bg-[#121212] flex items-center justify-center text-gray-500 border border-gray-800">
        Chart goes here
      </div>
    </div>

    <div className="p-4 rounded-xl bg-[#1f1f1f] text-[#00ff00] shadow-md">
    {/* <h2 className="text-xl font-bold">{ticker}</h2> */}
    
    {/* Existing stock info */}
    <p>Close: {predData.close} ?? 0</p>

    {/* Prediction badge */}
        {predData ? (
        <p>
        Prediction:{" "}
        <span
            className={
            predData.prediction === "Up"
                ? "text-green-400"
                : "text-red-400"
            }
        >
            {predData.prediction}
        </span>
        </p>
    ) : (
        <p>Prediction: Loading…</p>
    )}
    </div>
    </>
  );
}

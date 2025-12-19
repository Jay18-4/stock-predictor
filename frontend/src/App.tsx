// import { useQuery } from "@tanstack/react-query";
// import { fetchLatestData } from "./api/client";
import "./index.css";
import StockDashboard from "./components/StockDashboard";

// function App() {
//   const { data, isLoading, error } = useQuery({
//     queryKey: ["latest-data"],
//     queryFn: fetchLatestData,
//     staleTime: 60_000,
//   });

//   if (isLoading) return <div className="text-white">Loading...</div>;
//   if (error) return <div className="text-red-500">Error loading data</div>;

//   return (
//     <div className="min-h-screen bg-gray-900 text-white p-8">
//       <h1 className="text-3xl font-bold mb-6">Stock Dashboard</h1>
//       <pre className="bg-gray-800 p-4 rounded-lg overflow-auto">
//         {JSON.stringify(data, null, 2)}
//       </pre>
//     </div>
//   );
// }

// export default App;

// export default function App() {
//   return (
//     <div className="min-h-screen bg-[#1f1f1f] p-6">
//       <h1 className="text-3xl text-[#FFFFFF] font-sans mb-4">Stock Dashboard</h1>
//       <LatestDataCard />
//     </div>
//   );
// }

function App() {
  return (
    <div className="min-h-screen bg-[#1f1f1f] text-[#00ff00] p-6">
      <h1 className="text-3xl font-bold mb-6">Stock Dashboard</h1>

      {/* Unified dashboard showing latest data + predictions */}
      <StockDashboard />
    </div>
  );
}

export default App;



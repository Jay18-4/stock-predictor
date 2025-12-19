type KpiCardProps = {
  label: string;
  value: string | number;
  accent?: "green" | "red" | "blue";
};

const accentMap = {
  green: "text-green-400",
  red: "text-red-400",
  blue: "text-blue-400",
};

export default function KpiCard({
  label,
  value,
  accent = "green",
}: KpiCardProps) {
  return (
    <div className="bg-[#161616] rounded-lg p-4 shadow border border-gray-800">
      <p className="text-sm text-gray-400">{label}</p>
      <p className={`text-2xl font-semibold ${accentMap[accent]}`}>
        {value}
      </p>
    </div>
  );
}

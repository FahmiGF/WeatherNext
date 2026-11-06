"use client";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

interface RainChartProps {
  data: Array<{
    label: string;
    rain_probability?: number;
    rain_actual?: number;
    rain_predicted?: number;
  }>;
  mode?: "area" | "bar" | "comparison";
}

export default function RainChart({ data, mode = "area" }: RainChartProps) {
  const tooltipStyle = {
    backgroundColor: "rgba(15,31,61,0.95)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "12px",
    color: "#fff",
    fontSize: 12,
  };

  if (mode === "comparison") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="label" stroke="#64748b" fontSize={11} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} unit=" mm" />
          <Tooltip contentStyle={tooltipStyle} />
          <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
          <Bar dataKey="rain_actual" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Aktual" />
          <Bar dataKey="rain_predicted" fill="#f59e0b" radius={[4, 4, 0, 0]} name="Prediksi" />
        </BarChart>
      </ResponsiveContainer>
    );
  }

  if (mode === "bar") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="label" stroke="#64748b" fontSize={11} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} unit="%" />
          <Tooltip contentStyle={tooltipStyle} />
          <Bar dataKey="rain_probability" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Hujan %" />
        </BarChart>
      </ResponsiveContainer>
    );
  }

  // area
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <defs>
          <linearGradient id="rainGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="label" stroke="#64748b" fontSize={11} tickLine={false} />
        <YAxis stroke="#64748b" fontSize={11} tickLine={false} unit="%" domain={[0, 100]} />
        <Tooltip contentStyle={tooltipStyle} />
        <Area
          type="monotone"
          dataKey="rain_probability"
          stroke="#3b82f6"
          fill="url(#rainGrad)"
          strokeWidth={2}
          name="Prob. Hujan"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

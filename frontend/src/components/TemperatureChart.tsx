"use client";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Area,
  AreaChart,
} from "recharts";

interface TemperatureChartProps {
  data: Array<{
    label: string;
    temp_max?: number;
    temp_min?: number;
    temperature?: number;
    temp_actual?: number;
    temp_predicted?: number;
  }>;
  mode?: "minmax" | "single" | "comparison";
}

export default function TemperatureChart({ data, mode = "minmax" }: TemperatureChartProps) {
  if (mode === "comparison") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="label" stroke="#64748b" fontSize={11} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} unit="°" />
          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(15,31,61,0.95)",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: "12px",
              color: "#fff",
              fontSize: 12,
            }}
          />
          <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
          <Line
            type="monotone"
            dataKey="temp_actual"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={{ fill: "#3b82f6", r: 3 }}
            name="Aktual"
          />
          <Line
            type="monotone"
            dataKey="temp_predicted"
            stroke="#f59e0b"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: "#f59e0b", r: 3 }}
            name="Prediksi"
          />
        </LineChart>
      </ResponsiveContainer>
    );
  }

  if (mode === "single") {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <defs>
            <linearGradient id="tempGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="label" stroke="#64748b" fontSize={11} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} unit="°" />
          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(15,31,61,0.95)",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: "12px",
              color: "#fff",
              fontSize: 12,
            }}
          />
          <Area
            type="monotone"
            dataKey="temperature"
            stroke="#3b82f6"
            fill="url(#tempGrad)"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    );
  }

  // minmax mode
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <defs>
          <linearGradient id="maxGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="minGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="label" stroke="#64748b" fontSize={11} tickLine={false} />
        <YAxis stroke="#64748b" fontSize={11} tickLine={false} unit="°" />
        <Tooltip
          contentStyle={{
            backgroundColor: "rgba(15,31,61,0.95)",
            border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: "12px",
            color: "#fff",
            fontSize: 12,
          }}
        />
        <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
        <Area
          type="monotone"
          dataKey="temp_max"
          stroke="#f59e0b"
          fill="url(#maxGrad)"
          strokeWidth={2}
          name="Maks"
        />
        <Area
          type="monotone"
          dataKey="temp_min"
          stroke="#3b82f6"
          fill="url(#minGrad)"
          strokeWidth={2}
          name="Min"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

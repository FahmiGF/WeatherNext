"use client";

import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface WeatherMetricCardProps {
  icon: ReactNode;
  label: string;
  value: string;
  sub?: string;
  color?: string;
}

export default function WeatherMetricCard({
  icon,
  label,
  value,
  sub,
  color = "text-blue-400",
}: WeatherMetricCardProps) {
  return (
    <div className="glass-card flex items-center gap-4 rounded-xl p-4 transition-transform hover:scale-105">
      <div className={cn("shrink-0", color)}>{icon}</div>
      <div>
        <p className="text-xs text-slate-400">{label}</p>
        <p className="text-lg font-bold text-white">{value}</p>
        {sub && <p className="text-[10px] text-slate-500">{sub}</p>}
      </div>
    </div>
  );
}

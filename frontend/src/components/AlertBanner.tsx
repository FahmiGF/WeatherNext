"use client";

import type { WeatherAlert } from "@/types/weather";
import { AlertTriangle, X } from "lucide-react";
import { useState } from "react";

interface AlertBannerProps {
  alerts: WeatherAlert[];
}

const severityStyles: Record<string, string> = {
  rendah: "border-yellow-500/50 bg-yellow-500/10 text-yellow-300",
  sedang: "border-orange-500/50 bg-orange-500/10 text-orange-300",
  tinggi: "border-red-500/50 bg-red-500/10 text-red-300",
  ekstrem: "border-red-700/50 bg-red-700/20 text-red-200",
};

export default function AlertBanner({ alerts }: AlertBannerProps) {
  const [dismissed, setDismissed] = useState<Set<string>>(new Set());

  const visible = alerts.filter((a) => !dismissed.has(a.id));
  if (visible.length === 0) return null;

  return (
    <div className="space-y-2">
      {visible.map((alert) => (
        <div
          key={alert.id}
          className={`flex items-start gap-3 rounded-xl border p-4 backdrop-blur-sm ${
            severityStyles[alert.severity] ?? severityStyles.sedang
          }`}
        >
          <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0" />
          <div className="flex-1 space-y-1">
            <p className="text-sm font-semibold">{alert.title}</p>
            <p className="text-xs opacity-80">{alert.description}</p>
            <p className="text-xs opacity-60">
              Wilayah: {alert.area} • Sumber: {alert.source}
            </p>
          </div>
          <button
            onClick={() => setDismissed((prev) => new Set(prev).add(alert.id))}
            className="shrink-0 rounded-lg p-1 transition-colors hover:bg-white/10"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      ))}
    </div>
  );
}

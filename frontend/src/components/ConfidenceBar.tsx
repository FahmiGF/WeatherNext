"use client";

import { cn } from "@/lib/utils";

interface ConfidenceBarProps {
  confidence: number;
  showLabel?: boolean;
  size?: "sm" | "md";
}

export default function ConfidenceBar({ confidence, showLabel = true, size = "md" }: ConfidenceBarProps) {
  const getColor = (c: number) => {
    if (c >= 90) return "bg-emerald-500";
    if (c >= 75) return "bg-green-500";
    if (c >= 60) return "bg-yellow-500";
    if (c >= 40) return "bg-orange-500";
    return "bg-red-500";
  };

  const getLabel = (c: number) => {
    if (c >= 90) return "Sangat Tinggi";
    if (c >= 75) return "Tinggi";
    if (c >= 60) return "Sedang";
    if (c >= 40) return "Rendah";
    return "Sangat Rendah";
  };

  return (
    <div className="flex items-center gap-2">
      <div
        className={cn(
          "flex-1 overflow-hidden rounded-full bg-white/10",
          size === "sm" ? "h-1.5" : "h-2.5",
        )}
      >
        <div
          className={cn("h-full rounded-full transition-all duration-700", getColor(confidence))}
          style={{ width: `${confidence}%` }}
        />
      </div>
      {showLabel && (
        <span className="min-w-[3rem] text-right text-xs text-slate-400">
          {confidence}% — {getLabel(confidence)}
        </span>
      )}
    </div>
  );
}

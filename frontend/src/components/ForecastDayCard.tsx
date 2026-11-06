"use client";

import WeatherIcon from "./WeatherIcon";
import ConfidenceBar from "./ConfidenceBar";
import { formatTemperature, formatDate } from "@/lib/utils";
import type { ForecastDay } from "@/types/weather";
import { Droplets, Wind } from "lucide-react";

interface ForecastDayCardProps {
  day: ForecastDay;
  detailed?: boolean;
}

export default function ForecastDayCard({ day, detailed = false }: ForecastDayCardProps) {
  if (!detailed) {
    // Compact card for the 7-day strip
    return (
      <div className="glass-card flex min-w-[120px] flex-col items-center gap-2 rounded-xl p-4 transition-transform hover:scale-105">
        <p className="text-xs font-semibold text-blue-400">{day.day_name}</p>
        <p className="text-[10px] text-slate-500">{formatDate(day.date, "short")}</p>
        <WeatherIcon condition={day.condition} size="sm" animated={false} />
        <div className="text-center">
          <span className="text-sm font-bold text-white">{formatTemperature(day.temp_max)}</span>
          <span className="mx-1 text-slate-600">/</span>
          <span className="text-xs text-slate-400">{formatTemperature(day.temp_min)}</span>
        </div>
        <div className="flex items-center gap-1 text-[10px] text-blue-300">
          <Droplets className="h-3 w-3" />
          {day.rain_probability}%
        </div>
      </div>
    );
  }

  // Detailed card for forecast page
  return (
    <div className="glass-card rounded-xl p-5 transition-transform hover:scale-[1.02]">
      <div className="flex items-center gap-4">
        <div className="flex flex-col items-center gap-1">
          <WeatherIcon condition={day.condition} size="md" animated={false} />
        </div>
        <div className="flex-1">
          <div className="flex items-baseline gap-2">
            <p className="text-base font-bold text-white">{day.day_name}</p>
            <p className="text-xs text-slate-500">{formatDate(day.date, "short")}</p>
          </div>
          <p className="text-sm text-slate-400">{day.condition_text}</p>
          <div className="mt-2 flex items-center gap-4 text-sm">
            <span className="font-semibold text-white">
              {formatTemperature(day.temp_max)} / {formatTemperature(day.temp_min)}
            </span>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-slate-400">
          <div className="flex items-center gap-1">
            <Droplets className="h-3 w-3 text-blue-400" /> {day.rain_probability}%
          </div>
          <div className="flex items-center gap-1">
            <Wind className="h-3 w-3 text-cyan-400" /> {day.wind_speed} km/h
          </div>
          <div>💧 {day.humidity}%</div>
          <div>☀️ UV {day.uv_index}</div>
        </div>
      </div>
      <div className="mt-3">
        <p className="mb-1 text-[10px] text-slate-500">Tingkat Kepercayaan</p>
        <ConfidenceBar confidence={day.confidence} size="sm" />
      </div>
    </div>
  );
}

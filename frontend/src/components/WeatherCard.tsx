"use client";

import WeatherIcon from "./WeatherIcon";
import { formatTemperature, getWeatherGradient } from "@/lib/utils";
import type { CurrentWeather } from "@/types/weather";
import { Droplets, Wind, Eye, Thermometer } from "lucide-react";

interface WeatherCardProps {
  weather: CurrentWeather;
}

export default function WeatherCard({ weather }: WeatherCardProps) {
  return (
    <div
      className={`glass-card relative overflow-hidden rounded-2xl bg-gradient-to-br ${getWeatherGradient(
        weather.condition,
      )} p-6 md:p-8`}
    >
      {/* Decorative circles */}
      <div className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/5" />
      <div className="pointer-events-none absolute -bottom-8 -left-8 h-32 w-32 rounded-full bg-white/5" />

      <div className="relative z-10 flex flex-col items-center gap-4 md:flex-row md:items-start md:gap-8">
        {/* Icon & Temperature */}
        <div className="flex flex-col items-center gap-2">
          <WeatherIcon condition={weather.condition} size="xl" />
          <p className="text-lg font-medium text-slate-300">{weather.condition_text}</p>
        </div>

        {/* Main temp */}
        <div className="flex flex-col items-center md:items-start">
          <p className="text-7xl font-bold tracking-tight text-white md:text-8xl">
            {formatTemperature(weather.temperature)}
          </p>
          <p className="mt-1 text-sm text-slate-400">
            Terasa seperti {formatTemperature(weather.feels_like)}
          </p>
        </div>

        {/* Quick metrics */}
        <div className="mt-2 grid grid-cols-2 gap-x-6 gap-y-3 md:ml-auto md:mt-0">
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <Droplets className="h-4 w-4 text-blue-400" />
            <span>Kelembapan: {weather.humidity}%</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <Wind className="h-4 w-4 text-cyan-400" />
            <span>Angin: {weather.wind_speed} km/h</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <Eye className="h-4 w-4 text-purple-400" />
            <span>Visibilitas: {weather.visibility} km</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-300">
            <Thermometer className="h-4 w-4 text-orange-400" />
            <span>Tekanan: {weather.pressure} hPa</span>
          </div>
        </div>
      </div>

      {/* Sunrise / Sunset */}
      <div className="relative z-10 mt-6 flex items-center justify-center gap-8 border-t border-white/10 pt-4 text-sm text-slate-400">
        <span>🌅 Terbit {weather.sunrise}</span>
        <span>🌇 Terbenam {weather.sunset}</span>
      </div>
    </div>
  );
}

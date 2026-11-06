"use client";

import { getWeatherEmoji } from "@/lib/utils";
import type { WeatherCondition } from "@/types/weather";

interface WeatherIconProps {
  condition: WeatherCondition;
  size?: "sm" | "md" | "lg" | "xl";
  animated?: boolean;
}

const sizeClasses = {
  sm: "text-2xl",
  md: "text-4xl",
  lg: "text-6xl",
  xl: "text-8xl",
};

export default function WeatherIcon({ condition, size = "md", animated = true }: WeatherIconProps) {
  const emoji = getWeatherEmoji(condition);

  return (
    <span
      className={`${sizeClasses[size]} inline-block select-none ${
        animated ? "animate-bounce-slow" : ""
      }`}
      role="img"
      aria-label={condition}
    >
      {emoji}
    </span>
  );
}

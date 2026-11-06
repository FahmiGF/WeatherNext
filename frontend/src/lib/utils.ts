// ==========================================
// WeatherNext AI — Utility Functions
// ==========================================

import type { WeatherCondition } from "@/types/weather";

/**
 * Format temperature with degree symbol
 */
export function formatTemperature(temp: number, unit: string = "C"): string {
  return `${Math.round(temp)}°${unit}`;
}

/**
 * Format date to Indonesian locale
 */
export function formatDate(dateStr: string, style: "full" | "short" | "day" = "full"): string {
  const date = new Date(dateStr);
  const days = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
  const months = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
  ];

  if (style === "day") {
    return days[date.getDay()];
  }

  if (style === "short") {
    return `${date.getDate()} ${months[date.getMonth()].slice(0, 3)}`;
  }

  return `${days[date.getDay()]}, ${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

/**
 * Format time HH:MM
 */
export function formatTime(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit", hour12: false });
}

/**
 * Get current time formatted
 */
export function getCurrentTime(): string {
  return new Date().toLocaleTimeString("id-ID", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
}

/**
 * Get current date formatted in Indonesian
 */
export function getCurrentDate(): string {
  const now = new Date();
  return formatDate(now.toISOString(), "full");
}

/**
 * Map weather condition to emoji
 */
export function getWeatherEmoji(condition: WeatherCondition): string {
  const map: Record<WeatherCondition, string> = {
    cerah: "☀️",
    cerah_berawan: "⛅",
    berawan: "☁️",
    mendung: "🌥️",
    hujan_ringan: "🌦️",
    hujan_sedang: "🌧️",
    hujan_lebat: "⛈️",
    hujan_petir: "🌩️",
    kabut: "🌫️",
    asap: "😶‍🌫️",
  };
  return map[condition] || "🌤️";
}

/**
 * Get CSS gradient for weather condition
 */
export function getWeatherGradient(condition: WeatherCondition): string {
  const gradients: Record<WeatherCondition, string> = {
    cerah: "from-amber-500/20 via-orange-400/10 to-blue-600/20",
    cerah_berawan: "from-blue-400/20 via-sky-300/10 to-blue-700/20",
    berawan: "from-slate-400/20 via-gray-400/10 to-slate-600/20",
    mendung: "from-gray-500/20 via-slate-500/10 to-gray-700/20",
    hujan_ringan: "from-blue-500/20 via-cyan-400/10 to-blue-700/20",
    hujan_sedang: "from-blue-600/20 via-indigo-500/10 to-blue-800/20",
    hujan_lebat: "from-indigo-600/20 via-blue-600/10 to-indigo-900/20",
    hujan_petir: "from-purple-600/20 via-indigo-600/10 to-gray-900/20",
    kabut: "from-gray-400/20 via-slate-300/10 to-gray-500/20",
    asap: "from-yellow-700/20 via-amber-600/10 to-gray-600/20",
  };
  return gradients[condition] || gradients.cerah;
}

/**
 * Format rain probability
 */
export function formatRainProbability(prob: number): string {
  if (prob <= 10) return "Sangat kecil";
  if (prob <= 30) return "Kecil";
  if (prob <= 50) return "Sedang";
  if (prob <= 70) return "Cukup tinggi";
  if (prob <= 90) return "Tinggi";
  return "Sangat tinggi";
}

/**
 * Get confidence label
 */
export function getConfidenceLabel(confidence: number): string {
  if (confidence >= 90) return "Sangat Tinggi";
  if (confidence >= 75) return "Tinggi";
  if (confidence >= 60) return "Sedang";
  if (confidence >= 40) return "Rendah";
  return "Sangat Rendah";
}

/**
 * Get confidence color
 */
export function getConfidenceColor(confidence: number): string {
  if (confidence >= 90) return "text-emerald-400";
  if (confidence >= 75) return "text-green-400";
  if (confidence >= 60) return "text-yellow-400";
  if (confidence >= 40) return "text-orange-400";
  return "text-red-400";
}

/**
 * Get UV index label
 */
export function getUVLabel(uv: number): string {
  if (uv <= 2) return "Rendah";
  if (uv <= 5) return "Sedang";
  if (uv <= 7) return "Tinggi";
  if (uv <= 10) return "Sangat Tinggi";
  return "Ekstrem";
}

/**
 * Get UV color
 */
export function getUVColor(uv: number): string {
  if (uv <= 2) return "text-green-400";
  if (uv <= 5) return "text-yellow-400";
  if (uv <= 7) return "text-orange-400";
  if (uv <= 10) return "text-red-400";
  return "text-purple-400";
}

/**
 * Generate UUID
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

/**
 * Clamp number between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

/**
 * Cn classname merge helper
 */
export function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}

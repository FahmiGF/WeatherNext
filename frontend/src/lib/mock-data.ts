// ==========================================
// WeatherNext AI — Mock Data
// Realistic weather data for Surabaya, Indonesia
// ==========================================

import type {
  CurrentWeather,
  HourlyForecast,
  ForecastDay,
  MonthlyOutlook,
  WeatherHistoryRecord,
  WeatherAlert,
  CityMarker,
} from "@/types/weather";

// ---- Helpers ----
function getDateStr(daysFromNow: number): string {
  const d = new Date();
  d.setDate(d.getDate() + daysFromNow);
  return d.toISOString().slice(0, 10);
}

function getDayName(daysFromNow: number): string {
  const days = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
  const d = new Date();
  d.setDate(d.getDate() + daysFromNow);
  return days[d.getDay()];
}

// ---- Current Weather ----
export const mockCurrentWeather: CurrentWeather = {
  location: "Surabaya",
  province: "Jawa Timur",
  timestamp: new Date().toISOString(),
  temperature: 32,
  feels_like: 35,
  condition: "cerah_berawan",
  condition_text: "Cerah Berawan",
  humidity: 72,
  wind_speed: 15,
  wind_direction: "Tenggara",
  pressure: 1012,
  uv_index: 7,
  visibility: 10,
  cloud_cover: 35,
  dew_point: 26,
  rain_probability: 25,
  sunrise: "05:28",
  sunset: "17:32",
};

// ---- Hourly Forecast (24h) ----
export const mockHourlyForecast: HourlyForecast[] = [
  { time: "00:00", temperature: 27, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 80, wind_speed: 8 },
  { time: "01:00", temperature: 26, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 82, wind_speed: 7 },
  { time: "02:00", temperature: 26, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 83, wind_speed: 6 },
  { time: "03:00", temperature: 25, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 85, wind_speed: 5 },
  { time: "04:00", temperature: 25, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 86, wind_speed: 5 },
  { time: "05:00", temperature: 25, condition: "cerah", condition_text: "Cerah", rain_probability: 10, humidity: 85, wind_speed: 6 },
  { time: "06:00", temperature: 26, condition: "cerah", condition_text: "Cerah", rain_probability: 10, humidity: 82, wind_speed: 8 },
  { time: "07:00", temperature: 27, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 10, humidity: 78, wind_speed: 10 },
  { time: "08:00", temperature: 28, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 15, humidity: 75, wind_speed: 12 },
  { time: "09:00", temperature: 30, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 15, humidity: 72, wind_speed: 13 },
  { time: "10:00", temperature: 31, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 20, humidity: 70, wind_speed: 14 },
  { time: "11:00", temperature: 32, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 25, humidity: 68, wind_speed: 15 },
  { time: "12:00", temperature: 33, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 30, humidity: 65, wind_speed: 15 },
  { time: "13:00", temperature: 34, condition: "berawan", condition_text: "Berawan", rain_probability: 35, humidity: 63, wind_speed: 16 },
  { time: "14:00", temperature: 33, condition: "berawan", condition_text: "Berawan", rain_probability: 40, humidity: 65, wind_speed: 15 },
  { time: "15:00", temperature: 32, condition: "hujan_ringan", condition_text: "Hujan Ringan", rain_probability: 55, humidity: 70, wind_speed: 14 },
  { time: "16:00", temperature: 31, condition: "hujan_ringan", condition_text: "Hujan Ringan", rain_probability: 50, humidity: 73, wind_speed: 13 },
  { time: "17:00", temperature: 30, condition: "berawan", condition_text: "Berawan", rain_probability: 35, humidity: 75, wind_speed: 12 },
  { time: "18:00", temperature: 29, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 20, humidity: 77, wind_speed: 10 },
  { time: "19:00", temperature: 28, condition: "cerah_berawan", condition_text: "Cerah Berawan", rain_probability: 15, humidity: 78, wind_speed: 9 },
  { time: "20:00", temperature: 28, condition: "cerah", condition_text: "Cerah", rain_probability: 10, humidity: 79, wind_speed: 8 },
  { time: "21:00", temperature: 27, condition: "cerah", condition_text: "Cerah", rain_probability: 10, humidity: 80, wind_speed: 8 },
  { time: "22:00", temperature: 27, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 81, wind_speed: 7 },
  { time: "23:00", temperature: 27, condition: "cerah", condition_text: "Cerah", rain_probability: 5, humidity: 82, wind_speed: 7 },
];

// ---- 7-Day Forecast ----
export const mockWeeklyForecast: ForecastDay[] = [
  {
    date: getDateStr(0), day_name: getDayName(0), condition: "cerah_berawan",
    condition_text: "Cerah Berawan", temp_min: 25, temp_max: 34,
    rain_probability: 25, humidity: 72, wind_speed: 15, wind_direction: "Tenggara",
    uv_index: 7, sunrise: "05:28", sunset: "17:32", confidence: 97,
  },
  {
    date: getDateStr(1), day_name: getDayName(1), condition: "hujan_ringan",
    condition_text: "Hujan Ringan", temp_min: 24, temp_max: 32,
    rain_probability: 60, humidity: 78, wind_speed: 18, wind_direction: "Selatan",
    uv_index: 5, sunrise: "05:28", sunset: "17:32", confidence: 94,
  },
  {
    date: getDateStr(2), day_name: getDayName(2), condition: "hujan_sedang",
    condition_text: "Hujan Sedang", temp_min: 24, temp_max: 30,
    rain_probability: 75, humidity: 85, wind_speed: 22, wind_direction: "Barat Daya",
    uv_index: 3, sunrise: "05:28", sunset: "17:33", confidence: 91,
  },
  {
    date: getDateStr(3), day_name: getDayName(3), condition: "berawan",
    condition_text: "Berawan", temp_min: 25, temp_max: 31,
    rain_probability: 40, humidity: 75, wind_speed: 16, wind_direction: "Barat",
    uv_index: 5, sunrise: "05:28", sunset: "17:33", confidence: 88,
  },
  {
    date: getDateStr(4), day_name: getDayName(4), condition: "cerah",
    condition_text: "Cerah", temp_min: 25, temp_max: 35,
    rain_probability: 10, humidity: 65, wind_speed: 12, wind_direction: "Tenggara",
    uv_index: 9, sunrise: "05:28", sunset: "17:33", confidence: 85,
  },
  {
    date: getDateStr(5), day_name: getDayName(5), condition: "cerah_berawan",
    condition_text: "Cerah Berawan", temp_min: 26, temp_max: 34,
    rain_probability: 20, humidity: 70, wind_speed: 14, wind_direction: "Timur",
    uv_index: 7, sunrise: "05:29", sunset: "17:33", confidence: 82,
  },
  {
    date: getDateStr(6), day_name: getDayName(6), condition: "hujan_ringan",
    condition_text: "Hujan Ringan", temp_min: 24, temp_max: 31,
    rain_probability: 55, humidity: 80, wind_speed: 20, wind_direction: "Barat",
    uv_index: 4, sunrise: "05:29", sunset: "17:33", confidence: 78,
  },
];

// ---- 30-Day Outlook ----
export const mockMonthlyOutlook: MonthlyOutlook[] = Array.from({ length: 30 }, (_, i) => {
  const conditions: Array<{ cond: MonthlyOutlook["condition"]; text: string }> = [
    { cond: "cerah", text: "Cerah" },
    { cond: "cerah_berawan", text: "Cerah Berawan" },
    { cond: "berawan", text: "Berawan" },
    { cond: "hujan_ringan", text: "Hujan Ringan" },
    { cond: "hujan_sedang", text: "Hujan Sedang" },
  ];
  const pick = conditions[Math.floor(Math.abs(Math.sin(i * 2.1)) * conditions.length)];
  const baseMin = 24 + Math.round(Math.sin(i * 0.3) * 2);
  const baseMax = 31 + Math.round(Math.sin(i * 0.3 + 1) * 3);

  return {
    date: getDateStr(i),
    day_name: getDayName(i),
    temp_min: baseMin,
    temp_max: baseMax,
    rain_probability: Math.round(20 + Math.abs(Math.sin(i * 0.7)) * 60),
    condition: pick.cond,
    condition_text: pick.text,
    confidence: Math.max(30, Math.round(97 - i * 2.2)),
  };
});

// ---- History Data (last 30 days) ----
export const mockHistoryData: WeatherHistoryRecord[] = Array.from({ length: 30 }, (_, i) => {
  const idx = 29 - i;
  const tempActual = 28 + Math.round(Math.sin(idx * 0.4) * 4);
  const tempPredicted = tempActual + Math.round((Math.random() - 0.5) * 3);
  const rainActual = Math.round(Math.max(0, Math.sin(idx * 0.5) * 15 + Math.random() * 10));
  const rainPredicted = rainActual + Math.round((Math.random() - 0.5) * 8);
  const conditions: Array<{ cond: WeatherHistoryRecord["condition"]; text: string }> = [
    { cond: "cerah", text: "Cerah" },
    { cond: "cerah_berawan", text: "Cerah Berawan" },
    { cond: "berawan", text: "Berawan" },
    { cond: "hujan_ringan", text: "Hujan Ringan" },
  ];
  const pick = conditions[Math.floor(Math.abs(Math.sin(idx * 1.3)) * conditions.length)];

  return {
    date: getDateStr(-idx),
    temp_actual: tempActual,
    temp_predicted: Math.max(22, tempPredicted),
    rain_actual: Math.max(0, rainActual),
    rain_predicted: Math.max(0, rainPredicted),
    humidity: 65 + Math.round(Math.sin(idx * 0.3) * 15),
    condition: pick.cond,
    condition_text: pick.text,
  };
});

// ---- Weather Alerts ----
export const mockAlerts: WeatherAlert[] = [
  {
    id: "alert-1",
    type: "warning",
    severity: "sedang",
    title: "Peringatan Hujan Lebat",
    description:
      "Potensi hujan lebat disertai petir dan angin kencang di wilayah Surabaya dan sekitarnya pada sore hingga malam hari.",
    area: "Surabaya, Sidoarjo, Gresik",
    start_time: new Date().toISOString(),
    end_time: new Date(Date.now() + 12 * 3600 * 1000).toISOString(),
    source: "BMKG",
  },
];

// ---- City Markers for Map ----
export const mockCityMarkers: CityMarker[] = [
  { name: "Jakarta", lat: -6.2, lon: 106.85, temperature: 31, condition: "berawan", condition_text: "Berawan" },
  { name: "Surabaya", lat: -7.25, lon: 112.75, temperature: 32, condition: "cerah_berawan", condition_text: "Cerah Berawan" },
  { name: "Bandung", lat: -6.9, lon: 107.6, temperature: 25, condition: "hujan_ringan", condition_text: "Hujan Ringan" },
  { name: "Medan", lat: 3.6, lon: 98.7, temperature: 30, condition: "mendung", condition_text: "Mendung" },
  { name: "Makassar", lat: -5.15, lon: 119.4, temperature: 33, condition: "cerah", condition_text: "Cerah" },
  { name: "Semarang", lat: -6.97, lon: 110.42, temperature: 31, condition: "cerah_berawan", condition_text: "Cerah Berawan" },
  { name: "Yogyakarta", lat: -7.8, lon: 110.36, temperature: 29, condition: "berawan", condition_text: "Berawan" },
  { name: "Denpasar", lat: -8.65, lon: 115.22, temperature: 30, condition: "cerah", condition_text: "Cerah" },
  { name: "Palembang", lat: -2.99, lon: 104.75, temperature: 32, condition: "hujan_ringan", condition_text: "Hujan Ringan" },
  { name: "Balikpapan", lat: -1.24, lon: 116.85, temperature: 29, condition: "hujan_sedang", condition_text: "Hujan Sedang" },
  { name: "Manado", lat: 1.47, lon: 124.84, temperature: 28, condition: "berawan", condition_text: "Berawan" },
  { name: "Pontianak", lat: 0.0, lon: 109.33, temperature: 31, condition: "cerah_berawan", condition_text: "Cerah Berawan" },
];

// ==========================================
// WeatherNext AI — API Client
// ==========================================

import axios, { type AxiosInstance } from "axios";
import type {
  CurrentWeather,
  ForecastDay,
  MonthlyOutlook,
  WeatherHistoryRecord,
  WeatherAlert,
  Location,
  ChatRequest,
  ChatResponse,
  AdminModel,
  AdminAccuracy,
  AdminStats,
} from "@/types/weather";
import {
  mockCurrentWeather,
  mockWeeklyForecast,
  mockMonthlyOutlook,
  mockHistoryData,
  mockAlerts,
} from "@/lib/mock-data";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

// ------- Weather endpoints -------

export async function fetchCurrentWeather(city: string = "Surabaya"): Promise<CurrentWeather> {
  try {
    const res = await api.get<CurrentWeather>("/api/weather/current", { params: { city } });
    return res.data;
  } catch {
    console.warn("API tidak tersedia, menggunakan mock data.");
    return { ...mockCurrentWeather, location: city };
  }
}

export async function fetchTomorrowWeather(city: string = "Surabaya"): Promise<ForecastDay> {
  try {
    const res = await api.get<ForecastDay>("/api/weather/tomorrow", { params: { city } });
    return res.data;
  } catch {
    return mockWeeklyForecast[1];
  }
}

export async function fetchWeeklyForecast(city: string = "Surabaya"): Promise<ForecastDay[]> {
  try {
    const res = await api.get<ForecastDay[]>("/api/weather/weekly", { params: { city } });
    return res.data;
  } catch {
    return mockWeeklyForecast;
  }
}

export async function fetchMonthlyOutlook(city: string = "Surabaya"): Promise<MonthlyOutlook[]> {
  try {
    const res = await api.get<MonthlyOutlook[]>("/api/weather/monthly", { params: { city } });
    return res.data;
  } catch {
    return mockMonthlyOutlook;
  }
}

export async function fetchWeatherHistory(
  city: string = "Surabaya",
  startDate?: string,
  endDate?: string,
): Promise<WeatherHistoryRecord[]> {
  try {
    const res = await api.get<WeatherHistoryRecord[]>("/api/weather/history", {
      params: { city, start_date: startDate, end_date: endDate },
    });
    return res.data;
  } catch {
    return mockHistoryData;
  }
}

export async function fetchWeatherAlerts(city: string = "Surabaya"): Promise<WeatherAlert[]> {
  try {
    const res = await api.get<WeatherAlert[]>("/api/weather/alerts", { params: { city } });
    return res.data;
  } catch {
    return mockAlerts;
  }
}

// ------- Location search -------

export async function searchLocations(query: string): Promise<Location[]> {
  try {
    const res = await api.get<Location[]>("/api/locations/search", { params: { q: query } });
    return res.data;
  } catch {
    // Return common cities as fallback
    const cities: Location[] = [
      { id: "sby", name: "Surabaya", province: "Jawa Timur", country: "Indonesia", lat: -7.25, lon: 112.75 },
      { id: "jkt", name: "Jakarta", province: "DKI Jakarta", country: "Indonesia", lat: -6.2, lon: 106.85 },
      { id: "bdg", name: "Bandung", province: "Jawa Barat", country: "Indonesia", lat: -6.9, lon: 107.6 },
      { id: "smg", name: "Semarang", province: "Jawa Tengah", country: "Indonesia", lat: -6.97, lon: 110.42 },
      { id: "mdn", name: "Medan", province: "Sumatera Utara", country: "Indonesia", lat: 3.6, lon: 98.7 },
      { id: "mks", name: "Makassar", province: "Sulawesi Selatan", country: "Indonesia", lat: -5.15, lon: 119.4 },
      { id: "dps", name: "Denpasar", province: "Bali", country: "Indonesia", lat: -8.65, lon: 115.22 },
      { id: "ygk", name: "Yogyakarta", province: "DI Yogyakarta", country: "Indonesia", lat: -7.8, lon: 110.36 },
    ];
    return cities.filter(
      (c) =>
        c.name.toLowerCase().includes(query.toLowerCase()) ||
        c.province.toLowerCase().includes(query.toLowerCase()),
    );
  }
}

// ------- AI Chat -------

export async function sendChatMessage(req: ChatRequest): Promise<ChatResponse> {
  try {
    const res = await api.post<ChatResponse>("/api/ai/chat", req);
    return res.data;
  } catch {
    // Generate mock response
    return {
      reply: `Maaf, saat ini layanan AI sedang tidak tersedia. Berdasarkan data terakhir, cuaca di ${req.location} saat ini cerah berawan dengan suhu sekitar 32°C dan kelembapan 72%. Kemungkinan hujan ringan pada sore hari.`,
      session_id: req.session_id,
    };
  }
}

// ------- Admin -------

export async function fetchAdminModels(): Promise<AdminModel[]> {
  try {
    const res = await api.get<AdminModel[]>("/api/admin/models");
    return res.data;
  } catch {
    return [];
  }
}

export async function fetchAdminAccuracy(): Promise<AdminAccuracy[]> {
  try {
    const res = await api.get<AdminAccuracy[]>("/api/admin/accuracy");
    return res.data;
  } catch {
    return [];
  }
}

export async function fetchAdminStats(): Promise<AdminStats | null> {
  try {
    const res = await api.get<AdminStats>("/api/admin/stats");
    return res.data;
  } catch {
    return null;
  }
}

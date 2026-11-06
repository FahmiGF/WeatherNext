// ==========================================
// WeatherNext AI — TypeScript Type Definitions
// ==========================================

export interface Location {
  id: string;
  name: string;
  province: string;
  country: string;
  lat: number;
  lon: number;
}

export interface CurrentWeather {
  location: string;
  province: string;
  timestamp: string;
  temperature: number;
  feels_like: number;
  condition: WeatherCondition;
  condition_text: string;
  humidity: number;
  wind_speed: number;
  wind_direction: string;
  pressure: number;
  uv_index: number;
  visibility: number;
  cloud_cover: number;
  dew_point: number;
  rain_probability: number;
  sunrise: string;
  sunset: string;
}

export type WeatherCondition =
  | "cerah"
  | "cerah_berawan"
  | "berawan"
  | "mendung"
  | "hujan_ringan"
  | "hujan_sedang"
  | "hujan_lebat"
  | "hujan_petir"
  | "kabut"
  | "asap";

export interface HourlyForecast {
  time: string;
  temperature: number;
  condition: WeatherCondition;
  condition_text: string;
  rain_probability: number;
  humidity: number;
  wind_speed: number;
}

export interface ForecastDay {
  date: string;
  day_name: string;
  condition: WeatherCondition;
  condition_text: string;
  temp_min: number;
  temp_max: number;
  rain_probability: number;
  humidity: number;
  wind_speed: number;
  wind_direction: string;
  uv_index: number;
  sunrise: string;
  sunset: string;
  confidence: number;
  hourly?: HourlyForecast[];
}

export interface MonthlyOutlook {
  date: string;
  day_name: string;
  temp_min: number;
  temp_max: number;
  rain_probability: number;
  condition: WeatherCondition;
  condition_text: string;
  confidence: number;
}

export interface WeatherHistoryRecord {
  date: string;
  temp_actual: number;
  temp_predicted: number;
  rain_actual: number;
  rain_predicted: number;
  humidity: number;
  condition: WeatherCondition;
  condition_text: string;
}

export interface WeatherAlert {
  id: string;
  type: "warning" | "watch" | "advisory";
  severity: "rendah" | "sedang" | "tinggi" | "ekstrem";
  title: string;
  description: string;
  area: string;
  start_time: string;
  end_time: string;
  source: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  weather_data?: CurrentWeather | ForecastDay[] | null;
}

export interface ChatRequest {
  session_id: string;
  message: string;
  location: string;
}

export interface ChatResponse {
  reply: string;
  weather_data?: CurrentWeather | ForecastDay[] | null;
  session_id: string;
}

export interface AdminModel {
  name: string;
  version: string;
  type: string;
  status: "active" | "training" | "inactive";
  accuracy: number;
  last_updated: string;
}

export interface AdminAccuracy {
  model: string;
  period: string;
  mae: number;
  rmse: number;
  accuracy_pct: number;
}

export interface AdminStats {
  total_predictions: number;
  total_users: number;
  avg_accuracy: number;
  cities_covered: number;
  uptime_pct: number;
}

export interface CityMarker {
  name: string;
  lat: number;
  lon: number;
  temperature: number;
  condition: WeatherCondition;
  condition_text: string;
}

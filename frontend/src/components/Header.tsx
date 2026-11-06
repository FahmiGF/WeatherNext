"use client";

import { useState, useEffect } from "react";
import { MapPin, Clock } from "lucide-react";
import SearchCity from "./SearchCity";
import { getCurrentTime, getCurrentDate } from "@/lib/utils";

interface HeaderProps {
  city: string;
  onCityChange: (city: string) => void;
}

export default function Header({ city, onCityChange }: HeaderProps) {
  const [time, setTime] = useState(getCurrentTime());
  const [date] = useState(getCurrentDate());

  useEffect(() => {
    const interval = setInterval(() => setTime(getCurrentTime()), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-30 flex flex-wrap items-center justify-between gap-3 border-b border-white/5 bg-[#0a1628]/80 px-4 py-3 backdrop-blur-xl md:px-6">
      <div className="flex items-center gap-4">
        {/* City name */}
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-blue-400" />
          <span className="text-sm font-semibold text-white">{city}</span>
        </div>

        {/* Date & Time */}
        <div className="hidden items-center gap-2 text-xs text-slate-400 sm:flex">
          <Clock className="h-3.5 w-3.5" />
          <span>{date}</span>
          <span className="font-mono text-blue-400">{time}</span>
        </div>
      </div>

      {/* Search */}
      <div className="w-full sm:w-64">
        <SearchCity currentCity={city} onCityChange={onCityChange} />
      </div>
    </header>
  );
}

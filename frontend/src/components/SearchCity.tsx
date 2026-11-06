"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Search, MapPin, X } from "lucide-react";
import { searchLocations } from "@/lib/api";
import type { Location } from "@/types/weather";

interface SearchCityProps {
  currentCity: string;
  onCityChange: (city: string) => void;
}

export default function SearchCity({ currentCity, onCityChange }: SearchCityProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Location[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();

  // Close on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const doSearch = useCallback(async (q: string) => {
    if (q.length < 2) {
      setResults([]);
      return;
    }
    setLoading(true);
    const res = await searchLocations(q);
    setResults(res);
    setLoading(false);
  }, []);

  const handleInputChange = (val: string) => {
    setQuery(val);
    setIsOpen(true);
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => doSearch(val), 300);
  };

  const selectCity = (loc: Location) => {
    onCityChange(loc.name);
    setQuery("");
    setIsOpen(false);
  };

  return (
    <div ref={wrapperRef} className="relative">
      <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-2 backdrop-blur-sm transition-colors focus-within:border-blue-500/50">
        <Search className="h-4 w-4 text-slate-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => handleInputChange(e.target.value)}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          placeholder={`Cari kota... (${currentCity})`}
          className="w-full bg-transparent text-sm text-white placeholder-slate-500 outline-none"
        />
        {query && (
          <button onClick={() => { setQuery(""); setIsOpen(false); }}>
            <X className="h-4 w-4 text-slate-400 hover:text-white" />
          </button>
        )}
      </div>

      {isOpen && (query.length >= 2) && (
        <div className="absolute top-full z-50 mt-1 w-full overflow-hidden rounded-xl border border-white/10 bg-[#0f1f3d]/95 shadow-2xl backdrop-blur-xl">
          {loading ? (
            <div className="p-3 text-center text-xs text-slate-400">Mencari...</div>
          ) : results.length === 0 ? (
            <div className="p-3 text-center text-xs text-slate-400">Tidak ditemukan</div>
          ) : (
            results.map((loc) => (
              <button
                key={loc.id}
                onClick={() => selectCity(loc)}
                className="flex w-full items-center gap-3 px-3 py-2.5 text-left transition-colors hover:bg-white/10"
              >
                <MapPin className="h-4 w-4 shrink-0 text-blue-400" />
                <div>
                  <p className="text-sm font-medium text-white">{loc.name}</p>
                  <p className="text-xs text-slate-400">{loc.province}, {loc.country}</p>
                </div>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}

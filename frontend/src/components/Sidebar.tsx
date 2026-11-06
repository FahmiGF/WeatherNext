"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  CalendarDays,
  CalendarRange,
  History,
  Bot,
  Map,
  Info,
  CloudSun,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

const navItems = [
  { href: "/", label: "Beranda", icon: Home },
  { href: "/forecast", label: "Prakiraan 7 Hari", icon: CalendarDays },
  { href: "/outlook", label: "Outlook 30 Hari", icon: CalendarRange },
  { href: "/history", label: "Histori Cuaca", icon: History },
  { href: "/assistant", label: "Asisten AI", icon: Bot },
  { href: "/map", label: "Peta Cuaca", icon: Map },
  { href: "/about", label: "Tentang", icon: Info },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <>
      {/* Desktop Sidebar */}
      <aside
        className={cn(
          "hidden md:flex flex-col fixed left-0 top-0 z-40 h-screen border-r border-white/5 bg-[#070e1b]/80 backdrop-blur-xl transition-all duration-300",
          collapsed ? "w-[72px]" : "w-60",
        )}
      >
        {/* Logo */}
        <div className="flex h-16 items-center gap-3 border-b border-white/5 px-4">
          <CloudSun className="h-8 w-8 shrink-0 text-blue-400" />
          {!collapsed && (
            <div>
              <h1 className="text-base font-bold text-white">WeatherNext</h1>
              <p className="text-[10px] text-blue-400">AI Weather Platform</p>
            </div>
          )}
        </div>

        {/* Nav items */}
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
                  active
                    ? "bg-blue-600/20 text-blue-400"
                    : "text-slate-400 hover:bg-white/5 hover:text-white",
                  collapsed && "justify-center px-0",
                )}
                title={collapsed ? item.label : undefined}
              >
                <item.icon className="h-5 w-5 shrink-0" />
                {!collapsed && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Collapse toggle */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex h-12 items-center justify-center border-t border-white/5 text-slate-500 transition-colors hover:text-white"
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </aside>

      {/* Mobile Bottom Nav */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 flex items-center justify-around border-t border-white/10 bg-[#070e1b]/95 py-2 backdrop-blur-xl md:hidden">
        {navItems.slice(0, 5).map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex flex-col items-center gap-0.5 px-2 py-1 text-[10px] transition-colors",
                active ? "text-blue-400" : "text-slate-500",
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.label.split(" ")[0]}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}

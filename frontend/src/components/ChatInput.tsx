"use client";

import { useState, type FormEvent } from "react";
import { Send, Mic } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [text, setText] = useState("");
  const [showMicTooltip, setShowMicTooltip] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-2">
      <div className="relative flex-1">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          placeholder="Tanyakan tentang cuaca..."
          rows={1}
          disabled={disabled}
          className="w-full resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 pr-12 text-sm text-white placeholder-slate-500 backdrop-blur-sm transition-colors focus:border-blue-500/50 focus:outline-none focus:ring-1 focus:ring-blue-500/30 disabled:opacity-50"
        />
      </div>

      {/* Mic button */}
      <div className="relative">
        <button
          type="button"
          onMouseEnter={() => setShowMicTooltip(true)}
          onMouseLeave={() => setShowMicTooltip(false)}
          className="rounded-xl border border-white/10 bg-white/5 p-3 text-slate-400 transition-colors hover:bg-white/10 hover:text-white"
        >
          <Mic className="h-5 w-5" />
        </button>
        {showMicTooltip && (
          <div className="absolute -top-10 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-lg bg-slate-800 px-3 py-1.5 text-xs text-slate-300 shadow-lg">
            Segera hadir!
          </div>
        )}
      </div>

      {/* Send button */}
      <button
        type="submit"
        disabled={disabled || !text.trim()}
        className="rounded-xl bg-blue-600 p-3 text-white transition-colors hover:bg-blue-700 disabled:opacity-40 disabled:hover:bg-blue-600"
      >
        <Send className="h-5 w-5" />
      </button>
    </form>
  );
}

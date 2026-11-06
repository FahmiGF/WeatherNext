"use client";

export default function LoadingSpinner({ text = "Memuat data..." }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-20">
      <div className="relative h-12 w-12">
        <div className="absolute inset-0 rounded-full border-4 border-white/10" />
        <div className="absolute inset-0 animate-spin rounded-full border-4 border-transparent border-t-blue-500" />
      </div>
      <p className="text-sm text-slate-400">{text}</p>
    </div>
  );
}

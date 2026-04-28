"use client";

import { useState, useEffect } from "react";
import type { DashboardState } from "@/lib/types";

interface TopBarProps {
  state: DashboardState;
  connected: boolean;
  onRun: () => void;
}

export default function TopBar({ state, connected, onRun }: TopBarProps) {
  const [time, setTime] = useState("");

  useEffect(() => {
    const update = () => {
      const now = new Date();
      const h = String(now.getUTCHours()).padStart(2, "0");
      const m = String(now.getUTCMinutes()).padStart(2, "0");
      const s = String(now.getUTCSeconds()).padStart(2, "0");
      setTime(`${h}:${m}:${s} UTC`);
    };
    update();
    const id = setInterval(update, 1000);
    return () => clearInterval(id);
  }, []);

  const regimeLabel = state.regime
    ? state.regime.replace(/_/g, " ")
    : "UNKNOWN";

  return (
    <nav className="sticky top-0 z-100 flex items-center justify-between px-8 h-14 bg-[rgba(10,10,18,0.85)] backdrop-blur-[20px] border-b border-[var(--color-border-subtle)]">
      <div className="flex items-center gap-4">
        <div className="font-[var(--font-display)] text-[28px] tracking-[4px] text-[var(--color-cyan)] leading-none">
          ATLAS
          <span className="text-[var(--color-text-muted)] text-sm tracking-[2px] font-[var(--font-mono)] font-light ml-2">
            Polymarket
          </span>
        </div>
      </div>

      <div className="hidden md:flex items-center gap-6">
        <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-[20px] font-[var(--font-mono)] text-xs font-medium tracking-[1px] uppercase bg-[var(--color-green-dim)] text-[var(--color-green)] border border-[rgba(0,255,136,0.2)]">
          <div className="w-1.5 h-1.5 rounded-full bg-current animate-[pulse_2s_ease-in-out_infinite]" />
          PRISM · {regimeLabel}
        </div>
        <div className="flex items-center gap-1.5 font-[var(--font-mono)] text-[11px] text-[var(--color-text-muted)] tracking-[0.5px]">
          <div
            className="w-[7px] h-[7px] rounded-full"
            style={{
              background: connected
                ? "var(--color-green)"
                : "var(--color-red)",
              boxShadow: connected
                ? "0 0 8px var(--color-green)"
                : "0 0 8px var(--color-red)",
            }}
          />
          {connected ? "ALL SYSTEMS NOMINAL" : "DISCONNECTED"}
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="px-3.5 py-1.5 rounded-md border border-[var(--color-amber)] bg-[var(--color-amber-dim)] text-[var(--color-amber)] font-[var(--font-mono)] text-[11px] font-medium tracking-[1px] uppercase">
          PAPER TRADE
        </div>
        <div className="flex items-center gap-1.5 font-[var(--font-mono)] text-[11px] text-[var(--color-text-muted)] tracking-[0.5px]">
          <div
            className="w-[7px] h-[7px] rounded-full"
            style={{
              background: "var(--color-cyan)",
              boxShadow: "0 0 8px var(--color-cyan)",
            }}
          />
          {state.status === "running" ? "ANALYZING" : time || "LIVE"}
        </div>
      </div>
    </nav>
  );
}

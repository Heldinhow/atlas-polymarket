"use client";

import type { DashboardState } from "@/lib/types";

interface PRISMPanelProps {
  state: DashboardState;
}

const regimes = [
  { key: "RECOVERY", label: "Recovery", icon: "▲", color: "var(--color-green)" },
  { key: "CRISIS", label: "Crisis", icon: "▼", color: "var(--color-red)" },
  { key: "RATE_TIGHTENING", label: "Rate Tightening", icon: "◆", color: "var(--color-orange)" },
  { key: "BULL_LOW_VOL", label: "Bull", icon: "●", color: "var(--color-cyan)" },
  { key: "EUPHORIA", label: "Euphoria", icon: "★", color: "var(--color-purple)" },
];

export default function PRISMPanel({ state }: PRISMPanelProps) {
  return (
    <div className="animate-fade-up delay-7 bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-panel)] p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
          PRISM REGIME
        </div>
      </div>
      <div className="flex flex-col gap-2.5 mt-4">
        {regimes.map((regime) => {
          const prob = state.prism_probabilities[regime.key] || 0;
          const isActive = state.regime === regime.key;

          return (
            <div
              key={regime.key}
              className={`flex items-center gap-3 p-2.5 rounded-lg border transition-all ${
                isActive
                  ? "border-[rgba(0,255,136,0.2)] bg-[rgba(0,255,136,0.03)]"
                  : "border-[var(--color-border-subtle)] bg-[var(--color-bg-deep)]"
              }`}
            >
              <div
                className="w-8 h-8 rounded-md flex items-center justify-center text-sm shrink-0"
                style={{
                  background: `color-mix(in srgb, ${regime.color} 15%, transparent)`,
                  color: regime.color,
                }}
              >
                {regime.icon}
              </div>
              <div className="flex-1">
                <div className="font-[var(--font-mono)] text-xs font-medium text-[var(--color-text-primary)] tracking-[0.5px]">
                  {regime.label}
                </div>
                <div className="font-[var(--font-mono)] text-[11px] text-[var(--color-text-muted)] mt-0.5">
                  Confidence: {prob}%
                </div>
              </div>
              <div className="w-[60px] h-1 bg-[var(--color-bg-elevated)] rounded-full overflow-hidden shrink-0">
                <div
                  className="h-full rounded-full transition-all duration-1000"
                  style={{
                    width: `${prob}%`,
                    background: regime.color,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

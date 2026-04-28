"use client";

import type { Position } from "@/lib/types";

interface PositionsTableProps {
  positions: Position[];
}

const MARKET_ICONS: Record<string, { emoji: string; className: string }> = {
  esport: { emoji: "🎮", className: "bg-[var(--color-purple-dim)] text-[var(--color-purple)]" },
  cs2: { emoji: "🎯", className: "bg-[var(--color-purple-dim)] text-[var(--color-purple)]" },
  lol: { emoji: "🎮", className: "bg-[var(--color-purple-dim)] text-[var(--color-purple)]" },
  sport: { emoji: "⚽", className: "bg-[var(--color-cyan-dim)] text-[var(--color-cyan)]" },
  nfl: { emoji: "🏈", className: "bg-[var(--color-cyan-dim)] text-[var(--color-cyan)]" },
  football: { emoji: "⚽", className: "bg-[var(--color-cyan-dim)] text-[var(--color-cyan)]" },
};

function getMarketIcon(category?: string) {
  const cfg = MARKET_ICONS[category ?? ""] ?? MARKET_ICONS.esport;
  return { emoji: cfg.emoji, className: cfg.className };
}

export default function PositionsTable({ positions }: PositionsTableProps) {
  if (positions.length === 0) {
    return (
      <div className="col-span-full xl:col-span-2 animate-fade-up delay-9 bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-panel)] p-6">
        <div className="flex items-center justify-between mb-5">
          <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
            ACTIVE POSITIONS
          </div>
        </div>
        <div className="flex items-center justify-center h-40 font-[var(--font-mono)] text-sm text-[var(--color-text-muted)]">
          No active positions — run an analysis to start trading
        </div>
      </div>
    );
  }

  return (
    <div className="col-span-full xl:col-span-2 animate-fade-up delay-9 bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-panel)] p-6">
      <div className="flex items-center justify-between mb-5">
        <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
          ACTIVE POSITIONS
        </div>
        <div className="flex gap-1 bg-[var(--color-bg-deep)] p-[3px] rounded-md">
          {["All", "Esports", "Sports"].map((tab, i) => (
            <button
              key={tab}
              className={`px-3.5 py-[5px] rounded font-[var(--font-mono)] text-[11px] tracking-[0.5px] border-none transition-all ${
                i === 0
                  ? "bg-[var(--color-bg-elevated)] text-[var(--color-cyan)]"
                  : "bg-transparent text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>
      <table className="w-full border-collapse">
        <thead>
          <tr>
            {["Market", "Side", "Entry", "Current", "Size", "P&L", "Agent"].map((th) => (
              <th
                key={th}
                className="font-[var(--font-mono)] text-[10px] tracking-[1.5px] uppercase text-[var(--color-text-muted)] text-left px-3 pb-3 border-b border-[var(--color-border-medium)] font-normal"
              >
                {th}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {positions.map((pos, i) => {
            const currentPrice = pos.current_price ?? pos.avg_price;
            const pnl = pos.pnl ?? (currentPrice - pos.avg_price) * pos.amount;
            const side = pos.side || "YES";
            const icon = getMarketIcon(pos.category);
            const agentName = pos.agent || "—";

            return (
              <tr
                key={i}
                className="transition-colors hover:bg-[rgba(255,255,255,0.015)]"
              >
                <td className="font-[var(--font-mono)] text-xs text-[var(--color-text-secondary)] px-3 py-3.5 border-b border-[var(--color-border-subtle)]">
                  <div className="flex items-center gap-2.5">
                    <div className={`w-7 h-7 rounded-md flex items-center justify-center text-xs shrink-0 ${icon.className}`}>
                      {icon.emoji}
                    </div>
                    <div>
                      <div className="text-[var(--color-text-primary)] font-medium text-xs">
                        {pos.market_id}
                      </div>
                      {pos.subtitle && (
                        <div className="text-[10px] text-[var(--color-text-muted)] mt-px">
                          {pos.subtitle}
                        </div>
                      )}
                    </div>
                  </div>
                </td>
                <td className="font-[var(--font-mono)] text-xs text-[var(--color-text-secondary)] px-3 py-3.5 border-b border-[var(--color-border-subtle)]">
                  <span
                    className={`px-2.5 py-[3px] rounded text-[10px] font-medium tracking-[1px] uppercase ${
                      side === "YES"
                        ? "bg-[var(--color-green-dim)] text-[var(--color-green)]"
                        : "bg-[var(--color-red-dim)] text-[var(--color-red)]"
                    }`}
                  >
                    {side}
                  </span>
                </td>
                <td className="font-[var(--font-mono)] text-xs text-[var(--color-text-secondary)] px-3 py-3.5 border-b border-[var(--color-border-subtle)]">
                  {pos.avg_price.toFixed(2)}
                </td>
                <td className="font-[var(--font-mono)] text-xs text-[var(--color-text-secondary)] px-3 py-3.5 border-b border-[var(--color-border-subtle)]">
                  {currentPrice.toFixed(2)}
                </td>
                <td className="font-[var(--font-mono)] text-xs text-[var(--color-text-secondary)] px-3 py-3.5 border-b border-[var(--color-border-subtle)]">
                  ${pos.amount.toLocaleString()}
                </td>
                <td
                  className={`font-[var(--font-mono)] text-xs px-3 py-3.5 border-b border-[var(--color-border-subtle)] ${
                    pnl >= 0
                      ? "text-[var(--color-green)]"
                      : "text-[var(--color-red)]"
                  }`}
                >
                  {pnl >= 0 ? "+" : ""}${pnl.toFixed(0)}
                </td>
                <td
                  className="font-[var(--font-mono)] text-xs px-3 py-3.5 border-b border-[var(--color-border-subtle)]"
                  style={{ color: "var(--color-cyan)" }}
                >
                  {agentName}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

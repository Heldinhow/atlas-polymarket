"use client";

import type { DashboardState } from "@/lib/types";

interface KPICardsProps {
  state: DashboardState;
}

const cards = [
  { label: "Portfolio Value", color: "var(--color-cyan)", key: "balance" },
  { label: "Total P&L", color: "var(--color-green)", key: "pnl" },
  { label: "Win Rate", color: "var(--color-orange)", key: "winrate" },
  {
    label: "Active Positions",
    color: "var(--color-purple)",
    key: "positions",
  },
  { label: "Sharpe Ratio", color: "var(--color-amber)", key: "sharpe" },
] as const;

function formatValue(key: string, state: DashboardState): string {
  switch (key) {
    case "balance":
      return `$${state.portfolio.balance.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    case "pnl": {
      const pnl = state.portfolio.pnl;
      return `${pnl >= 0 ? "+" : ""}$${pnl.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
    case "winrate":
      return `${state.win_rate.toFixed(1)}%`;
    case "positions":
      return `${state.active_positions_count || state.portfolio.positions.length}`;
    case "sharpe":
      return state.sharpe_ratio.toFixed(2);
    default:
      return "—";
  }
}

function formatSub(key: string, state: DashboardState): string {
  switch (key) {
    case "balance": {
      const pnl = state.portfolio.pnl;
      const pct = state.portfolio.balance > 0 ? (pnl / (state.portfolio.balance - pnl)) * 100 : 0;
      return `${pnl >= 0 ? "+" : ""}${pct.toFixed(1)}% this cycle`;
    }
    case "pnl":
      return "all time";
    case "winrate":
      return `${state.winning_trades} / ${state.total_trades} trades`;
    case "positions":
      return "across all markets";
    case "sharpe":
      return "30-day rolling";
    default:
      return "";
  }
}

function isPositive(key: string, state: DashboardState): boolean {
  switch (key) {
    case "balance":
    case "pnl":
      return state.portfolio.pnl >= 0;
    case "winrate":
      return state.win_rate >= 50;
    default:
      return true;
  }
}

export default function KPICards({ state }: KPICardsProps) {
  return (
    <div className="col-span-full grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-5 gap-3">
      {cards.map((card, i) => (
        <div
          key={card.key}
          className={`animate-fade-up delay-${i + 1} bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-lg p-[18px] relative overflow-hidden`}
        >
          <div
            className="absolute top-0 left-0 right-0 h-[2px]"
            style={{ background: card.color }}
          />
          <div className="font-[var(--font-mono)] text-[10px] font-normal tracking-[1.5px] uppercase text-[var(--color-text-muted)] mb-2.5">
            {card.label}
          </div>
          <div
            className="font-[var(--font-display)] text-[26px] md:text-[32px] tracking-[2px] leading-none mb-1.5"
            style={{ color: card.color }}
          >
            {formatValue(card.key, state)}
          </div>
          <div className="font-[var(--font-mono)] text-[11px] text-[var(--color-text-secondary)]">
            <span
              className={
                isPositive(card.key, state)
                  ? "text-[var(--color-green)]"
                  : "text-[var(--color-red)]"
              }
            >
              {formatSub(card.key, state)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

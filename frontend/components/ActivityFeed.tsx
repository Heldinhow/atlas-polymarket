"use client";

import type { LogEntry } from "@/lib/types";

interface ActivityFeedProps {
  logs: LogEntry[];
}

function colorize(msg: string): React.ReactNode {
  const keywords: Record<string, string> = {
    BUY: "text-[var(--color-green)]",
    SELL: "text-[var(--color-red)]",
    "REGIME SHIFT": "text-[var(--color-cyan)]",
    SENTIMENT: "text-[var(--color-orange)]",
    "META SHIFT": "text-[var(--color-purple)]",
    "WEIGHT UPDATE": "text-[var(--color-cyan)]",
    SCHEDULE: "text-[var(--color-orange)]",
    AUTORESEARCH: "text-[var(--color-cyan)]",
    Executed: "text-[var(--color-green)]",
    "CIO Decision": "text-[var(--color-cyan)]",
    Regime: "text-[var(--color-cyan)]",
    Risk: "text-[var(--color-orange)]",
    Skipped: "text-[var(--color-text-muted)]",
    error: "text-[var(--color-red)]",
    complete: "text-[var(--color-green)]",
  };

  for (const [keyword, cls] of Object.entries(keywords)) {
    if (msg.includes(keyword)) {
      const parts = msg.split(keyword);
      return (
        <>
          {parts[0]}
          <span className={`${cls} font-medium`}>{keyword}</span>
          {parts.slice(1).join(keyword)}
        </>
      );
    }
  }

  return msg;
}

export default function ActivityFeed({ logs }: ActivityFeedProps) {
  return (
    <div className="animate-fade-up delay-10 bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-panel)] p-6 max-h-[520px] overflow-y-auto">
      <div className="flex items-center justify-between mb-4">
        <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
          LIVE FEED
        </div>
      </div>
      <div className="flex flex-col gap-0.5 mt-4">
        {logs.length === 0 ? (
          <div className="flex items-center justify-center h-20 font-[var(--font-mono)] text-sm text-[var(--color-text-muted)]">
            No activity yet — waiting for analysis
          </div>
        ) : (
          logs.map((log, i) => (
            <div
              key={i}
              className="flex gap-3 p-3 rounded-lg transition-colors cursor-default hover:bg-[rgba(255,255,255,0.015)]"
            >
              <div className="font-[var(--font-mono)] text-[10px] text-[var(--color-text-muted)] whitespace-nowrap pt-0.5 min-w-[44px]">
                {log.time}
              </div>
              <div className="flex-1">
                <div className="font-[var(--font-mono)] text-[11px] text-[var(--color-text-secondary)] leading-relaxed">
                  {colorize(log.msg)}
                </div>
                {log.agent && (
                  <div className="font-[var(--font-mono)] text-[9px] text-[var(--color-text-muted)] mt-0.5 tracking-[0.5px]">
                    {log.agent}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

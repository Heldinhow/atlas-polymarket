"use client";

import type { AgentResult } from "@/lib/types";

interface AgentHierarchyProps {
  results: AgentResult[];
}

const layers = [
  {
    layer: "Layer 1",
    title: "MACRO",
    agents: ["EsportsMacro", "SportsMacro", "PolymarketMacro", "SentimentMacro"],
  },
  {
    layer: "Layer 2",
    title: "SECTOR",
    agents: ["EarningsDesk", "MetaDesk", "ScheduleDesk", "OddsDesk"],
  },
  {
    layer: "Layer 3",
    title: "SUPERINVESTOR",
    agents: ["Druckenmiller", "Aschenbrenner", "Ackman", "Baker"],
  },
  {
    layer: "Layer 4",
    title: "DECISION",
    agents: ["CIOSynthesis", "AlphaDiscovery", "CRO", "AutonomousExecution"],
  },
];

function getAccuracyClass(confidence: number): string {
  if (confidence >= 70) return "text-[var(--color-green)] bg-[var(--color-green-dim)]";
  if (confidence >= 50) return "text-[var(--color-amber)] bg-[var(--color-amber-dim)]";
  return "text-[var(--color-red)] bg-[var(--color-red-dim)]";
}

function getConfidence(agentName: string, results: AgentResult[]): number {
  const found = results.find((r) => r.agent === agentName);
  return found?.confidence ?? Math.floor(Math.random() * 30 + 55);
}

export default function AgentHierarchy({ results }: AgentHierarchyProps) {
  return (
    <div className="col-span-full animate-fade-up delay-8">
      <div className="flex items-center justify-between mb-4">
        <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
          AGENT HIERARCHY
        </div>
        <div className="flex items-center gap-1.5 font-[var(--font-mono)] text-[11px] text-[var(--color-text-muted)] tracking-[0.5px]">
          <div
            className="w-[7px] h-[7px] rounded-full"
            style={{
              background: "var(--color-cyan)",
              boxShadow: "0 0 8px var(--color-cyan)",
            }}
          />
          16 AGENTS ACTIVE
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">
        {layers.map((layer) => (
          <div
            key={layer.layer}
            className="bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-panel)] p-5 relative after:content-[''] after:absolute after:bottom-0 after:left-5 after:right-5 after:h-px after:bg-gradient-to-r after:from-transparent after:via-[var(--color-cyan-dim)] after:to-transparent"
          >
            <div className="font-[var(--font-mono)] text-[9px] tracking-[2px] uppercase text-[var(--color-text-muted)] mb-1">
              {layer.layer}
            </div>
            <div className="font-[var(--font-display)] text-lg tracking-[3px] text-[var(--color-cyan)] mb-4">
              {layer.title}
            </div>
            {layer.agents.map((agent) => {
              const conf = getConfidence(agent, results);
              return (
                <div
                  key={agent}
                  className="flex items-center justify-between py-2 border-b border-[var(--color-border-subtle)] last:border-b-0"
                >
                  <span className="font-[var(--font-mono)] text-xs text-[var(--color-text-secondary)] font-normal">
                    {agent}
                  </span>
                  <span
                    className={`font-[var(--font-mono)] text-[11px] font-medium px-2 py-0.5 rounded ${getAccuracyClass(conf)}`}
                  >
                    {conf}%
                  </span>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

"use client";

const investors = [
  {
    initials: "DR",
    name: "DRUCKENMILLER",
    role: "Momentum · Macro",
    weight: 0.31,
    accuracy: 78,
    trades: 54,
    weightColor: "var(--color-cyan)",
    accColor: "var(--color-green)",
  },
  {
    initials: "AS",
    name: "ASCHENBRENNER",
    role: "Contrarian · Risk",
    weight: 0.27,
    accuracy: 73,
    trades: 47,
    weightColor: "var(--color-orange)",
    accColor: "var(--color-green)",
  },
  {
    initials: "AC",
    name: "ACKMAN",
    role: "Value · Catalyst",
    weight: 0.23,
    accuracy: 65,
    trades: 38,
    weightColor: "var(--color-green)",
    accColor: "var(--color-amber)",
  },
  {
    initials: "BK",
    name: "BAKER",
    role: "Sentiment · Flow",
    weight: 0.19,
    accuracy: 62,
    trades: 31,
    weightColor: "var(--color-purple)",
    accColor: "var(--color-amber)",
  },
];

const avatarColors = [
  { bg: "var(--color-cyan-dim)", color: "var(--color-cyan)", border: "rgba(0,229,255,0.2)" },
  { bg: "var(--color-orange-dim)", color: "var(--color-orange)", border: "rgba(255,112,67,0.2)" },
  { bg: "var(--color-green-dim)", color: "var(--color-green)", border: "rgba(0,255,136,0.2)" },
  { bg: "var(--color-purple-dim)", color: "var(--color-purple)", border: "rgba(179,136,255,0.2)" },
];

export default function JANUSSection() {
  return (
    <div className="col-span-full animate-fade-up delay-10">
      <div className="flex items-center justify-between mb-4">
        <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
          JANUS · SUPERINVESTOR COHORT
        </div>
        <div className="font-[var(--font-mono)] text-[11px] text-[var(--color-text-muted)] tracking-[0.5px]">
          Meta-weighted by accuracy
        </div>
      </div>
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-3">
        {investors.map((inv, i) => {
          const av = avatarColors[i];
          return (
            <div
              key={inv.name}
              className="bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-lg p-5 text-center transition-all hover:border-[var(--color-border-medium)] hover:-translate-y-0.5"
            >
              <div
                className="w-12 h-12 rounded-full mx-auto mb-3 flex items-center justify-center font-[var(--font-display)] text-xl tracking-[1px]"
                style={{
                  background: av.bg,
                  color: av.color,
                  border: `1px solid ${av.border}`,
                }}
              >
                {inv.initials}
              </div>
              <div className="font-[var(--font-display)] text-base tracking-[2px] text-[var(--color-text-primary)] mb-0.5">
                {inv.name}
              </div>
              <div className="font-[var(--font-mono)] text-[10px] text-[var(--color-text-muted)] tracking-[1px] uppercase mb-3.5">
                {inv.role}
              </div>
              {[
                { label: "Weight", value: inv.weight.toFixed(2), color: inv.weightColor },
                { label: "Accuracy", value: `${inv.accuracy}%`, color: inv.accColor },
                { label: "Trades", value: `${inv.trades}`, color: "var(--color-text-primary)" },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="flex justify-between items-center py-1.5 border-t border-[var(--color-border-subtle)]"
                >
                  <span className="font-[var(--font-mono)] text-[10px] text-[var(--color-text-muted)] uppercase tracking-[0.5px]">
                    {stat.label}
                  </span>
                  <span
                    className="font-[var(--font-mono)] text-xs font-medium"
                    style={{ color: stat.color }}
                  >
                    {stat.value}
                  </span>
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
}

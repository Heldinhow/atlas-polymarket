"use client";

import { useEffect, useRef } from "react";
import type { PortfolioEntry } from "@/lib/types";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

interface PerformanceChartProps {
  portfolioData: PortfolioEntry[];
}

const TABS = ["7D", "30D", "90D", "ALL"];

export default function PerformanceChart({
  portfolioData,
}: PerformanceChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartRef = useRef<Chart | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const ctx = canvasRef.current.getContext("2d");
    if (!ctx) return;

    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const labels = portfolioData.map((d) => d.label);
    const data = portfolioData.map((d) => d.value);

    const gradient = ctx.createLinearGradient(0, 0, 0, 280);
    gradient.addColorStop(0, "rgba(0, 229, 255, 0.12)");
    gradient.addColorStop(0.5, "rgba(0, 229, 255, 0.03)");
    gradient.addColorStop(1, "rgba(0, 229, 255, 0)");

    chartRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            data,
            borderColor: "#00e5ff",
            borderWidth: 2,
            backgroundColor: gradient,
            fill: true,
            tension: 0.4,
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#00e5ff",
            pointHoverBorderColor: "#0a0a12",
            pointHoverBorderWidth: 3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: "index",
          intersect: false,
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#1a1a2e",
            titleColor: "#8888a0",
            bodyColor: "#e8e8f0",
            borderColor: "rgba(255,255,255,0.08)",
            borderWidth: 1,
            titleFont: { family: "'DM Mono', monospace", size: 10 },
            bodyFont: {
              family: "'DM Mono', monospace",
              size: 13,
              weight: 500,
            },
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              title: (items) => items[0].label.toUpperCase(),
              label: (item) => "$" + (item.parsed.y ?? 0).toLocaleString(),
            },
          },
        },
        scales: {
          x: {
            grid: {
              color: "rgba(255,255,255,0.03)",
            },
            ticks: {
              color: "#55556a",
              font: { family: "'DM Mono', monospace", size: 10 },
            },
            border: { display: false },
          },
          y: {
            position: "right",
            grid: {
              color: "rgba(255,255,255,0.03)",
            },
            ticks: {
              color: "#55556a",
              font: { family: "'DM Mono', monospace", size: 10 },
              callback: (v) => "$" + ((v as number) / 1000).toFixed(0) + "k",
              maxTicksLimit: 5,
            },
            border: { display: false },
          },
        },
      },
    });

    return () => {
      chartRef.current?.destroy();
    };
  }, [portfolioData]);

  return (
    <div className="col-span-full xl:col-span-2 animate-fade-up delay-6 bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-panel)] p-6">
      <div className="flex items-center justify-between mb-5">
        <div className="font-[var(--font-display)] text-xl tracking-[3px] text-[var(--color-text-primary)]">
          PORTFOLIO PERFORMANCE
        </div>
        <div className="flex gap-1 bg-[var(--color-bg-deep)] p-[3px] rounded-md">
          {TABS.map((tab, i) => (
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
      <div className="relative h-[280px]">
        <canvas ref={canvasRef} />
      </div>
    </div>
  );
}

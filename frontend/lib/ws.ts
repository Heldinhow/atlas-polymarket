"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import type { DashboardState } from "./types";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:3001/ws";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";

const DEFAULT_STATE: DashboardState = {
  status: "idle",
  last_update: null,
  markets: [],
  layer1_results: [],
  regime: null,
  cio_decision: null,
  portfolio: { balance: 10000, positions: [], pnl: 0 },
  logs: [],
  volume_data: [],
  portfolio_history: [
    { label: "Mon", value: 44200 },
    { label: "Tue", value: 45100 },
    { label: "Wed", value: 44800 },
    { label: "Thu", value: 46300 },
    { label: "Fri", value: 45900 },
    { label: "Sat", value: 47100 },
    { label: "Sun", value: 47832 },
  ],
  prism_probabilities: {
    RECOVERY: 62,
    CRISIS: 8,
    RATE_TIGHTENING: 12,
    BULL_LOW_VOL: 14,
    EUPHORIA: 4,
  },
  win_rate: 0,
  total_trades: 0,
  winning_trades: 0,
  sharpe_ratio: 0,
  active_positions_count: 0,
};

export function useDashboard() {
  const [state, setState] = useState<DashboardState>(DEFAULT_STATE);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as DashboardState;
        setState(data);
      } catch {
        // ignore malformed messages
      }
    };

    ws.onclose = () => {
      setConnected(false);
      reconnectRef.current = setTimeout(connect, 3000);
    };

    ws.onerror = () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectRef.current);
      wsRef.current?.close();
    };
  }, [connect]);

  const runAnalysis = useCallback(async () => {
    try {
      await fetch(`${API_URL}/api/run`, { method: "POST" });
    } catch {
      // silently fail
    }
  }, []);

  return { state, connected, runAnalysis };
}

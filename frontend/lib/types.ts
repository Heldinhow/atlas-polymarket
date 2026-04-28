export interface DashboardState {
  status: string;
  last_update: string | null;
  markets: Market[];
  layer1_results: AgentResult[];
  regime: string | null;
  cio_decision: CIODecision | null;
  portfolio: Portfolio;
  logs: LogEntry[];
  volume_data: VolumeEntry[];
  portfolio_history: PortfolioEntry[];
  prism_probabilities: Record<string, number>;
  win_rate: number;
  total_trades: number;
  winning_trades: number;
  sharpe_ratio: number;
  active_positions_count: number;
}

export interface Market {
  question: string;
  volume24hr?: number;
  [key: string]: unknown;
}

export interface AgentResult {
  agent: string;
  regime: string;
  analysis: string;
  confidence: number;
}

export interface CIODecision {
  action: string;
  confidence: number;
  synthesis: string;
}

export interface Portfolio {
  balance: number;
  positions: Position[];
  pnl: number;
}

export interface Position {
  market_id: string;
  side?: string;
  amount: number;
  cost: number;
  avg_price: number;
  current_price?: number;
  pnl?: number;
  category?: string;
  subtitle?: string;
  agent?: string;
}

export interface LogEntry {
  time: string;
  msg: string;
  agent?: string;
}

export interface VolumeEntry {
  question: string;
  volume: number;
}

export interface PortfolioEntry {
  label: string;
  value: number;
}

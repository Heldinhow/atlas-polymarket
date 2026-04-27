"""Professional Dash dashboard for ATLAS-Polymarket trading system."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import threading
from datetime import datetime
from dash import Dash, html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px

from src.config import get_settings
from src.agents.layer1 import (
    EsportsMacroAgent,
    SportsMacroAgent,
    PolymarketMacroAgent,
    SentimentMacroAgent,
)
from src.agents.layer4 import (
    CIOSynthesisAgent,
    CROAgent,
    AutonomousExecutionAgent,
)
from src.core.prism import PRISM
from src.data.polymarket_client import PolymarketClient
from src.execution.paper_trade import PaperTrader

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    "/assets/styles.css"
])

# Global state
state = {
    "status": "idle",
    "last_update": None,
    "markets": [],
    "layer1_results": [],
    "regime": None,
    "cio_decision": None,
    "portfolio": {"balance": 10000, "positions": [], "pnl": 0},
    "logs": [],
    "volume_data": [],
}


def log(msg):
    """Add log entry."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    state["logs"].insert(0, {"time": timestamp, "msg": msg})
    if len(state["logs"]) > 100:
        state["logs"] = state["logs"][:100]


async def run_analysis():
    """Run one trading cycle."""
    state["status"] = "running"
    state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log("Starting analysis...")

    settings = get_settings()
    trader = PaperTrader() if settings.paper_trade else None

    # Agents
    layer1_agents = [
        EsportsMacroAgent(),
        SportsMacroAgent(),
        PolymarketMacroAgent(),
        SentimentMacroAgent(),
    ]
    cio = CIOSynthesisAgent()
    cro = CROAgent()
    executor = AutonomousExecutionAgent(paper_trade=settings.paper_trade)
    prism = PRISM()

    # Fetch markets
    polymarket = PolymarketClient(api_key=settings.polymarket_api_url)
    all_markets = await polymarket.get_markets()
    markets = sorted(all_markets, key=lambda x: x.get("volume24hr", 0), reverse=True)[:20]
    state["markets"] = markets[:15]
    state["volume_data"] = [
        {"question": m.get("question", "")[:50], "volume": m.get("volume24hr", 0)}
        for m in markets[:15]
    ]
    log(f"Fetched {len(markets)} markets")
    await polymarket.close()

    # Layer 1 analysis
    log("Analyzing with Layer 1 agents...")
    layer1_results = []
    for agent in layer1_agents:
        market_summary = [
            {"question": m.get("question", "")[:60], "volume": m.get("volume24hr", 0)}
            for m in markets[:10]
        ]
        result = await agent.analyze({"markets": market_summary})
        layer1_results.append({
            "agent": agent.name,
            "regime": result.get("regime", "UNKNOWN"),
            "analysis": result.get("analysis", ""),
            "confidence": result.get("confidence", 0),
        })
        log(f"  {agent.name}: {result.get('regime', 'UNKNOWN')}")

    state["layer1_results"] = layer1_results

    # Regime detection
    total_volume = sum(m.get("volume24hr", 0) for m in markets)
    regime = prism.detect_regime({"volume": total_volume, "volatility": "medium", "sentiment": "neutral"})
    state["regime"] = regime.value
    log(f"Regime: {regime.value}")

    # CIO decision
    log("Running CIO synthesis...")
    synthesis = await cio.synthesize(
        layer1_output=layer1_results[0] if layer1_results else {},
        layer2_output={},
        layer3_output={},
    )
    state["cio_decision"] = {
        "action": synthesis.get("action", "HOLD"),
        "confidence": synthesis.get("confidence", 0),
        "synthesis": synthesis.get("synthesis", ""),
    }
    log(f"CIO Decision: {synthesis.get('action')} (conf: {synthesis.get('confidence')})")

    # Execute if confident
    if synthesis.get("action") == "BUY" and synthesis.get("confidence", 0) >= 7 and markets:
        signal = {
            "action": synthesis["action"],
            "market": markets[0].get("question", "Unknown"),
            "confidence": synthesis["confidence"],
        }
        if trader:
            risk = await cro.assess_risk({"position": signal, "portfolio_value": trader.balance})
            log(f"  Risk: {risk.get('risk_score')}/10")
        exec_result = await executor.execute(signal)
        log(f"  Executed: {exec_result.get('status')}")
    else:
        log("  Skipped (low confidence)")

    # Portfolio
    if trader:
        state["portfolio"] = {
            "balance": trader.balance,
            "positions": trader.get_positions(),
            "pnl": trader.get_total_pnl(),
        }

    state["status"] = "idle"
    log("Analysis complete")


def background_task():
    """Run analysis in background thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_analysis())


# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("ATLAS-Polymarket", className="header-title"),
        html.Div([
            html.Span("Status: ", className="label"),
            html.Span(id="status-badge", children="IDLE", className="badge badge-idle"),
        ], className="header-status"),
        html.Div([
            html.Span("Last: ", className="label"),
            html.Span(id="last-update", children="Never"),
        ], className="header-time"),
        html.Button("Run Analysis", id="run-btn", n_clicks=0, className="btn-primary"),
    ], className="header"),

    # Stats cards
    html.Div([
        html.Div([
            html.H3("Portfolio Balance"),
            html.P(id="balance-value", children="$10,000.00", className="stat-value"),
        ], className="stat-card"),
        html.Div([
            html.H3("Total P&L"),
            html.P(id="pnl-value", children="$0.00", className="stat-value"),
        ], className="stat-card"),
        html.Div([
            html.H3("Market Regime"),
            html.P(id="regime-value", children="N/A", className="stat-value"),
        ], className="stat-card"),
        html.Div([
            html.H3("CIO Decision"),
            html.P(id="decision-value", children="HOLD", className="stat-value"),
        ], className="stat-card"),
    ], className="stats-grid"),

    # Charts row
    html.Div([
        html.Div([
            html.H3("Market Volumes (Top 15)"),
            dcc.Graph(id="volume-chart"),
        ], className="chart-card"),
        html.Div([
            html.H3("Agent Regime Distribution"),
            dcc.Graph(id="regime-pie"),
        ], className="chart-card"),
    ], className="charts-row"),

    # Agent analysis
    html.Div([
        html.H2("Layer 1 Agent Analysis"),
        html.Div(id="agent-cards", className="agent-grid"),
    ], className="section"),

    # CIO Decision detail
    html.Div([
        html.H2("CIO Synthesis"),
        html.Div([
            html.Div([
                html.Span("Action: ", className="label"),
                html.Span(id="cio-action", className="action-value"),
            ]),
            html.Div([
                html.Span("Confidence: ", className="label"),
                html.Span(id="cio-confidence"),
            ]),
        ], className="cio-header"),
        html.P(id="cio-reasoning", className="cio-reasoning"),
    ], className="section cio-card"),

    # Logs
    html.Div([
        html.H2("Activity Log"),
        html.Div(id="log-container", className="log-container"),
    ], className="section"),

    # Interval for auto-refresh
    dcc.Interval(id="refresh-interval", interval=3000, n_intervals=0),
], className="dashboard")


@app.callback(
    Output("status-badge", "children"),
    Output("status-badge", "className"),
    Output("last-update", "children"),
    Output("balance-value", "children"),
    Output("pnl-value", "children"),
    Output("regime-value", "children"),
    Output("decision-value", "children"),
    Output("decision-value", "className"),
    Output("volume-chart", "figure"),
    Output("regime-pie", "figure"),
    Output("agent-cards", "children"),
    Output("cio-action", "children"),
    Output("cio-confidence", "children"),
    Output("cio-reasoning", "children"),
    Output("log-container", "children"),
    Input("refresh-interval", "n_intervals"),
)
def update_dashboard(n):
    """Update all dashboard components."""
    # Status
    status = state["status"].upper()
    status_class = f"badge badge-{state['status']}"

    # Time
    last_update = state["last_update"] or "Never"

    # Portfolio
    balance = f"${state['portfolio']['balance']:,.2f}"
    pnl = state["portfolio"]["pnl"]
    pnl_str = f"${pnl:+,.2f}"

    # Regime
    regime = state["regime"] or "N/A"

    # Decision
    decision = state["cio_decision"]["action"] if state["cio_decision"] else "HOLD"
    decision_class = f"action-value action-{decision.lower()}"

    # Volume chart
    vol_data = state.get("volume_data", [])
    if vol_data:
        fig_bar = px.bar(
            vol_data,
            x="question",
            y="volume",
            template="plotly_dark",
            color_discrete_sequence=["#00D4FF"],
        )
        fig_bar.update_layout(
            paper_bgcolor="transparent",
            plot_bgcolor="transparent",
            font={"color": "#E0E0E0"},
            height=300,
            margin=dict(l=20, r=20, t=20, b=100),
            xaxis_title="",
            yaxis_title="Volume (24h)",
        )
        fig_bar.update_traces(width=0.7)
    else:
        fig_bar = go.Figure()

    # Regime pie
    regimes = [r["regime"] for r in state["layer1_results"]]
    regime_counts = {}
    for r in regimes:
        regime_counts[r] = regime_counts.get(r, 0) + 1
    if regime_counts:
        fig_pie = px.pie(
            list(regime_counts.keys()),
            values=list(regime_counts.values()),
            names=list(regime_counts.keys()),
            template="plotly_dark",
            color_discrete_sequence=["#00D4FF", "#FF6B6B", "#28A745", "#FFC107", "#6F42C1"],
        )
        fig_pie.update_layout(
            paper_bgcolor="transparent",
            font={"color": "#E0E0E0"},
            height=250,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
        )
    else:
        fig_pie = go.Figure()

    # Agent cards
    agent_cards = []
    for r in state["layer1_results"]:
        card = html.Div([
            html.H4(r["agent"]),
            html.Div([
                html.Span(r["regime"], className=f"regime-badge regime-{r['regime'].lower()}"),
                html.Span(f"Conf: {r['confidence']}", className="confidence"),
            ], className="agent-meta"),
            html.P(r["analysis"][:150] + "..." if len(r["analysis"]) > 150 else r["analysis"], className="agent-analysis"),
        ], className="agent-card")
        agent_cards.append(card)

    # CIO
    cio_action = state["cio_decision"]["action"] if state["cio_decision"] else "N/A"
    cio_confidence = f"{state['cio_decision']['confidence']}/10" if state["cio_decision"] else "N/A"
    cio_reasoning = state["cio_decision"]["synthesis"][:300] if state["cio_decision"] else "No analysis run yet."

    # Logs
    log_items = [
        html.Div([
            html.Span(log["time"], className="log-time"),
            html.Span(log["msg"], className="log-msg"),
        ], className="log-entry")
        for log in state["logs"][:20]
    ]

    return (
        status, status_class, last_update,
        balance, pnl_str, regime,
        decision, decision_class,
        fig_bar, fig_pie,
        agent_cards,
        cio_action, cio_confidence, cio_reasoning,
        log_items
    )


@app.callback(
    Output("run-btn", "disabled"),
    Input("run-btn", "n_clicks"),
)
def run_analysis_callback(n_clicks):
    """Trigger analysis on button click."""
    if n_clicks > 0 and state["status"] != "running":
        threading.Thread(target=background_task, daemon=True).start()
    return state["status"] == "running"


if __name__ == "__main__":
    print("=" * 50)
    print("ATLAS-Polymarket Dashboard")
    print("Open: http://localhost:8050")
    print("=" * 50)
    app.run(host="0.0.0.0", port=8050, debug=False)

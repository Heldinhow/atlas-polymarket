# ATLAS-Polymarket: Design Specification

## Overview

Framework de trading autonomo baseado no ATLAS, adaptado para mercados de esports/sports do Polymarket. Usa agentes de IA hierárquicos em 4 camadas que analisam, decidem e executam trades automaticamente.

**Origem:** Adaptado de [ATLAS by General Intelligence Capital](https://github.com/chrisworsey55/atlas-gic)
**Domínio:** Trading em mercados de esports/sports do Polymarket

---

## Architecture: 4 Layers

### Layer 1 - Macro Agents (Mercado)
- `EsportsMacro`: Analisa tendências de esports (meta de jogos, popularidade, torneios)
- `SportsMacro`: Analisa tendências de sports (ligas, temporadas, transferências)
- `PolymarketMacro`: Analisa volume, liquidez e fluxo de dinheiro no Polymarket
- `SentimentMacro`: Monitora narrativas sociais sobre times/jogadores

### Layer 2 - Sector Desk Agents
- `EarningsDesk`: Analisa desempenho de equipes/times (head-to-head, forma recente)
- `MetaDesk`: Analisa "meta" atual (meta de jogo, patch notes, estratégias)
- `ScheduleDesk`: Analisa calendário de jogos, cansaço de equipes, home/away
- `OddsDesk`: Compara probabilidades do Polymarket com odds de sportsbooks

### Layer 3 - Superinvestor Agents
- `DruckenmillerBot`: Posicionamentos macro baseado em tendências
- `AschenbrennerBot`: Identificação de narrativas de alto impacto
- `AckmanBot`: Apostas de alta convicção em poucas escolhas
- `BakerBot`: Análise quantitativa e modelagem de probabilidades

### Layer 4 - Decision Layer
- `CIOSynthesis`: Síntese final de todas as análises
- `AlphaDiscovery`: Identifica alphas não explorados
- `CRO`: Gestão de risco e position sizing
- `AutonomousExecution`: Executa trades baseados em sinais

---

## Data Flow

```
Polymarket API ──┐
                 ├──> Layer 1 (Macro) ──> Layer 2 (Sector) ──> Layer 3 (Superinvestors) ──> Layer 4 (Decision) ──> Execution
External APIs ───┘        │                    │                    │                         │
(Sports/Esports)          v                    v                    v                         v
                    Regime Detection    Sector Analysis     Position Building          Risk Check
```

### Fontes de Dados
- **Polymarket API**: Preços, volumes, mercados
- **APIs de Esports**: PandaScore, ESportsAPI, etc.
- **APIs de Sports**: TheSportsDB, API-Football, etc.
- **Dados de Odds**: OddsAPI, TheOddsAPI

---

## Autoresearch Loop

Inspirado no Karpathy's autoresearch:

1. Identificar pior agente (menor Sharpe ratio)
2. Gerar modificação de prompt
3. Testar por 5 dias (trades simuladas)
4. Se positivo → Commit mudança no git
5. Se negativo → Reverter mudança

Versionamento de prompts via git.

---

## Execution Modes

**Variável de ambiente:** `PAPER_TRADE=true/false`

| Mode | Description |
|------|-------------|
| `PAPER_TRADE=true` | Trades simuladas, sem wallet real |
| `PAPER_TRADE=false` | Conecta com wallet real para execução |

**Fases de Deploy:**
1. **Fase 1**: Paper trade até validar performance (Sharpe > 1.0)
2. **Fase 2**: Live trading gradual (start small, 5-10% do bankroll)

---

## Tech Stack

- **Linguagem**: Python 3.11+
- **LLM**: MiniMax API (mesma configuração do Claude Code)
- **Infra**: VPS Contabo (existente)
- **Dados**: Polymarket API + fontes externas
- **Storage**:
  - PostgreSQL: Portfolio, trades, histórico
  - Redis: Cache de dados, filas

---

## Sistema PRISM (Market Regimes)

Cinco regimes de mercado para training:

1. **Bull/Low Vol**: Mercado tranquilo, probabilidades estáveis
2. **Crisis**: Eventos inesperados, volumes altos
3. **Rate Tightening**: Mudanças rápidas de odds
4. **Recovery**: Reversão de tendências
5. **Euphoria**: Hype tinggi, volumes extremos

---

## Sistema JANUS (Meta-Weighting)

Camada meta que pondera automaticamente múltiplas cohortes de agentes baseado em accuracy recente.

---

## Sistema Soros Reflexivity Engine

Modela feedback loops de mercado:
- Price → Fundamentals
- P&L → Behavior
- Narrative → Flows

---

## Scope Inicial (MVP)

**Incluído:**
- Framework de 4 layers completo
- Autoresearch loop
- Papel PRISM e JANUS
- Polymarket API integration
- Umas 2-3 APIs externas de dados
- Paper trading mode
- Estrutura准备好 para live trading

**Excluído (futuro):**
- Live trading (até validar paper trade)
- Múltiplas wallets/exchanges
- Otimização de prompts mais avançada

---

## Success Criteria

1. Paper trade por 30 dias com Sharpe > 1.0
2. Drawdown máximo < 20%
3. Positivas trades > 55%
4. Taxa de sobrevivência do autoresearch > 25%

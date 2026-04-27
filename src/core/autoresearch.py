"""Autoresearch loop - self-improving agent prompts."""
from __future__ import annotations

import subprocess
from datetime import datetime, timedelta
from typing import Any, Optional


class Autoresearch:
    """Self-improving agent prompt system inspired by Karpathy's autoresearch."""

    def __init__(self, test_duration_days: int = 5):
        self.test_duration_days = test_duration_days
        self.tracking_file = ".agent_sharpe.json"

    async def identify_worst_agent(self) -> str:
        """Identify worst performing agent by Sharpe ratio."""
        metrics = await self.get_agent_metrics()
        if not metrics:
            return ""

        worst_agent = min(metrics.items(), key=lambda x: x[1].get("sharpe", 0))
        return worst_agent[0]

    async def get_agent_metrics(self) -> dict[str, Any]:
        """Get Sharpe ratios for all agents from tracking file."""
        import json
        import os

        if not os.path.exists(self.tracking_file):
            return {}

        with open(self.tracking_file) as f:
            data = json.load(f)
        return data.get("agents", {})

    async def generate_prompt_modification(
        self, agent_name: str, performance_issue: str
    ) -> str:
        """Generate a prompt modification for underperforming agent."""
        from src.agents.base import BaseAgent

        agent = self._load_agent(agent_name)
        prompt = f"""Analyze this agent's performance issue and generate a prompt modification:

Agent: {agent_name}
Current Prompt: {agent.prompt if agent else 'Unknown'}
Issue: {performance_issue}

Generate a specific, targeted modification to improve performance.
Focus on: clarity, specificity, and actionable instructions.
"""
        response = await agent.think(prompt)
        return response

    def _load_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Load agent by name."""
        from src.agents.layer1 import EsportsMacroAgent, SportsMacroAgent
        from src.agents.layer1 import PolymarketMacroAgent, SentimentMacroAgent

        agents = {
            "EsportsMacro": EsportsMacroAgent,
            "SportsMacro": SportsMacroAgent,
            "PolymarketMacro": PolymarketMacroAgent,
            "SentimentMacro": SentimentMacroAgent,
        }

        agent_class = agents.get(agent_name)
        if agent_class:
            return agent_class()
        return None

    async def test_modification(
        self, agent_name: str, modification: str, test_days: int = 5
    ) -> dict[str, Any]:
        """Test a prompt modification for specified days."""
        start_date = datetime.now()
        end_date = start_date + timedelta(days=test_days)

        return {
            "agent": agent_name,
            "modification": modification,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": "TESTING",
        }

    async def commit_or_revert(self, test_result: dict[str, Any]) -> bool:
        """Commit successful modification or revert failed one."""
        if test_result.get("sharpe_improvement", 0) > 0:
            await self._commit_modification(test_result)
            return True
        else:
            await self._revert_modification(test_result)
            return False

    def _commit_modification(self, test_result: dict[str, Any]) -> None:
        """Commit the successful modification via git."""
        subprocess.run(
            ["git", "add", "-A"],
            cwd=".",
            check=True,
        )
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"feat(autoresearch): improve {test_result['agent']} prompt",
            ],
            check=True,
        )

    def _revert_modification(self, test_result: dict[str, Any]) -> None:
        """Revert to previous version."""
        subprocess.run(
            ["git", "revert", "HEAD"],
            cwd=".",
            check=True,
        )

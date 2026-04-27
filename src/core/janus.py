"""JANUS: Meta-weighting system for agent cohorts."""
from typing import Any


class JANUS:
    """Meta-layer that weights multiple agent cohorts by recent accuracy."""

    def __init__(self, decay_factor: float = 0.9):
        self.decay_factor = decay_factor
        self.agent_weights: dict[str, float] = {}
        self.agent_accuracy: dict[str, list[float]] = {}

    def update_accuracy(self, agent_name: str, accuracy: float) -> None:
        """Update accuracy history for an agent."""
        if agent_name not in self.agent_accuracy:
            self.agent_accuracy[agent_name] = []
        self.agent_accuracy[agent_name].append(accuracy)

        if len(self.agent_accuracy[agent_name]) > 10:
            self.agent_accuracy[agent_name] = self.agent_accuracy[agent_name][-10:]

        self._recompute_weight(agent_name)

    def _recompute_weight(self, agent_name: str) -> None:
        """Recompute weight based on recent accuracy."""
        accuracies = self.agent_accuracy.get(agent_name, [])
        if not accuracies:
            self.agent_weights[agent_name] = 1.0
            return

        recent_avg = sum(accuracies[-3:]) / min(len(accuracies), 3)
        self.agent_weights[agent_name] = recent_avg * self.decay_factor

    def get_weight(self, agent_name: str) -> float:
        """Get weight for an agent."""
        return self.agent_weights.get(agent_name, 1.0)

    def get_weighted_signal(
        self, signals: dict[str, tuple[str, float]]
    ) -> tuple[str, float]:
        """Get weighted average signal from multiple agents.

        Args:
            signals: dict of agent_name -> (signal, confidence)

        Returns:
            tuple of (dominant_signal, weighted_confidence)
        """
        weighted_scores: dict[str, float] = {"BUY": 0, "SELL": 0, "HOLD": 0}

        for agent_name, (signal, confidence) in signals.items():
            weight = self.get_weight(agent_name)
            weighted_scores[signal] += confidence * weight

        dominant = max(weighted_scores.items(), key=lambda x: x[1])
        return dominant[0], dominant[1]

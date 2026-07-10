"""Universe Explorer — v0 (black hole).

A knowledge-exploration system that honestly separates what humanity knows
from what it does not. Layer dependency is one-directional and irreversible:

    Data Layer -> Evidence Layer -> Knowledge Layer -> AI Narrative Layer

AI sits at the *bottom*. It may not fabricate facts or precision; it may only
organise evidence that has already been recorded with a real source.

This package implements the frozen v0 data model (model.py), a mechanical
constitution checker (validator.py), the four hand-filled black-hole claims
(data/black_hole.py) and a plain static-HTML renderer (render.py).
"""

from .model import (
    Status,
    STATUS_CONDITIONS,
    ConditionAssessment,
    Evidence,
    CompetingModel,
    Source,
    StatusChange,
    Claim,
    Topic,
)

__all__ = [
    "Status",
    "STATUS_CONDITIONS",
    "ConditionAssessment",
    "Evidence",
    "CompetingModel",
    "Source",
    "StatusChange",
    "Claim",
    "Topic",
]

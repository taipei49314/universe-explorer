"""Topic registry — the Data-layer seam (P4).

The whole cross-domain claim rests here: adding a domain means adding a Topic to
this list, nothing more. The engine (model / validator / axes / provenance /
proposals / watch) never learns a topic's name; it only ever receives a Topic.
"""

from __future__ import annotations

from typing import List

from ..model import Topic
from .black_hole import BLACK_HOLE
from .exoplanets import EXOPLANETS
from .ocean import OCEAN

TOPICS: List[Topic] = [BLACK_HOLE, OCEAN, EXOPLANETS]


def get_topic(topic_id: str) -> Topic:
    for t in TOPICS:
        if t.id == topic_id:
            return t
    raise KeyError(f"no topic {topic_id!r}; have {[t.id for t in TOPICS]}")

"""Topic registry — the Data-layer seam (P4).

The whole cross-domain claim rests here: adding a domain means adding a Topic to
this list, nothing more. The engine (model / validator / axes / provenance /
proposals / watch) never learns a topic's name; it only ever receives a Topic.
"""

from __future__ import annotations

from typing import List

from ..model import Topic
from .black_hole import BLACK_HOLE
from .cosmology import COSMOLOGY
from .dark_matter import DARK_MATTER
from .exoplanets import EXOPLANETS
from .ocean import OCEAN
from .planets import PLANETS
from .seismology import SEISMOLOGY
from .stars import STARS

# Theme clusters (documentation only; engine iterates TOPICS flat):
#   宇宙 cosmos  — cosmology, dark_matter, black_hole, stars
#   星球 planets — planets, exoplanets
#   地球 Earth   — ocean, seismology
TOPICS: List[Topic] = [
    BLACK_HOLE,
    COSMOLOGY,
    DARK_MATTER,
    STARS,
    EXOPLANETS,
    PLANETS,
    OCEAN,
    SEISMOLOGY,
]


def get_topic(topic_id: str) -> Topic:
    for t in TOPICS:
        if t.id == topic_id:
            return t
    raise KeyError(f"no topic {topic_id!r}; have {[t.id for t in TOPICS]}")

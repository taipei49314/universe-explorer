"""Pytest hooks for universe_explorer.

Note: modules that ``from universe_explorer.validator import validate_claim``
bind the function at import time; production default remains
``check_provenance=True`` (amendment-10 / C4). Shape-only unit tests should
pass ``check_provenance=False`` or use real cached endpoints.
"""

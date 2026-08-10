"""Cross-Domain Epistemic Map — find connections between isolated domains.

Three analysis passes:
  1. shared_source — scan all claims for cross-domain source sharing
  2. evidence_conflict — detect same-evidence-different-interpretation
  3. gap_analyzer — find structural evidence gaps per domain

Results feed into graph_builder (knowledge graph) and render_map (HTML).
"""

"""RETIRED — do not import from this module.

This was a second, parallel PRISM tracer that coexisted with
``app/observability/prism_tracer.py``. Both were wired into the live code
path at the same time (this one inside ``AgentRunner.process_turn``, the
other explicitly in ``app/server.py``'s ``/api/call/turn``), so every live
turn fired two independent trace requests to two different endpoints
(``/api/traces`` here, ``/api/spans/ingest`` there) -- double PRISM credit
consumption on a 98-of-100-credit Free-tier budget, plus duplicate,
differently-shaped records for the same conversation in the dashboard.

This module's own header comment also misquoted its cited source
(``docs/research/prism/03-fastapi-agent-integration-recipe.md``'s decision
table): it claimed ``/api/traces`` was "the sanctioned path" for a
hand-rolled FastAPI tool-calling agent, when that table actually
recommends structured ``/api/spans/ingest`` for exactly this case.

``app/observability/prism_tracer.py`` is the canonical tracer -- it already
had correct per-version ``agent_id`` mapping, ``category``/``eval_set``
support, structured nested spans (tool calls and commit-window transitions
as separate child spans), and it uses the endpoint the team's own research
recommends for this architecture. ``app/server.py`` and ``evals/checker.py``
both build a ``TurnTracer`` from it directly -- do the same for any new
call site instead of resurrecting this module.
"""

raise ImportError(
    "app.prism_tracing is retired. Use app.observability.prism_tracer.TurnTracer instead "
    "(see this module's docstring for why)."
)

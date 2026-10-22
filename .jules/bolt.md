
## 2025-02-28 - Bottleneck in _cambiar_estado_bulk updates
**Learning:** Looping over campaigns to individually query `mediosxcampania` and update `resultadosxcampania` in `_cambiar_estado_bulk` creates a severe N+1 query problem, doing ~3 queries per active campaign on a single WhatsApp reply webhook.
**Action:** When updating related records across multiple parent objects (like campaigns), gather the target IDs first using a single `__in` filter, build a combined `Q` object representing the final conditions, and perform a single `.update()` call.

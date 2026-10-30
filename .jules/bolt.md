
## 2024-05-24 - Bulk State Updates
**Learning:** The `_cambiar_estado_bulk` function executes an N+1 query loop when updating campaign states, resulting in a database query for each campaign.
**Action:** Use `.filter(campania_id__in=campanias)` and construct a single `.update()` using combined `Q()` objects to eliminate the N+1 problem.

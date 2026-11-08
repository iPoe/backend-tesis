## 2024-05-14 - Optimize _cambiar_estado_bulk in campaigns/views.py
**Learning:** The loop inside `_cambiar_estado_bulk` creates an N+1 query issue when iterating over `campanias` to execute `.filter().first()` and `.update()`. This leads to ~3N+1 queries for N campaigns.
**Action:** Used bulk `.filter()` fetch on `mediosxcampania` and a single `.update()` with combined `Q` objects to resolve the bottleneck and reduce it to exactly 3 queries.

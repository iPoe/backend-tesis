
## 2024-05-18 - Optimized `_cambiar_estado_bulk` in `campaigns/views.py`
**Learning:** The `_cambiar_estado_bulk` function had an N+1 query problem by iterating through campaigns and individually calling `.first()` on `mediosxcampania` and then a separate `.update()` on `resultadosxcampania` for each iteration.
**Action:** The loop was replaced with a bulk `.filter()` fetch on `mediosxcampania` and a single `.update()` on `resultadosxcampania` using dynamically constructed `Q` objects with `|=`, which minimized database round trips significantly.

## 2023-10-29 - [Eliminating N+1 .update() with Q objects]
**Learning:** Bulk updates triggered sequentially within loops are an overlooked form of N+1 bottlenecks.
**Action:** When a bulk update applies conditionally to a known set of relational rows, group conditions with a single combined `Q()` object and apply a solitary `.update()` to eliminate the loop overhead entirely.

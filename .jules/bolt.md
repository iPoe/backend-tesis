
## 2024-06-28 - Optimize bulk updates across multiple dynamic criteria
**Learning:** In Django, solving N+1 query problems during mass assignments across disparate criteria (like specific pairs of foreign keys: `campania_id` and `medio_id`) requires dynamically constructing a `Q` object to combine `OR` conditions (`|=`). This reduces repetitive single-row `.update()` calls inside a loop into a single, efficient bulk `UPDATE` query.
**Action:** When updating rows within a loop where the filtering criteria change dynamically per iteration, use `Q` objects constructed iteratively with `|=` operator inside a `.filter()` combined with `.update()` to minimize database round trips and execute a single optimized query.

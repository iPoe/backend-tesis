
## 2023-10-28 - [N+1 Query Bottleneck in Bulk Updates]
**Learning:** Found an N+1 query issue in `_cambiar_estado_bulk` where each campaign in the active campaigns list independently queried `mediosxcampania` and updated `resultadosxcampania`, leading to O(N) queries relative to the number of campaigns. This pattern can quickly degrade performance when users are enrolled in multiple campaigns simultaneously.
**Action:** When updating multiple related objects mapped by parent instances in a loop, extract the IDs, fetch all mappings via `.filter(__in=)` combined with `.values_list()`, and build dynamic `Q` objects to perform a single `update()` operation instead of iterative updates.

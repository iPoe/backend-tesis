## 2024-05-24 - Bulk Q Object Updates
**Learning:** Replacing an iterative loop of ORM `.update()` calls with a single `.update()` using `Q` objects resolves N+1 performance bottlenecks in Django when updating multiple distinct relations.
**Action:** Use combined `Q` objects to perform bulk updates across varied conditions instead of executing separate updates inside a loop.

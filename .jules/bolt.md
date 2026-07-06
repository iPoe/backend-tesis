
## 2024-07-06 - Fixing N+1 in Multi-Criteria Bulk Updates
**Learning:** When performing updates based on multiple distinct criteria (like a set of specific composite keys from a foreign key pairing, rather than a simple `__in` filter on one column), creating an empty `Q()` object and iteratively appending `|= Q(field_A=val_A, field_B=val_B)` is the most efficient way to achieve O(1) query bulk updating in Django. However, passing an empty `Q()` to `.filter()` can match all rows and cause catastrophic mass updates, so checking `if q_objects:` before `.update()` is critical.
**Action:** Use `Q` objects with `|=` for complex bulk updates but strictly enforce an early return or `if q_objects:` safety check before calling `.update()`.

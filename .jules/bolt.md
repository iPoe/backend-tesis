## 2024-05-24 - Untracked Scratchpad Files Polluting PRs
**Learning:** When using python scripts for codebase exploration or rapid prototyping (e.g., `patch.py`), failing to explicitly clean them up results in dirty workspaces which fail code review if committed alongside the target optimizations.
**Action:** Always clean up temporary workspace files (`rm patch*.py run_tests_sqlite.py`) immediately after their useful purpose has ended, and strictly before calling `request_code_review` or `submit`.

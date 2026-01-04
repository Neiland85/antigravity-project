---
description: Start here - Become one with the data before writing any logic
---

# 🔬 Step 1: Inspect Data (Karpathy Rule #1)

Before touching any model code, you must deeply understand your inputs.

## Steps

1. Open SQLite DB and inspect the `questions` table:

   ```bash
   sqlite3 data/antigravity.db "SELECT * FROM questions LIMIT 10;"
   ```

2. Analyze the `oracle_cache.json` for cached responses:

   ```bash
   cat oracle_cache.json | python -m json.tool | head -50
   ```

3. Look for patterns:

   - What types of questions are users asking?
   - Are there repeated questions?
   - What's the average question length?

4. Document 3 observations in your notes before proceeding.

## Next Workflow

After completing this, run: `/baseline-model`

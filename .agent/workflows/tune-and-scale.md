---
description: Scale up once everything works on small data
---

# 🚀 Step 5: Tune and Scale (Karpathy Rule #5)

Only now do you scale. Never scale broken things.

## Steps

1. **Increase Context Window**:

   - Change `limit(5)` to `limit(10)` in the history query.
   - Measure impact on quality and latency.

2. **A/B Test Prompts**:

   - Create 2-3 variations of the System Prompt.
   - Log results in `EXPERIMENTS.md`.

3. **Monitor Costs**:

   ```bash
   # Check token usage in Gemini dashboard
   open https://ai.dev/usage
   ```

4. **Enable Production Mode**:

   - Set `MOCK_AI=false` in `.env`.
   - Monitor rate limits.

5. **Deploy**:
   ```bash
   docker-compose up -d --build
   docker-compose logs -f
   ```

## Full Cycle Complete! 🎉

Return to `/inspect-data` when adding new features.

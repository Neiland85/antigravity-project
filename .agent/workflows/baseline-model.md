---
description: Establish a dumb baseline before any fancy architecture
---

# 📊 Step 2: Baseline Model (Karpathy Rule #2)

Never start with a complex model. Start with the stupidest thing that could work.

## Steps

1. The current "baseline" is the `mock_responses` list in `web/main_web.py`.

   - This is literally hardcoded answers. Good. Document its "accuracy" (0%).

2. Test the simplest AI call (no context, no reasoning):

   ```python
   response = model.generate_content(f"Answer: {question}")
   ```

3. Measure qualitative "score":

   - Ask 5 questions manually.
   - Rate each answer 1-5.
   - Calculate average. This is your baseline score.

4. Log baseline in `EXPERIMENTS.md`:
   ```markdown
   | Model             | Context | Reasoning | Score |
   | ----------------- | ------- | --------- | ----- |
   | Baseline (no ctx) | ❌      | ❌        | X.X   |
   ```

## Next Workflow

After completing this, run: `/overfit-single-batch`

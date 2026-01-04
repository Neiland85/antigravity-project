---
description: Add context and constraints to prevent overfitting to examples
---

# 🛡️ Step 4: Add Regularization (Karpathy Rule #4)

Now that you can overfit, add constraints to generalize.

## Steps

1. **Add Context Window**: Enable the history retrieval in `web/main_web.py`:

   - The system already fetches `last_interactions`. Verify it's working.
   - Test with: `/history` endpoint to see stored Q&A.

2. **Add Temperature Control**:

   ```python
   generation_config = genai.GenerationConfig(temperature=0.7)
   model.generate_content(prompt, generation_config=generation_config)
   ```

3. **Add System Prompt Constraints**:

   - "Do not make up citations."
   - "If unsure, say 'I don't know'."
   - "Be concise: max 3 paragraphs."

4. Re-run 5 questions from Step 2. Compare scores.

## Next Workflow

After completing this, run: `/tune-and-scale`

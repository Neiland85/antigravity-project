---
description: Prove the model can memorize before generalizing
---

# 🎯 Step 3: Overfit a Single Batch (Karpathy Rule #3)

Can your model perfectly answer ONE question? If not, don't bother with thousands.

## Steps

1. Pick ONE specific question from your data:

   ```
   "¿Puede un bounded context demostrar su propia consistencia sin violar a Gödel?"
   ```

2. Craft the PERFECT expected answer manually (your "ground truth").

3. Modify the prompt in `IntuitionEngine` to include this as a "few-shot example":

   ```python
   example = "Q: [your question]\nA: [your perfect answer]"
   full_prompt = f"{example}\n\nNow answer: {user_question}"
   ```

4. Test if the model can reproduce your perfect answer when asked the SAME question.
   - If YES: Move to next step.
   - If NO: Debug the prompt until it works.

## Next Workflow

After completing this, run: `/add-regularization`

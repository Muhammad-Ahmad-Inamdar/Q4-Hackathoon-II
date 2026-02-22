---
name: response-confirmation
description: Generates clear, friendly confirmations after actions are performed, improving user trust and conversational clarity.
---

# Response Confirmation Skill

## Instructions
1. **Analyze tool result**
   - Check if operation succeeded
   - Extract key details (task title, ID, status)
   - Identify what changed

2. **Generate confirmation message**
   - Use natural, conversational language
   - Confirm the specific action taken
   - Include relevant details (e.g., task title)
   - Avoid technical jargon

3. **Match user's language style**
   - Mirror formality level
   - Use similar phrasing when appropriate
   - Keep tone friendly and helpful

4. **Provide next steps (optional)**
   - Suggest related actions if helpful
   - Offer to show results (e.g., "Would you like to see your task list?")

5. **Handle partial success**
   - Clearly state what succeeded and what failed
   - Explain why if known
   - Suggest corrective action

## Best Practices
- Be specific: "Added 'Buy groceries' to your tasks" not "Task added"
- Never exaggerate or misrepresent what happened
- Keep confirmations concise (1-2 sentences)
- Use positive, encouraging language
- Reflect exact action taken, not assumptions

from app.utils.logger import log_ai_interaction

from .ai_client import generate_ai_response


def generate_b2b_proposal(data):

    prompt = f"""
You are an AI assistant for a sustainability ecommerce platform.

Generate a sustainable corporate product proposal.

Return ONLY valid JSON in EXACTLY this format:

{{
 "product_mix": [
  {{
   "product": "",
   "quantity": 0
  }}
 ],
 "budget_allocation": {{
  "products": 0,
  "logistics": 0,
  "buffer": 0
 }},
 "impact_summary": ""
}}

Rules:
- Do NOT include explanations or markdown
- Do NOT add extra fields
- product_mix should contain 2–4 recommended sustainable products
- total budget allocation must not exceed the client budget
- impact_summary should briefly explain sustainability impact

Client Details:
Client type: {data.client_type}
Budget: {data.budget}
Employees: {data.employee_count}
Sustainability goal: {data.sustainability_goal}
"""

    response = generate_ai_response(prompt)

    log_ai_interaction(module="proposal_generator", prompt=prompt, response=response)

    return response

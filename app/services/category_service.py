from app.services.ai_client import generate_ai_response
from app.utils.logger import log_ai_interaction


def generate_impact_report(data):

    product_list = "\n".join(
        [
            f"- {p.product_name} (qty: {p.quantity}, material: {p.material})"
            for p in data.products
        ]
    )

    prompt = f"""
You are an AI sustainability analyst for an ecommerce platform.

Generate an environmental impact report for this order.

Return ONLY valid JSON in EXACTLY this format:

{{
  "order_id": "{data.order_id}",
  "plastic_saved_kg": 0.0,
  "carbon_avoided_kg": 0.0,
  "local_sourcing_summary": "example sentence",
  "impact_statement": "example impact summary"
}}

Rules:
- Return ONLY JSON (no markdown, no explanation)
- Do NOT add extra fields
- NEVER return null values
- plastic_saved_kg must be a number (float) >= 0
- carbon_avoided_kg must be a number (float) >= 0
- local_sourcing_summary must be exactly 1 sentence
- impact_statement must be 1-2 sentences summarizing the environmental benefit
- Use reasonable estimation logic (e.g. bamboo toothbrush avoids ~15g plastic vs plastic equivalent)

Order ID: {data.order_id}

Products:
{product_list}
"""

    response = generate_ai_response(prompt)

    log_ai_interaction(module="impact_generator", prompt=prompt, response=response)

    return response

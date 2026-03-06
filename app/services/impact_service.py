from app.services.ai_client import generate_ai_response
from app.utils.logger import log_ai_interaction


def generate_impact_report(data):

    product_list = "\n".join(
        [f"- {p.product_name} (qty: {p.quantity}, material: {p.material})" for p in data.products]
    )

    prompt = f"""
You are an AI sustainability analyst for an ecommerce platform.

Generate an environmental impact report for this order.

Return ONLY valid JSON in EXACTLY this format:

{{
  "order_id": "{data.order_id}",
  "plastic_saved_kg": 0.0,
  "carbon_avoided_kg": 0.0,
  "local_sourcing_summary": "",
  "impact_statement": ""
}}

Rules:
- Do NOT add explanations or markdown
- Do NOT add extra fields
- plastic_saved_kg: estimate total kg of single-use plastic avoided based on products and quantities
- carbon_avoided_kg: estimate total kg of CO2 equivalent emissions avoided
- Use logic-based estimation: e.g. bamboo toothbrush saves ~15g plastic vs plastic equivalent
- local_sourcing_summary: 1 sentence estimating local sourcing based on materials
- impact_statement: 1-2 sentence human-readable summary of the environmental impact

Order ID: {data.order_id}
Products:
{product_list}
"""

    response = generate_ai_response(prompt)
    log_ai_interaction(module="impact_generator", prompt=prompt, response=response)
    return response
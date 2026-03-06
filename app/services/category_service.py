from app.services.ai_client import generate_ai_response
from app.utils.logger import log_ai_interaction


def generate_category_tags(product):

    prompt = f"""
You are an AI for an ecommerce sustainability platform.

Classify the product and score its sustainability.

Choose primary_category ONLY from this list:
- personal_care
- kitchen
- office_supplies
- packaging
- home_products

Return ONLY valid JSON in EXACTLY this format:

{{
  "primary_category": "",
  "sub_category": "",
  "seo_tags": ["example tag 1", "example tag 2", "example tag 3", "example tag 4", "example tag 5"],
  "sustainability_filters": [],
  "sustainability_score": 0,
  "score_reasoning": ""
}}

Rules:
- Do NOT add explanations or markdown
- Do NOT add extra fields
- primary_category must be one of the five values listed above
- seo_tags MUST be an array of 5–10 strings
- NEVER return null values
- sustainability_filters must be an array of eco attributes (biodegradable, plastic-free, compostable, vegan, recycled, renewable, etc.)
- sustainability_score must be an integer between 0 and 100
- score_reasoning must be exactly one sentence

Product Details:
Name: {product.product_name}
Description: {product.description}
Material: {product.material}
Use Case: {product.use_case}
"""

    response = generate_ai_response(prompt)
    log_ai_interaction(module="category_generator", prompt=prompt, response=response)
    return response

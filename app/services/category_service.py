from app.services.ai_client import generate_ai_response
from app.utils.logger import log_ai_interaction


def generate_category_tags(product):

    prompt = f"""
You are an AI for an ecommerce sustainability platform.

Classify the product into sustainability-friendly categories.

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
  "seo_tags": [],
  "sustainability_filters": []
}}

Rules:
- Do NOT add explanations or markdown
- Do NOT add extra fields
- primary_category must be one of the five values listed above
- seo_tags must contain between 5 and 10 relevant keywords
- sustainability_filters should describe eco attributes (e.g. biodegradable, plastic-free, compostable, vegan, recycled, renewable)

Product Details:
Name: {product.product_name}
Description: {product.description}
Material: {product.material}
Use Case: {product.use_case}
"""

    response = generate_ai_response(prompt)
    log_ai_interaction(module="category_generator", prompt=prompt, response=response)
    return response
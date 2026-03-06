import json

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.ai_client import generate_ai_response
from app.utils.logger import log_ai_interaction

router = APIRouter()


class WhatsAppMessage(BaseModel):
    phone_number: str
    message: str


class WhatsAppResponse(BaseModel):
    intent: str
    reply: str
    escalated: bool


@router.post(
    "/whatsapp/webhook",
    response_model=WhatsAppResponse,
    tags=["Module 4: AI WhatsApp Support Bot (Stub)"],
)
def whatsapp_webhook(payload: WhatsAppMessage):
    intent_prompt = f"""
You are a customer support classifier for a sustainable ecommerce platform.
Classify the customer message into one of these intents:
- order_status
- return_policy
- escalation
- general
Return ONLY valid JSON: {{"intent": ""}}
Rules:
- Use "escalation" if the message involves complaints, refunds, damage, or frustration
- Do NOT add explanations
Message: {payload.message}
"""
    try:
        intent_result = generate_ai_response(intent_prompt)
        intent_json = json.loads(intent_result)
        intent = intent_json.get("intent", "general")
    except Exception:
        intent = "general"

    if intent == "escalation":
        log_ai_interaction(
            module="whatsapp_bot",
            prompt=intent_prompt,
            response=f"ESCALATED: {payload.message}",
        )
        return WhatsAppResponse(
            intent="escalation",
            reply="We've escalated your query to a human agent. Someone will contact you shortly.",
            escalated=True,
        )

    reply_prompt = f"""
You are a helpful customer support agent for a sustainable ecommerce platform called Rayeva.
The customer sent: "{payload.message}"
Classified intent: {intent}
Guidelines:
- order_status: ask for order ID, explain you'll look it up
- return_policy: returns accepted within 7 days of delivery for unused products
- general: friendly, helpful sustainability-focused response
Return ONLY valid JSON: {{"reply": ""}}
Keep the reply under 3 sentences. Be friendly and professional.
"""
    try:
        reply_result = generate_ai_response(reply_prompt)
        reply_json = json.loads(reply_result)
        reply = reply_json.get(
            "reply", "Thank you for reaching out! How can we help you today?"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service failed: {str(e)}",
        )

    log_ai_interaction(module="whatsapp_bot", prompt=reply_prompt, response=reply)
    return WhatsAppResponse(intent=intent, reply=reply, escalated=False)

"""
=============================================================
 AI ENGINE — The "Intelligence" behind ServiceBuddy
 ---------------------------------------------------
 This file handles all AI-related logic.

 HOW IT WORKS:
 1. User describes a car problem (e.g. "engine noise at high speed")
 2. We send this to OpenAI/Claude with a carefully crafted "prompt"
    (instructions telling the AI HOW to respond)
 3. The AI analyzes the problem like an expert mechanic would
 4. We format the response and send it back

 WHAT'S A PROMPT?
 Think of it like a job description. We tell the AI:
 "You are a certified car mechanic working for Cars24.
  When someone describes a problem, give them a diagnosis,
  tell them what work is needed, AND warn them about
  unnecessary upsells."

 The better the prompt, the better the AI's responses.
=============================================================
"""

import os
import json
from typing import Optional

# --------------- CONFIGURATION ---------------
# The AI_PROVIDER setting lets you switch between OpenAI, Claude, or offline mode
# Set these in your .env file (explained in the setup guide)

AI_PROVIDER = os.getenv("AI_PROVIDER", "offline")  # "openai", "claude", or "offline"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")


# ============================================================
# THE SYSTEM PROMPT — This is the most important part!
# ============================================================
# This tells the AI exactly how to behave. A great prompt = great results.
# Feel free to customize this for Cars24's tone and style.

SYSTEM_PROMPT = """You are ServiceBuddy, an AI car service assistant for Cars24 — India's largest used car platform.

YOUR ROLE:
You help Cars24 customers understand car problems, know what service is genuinely needed, and avoid being overcharged or upsold on unnecessary repairs.

RULES:
1. Be friendly, clear, and speak in simple language (avoid jargon)
2. Always provide a cost estimate range in Indian Rupees (₹)
3. ALWAYS include a "what to avoid" section — warn about common unnecessary upsells
4. Rate urgency as "high" (safety risk, fix now), "medium" (fix within a week), or "low" (can wait)
5. If the user's car model is provided, give model-specific advice when possible
6. Prioritize SAFETY — brake, steering, and tyre issues are always high urgency
7. Be honest — if something genuinely needs fixing, say so. Don't downplay real issues.
8. Remind users that their Cars24 lifetime warranty may cover the repair

RESPONSE FORMAT (you MUST respond in this exact JSON format):
{
    "diagnosis": "A brief 1-2 sentence explanation of what's likely happening",
    "likely_causes": ["cause 1", "cause 2", "cause 3"],
    "recommended_action": "What the user should actually do, with cost estimate",
    "what_to_avoid": "What the mechanic might try to upsell that isn't needed",
    "urgency": "high/medium/low",
    "estimated_cost_range": "₹X,XXX - ₹X,XXX"
}

IMPORTANT: Respond ONLY with the JSON. No extra text before or after."""


# ============================================================
# AI FUNCTION: Get Diagnosis
# ============================================================

async def get_ai_diagnosis(
    message: str,
    car_model: Optional[str] = None,
    mileage_km: Optional[int] = None
) -> dict:
    """
    Main function that processes user's car problem and returns AI diagnosis.

    It tries the following in order:
    1. If OpenAI key is set → use GPT-4
    2. If Claude key is set → use Claude
    3. If no key → use smart offline/rule-based responses
    """

    # Build the user's message with context
    user_message = f"Car problem: {message}"
    if car_model:
        user_message += f"\nCar model: {car_model}"
    if mileage_km:
        user_message += f"\nCurrent mileage: {mileage_km:,} km"

    # Try AI providers in order
    if AI_PROVIDER == "openai" and OPENAI_API_KEY:
        return await _call_openai(user_message)
    elif AI_PROVIDER == "claude" and CLAUDE_API_KEY:
        return await _call_claude(user_message)
    else:
        # Offline mode — uses smart rule-based matching
        return _get_offline_diagnosis(message, car_model, mileage_km)


# ============================================================
# OPENAI INTEGRATION
# ============================================================

async def _call_openai(user_message: str) -> dict:
    """
    Calls OpenAI's GPT-4o-mini API.
    GPT-4o-mini is recommended because it's:
    - Fast (responds in 1-2 seconds)
    - Cheap (₹0.05-0.10 per conversation)
    - Smart enough for car diagnosis
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",           # Affordable + fast model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,                # Lower = more consistent responses
            response_format={"type": "json_object"}  # Forces JSON output
        )

        # Parse the AI's response
        result = json.loads(response.choices[0].message.content)
        return result

    except ImportError:
        print("⚠️ OpenAI package not installed. Run: pip install openai")
        return _get_offline_diagnosis(user_message)
    except Exception as e:
        print(f"⚠️ OpenAI error: {e}. Falling back to offline mode.")
        return _get_offline_diagnosis(user_message)


# ============================================================
# CLAUDE (ANTHROPIC) INTEGRATION
# ============================================================

async def _call_claude(user_message: str) -> dict:
    """
    Calls Anthropic's Claude API.
    Claude is great at following structured instructions.
    """
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=CLAUDE_API_KEY)

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Parse the response
        result = json.loads(response.content[0].text)
        return result

    except ImportError:
        print("⚠️ Anthropic package not installed. Run: pip install anthropic")
        return _get_offline_diagnosis(user_message)
    except Exception as e:
        print(f"⚠️ Claude error: {e}. Falling back to offline mode.")
        return _get_offline_diagnosis(user_message)


# ============================================================
# OFFLINE MODE — Smart Rule-Based Responses
# ============================================================
# This works WITHOUT any AI API key. It uses keyword matching
# to give useful responses. Great for demos and testing.

# Knowledge base — common car problems and advice
KNOWLEDGE_BASE = {
    "engine noise": {
        "diagnosis": "Engine noise can indicate several issues, ranging from simple (low oil) to serious (timing chain wear).",
        "likely_causes": [
            "Low engine oil level or degraded oil",
            "Worn timing belt or chain",
            "Loose or damaged accessory belt",
            "Valve train wear"
        ],
        "recommended_action": "Start with an engine oil level check (free). If oil is fine, get a mechanic to listen with a stethoscope to identify the source. Oil + filter change costs ₹2,000-3,500.",
        "what_to_avoid": "Don't let anyone convince you to do a full engine overhaul without proper diagnosis. A simple oil top-up often fixes this. Also avoid 'engine flush' treatments — they're usually unnecessary and can cost ₹1,500-3,000.",
        "urgency": "medium",
        "estimated_cost_range": "₹0 - ₹3,500"
    },
    "ac not cooling": {
        "diagnosis": "AC not cooling is very common in Indian conditions. In 70% of cases, it's a simple gas top-up.",
        "likely_causes": [
            "Low refrigerant (AC gas) level",
            "Dirty or clogged cabin air filter",
            "Faulty AC compressor clutch",
            "Condenser fan not working"
        ],
        "recommended_action": "Step 1: Replace cabin air filter (₹300-500). Step 2: AC gas top-up (₹1,500-2,000). These two fixes solve most AC problems.",
        "what_to_avoid": "Avoid compressor replacement unless confirmed faulty by pressure test. Many shops push this unnecessarily — it costs ₹8,000-15,000. Also avoid 'AC system flush' packages (₹3,000+) unless there's actual contamination.",
        "urgency": "low",
        "estimated_cost_range": "₹1,500 - ₹2,500"
    },
    "brake": {
        "diagnosis": "Brake issues should always be taken seriously as they directly affect safety.",
        "likely_causes": [
            "Worn brake pads (most common)",
            "Warped or scored brake discs",
            "Low brake fluid level",
            "Sticking brake caliper",
            "Dust buildup causing squealing"
        ],
        "recommended_action": "Get brake pad thickness measured immediately (free inspection). Replace pads if below 3mm. Pad replacement costs ₹1,500-3,000 per axle. Check brake fluid level — top-up is ₹200-300.",
        "what_to_avoid": "Don't agree to brake disc replacement unless the mechanic shows you visible deep scoring or measures disc thickness. Discs last 2-3 sets of pads usually. Disc replacement costs ₹3,000-6,000 per pair — avoid it if discs are still within spec.",
        "urgency": "high",
        "estimated_cost_range": "₹1,500 - ₹4,000"
    },
    "vibration": {
        "diagnosis": "Vibrations while driving are usually related to wheel/tyre issues, especially at higher speeds.",
        "likely_causes": [
            "Wheel misalignment",
            "Unbalanced tyres",
            "Worn suspension bushings",
            "Warped brake rotors (if vibration during braking)",
            "Worn CV joint (if vibration during turns)"
        ],
        "recommended_action": "Start with wheel alignment + balancing (₹800-1,200). This solves 60% of vibration issues. If it persists, check suspension bushings visually for cracks.",
        "what_to_avoid": "Don't agree to full suspension kit replacement (₹15,000-25,000) without trying alignment first. Also avoid unnecessary shock absorber replacement — they last 60,000-80,000 km typically.",
        "urgency": "medium",
        "estimated_cost_range": "₹800 - ₹1,200"
    },
    "mileage": {
        "diagnosis": "Reduced fuel efficiency usually happens gradually due to maintenance gaps or driving conditions.",
        "likely_causes": [
            "Dirty air filter restricting airflow",
            "Old or fouled spark plugs",
            "Incorrect tyre pressure (even 5 PSI low = 3% worse mileage)",
            "Clogged fuel injectors",
            "Faulty oxygen sensor"
        ],
        "recommended_action": "Quick wins first: check tyre pressure (free), replace air filter (₹300-500), and clean/replace spark plugs if >30,000 km (₹800-1,500). These alone can improve mileage by 10-15%.",
        "what_to_avoid": "Avoid expensive 'fuel system cleaning packages' (₹3,000-5,000). A ₹200-400 fuel injector cleaner additive from a trusted brand works just as well. Also don't fall for 'performance chips' or 'fuel saving devices' — they don't work.",
        "urgency": "low",
        "estimated_cost_range": "₹500 - ₹2,000"
    },
    "starting problem": {
        "diagnosis": "Car not starting or cranking slowly is most commonly a battery issue (80% of cases).",
        "likely_causes": [
            "Weak or dead battery (most common — batteries last 3-4 years)",
            "Corroded battery terminals",
            "Faulty starter motor",
            "Fuel pump issue",
            "Ignition switch problem"
        ],
        "recommended_action": "Step 1: Get battery voltage tested (free at most centres). If below 12.4V, replace it. New battery costs ₹3,500-6,000. Check terminal connections — cleaning corrosion (₹100-200) often fixes the issue.",
        "what_to_avoid": "Don't let anyone jump to starter motor (₹4,000-8,000) or alternator replacement (₹5,000-10,000) without testing the battery first. 80% of starting problems are just a weak battery.",
        "urgency": "high",
        "estimated_cost_range": "₹0 - ₹6,000"
    },
    "suspension": {
        "diagnosis": "Suspension noises (clunks, rattles over bumps) usually mean worn bushings or links.",
        "likely_causes": [
            "Worn stabilizer bar links (most common clunk)",
            "Deteriorated control arm bushings",
            "Worn strut mounts",
            "Damaged shock absorbers"
        ],
        "recommended_action": "Get a visual inspection of suspension components (free-₹500). Stabilizer links are cheap to replace (₹1,500-2,500 per pair). Bushings cost ₹800-1,500 per piece.",
        "what_to_avoid": "Don't agree to replacing the entire suspension kit when only one component is worn. Many shops bundle everything together (₹20,000-35,000) when you may only need a ₹2,000 link replacement.",
        "urgency": "medium",
        "estimated_cost_range": "₹1,500 - ₹5,000"
    },
    "clutch": {
        "diagnosis": "Clutch problems (slipping, hard pedal, or judder) typically appear after 50,000-80,000 km.",
        "likely_causes": [
            "Worn clutch plate (most common)",
            "Weak clutch spring/pressure plate",
            "Clutch cable stretch or hydraulic fluid leak",
            "Worn flywheel"
        ],
        "recommended_action": "If the clutch is slipping (engine revs increase but car doesn't accelerate proportionally), replacement is likely needed. Full clutch kit replacement costs ₹6,000-12,000 depending on car model.",
        "what_to_avoid": "If only the clutch cable needs adjustment (₹200-500), don't agree to full clutch plate replacement. Also, always insist on OEM or equivalent quality parts — cheap clutch plates wear out in 15,000-20,000 km.",
        "urgency": "medium",
        "estimated_cost_range": "₹500 - ₹12,000"
    },
    "tyre": {
        "diagnosis": "Tyre issues affect safety, comfort, and fuel efficiency significantly.",
        "likely_causes": [
            "Uneven tyre wear due to misalignment",
            "Low tread depth (below legal 1.6mm minimum)",
            "Incorrect tyre pressure",
            "Sidewall damage or bulge"
        ],
        "recommended_action": "Check tread depth with a ₹1 coin — if you can see the top of the coin in the groove, tyres need replacing. Alignment costs ₹600-1,000. New tyres: ₹3,000-8,000 each depending on size.",
        "what_to_avoid": "Don't get convinced to replace all 4 tyres if only 1-2 are worn. Also avoid cheap unknown-brand tyres — they compromise safety. Stick to brands like MRF, Apollo, Bridgestone, or CEAT.",
        "urgency": "medium",
        "estimated_cost_range": "₹600 - ₹8,000"
    },
    "battery": {
        "diagnosis": "Car batteries in India typically last 3-4 years due to extreme heat conditions.",
        "likely_causes": [
            "Battery past its lifespan (3-4 years)",
            "Corroded terminals reducing connection",
            "Parasitic drain from aftermarket accessories",
            "Faulty alternator not charging properly"
        ],
        "recommended_action": "Get battery voltage tested (free). If below 12.4V at rest, or below 10V while cranking, replace it. Amaron/Exide batteries cost ₹3,500-6,000 with 2-3 year warranty.",
        "what_to_avoid": "Don't pay for 'battery reconditioning' services (₹500-1,000) — they provide temporary fixes at best. Also, don't let anyone sell you a higher-capacity battery than your car needs — it won't help and costs more.",
        "urgency": "medium",
        "estimated_cost_range": "₹3,500 - ₹6,000"
    }
}

DEFAULT_RESPONSE = {
    "diagnosis": "I'd need a bit more detail to give specific advice. Could you describe the problem more? For example: what sound do you hear, when does it happen (starting, driving, braking), and how long has it been going on?",
    "likely_causes": [
        "Could be related to regular wear and tear",
        "May need a professional visual inspection",
        "Might be a minor adjustment needed"
    ],
    "recommended_action": "Visit the nearest Cars24 authorized service centre for a free diagnostic check. They'll give you an honest assessment. Remember, your Cars24 lifetime warranty may cover the repair!",
    "what_to_avoid": "General tip: Always ask for a written estimate before approving any work. Don't approve repairs over ₹5,000 without asking to see the worn/damaged part. Get a second opinion for any quote over ₹10,000.",
    "urgency": "low",
    "estimated_cost_range": "₹0 - ₹2,000 (diagnostic)"
}


def _get_offline_diagnosis(
    message: str,
    car_model: Optional[str] = None,
    mileage_km: Optional[int] = None
) -> dict:
    """
    Smart keyword matching for offline mode.
    Searches the knowledge base for relevant responses.
    """
    message_lower = message.lower()

    # Search through knowledge base for matching keywords
    best_match = None
    best_score = 0

    for keyword, response in KNOWLEDGE_BASE.items():
        # Check if any word in the keyword appears in the message
        keyword_words = keyword.split()
        score = sum(1 for word in keyword_words if word in message_lower)

        if score > best_score:
            best_score = score
            best_match = response

    if best_match and best_score > 0:
        result = best_match.copy()

        # Add car-specific context if model is provided
        if car_model:
            result["diagnosis"] = f"[{car_model}] {result['diagnosis']}"

        # Add mileage-based note
        if mileage_km and mileage_km > 50000:
            result["diagnosis"] += " Given your higher mileage, wear-related issues are more likely."

        return result

    return DEFAULT_RESPONSE

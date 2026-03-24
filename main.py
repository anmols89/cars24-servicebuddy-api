"""
=============================================================
 CARS24 SERVICEBUDDY API
 -------------------------
 This is the main file — the "brain" of your ServiceBuddy.

 WHAT THIS FILE DOES:
 It creates an API (think of it like a phone number that
 the Cars24 app can "call" to get answers). The API has
 4 main features:

 1. /chat          → AI chatbot for car problems
 2. /centres       → Find nearby service centres
 3. /schedule      → Get service schedule for a car
 4. /book          → Book an appointment

 HOW TO RUN:
 In your terminal, type: uvicorn main:app --reload
 Then open: http://localhost:8000/docs (to test it)
=============================================================
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime, timedelta

# --------------- STEP 1: Import the AI module ---------------
# This is a separate file (ai_engine.py) that handles talking to OpenAI/Claude
from ai_engine import get_ai_diagnosis

# --------------- STEP 2: Import mock data ---------------
# In production, this would come from Cars24's actual database
from mock_data import SERVICE_CENTRES, SERVICE_SCHEDULE, CAR_MODELS


# ============================================================
# CREATE THE APP
# ============================================================
# Think of FastAPI as the "skeleton" of your API.
# It handles receiving requests and sending responses.

app = FastAPI(
    title="Cars24 ServiceBuddy API",
    description="AI-powered car service assistant for Cars24 lifetime warranty customers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# This allows the Cars24 app (or any frontend) to talk to your API
# Without this, browsers would block the connection for security reasons
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with Cars24's actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DEFINE REQUEST/RESPONSE SHAPES
# ============================================================
# These are like "forms" — they define what data the API expects
# and what it sends back. This is called "schema" in tech terms.

class ChatRequest(BaseModel):
    """What the app sends when user asks a question"""
    message: str                         # The user's question, e.g. "my AC is not cooling"
    car_model: Optional[str] = None      # e.g. "Hyundai Creta 2023"
    mileage_km: Optional[int] = None     # e.g. 8450

class ChatResponse(BaseModel):
    """What we send back to the app"""
    diagnosis: str                       # What's likely wrong
    likely_causes: list[str]             # List of possible causes
    recommended_action: str              # What should be done
    what_to_avoid: str                   # What NOT to agree to (upsell guard)
    urgency: str                         # "high", "medium", or "low"
    estimated_cost_range: str            # e.g. "₹1,500 - ₹2,500"

class BookingRequest(BaseModel):
    """What the app sends for a booking"""
    centre_id: int
    car_model: str
    service_type: str
    preferred_date: str                  # e.g. "2026-04-15"
    preferred_time: str                  # e.g. "10:00 AM"
    customer_name: str
    customer_phone: str
    notes: Optional[str] = ""

class BookingResponse(BaseModel):
    """Booking confirmation sent back"""
    booking_id: str
    status: str
    centre_name: str
    date: str
    time: str
    message: str

class NearbyRequest(BaseModel):
    """User's location to find nearby centres"""
    latitude: float                      # User's GPS latitude
    longitude: float                     # User's GPS longitude
    radius_km: Optional[float] = 15.0   # How far to search


# ============================================================
# API ENDPOINT 1: AI CHATBOT
# ============================================================
# This is the star feature — when someone describes a car problem,
# the AI analyzes it and gives helpful advice.
#
# URL: POST /api/v1/chat
# Example: User sends "my car makes a grinding noise when braking"
# Response: Diagnosis + causes + what to do + what to avoid

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    AI-powered car diagnostic chat.
    User describes a problem → AI returns diagnosis + advice.
    """
    try:
        # Call the AI engine to get a diagnosis
        result = await get_ai_diagnosis(
            message=request.message,
            car_model=request.car_model,
            mileage_km=request.mileage_km
        )
        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


# ============================================================
# API ENDPOINT 2: FIND NEARBY SERVICE CENTRES
# ============================================================
# When user opens the app, we show them the nearest centres.
# In production, this would use real GPS + Google Maps API.
#
# URL: GET /api/v1/centres
# URL: POST /api/v1/centres/nearby  (with GPS location)

@app.get("/api/v1/centres")
async def list_all_centres():
    """Get all service centres (sorted by rating)"""
    sorted_centres = sorted(SERVICE_CENTRES, key=lambda x: x["rating"], reverse=True)
    return {"centres": sorted_centres, "total": len(sorted_centres)}


@app.post("/api/v1/centres/nearby")
async def find_nearby_centres(request: NearbyRequest):
    """
    Find centres near user's location.
    In production, this would calculate real distances using GPS coordinates.
    For the demo, we return mock data sorted by distance.
    """
    # Mock: just return centres sorted by distance
    sorted_centres = sorted(SERVICE_CENTRES, key=lambda x: x["distance_km"])
    nearby = [c for c in sorted_centres if c["distance_km"] <= request.radius_km]
    return {
        "centres": nearby,
        "total": len(nearby),
        "search_radius_km": request.radius_km
    }


@app.get("/api/v1/centres/{centre_id}")
async def get_centre_details(centre_id: int):
    """Get details for a specific centre"""
    centre = next((c for c in SERVICE_CENTRES if c["id"] == centre_id), None)
    if not centre:
        raise HTTPException(status_code=404, detail="Service centre not found")
    return centre


# ============================================================
# API ENDPOINT 3: SERVICE SCHEDULE
# ============================================================
# Shows the user what services are due for their car.
# Based on car model + current mileage, generates a schedule.
#
# URL: GET /api/v1/schedule/{car_model}?mileage=8450

@app.get("/api/v1/schedule/{car_id}")
async def get_service_schedule(car_id: str, mileage: Optional[int] = None):
    """
    Get service schedule for a car.
    car_id: A unique car identifier (or model name for demo)
    mileage: Current odometer reading in km
    """
    # For demo, return the mock schedule
    # In production, this would query Cars24's database based on
    # the actual car's purchase date, model, and mileage
    schedule = SERVICE_SCHEDULE.copy()

    if mileage:
        # Mark services as overdue if mileage is past their due point
        for item in schedule:
            due_km = int(item["due_mileage_km"].replace(",", ""))
            if mileage >= due_km and item["status"] != "completed":
                item["status"] = "overdue"
                item["priority"] = "high"

    return {
        "car_id": car_id,
        "current_mileage": mileage,
        "schedule": schedule,
        "next_service": next(
            (s for s in schedule if s["status"] in ["upcoming", "overdue"]),
            None
        )
    }


# ============================================================
# API ENDPOINT 4: BOOK APPOINTMENT
# ============================================================
# Lets users book a service appointment at a centre.
#
# URL: POST /api/v1/book

@app.post("/api/v1/book", response_model=BookingResponse)
async def book_appointment(request: BookingRequest):
    """
    Book a service appointment.
    In production, this would:
    1. Check centre availability
    2. Create booking in Cars24's system
    3. Send SMS/WhatsApp confirmation
    4. Block the time slot
    """
    # Find the centre
    centre = next((c for c in SERVICE_CENTRES if c["id"] == request.centre_id), None)
    if not centre:
        raise HTTPException(status_code=404, detail="Service centre not found")

    # Generate a mock booking ID
    booking_id = f"SB-{datetime.now().strftime('%Y%m%d')}-{request.centre_id:03d}"

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        centre_name=centre["name"],
        date=request.preferred_date,
        time=request.preferred_time,
        message=f"Appointment confirmed at {centre['name']}. "
                f"You'll receive a confirmation on {request.customer_phone} shortly."
    )


# ============================================================
# BONUS: HEALTH CHECK ENDPOINT
# ============================================================
# The Cars24 engineering team will use this to check if your
# API is running. Every good API needs one.

@app.get("/")
async def health_check():
    return {
        "status": "running",
        "service": "Cars24 ServiceBuddy API",
        "version": "1.0.0",
        "features": ["ai-chat", "service-centres", "schedule", "booking"]
    }


@app.get("/api/v1/car-models")
async def list_car_models():
    """List supported car models (for dropdown in the app)"""
    return {"models": CAR_MODELS}

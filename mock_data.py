"""
=============================================================
 MOCK DATA — Sample data for the prototype
 -------------------------------------------
 In the real Cars24 system, this data would come from:
 - Cars24's database (service centres, car details)
 - Google Maps API (distances, locations)
 - Cars24's CRM (customer bookings, history)

 For the demo, we use realistic sample data.
=============================================================
"""

SERVICE_CENTRES = [
    {
        "id": 1,
        "name": "Cars24 Authorized Service - Dwarka",
        "address": "Plot No. 5, Sector 12, Dwarka, New Delhi - 110078",
        "city": "New Delhi",
        "latitude": 28.5921,
        "longitude": 77.0460,
        "distance_km": 2.3,
        "rating": 4.6,
        "total_reviews": 342,
        "phone": "+91 98100 XXXXX",
        "services": ["General Service", "AC Repair", "Body Work", "Engine Repair", "Electrical"],
        "working_hours": "8:00 AM - 8:00 PM",
        "working_days": "Mon - Sat",
        "is_cars24_authorized": True,
        "average_wait_time_mins": 30,
        "available_slots_today": 4
    },
    {
        "id": 2,
        "name": "Cars24 Partner - Gurugram Central",
        "address": "SCO 45, MG Road, Sector 28, Gurugram, Haryana - 122001",
        "city": "Gurugram",
        "latitude": 28.4595,
        "longitude": 77.0266,
        "distance_km": 5.1,
        "rating": 4.8,
        "total_reviews": 518,
        "phone": "+91 99100 XXXXX",
        "services": ["General Service", "AC Repair", "Transmission", "Suspension", "Detailing"],
        "working_hours": "9:00 AM - 7:00 PM",
        "working_days": "Mon - Sat",
        "is_cars24_authorized": True,
        "average_wait_time_mins": 20,
        "available_slots_today": 6
    },
    {
        "id": 3,
        "name": "AutoCare Express - Noida",
        "address": "B-45, Sector 62, Noida, UP - 201301",
        "city": "Noida",
        "latitude": 28.6270,
        "longitude": 77.3654,
        "distance_km": 8.7,
        "rating": 4.3,
        "total_reviews": 189,
        "phone": "+91 97100 XXXXX",
        "services": ["General Service", "Tyre & Wheel", "Battery Replacement", "AC Repair"],
        "working_hours": "8:30 AM - 7:30 PM",
        "working_days": "Mon - Sat",
        "is_cars24_authorized": False,
        "average_wait_time_mins": 45,
        "available_slots_today": 3
    },
    {
        "id": 4,
        "name": "Cars24 Hub - South Delhi",
        "address": "Shop 12, Saket District Centre, New Delhi - 110017",
        "city": "New Delhi",
        "latitude": 28.5244,
        "longitude": 77.2066,
        "distance_km": 3.8,
        "rating": 4.7,
        "total_reviews": 456,
        "phone": "+91 96100 XXXXX",
        "services": ["General Service", "Engine Diagnostics", "Body Work", "Detailing", "Electrical"],
        "working_hours": "8:00 AM - 9:00 PM",
        "working_days": "Mon - Sun",
        "is_cars24_authorized": True,
        "average_wait_time_mins": 25,
        "available_slots_today": 5
    },
    {
        "id": 5,
        "name": "QuickFix Motors - Faridabad",
        "address": "Shop 8, NIT 5, Faridabad, Haryana - 121001",
        "city": "Faridabad",
        "latitude": 28.4089,
        "longitude": 77.3178,
        "distance_km": 12.4,
        "rating": 4.1,
        "total_reviews": 97,
        "phone": "+91 95100 XXXXX",
        "services": ["General Service", "AC Repair", "Battery Replacement", "Tyre & Wheel"],
        "working_hours": "9:00 AM - 6:00 PM",
        "working_days": "Mon - Sat",
        "is_cars24_authorized": False,
        "average_wait_time_mins": 60,
        "available_slots_today": 8
    },
    {
        "id": 6,
        "name": "Cars24 Mega Service Hub - Manesar",
        "address": "IMT Manesar, Sector 8, Gurugram, Haryana - 122051",
        "city": "Gurugram",
        "latitude": 28.3590,
        "longitude": 76.9373,
        "distance_km": 15.2,
        "rating": 4.9,
        "total_reviews": 723,
        "phone": "+91 98200 XXXXX",
        "services": ["General Service", "AC Repair", "Engine Overhaul", "Transmission", "Body Work", "Painting", "Detailing", "Electrical", "Suspension"],
        "working_hours": "7:00 AM - 10:00 PM",
        "working_days": "Mon - Sun",
        "is_cars24_authorized": True,
        "average_wait_time_mins": 15,
        "available_slots_today": 12
    }
]

SERVICE_SCHEDULE = [
    {
        "id": 1,
        "service": "Engine Oil & Filter Change",
        "description": "Replace engine oil and oil filter for optimal engine health",
        "due_mileage_km": "10,000",
        "due_date": "Apr 2026",
        "status": "upcoming",
        "priority": "high",
        "estimated_cost": "₹2,500 - ₹3,500",
        "covered_under_warranty": False,
        "estimated_duration_mins": 60
    },
    {
        "id": 2,
        "service": "Brake Pad Inspection",
        "description": "Check brake pad thickness and brake fluid level",
        "due_mileage_km": "15,000",
        "due_date": "Jun 2026",
        "status": "upcoming",
        "priority": "medium",
        "estimated_cost": "₹1,500 - ₹4,000",
        "covered_under_warranty": True,
        "estimated_duration_mins": 45
    },
    {
        "id": 3,
        "service": "AC Service & Gas Top-up",
        "description": "Clean AC vents, replace cabin filter, check gas level",
        "due_mileage_km": "12,000",
        "due_date": "May 2026",
        "status": "upcoming",
        "priority": "medium",
        "estimated_cost": "₹1,800 - ₹2,500",
        "covered_under_warranty": False,
        "estimated_duration_mins": 90
    },
    {
        "id": 4,
        "service": "Tyre Rotation & Alignment",
        "description": "Rotate tyres for even wear and check wheel alignment",
        "due_mileage_km": "10,000",
        "due_date": "Apr 2026",
        "status": "upcoming",
        "priority": "low",
        "estimated_cost": "₹800 - ₹1,200",
        "covered_under_warranty": False,
        "estimated_duration_mins": 40
    },
    {
        "id": 5,
        "service": "Air Filter Replacement",
        "description": "Replace engine air filter for better performance and mileage",
        "due_mileage_km": "20,000",
        "due_date": "Sep 2026",
        "status": "scheduled",
        "priority": "low",
        "estimated_cost": "₹500 - ₹800",
        "covered_under_warranty": False,
        "estimated_duration_mins": 15
    },
    {
        "id": 6,
        "service": "Coolant Flush & Refill",
        "description": "Replace engine coolant to prevent overheating",
        "due_mileage_km": "25,000",
        "due_date": "Dec 2026",
        "status": "scheduled",
        "priority": "medium",
        "estimated_cost": "₹1,200 - ₹1,800",
        "covered_under_warranty": False,
        "estimated_duration_mins": 60
    },
    {
        "id": 7,
        "service": "General Health Checkup",
        "description": "Multi-point inspection of all major systems",
        "due_mileage_km": "5,000",
        "due_date": "Feb 2026",
        "status": "completed",
        "priority": "low",
        "estimated_cost": "₹1,000",
        "covered_under_warranty": True,
        "estimated_duration_mins": 120
    },
    {
        "id": 8,
        "service": "Battery Health Check",
        "description": "Test battery voltage, check terminals, load test",
        "due_mileage_km": "5,000",
        "due_date": "Feb 2026",
        "status": "completed",
        "priority": "medium",
        "estimated_cost": "Free (Warranty)",
        "covered_under_warranty": True,
        "estimated_duration_mins": 20
    }
]

CAR_MODELS = [
    {"brand": "Hyundai", "model": "Creta", "years": [2020, 2021, 2022, 2023, 2024]},
    {"brand": "Hyundai", "model": "Venue", "years": [2020, 2021, 2022, 2023]},
    {"brand": "Hyundai", "model": "i20", "years": [2019, 2020, 2021, 2022, 2023]},
    {"brand": "Maruti Suzuki", "model": "Swift", "years": [2018, 2019, 2020, 2021, 2022, 2023]},
    {"brand": "Maruti Suzuki", "model": "Baleno", "years": [2019, 2020, 2021, 2022, 2023]},
    {"brand": "Maruti Suzuki", "model": "Brezza", "years": [2020, 2021, 2022, 2023]},
    {"brand": "Tata", "model": "Nexon", "years": [2020, 2021, 2022, 2023]},
    {"brand": "Tata", "model": "Punch", "years": [2022, 2023, 2024]},
    {"brand": "Tata", "model": "Harrier", "years": [2020, 2021, 2022, 2023]},
    {"brand": "Kia", "model": "Seltos", "years": [2020, 2021, 2022, 2023]},
    {"brand": "Kia", "model": "Sonet", "years": [2021, 2022, 2023]},
    {"brand": "Mahindra", "model": "XUV700", "years": [2022, 2023, 2024]},
    {"brand": "Mahindra", "model": "Thar", "years": [2021, 2022, 2023]},
    {"brand": "Honda", "model": "City", "years": [2019, 2020, 2021, 2022, 2023]},
    {"brand": "Toyota", "model": "Fortuner", "years": [2019, 2020, 2021, 2022, 2023]},
    {"brand": "MG", "model": "Hector", "years": [2020, 2021, 2022, 2023]},
]

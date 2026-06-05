import anthropic
import requests
import random
import os
from datetime import datetime

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MAKE_WEBHOOK_URL  = os.environ.get("MAKE_WEBHOOK_URL")

# Image pairs — always 2 images per post (before/after or job combos)
IMAGE_PAIRS = [
    # Before/after pairs
    ("https://peakpropertycleanouts.com/assets/ba1-before.jpg",
     "https://peakpropertycleanouts.com/assets/ba1-after.jpg"),
    ("https://peakpropertycleanouts.com/assets/ba2-before.jpg",
     "https://peakpropertycleanouts.com/assets/ba2-after.jpg"),
    # Job photo pairs
    ("https://peakpropertycleanouts.com/assets/hero.jpg",
     "https://peakpropertycleanouts.com/assets/rig.jpg"),
    ("https://peakpropertycleanouts.com/assets/result-yard.jpg",
     "https://peakpropertycleanouts.com/assets/result-room.jpg"),
    ("https://peakpropertycleanouts.com/assets/ba1-after.jpg",
     "https://peakpropertycleanouts.com/assets/hero.jpg"),
    ("https://peakpropertycleanouts.com/assets/ba2-after.jpg",
     "https://peakpropertycleanouts.com/assets/rig.jpg"),
]

BUSINESS_CONTEXT = """
Peak Property Cleanouts — junk removal in East Idaho.
- Teen-owned & operated (16-year-old founder Branson Denning). This is the #1 differentiator.
- Based in Rigby/Menan, Idaho
- Same-day service (~4 hr average), licensed & insured
- Phone: (208) 530-5009 | Website: peakpropertycleanouts.com

PRICING (flat-rate, labor+hauling+dump fees all included):
  Minimum $150 · 1/4 load $175 · 1/2 load $275 · 3/4 load $350 · Full load $425
  National chains charge $600-850 for the same haul.

ADD-ONS: fridge/freezer +$45, mattress +$25, TV +$25, tires +$15

SERVICE AREAS:
  Zone 1 FREE: Rigby, Menan
  Zone 2 +$25: Idaho Falls, Ammon, Rexburg, Sugar City, Roberts
  Zone 3 +$50: St. Anthony, Blackfoot, Pocatello

SERVICES: garage cleanouts, furniture removal, appliance removal,
  estate/foreclosure cleanouts, construction debris, yard waste, moving cleanouts

OFFERS:
  20% off repeat customers
  Refer a job = 10% cash (no cap)
  Property managers/landlords: 20% off locked for life (text "ACCOUNT")

REAL 5-STAR REVIEWS:
  "Wonderful, professional, timely, thorough" — Terri Barney
  "Everything cleaned up quick, fair price" — Joe
  "Would hire again" — Spencer Haacke

TAGLINES:
  "ONE TEXT. FLAT PRICE. YOUR SPACE BACK TODAY."
  "Text a photo, get a flat price in under an hour."
  "Faster, cleaner, more reliable or you don't pay a dime."
"""

POST_ANGLES = [
    "before/after transformation — the space went from chaos to completely clean",
    "pricing comparison — we charge $425, national chains charge $600-850 for the same haul",
    "same-day urgency — slots fill fast, text today and it's gone today",
    "teen-owned local business story — 16-year-old founder, hardworking East Idaho crew",
    "garage cleanout — most satisfying job, before and after are unrecognizable",
    "flat-rate pricing relief — no surprise fees, one price covers everything",
    "construction debris removal — contractors and homeowners both welcome",
    "repeat customer or referral deal — 20% off, 10% cash referral with no cap",
    "appliance removal — fridge, washer, dryer, no problem",
    "local East Idaho community focus — Rigby, Idaho Falls, Rexburg, Ammon area",
    "5-star review highlight — lead with a real customer quote",
    "estate or foreclosure cleanout — respectful, fast, professional",
    "property manager/landlord deal — 20% off for life after first job",
    "yard waste and outdoor cleanup — spring/summer angle",
    "moving cleanout — people are shocked how much they left behind",
]


def generate_post(angle):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    day = datetime.now().strftime("%A")

    prompt = f"""Write a Facebook/Instagram post for Peak Property Cleanouts.

Angle: {angle}
Day: {day}

Rules:
- 3-5 sentences, punchy and local-sounding — NOT corporate
- Reference a before/after transformation or visual result where natural
- End with a clear call to action (text us, call, visit site)
- Add 5-8 relevant hashtags on a new line at the end
- Max 2 emojis total
- Phone: (208) 530-5009

Business facts:
{BUSINESS_CONTEXT}

Output ONLY the post text. Nothing else."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def main():
    print("Peak Property Cleanouts Social Bot")
    print(datetime.now().strftime("%Y-%m-%d %H:%M UTC"))

    angle  = random.choice(POST_ANGLES)
    text   = generate_post(angle)
    image1, image2 = random.choice(IMAGE_PAIRS)

    print(f"\n--- POST ---\n{text}\n------------")
    print(f"Image 1: {image1}")
    print(f"Image 2: {image2}")

    print("\nSending to Make.com...")
    resp = requests.post(
        MAKE_WEBHOOK_URL,
        json={"text": text, "image1": image1, "image2": image2}
    )

    if resp.status_code == 200:
        print("Posted successfully to Facebook + Instagram!")
    else:
        print(f"Failed — status {resp.status_code}: {resp.text}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

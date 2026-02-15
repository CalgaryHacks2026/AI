import base64
import json

import requests


def converter(arr_topics, url, debug=False):
    im_url = url
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response_ = requests.get(im_url, headers=headers)
    image_data = response_.content

    # Debug: Check if image downloaded correctly
    if debug:
        print(f"[DEBUG] Image URL: {im_url}")
        print(f"[DEBUG] HTTP Status: {response_.status_code}")
        print(
            f"[DEBUG] Content-Type: {response_.headers.get('Content-Type', 'unknown')}"
        )
        print(f"[DEBUG] Downloaded size: {len(image_data)} bytes")
        # Check magic bytes to verify it's actually an image
        magic_bytes = image_data[:10]
        if magic_bytes[:3] == b"\xff\xd8\xff":
            print("[DEBUG] Image format: JPEG ✓")
        elif magic_bytes[:8] == b"\x89PNG\r\n\x1a\n":
            print("[DEBUG] Image format: PNG ✓")
        elif magic_bytes[:6] in (b"GIF87a", b"GIF89a"):
            print("[DEBUG] Image format: GIF ✓")
        elif magic_bytes[:4] == b"RIFF" and image_data[8:12] == b"WEBP":
            print("[DEBUG] Image format: WEBP ✓")
        else:
            print("[DEBUG] WARNING: Unknown format or not an image!")
            print(f"[DEBUG] First 100 bytes: {image_data[:100]}")

    # Verify we got a successful response
    if response_.status_code != 200:
        raise ValueError(f"Failed to download image: HTTP {response_.status_code}")

    def encode_image(image_data):
        return base64.b64encode(image_data).decode("utf-8")

    image_b64 = encode_image(image_data)

    if debug:
        print(f"[DEBUG] Base64 length: {len(image_b64)}")

    tags = arr_topics

    url = "http://10.0.11.2:30068/api/generate"

    # Convert tags list to a comma-separated string for cleaner prompt
    tags_str = ", ".join(tags)

    data = {
        "model": "gemma3:12b",
        "prompt": f"""Analyze this image and return relevant tags with importance weights.

STEP 1: Describe what you literally see in the image - objects, animals, people, text, colors, setting, mood.

STEP 2: Create tags based on what you ACTUALLY SEE. Prioritize:
  - Main subject (what is the focus?)
  - Secondary elements (what else is visible?)
  - Setting/environment (indoor, outdoor, kitchen, etc.)
  - Style/type (photo, meme, illustration, etc.)
  - Colors (if prominent)
  - Mood/tone (funny, serious, cute, etc.)
  - Any visible text or logos

STEP 3: Check if any of these provided tags match what you see:
[{tags_str}]
Only use tags from this list if they ACTUALLY appear in the image.

You MUST return exactly 10-15 tags. To reach 10 tags, use descriptive tags like:
- The main subject and what it's doing
- Colors you see (white, orange, gray, etc.)
- Composition (close-up, centered, etc.)
- Image type (photo, meme, screenshot, etc.)

ACCURACY IS CRITICAL: Every tag must describe something actually in the image. Never invent content.

WEIGHTS:
- 0.9-1.0 = main subject/focus
- 0.7-0.8 = clearly visible element
- 0.5-0.6 = secondary/supporting element
- 0.3-0.4 = minor detail or mood

OUTPUT FORMAT (JSON array only, no markdown, no explanation):
[{{"tag":"example","weight":0.95}},{{"tag":"another","weight":0.80}}]""",
        "images": [image_b64],
        "stream": False,
    }

    response = requests.post(url, json=data)
    result = response.json()["response"]

    if debug:
        print(f"[DEBUG] API Status: {response.status_code}")
        print(f"[DEBUG] Raw API Response: {result}")

    # Clean up response - remove markdown code blocks if present
    result = result.strip()
    if result.startswith("```json"):
        result = result[7:]
    elif result.startswith("```"):
        result = result[3:]
    if result.endswith("```"):
        result = result[:-3]
    result = result.strip()

    # Parse and validate JSON, deduplicate tags
    try:
        tags_list = json.loads(result)

        # Deduplicate by tag name (keep first occurrence with highest weight)
        seen = {}
        for item in tags_list:
            tag = item.get("tag", "").lower().strip()
            weight = item.get("weight", 0)
            if tag and (tag not in seen or weight > seen[tag]["weight"]):
                seen[tag] = {"tag": tag, "weight": weight}

        # Sort by weight descending
        deduplicated = sorted(seen.values(), key=lambda x: x["weight"], reverse=True)

        if debug:
            print(
                f"[DEBUG] Deduplicated from {len(tags_list)} to {len(deduplicated)} tags"
            )

        return json.dumps(deduplicated)
    except json.JSONDecodeError as e:
        if debug:
            print(f"[DEBUG] JSON parse error: {e}")
        # Return raw result if JSON parsing fails
        return result


if __name__ == "__main__":
    # Test with debug enabled
    im_url = "https://http.cat/images/418.jpg"
    tags = [
        "ww1",
        "ww2",
        "cold war",
        "renaissance",
        "industrial revolution",
        "roman empire",
        "islamic empire",
        "viking age",
        "medieval",
        "ancient greece",
        "civil rights movement",
        "space race",
        "great depression",
        "french revolution",
        "american revolution",
        "germany",
        "japan",
        "usa",
        "china",
        "russia",
        "egypt",
        "india",
        "brazil",
        "middle east",
        "europe",
        "africa",
        "southeast asia",
        "ibm",
        "apple",
        "microsoft",
        "nasa",
        "tesla",
        "ford",
        "boeing",
        "sony",
        "kodak",
        "polaroid",
        "cars",
        "planes",
        "trains",
        "ships",
        "motorcycles",
        "bicycles",
        "rockets",
        "coca cola",
        "pepsi",
        "mcdonalds",
        "nike",
        "levis",
        "disney",
        "music",
        "cinema",
        "photography",
        "painting",
        "sculpture",
        "architecture",
        "fashion",
        "literature",
        "family",
        "friends",
        "celebrities",
        "politicians",
        "athletes",
        "musicians",
        "scientists",
        "nature",
        "wildlife",
        "ocean",
        "mountains",
        "forests",
        "deserts",
        "wedding",
        "birthday",
        "graduation",
        "vacation",
        "holiday",
        "celebration",
        "sports",
        "food",
        "military",
        "education",
        "religion",
        "politics",
        "science",
        "medicine",
    ]
    result = converter(tags, im_url, debug=True)
    print(f"\nFinal result: {result}")

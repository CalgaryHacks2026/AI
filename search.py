import json

import requests


def searcher(arr_topics, text, year, debug=False):
    """
    Search and extrapolate relevant tags from a search topic and year.

    Args:
        arr_topics: List of allowed tags to choose from
        text: The search topic (e.g., "cars")
        year: The year for context (e.g., 1970)
        debug: Enable debug output

    Returns:
        JSON string of relevant tags with weights
    """
    allowed_tags = arr_topics
    tags_str = ", ".join(allowed_tags)

    url = "http://10.0.11.2:30068/api/generate"

    data = {
        "model": "llava:13b",
        "prompt": f"""You are an expert at understanding topics and finding related concepts.

TASK: Given a search topic and a time period, identify the most relevant tags from the allowed list.

SEARCH TOPIC: "{text}"
TIME PERIOD: {year}

STEP 1: Think about what "{text}" means in the context of {year}.
- What were the popular trends, styles, or variations of "{text}" during {year}?
- What brands, types, or categories were associated with "{text}" in {year}?
- What cultural or historical context applies to "{text}" in {year}?

STEP 2: From the following allowed tags ONLY, select those that are relevant:
[{tags_str}]

IMPORTANT RULES:
- You MUST ONLY return tags from the allowed list above
- Do NOT invent or create new tags
- Consider both direct matches and conceptually related tags
- Weight tags by relevance: how strongly they connect to "{text}" in the context of {year}

WEIGHTS:
- 0.9-1.0 = Direct match or extremely relevant to the topic+year
- 0.7-0.8 = Strongly related concept or common association
- 0.5-0.6 = Moderately related or tangentially connected
- 0.3-0.4 = Loosely related but still applicable

Return up to 15 of the most relevant tags.

OUTPUT FORMAT (JSON array only, no markdown, no explanation):
[{{"tag":"example","weight":0.95}},{{"tag":"another","weight":0.80}}]""",
        "stream": False,
    }

    if debug:
        print(f"[DEBUG] Search topic: {text}")
        print(f"[DEBUG] Year context: {year}")
        print(f"[DEBUG] Allowed tags count: {len(allowed_tags)}")
        print(f"[DEBUG] API URL: {url}")

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

        # Filter to only include tags that are actually in the allowed list
        allowed_lower = {t.lower().strip() for t in allowed_tags}
        filtered = {k: v for k, v in seen.items() if k in allowed_lower}

        # Sort by weight descending
        deduplicated = sorted(
            filtered.values(), key=lambda x: x["weight"], reverse=True
        )

        if debug:
            print(f"[DEBUG] Parsed {len(tags_list)} tags from response")
            print(f"[DEBUG] After deduplication: {len(seen)} tags")
            print(f"[DEBUG] After filtering to allowed list: {len(deduplicated)} tags")

        return json.dumps(deduplicated)
    except json.JSONDecodeError as e:
        if debug:
            print(f"[DEBUG] JSON parse error: {e}")
        # Return raw result if JSON parsing fails
        return result


# Example usage:
# text = "cars"
# year = 1970
# tags = [
#     "muscle cars", "jdm", "ford", "chevrolet", "dodge",
#     "classic cars", "racing", "hot rod", "vintage", "american",
#     "sports car", "convertible", "v8 engine", "drag racing"
# ]
# print(searcher(tags, text, year, debug=True))

import json
import ollama

from models.requirement import Requirement

MODEL_NAME = "qwen3:1.7b"

def build_prompt(user_request: str) -> str:
    return f"""
You are an AI business analyst.

Your task is to extract structured business requirements.

Return ONLY valid JSON.

Schema:

{{
  "objective": "",
  "entity_type": "",
  "hard_constraints": {{
      "locations": [],
      "product_category": "",
      "certifications": [],
      "minimum_capacity": null,
      "maximum_delivery_days": null
  }},
  "preferences": {{
      "startup_friendly": null,
      "sustainable_materials": null
  }},
  "requested_results": 3
}}

User Request:

{user_request}
"""


def parse_requirement(user_request: str) -> Requirement:
    prompt = build_prompt(user_request)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"].strip()


    data = json.loads(content)

    # ---- Normalize preference values ----
    preferences = data.get("preferences", {})

    if not isinstance(preferences.get("startup_friendly"), bool):
        preferences["startup_friendly"] = None

    if not isinstance(preferences.get("sustainable_materials"), bool):
        preferences["sustainable_materials"] = None

    data["preferences"] = preferences

    return Requirement.model_validate(data)


if __name__ == "__main__":
    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    result = parse_requirement(request)

    print(result.model_dump_json(indent=2))
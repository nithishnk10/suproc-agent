import json
import ollama

from models.requirement import Requirement

MODEL_NAME = "qwen3:1.7b"

def build_prompt(user_request: str) -> str:
    return f"""
You are an AI business analyst.

Your task is to extract structured business requirements.

Identify the correct entity_type based on the user's request.

Valid entity types:
- supplier
- professional
- opportunity

Examples:

User: Find suppliers of biodegradable containers.
entity_type: supplier

User: Find procurement consultants in Bangalore.
entity_type: professional

User: Find packaging tenders.
entity_type: opportunity

User: Find food packaging opportunities.
entity_type: opportunity

Return ONLY valid JSON.

Schema:

{{
  "objective": "",
  "entity_type": "supplier | professional | opportunity",
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

    requests = [

        "Find food-grade biodegradable suppliers in Tamil Nadu.",

        "Find procurement professionals in Karnataka.",

        "Find food packaging opportunities in South India."

    ]

    for request in requests:

        print("=" * 60)
        print(request)

        result = parse_requirement(request)

        print(result.model_dump_json(indent=2))
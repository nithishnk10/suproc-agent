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

User:
Find AI engineers with Python and FastAPI in Chennai.

entity_type:
professional

role:
AI Engineer

skills:
["Python","FastAPI"]

-----------------------------------

User:
Find Supply Chain consultants with 8 years experience.

entity_type:
professional

minimum_experience:
8

-----------------------------------

User:
Find high priority healthcare procurement opportunities with budget above 5 lakh.

entity_type:
opportunity

industry:
Healthcare

minimum_budget:
500000

priority:
High

Extraction Rules

IMPORTANT RULES

Always extract location names into "locations".

Examples:

User: Find procurement professionals in Karnataka.
locations: ["Karnataka"]

User: Find suppliers in Tamil Nadu.
locations: ["Tamil Nadu"]

User: Find opportunities in South India.
locations: ["South India"]

Always extract the main professional role.

Examples:

Procurement professionals -> "procurement"

Procurement managers -> "procurement manager"

Supply chain consultants -> "supply chain consultant"

If a role is mentioned, NEVER leave role empty.
If a location is mentioned, NEVER leave locations empty.

For supplier requests:

- Extract ONLY the product or material into product_category.
- Examples:
  - food-grade biodegradable suppliers -> "food-grade biodegradable"
  - paper cup suppliers -> "paper cups"
  - compostable plate suppliers -> "compostable plates"

- Never populate the role field.
- Never populate industry unless the user explicitly mentions an industry.
- Leave role as null or "".

Supplier Extraction Examples

User:
Find biodegradable suppliers with capacity of at least 10000 units.

product_category:
biodegradable

minimum_capacity:
10000

maximum_delivery_days:
null

-----------------------------------

User:
Find suppliers delivering within 20 days.

product_category:
null

minimum_capacity:
null

maximum_delivery_days:
20

-----------------------------------

User:
Find food-grade biodegradable suppliers with capacity 25000 units and delivery within 15 days.

product_category:
food-grade biodegradable

minimum_capacity:
25000

maximum_delivery_days:
15

-----------------------------------

User:
Find ISO 9001 certified biodegradable suppliers in Tamil Nadu.

locations:
["Tamil Nadu"]

product_category:
biodegradable

certifications:
["ISO 9001"]

minimum_capacity:
null

maximum_delivery_days:
null

IMPORTANT

- Numbers followed by "units", "pieces", "items", or "capacity" represent minimum_capacity.
- Numbers followed by "days" represent maximum_delivery_days.
- Never assign a capacity value to maximum_delivery_days.
- Never assign a delivery value to minimum_capacity.

For professional requests:

- Extract the professional role into role.
- Examples:
  - procurement professionals -> "procurement"
  - procurement manager -> "procurement manager"
  - supply chain consultant -> "supply chain consultant"

- Extract important skills into skills.
- Extract minimum_experience if mentioned.
- Never use product_category for professional requests.

For opportunity requests:

- Extract the business industry into industry.
- Examples:
  - food packaging opportunities -> industry = "Food Packaging"
  - healthcare tenders -> industry = "Healthcare"

- Never use product_category unless the user explicitly asks for a specific product.
- Extract minimum_budget if mentioned.
- Extract priority if mentioned.

Leave fields empty or null if they are not specified.

Entity-specific rules:

Supplier:
- role = null
- product_category = required when a product is mentioned

Professional:
- role = required
- product_category = null

Opportunity:
- industry = required when an industry is mentioned
- role = null

Return ONLY valid JSON.

Schema:

{{
  "objective": "",
  "entity_type": "supplier | professional | opportunity",

  "hard_constraints": {{

      "locations": [],

      "certifications": [],

      "product_category": "",
      "minimum_capacity": null,
      "maximum_delivery_days": null,

      "role": "",
      "skills": [],
      "minimum_experience": null,

      "industry": "",
      "minimum_budget": null,
      "priority": ""
  }},

  "preferences": {{
      "startup_friendly": null,
      "sustainable_materials": null
  }},

  "requested_results": 3
}}

User Request:

{user_request}

Return ONLY valid JSON.
Do not explain.
Do not omit any mentioned location or role.
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
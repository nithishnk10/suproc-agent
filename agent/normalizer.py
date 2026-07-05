from models.requirement import Requirement

LOCATION_MAP = {
    "south india": [
        "Tamil Nadu",
        "Karnataka",
        "Kerala",
        "Andhra Pradesh",
        "Telangana"
    ],

    "north india": [
        "Delhi",
        "Punjab",
        "Haryana",
        "Uttar Pradesh",
        "Rajasthan"
    ],

    "tn": ["Tamil Nadu"],
    "tamil nadu": ["Tamil Nadu"],

    "ka": ["Karnataka"],
    "karnataka": ["Karnataka"],

    "ap": ["Andhra Pradesh"],
    "andhra pradesh": ["Andhra Pradesh"],

    "ts": ["Telangana"],
    "telangana": ["Telangana"],

    "kl": ["Kerala"],
    "kerala": ["Kerala"],

    "bangalore": ["Karnataka"],
    "bengaluru": ["Karnataka"],

    "chennai": ["Tamil Nadu"],
    "hyderabad": ["Telangana"],
    "kochi": ["Kerala"],
}

def normalize_requirement(requirement: Requirement) -> Requirement:
    normalized_locations = []

    for location in requirement.hard_constraints.locations:
        key = location.lower().strip()

        if key in LOCATION_MAP:
            normalized_locations.extend(LOCATION_MAP[key])
        else:
            normalized_locations.append(location)

    # Remove duplicates
    normalized_locations = list(dict.fromkeys(normalized_locations))

    requirement.hard_constraints.locations = normalized_locations

    requirement.entity_type = requirement.entity_type.lower().strip()

    if requirement.entity_type.endswith("s"):
        requirement.entity_type = requirement.entity_type[:-1]

    # Normalize product/category

    if requirement.hard_constraints.product_category:

        requirement.hard_constraints.product_category = (
            requirement.hard_constraints.product_category
            .lower()
            .replace("-", " ")
            .strip()
        )

    # Normalize professional role

    if requirement.entity_type == "professional":

        role = requirement.hard_constraints.role

        if role:

            role = role.lower().strip()

            if "procurement" in role:
                requirement.hard_constraints.role = "procurement"

            elif "buyer" in role:
                requirement.hard_constraints.role = "buyer"

            elif "supply chain" in role:
                requirement.hard_constraints.role = "supply chain"

            elif "ai engineer" in role:
                requirement.hard_constraints.role = "ai engineer"

            elif "backend" in role:
                requirement.hard_constraints.role = "backend"

            elif "data scientist" in role:
                requirement.hard_constraints.role = "data scientist"

    return requirement

if __name__ == "__main__":

    from agent.parser import parse_requirement

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    req = parse_requirement(request)

    print("Before:")
    print(req.model_dump_json(indent=2))

    req = normalize_requirement(req)

    print("\nAfter:")
    print(req.model_dump_json(indent=2))
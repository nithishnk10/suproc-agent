from models.requirement import Requirement

LOCATION_MAP = {
    "south india": [
        "Tamil Nadu",
        "Karnataka",
        "Kerala",
        "Andhra Pradesh",
        "Telangana"
    ],
    "tn": ["Tamil Nadu"],
    "ka": ["Karnataka"],
    "ap": ["Andhra Pradesh"],
    "ts": ["Telangana"],
    "kl": ["Kerala"],
    "bangalore": ["Bengaluru"],
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
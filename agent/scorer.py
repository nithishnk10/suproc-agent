from models.match import Match
from models.requirement import Requirement


def calculate_match_score(
    supplier: dict,
    requirement: Requirement
    
) -> Match:
    evidence = []

    breakdown = {}

    score = 0

    # Product Match (30)

    supplier_product = supplier["product_category"].lower().replace("-", " ")
    required_product = requirement.hard_constraints.product_category.lower().replace("-", " ")

    if all(word in supplier_product for word in required_product.split()):
        score += 30
        breakdown["product"] = 30.0
        evidence.append("Product category matches the requirement.")
        
    else:
        breakdown["product"] = 0

    # Location (20)

    locations = requirement.hard_constraints.locations

    if not locations or supplier["state"] in locations:

        breakdown["location"] = 20
        score += 20

        if locations:
            evidence.append(f"Located in {supplier['state']}.")

    else:
        breakdown["location"] = 0

    # Capacity (25)

    capacity = requirement.hard_constraints.minimum_capacity

    if capacity is None or supplier["monthly_capacity"] >= capacity:

        breakdown["capacity"] = 25
        score += 25

        if capacity is not None:
            evidence.append(
                f"Monthly capacity {supplier['monthly_capacity']} meets the required capacity."
            )

    else:
        breakdown["capacity"] = 0

    # Delivery (15)

    delivery = requirement.hard_constraints.maximum_delivery_days

    if delivery is None or supplier["delivery_days"] <= delivery:

        breakdown["delivery"] = 15
        score += 15

        if delivery is not None:
            evidence.append(
                f"Delivery time of {supplier['delivery_days']} days satisfies the deadline."
            )

    else:
        breakdown["delivery"] = 0

    # Rating (10)

    rating_score = round((supplier["rating"] / 5) * 10, 2)

    breakdown["rating"] = rating_score

    score += rating_score
    evidence.append(
        f"Supplier rating: {supplier['rating']}/5."
    )

    return Match(
        supplier_id=supplier["supplier_id"],
        supplier_name=supplier["name"],
        state=supplier["state"],
        score=round(score, 2),
        breakdown=breakdown,
        evidence=evidence,
    )


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from agent.executor import execute_search

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    suppliers = execute_search(req)

    for supplier in suppliers:

        match = calculate_match_score(
            supplier,
            req
        )

        print(match.model_dump_json(indent=2))
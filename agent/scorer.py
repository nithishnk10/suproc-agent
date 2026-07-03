from models.match import Match
from models.requirement import Requirement


def calculate_match_score(
    supplier: dict,
    requirement: Requirement
) -> Match:

    breakdown = {}

    score = 0

    # Product Match (30)

    if supplier["product_category"].lower() == \
       requirement.hard_constraints.product_category.lower():

        breakdown["product"] = 30
        score += 30

    else:
        breakdown["product"] = 0

    # Location (20)

    if supplier["state"] in requirement.hard_constraints.locations:

        breakdown["location"] = 20
        score += 20

    else:
        breakdown["location"] = 0

    # Capacity (25)

    if supplier["monthly_capacity"] >= \
            requirement.hard_constraints.minimum_capacity:

        breakdown["capacity"] = 25
        score += 25

    else:
        breakdown["capacity"] = 0

    # Delivery (15)

    if supplier["delivery_days"] <= \
            requirement.hard_constraints.maximum_delivery_days:

        breakdown["delivery"] = 15
        score += 15

    else:
        breakdown["delivery"] = 0

    # Rating (10)

    rating_score = round((supplier["rating"] / 5) * 10, 2)

    breakdown["rating"] = rating_score

    score += rating_score

    return Match(
        supplier_id=supplier["supplier_id"],
        supplier_name=supplier["name"],
        score=round(score, 2),
        breakdown=breakdown
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
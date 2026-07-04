from models.requirement import Requirement


def filter_opportunities(
    opportunities: list[dict],
    requirement: Requirement,
):

    filtered = []

    for opportunity in opportunities:

        # Location filter
        if (
            requirement.hard_constraints.locations
            and opportunity["location"] not in requirement.hard_constraints.locations
        ):
            continue

        # Category filter
        if (
            requirement.hard_constraints.product_category
            and requirement.hard_constraints.product_category.lower()
            not in opportunity["title"].lower()
            and requirement.hard_constraints.product_category.lower()
            not in opportunity["category"].lower()
        ):
            continue

        filtered.append(opportunity)

    return filtered


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from tools.search import search_entities

    request = """
Find food packaging opportunities in South India.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    opportunities = search_entities(
        entity_type="opportunity"
    )

    results = filter_opportunities(
        opportunities,
        req
    )

    print(f"\nFound {len(results)} opportunities\n")

    for opportunity in results:
        print(
            opportunity["opportunity_id"],
            opportunity["title"],
            opportunity["location"]
        )
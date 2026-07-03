from tools.search import search_entities
from models.requirement import Requirement

from tools.search import search_entities
from models.requirement import Requirement


def execute_search(requirement: Requirement):
    all_results = []

    locations = requirement.hard_constraints.locations

    if not locations:
        return search_entities(
            entity_type=requirement.entity_type,
            product_category=requirement.hard_constraints.product_category,
        )

    for location in locations:
        results = search_entities(
            entity_type=requirement.entity_type,
            state=location,
            product_category=requirement.hard_constraints.product_category,
        )

        all_results.extend(results)

    # Remove duplicates
    unique_results = {}
    for supplier in all_results:
        unique_results[supplier["supplier_id"]] = supplier

    return list(unique_results.values())

if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    results = execute_search(req)

    print(f"Found {len(results)} suppliers\n")

    for supplier in results:
        print(f"{supplier['supplier_id']} - {supplier['name']} ({supplier['state']})")
from tools.search import search_entities
from models.requirement import Requirement

from tools.search import search_entities
from models.requirement import Requirement
from agent.filter_by_constraints import filter_by_constraints
from agent.filter_professionals import filter_professionals
from agent.filter_opportunities import filter_opportunities


def execute_search(requirement: Requirement):
    all_results = []

    locations = requirement.hard_constraints.locations

    if not locations:
        all_results = search_entities(
            entity_type=requirement.entity_type,
            product_category=requirement.hard_constraints.product_category,
        )
    else:
        for location in locations:
            results = search_entities(
                entity_type=requirement.entity_type,
                state=location,

                product_category=(
                    requirement.hard_constraints.product_category
                    if requirement.entity_type == "supplier"
                    else requirement.hard_constraints.industry
                ),

                role=requirement.hard_constraints.role,

                skills=(
                    requirement.hard_constraints.skills[0]
                    if requirement.hard_constraints.skills
                    else None
                ),
            )

            all_results.extend(results)


    # Remove duplicates
    # Remove duplicates
    entity_key = {
        "supplier": "supplier_id",
        "professional": "professional_id",
        "opportunity": "opportunity_id",
    }[requirement.entity_type]

    unique_results = {}

    for item in all_results:
        unique_results[item[entity_key]] = item

    results = list(unique_results.values())

    if requirement.entity_type == "supplier":
        results = filter_by_constraints(results, requirement)

    elif requirement.entity_type == "professional":
        results = filter_professionals(results, requirement)

    elif requirement.entity_type == "opportunity":
        results = filter_opportunities(results, requirement)

    return results

    



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
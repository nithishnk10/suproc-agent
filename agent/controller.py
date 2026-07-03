from agent.parser import parse_requirement
from agent.normalizer import normalize_requirement
from agent.planner import create_execution_plan
from agent.executor import execute_search
from agent.scorer import calculate_match_score
from agent.validator import validate_matches
from models.search_summary import SearchSummary
from tools.search import search_entities

def run_agent(user_request: str):

    # Step 1
    requirement = parse_requirement(user_request)

    # Step 2
    requirement = normalize_requirement(requirement)

    # Total suppliers
    total_suppliers = len(search_entities())


    # Suppliers matching the requested product
    product_matches = len(
        search_entities(
            product_category=requirement.hard_constraints.product_category
        )
    )

    product_suppliers = search_entities(
        product_category=requirement.hard_constraints.product_category
    )

    capacity_matches = sum(
        supplier["monthly_capacity"] >= requirement.hard_constraints.minimum_capacity
        for supplier in product_suppliers
    )

    delivery_matches = sum(
        supplier["delivery_days"] <= requirement.hard_constraints.maximum_delivery_days
        for supplier in product_suppliers
    )

    # Step 3
    plan = create_execution_plan(requirement)

    # Step 4
    suppliers = execute_search(requirement)

    # Step 5
    matches = [
        calculate_match_score(supplier, requirement)
        for supplier in suppliers
    ]

    # Step 6
    validation = validate_matches(
        matches,
        suppliers,
        requirement
    )

    summary = SearchSummary(
        total_suppliers=total_suppliers,
        product_matches=product_matches,
        capacity_matches=capacity_matches,
        delivery_matches=delivery_matches,
        final_matches=len(matches),
    )

    return {
        "requirement": requirement,
        "plan": plan,
        "matches": matches,
        "validation": validation,
        "summary": summary,
    }

if __name__ == "__main__":

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    result = run_agent(request)

    print("\nRequirement")
    print(result["requirement"].model_dump_json(indent=2))

    print("\nPlan")
    print(result["plan"].model_dump_json(indent=2))

    print("\nMatches")

    for match in result["matches"]:
        print(match.model_dump_json(indent=2))

    print("\nValidation")
    print(result["validation"].model_dump_json(indent=2))
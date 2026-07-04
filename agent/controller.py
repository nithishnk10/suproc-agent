from agent.parser import parse_requirement
from agent.normalizer import normalize_requirement
from agent.planner import create_execution_plan
from agent.executor import execute_search
from agent.scorer import calculate_match_score
from agent.validator import validate_matches
from models.search_summary import SearchSummary
from tools.search import search_entities
from agent.risk_analyzer import analyze_supplier_risk
from agent.missing_information import detect_missing_information
from agent.dataset_capability import check_dataset_capability
from agent.execution_trace import build_execution_trace


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

    capacity_requirement = requirement.hard_constraints.minimum_capacity
    delivery_requirement = requirement.hard_constraints.maximum_delivery_days

    capacity_matches = (
        sum(
            supplier["monthly_capacity"] >= capacity_requirement
            for supplier in product_suppliers
        )
        if capacity_requirement is not None
        else len(product_suppliers)
    )

    delivery_matches = (
        sum(
            supplier["delivery_days"] <= delivery_requirement
            for supplier in product_suppliers
        )
        if delivery_requirement is not None
        else len(product_suppliers)
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

    risks = [
        analyze_supplier_risk(supplier)
        for supplier in suppliers
    ]

    missing_information = detect_missing_information(requirement)

    # Step 6
    validation = validate_matches(
        matches,
        suppliers,
        requirement
    )

    # Step 7 - Correction Attempt

    attempt = 1

    while not validation.passed and attempt <= 3:

        print(f"\nValidation failed. Correction attempt {attempt}/3")

        for error in validation.errors:
            print(f"  • {error}")

        if attempt == 1:
            print("\nAction: Re-running supplier search with the original constraints.")

        elif attempt == 2:
            print("\nAction: Constraints appear too restrictive.")
            print("Suggestion: Consider reducing the required capacity or increasing the delivery window.")

        else:
            print("\nAction: Maximum correction attempts reached.")
            print("Preparing recommendations for the user.")

        suppliers = execute_search(requirement)

        matches = [
            calculate_match_score(supplier, requirement)
            for supplier in suppliers
        ]

        validation = validate_matches(
            matches,
            suppliers,
            requirement
        )

        attempt += 1

    summary = SearchSummary(
        total_suppliers=total_suppliers,
        product_matches=product_matches,
        capacity_matches=capacity_matches,
        delivery_matches=delivery_matches,
        final_matches=len(matches),
    )

    capability = check_dataset_capability(requirement)

    trace = build_execution_trace()

    return {
        "requirement": requirement,
        "plan": plan,
        "summary": summary,
        "suppliers": suppliers,
        "matches": matches,
        "risks": risks,
        "missing_information": missing_information,
        "validation": validation,
        "capability": capability,
        "trace": trace,
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
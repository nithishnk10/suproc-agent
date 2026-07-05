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
    




    # Suppliers matching the requested product
    # Generic search summary

    # Get the complete dataset for summary statistics
    all_entities = search_entities(entity_type=requirement.entity_type)

    total_entities = len(all_entities)
    location_matches = [
        e for e in all_entities
        if (
            not requirement.hard_constraints.locations
            or (
                e.get("state") in requirement.hard_constraints.locations
                or e.get("location") in requirement.hard_constraints.locations
            )
        )
    ]

    location_matches_count = len(location_matches)

    # Use the full dataset to calculate search summary
    entities = all_entities

    if requirement.entity_type == "supplier":

        required_product = requirement.hard_constraints.product_category or ""

        required_words = (
            required_product.lower()
            .replace("-", " ")
            .split()
        )


        # Product matches (after location filter)
        match1 = len([
            s for s in location_matches
            if all(
                word in s["product_category"].lower().replace("-", " ")
                for word in required_words
            )
        ])

        # Capacity matches
        if requirement.hard_constraints.minimum_capacity is not None:
            match2 = len([
                s for s in location_matches
                if s["monthly_capacity"] >= requirement.hard_constraints.minimum_capacity
            ])
        else:
            match2 = None

        # Delivery matches
        if requirement.hard_constraints.maximum_delivery_days is not None:
            match3 = len([
                s for s in location_matches
                if s["delivery_days"] <= requirement.hard_constraints.maximum_delivery_days
            ])
        else:
            match3 = None


    elif requirement.entity_type == "professional":

        role = requirement.hard_constraints.role
        skills = requirement.hard_constraints.skills
        experience = requirement.hard_constraints.minimum_experience

        # Role matches
        match1 = len([
            p for p in entities
            if (
                not role
                or role.lower() in p["role"].lower()
            )
        ])

        # Skills matches
        if skills:
            match2 = len([
                p for p in entities
                if all(
                    skill.lower() in p["skills"].lower()
                    for skill in skills
                )
            ])
        else:
            match2 = None

        # Experience matches
        if experience is not None:
            match3 = len([
                p for p in entities
                if p["experience_years"] >= experience
            ])
        else:
            match3 = None

    else:

        industry = requirement.hard_constraints.industry
        budget = requirement.hard_constraints.minimum_budget
        priority = requirement.hard_constraints.priority

        match1 = len([
            o for o in entities
            if (
                not industry
                or industry.lower() in o["industry"].lower()
            )
        ])

        match2 = len([
            o for o in entities
            if (
                budget is None
                or o["budget"] >= budget
            )
        ])

        match3 = len([
            o for o in entities
            if (
                not priority
                or o["priority"].lower() == priority.lower()
            )
        ])

    # Step 3
    plan = create_execution_plan(requirement)

    # Step 4
    # Perform the actual filtered search for recommendations
    filtered_entities = execute_search(requirement)

    entities = filtered_entities


    # Step 5
    matches = [
        calculate_match_score(entity, requirement)
        for entity in entities
    ]

    if requirement.entity_type == "supplier":
        risks = [
            analyze_supplier_risk(entity)
            for entity in entities
        ]
    else:
        risks = []

    missing_information = detect_missing_information(requirement)

    # Step 6
    validation = validate_matches(
        matches,
        entities,
        requirement
    )

    # Step 7 - Correction Attempt

    attempt = 1

    while not validation.passed and attempt <= 3:

        print(f"\nValidation failed. Correction attempt {attempt}/3")

        for error in validation.errors:
            print(f"  • {error}")

        if attempt == 1:
            print(
                f"\nAction: Re-running {requirement.entity_type} search with the original constraints."
            )

        elif attempt == 2:
            print("\nAction: Constraints appear too restrictive.")
            print("Suggestion: Consider reducing the required capacity or increasing the delivery window.")

        else:
            print("\nAction: Maximum correction attempts reached.")
            print("Preparing recommendations for the user.")

        entities = execute_search(requirement)

        matches = [
            calculate_match_score(entity, requirement)
            for entity in entities
        ]

        print(f"Entities found : {len(entities)}")
        print(f"Matches created: {len(matches)}")

        validation = validate_matches(
            matches,
            entities,
            requirement
        )

        attempt += 1

    summary = SearchSummary(
        total_entities=total_entities,
        location_matches=location_matches_count,
        match1=match1,
        match2=match2,
        match3=match3,
        final_matches=len(matches),
    )

    capability = check_dataset_capability(requirement)

    trace = build_execution_trace(requirement.entity_type)

    return {
        "requirement": requirement,
        "plan": plan,
        "summary": summary,
        "entities": entities,
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
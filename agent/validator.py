from models.validation import ValidationResult
from models.requirement import Requirement
from models.match import Match


def validate_matches(
    matches: list[Match],
    entities: list[dict],
    requirement: Requirement,
) -> ValidationResult:

    errors = []

    id_key = {
        "supplier": "supplier_id",
        "professional": "professional_id",
        "opportunity": "opportunity_id",
    }[requirement.entity_type]

    entity_lookup = {
        entity[id_key]: entity
        for entity in entities
    }

    seen = set()

    for match in matches:

        entity = entity_lookup.get(match.entity_id)

        if entity is None:
            errors.append(
                f"{match.entity_id} not found in database."
            )
            continue

        if match.entity_id in seen:
            errors.append(
                f"Duplicate {requirement.entity_type} {match.entity_id}"
            )

        seen.add(match.entity_id)

        if requirement.entity_type == "supplier":

            if (
                requirement.hard_constraints.locations
                and entity["state"] not in requirement.hard_constraints.locations
            ):
                errors.append(f"{entity[id_key]} failed location constraint.")

            if (
                requirement.hard_constraints.minimum_capacity is not None
                and entity["monthly_capacity"] < requirement.hard_constraints.minimum_capacity
            ):
                errors.append(f"{entity[id_key]} insufficient capacity.")

            if (
                requirement.hard_constraints.maximum_delivery_days is not None
                and entity["delivery_days"] > requirement.hard_constraints.maximum_delivery_days
            ):
                errors.append(f"{entity[id_key]} delivery deadline not met.")

        # Check requested number of results
    if len(matches) < requirement.requested_results:
        print(
            f"\nNote: Only {len(matches)} {requirement.entity_type}(s) matched "
            f"although {requirement.requested_results} were requested."
        )

    passed = len(matches) > 0

    return ValidationResult(
        passed=passed,
        errors=errors,
    )

if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from agent.executor import execute_search
    from agent.scorer import calculate_match_score

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    entities = execute_search(req)

    matches = [
        calculate_match_score(entity, req)
        for entity in entities
    ]

    result = validate_matches(
        matches,
        entities,
        req,
    )

    print(result.model_dump_json(indent=2))
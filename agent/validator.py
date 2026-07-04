from models.validation import ValidationResult
from models.requirement import Requirement
from models.match import Match


def validate_matches(
    matches: list[Match],
    suppliers: list[dict],
    requirement: Requirement,
) -> ValidationResult:

    errors = []

    supplier_lookup = {
        s["supplier_id"]: s
        for s in suppliers
    }

    seen = set()

    for match in matches:

        supplier = supplier_lookup.get(match.supplier_id)

        if supplier is None:
            errors.append(
                f"{match.supplier_id} not found in database."
            )
            continue

        if match.supplier_id in seen:
            errors.append(
                f"Duplicate supplier {match.supplier_id}"
            )

        seen.add(match.supplier_id)

        if (
            requirement.hard_constraints.locations
            and supplier["state"] not in requirement.hard_constraints.locations
        ):
            errors.append(f"{supplier['supplier_id']} failed location constraint.")

        if (
            requirement.hard_constraints.minimum_capacity is not None
            and supplier["monthly_capacity"] < requirement.hard_constraints.minimum_capacity
        ):
            errors.append(f"{supplier['supplier_id']} insufficient capacity.")

        if (
            requirement.hard_constraints.maximum_delivery_days is not None
            and supplier["delivery_days"] > requirement.hard_constraints.maximum_delivery_days
        ):
            errors.append(f"{supplier['supplier_id']} delivery deadline not met.")

    return ValidationResult(    
        passed=len(errors) == 0,
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

    suppliers = execute_search(req)

    matches = [
        calculate_match_score(supplier, req)
        for supplier in suppliers
    ]

    result = validate_matches(
        matches,
        suppliers,
        req,
    )

    print(result.model_dump_json(indent=2))
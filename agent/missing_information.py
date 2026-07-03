from models.missing_information import MissingInformation
from models.requirement import Requirement


def detect_missing_information(requirement: Requirement):

    missing = []

    # Dataset does not contain pricing
    if "price" in requirement.objective.lower() or "budget" in requirement.objective.lower():
        missing.append(
            "Pricing information is not available in the dataset."
        )

    # Dataset does not contain payment terms
    if "payment" in requirement.objective.lower():
        missing.append(
            "Payment terms are not available."
        )

    # Dataset does not contain warranty
    if "warranty" in requirement.objective.lower():
        missing.append(
            "Warranty information is not available."
        )

    # Certifications not specified
    if not requirement.hard_constraints.certifications:
        missing.append(
            "No certification preference was specified."
        )

    return MissingInformation(items=missing)


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement

    request = """
Need food-grade biodegradable container suppliers
under ₹50,000 with payment terms.
"""

    req = normalize_requirement(parse_requirement(request))

    result = detect_missing_information(req)

    print(result.model_dump_json(indent=2))
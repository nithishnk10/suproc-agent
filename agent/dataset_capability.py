from models.dataset_capability import DatasetCapability
from models.requirement import Requirement


def check_dataset_capability(requirement: Requirement):

    # ---------------- Available Fields ----------------

    if requirement.entity_type == "supplier":

        available = [
            "Product Category",
            "State",
            "Monthly Capacity",
            "Delivery Days",
            "Supplier Rating",
            "Sustainability Score",
            "Startup Friendly",
            "Certifications",
        ]

    elif requirement.entity_type == "professional":

        available = [
            "Role",
            "Skills",
            "Experience",
            "State",
            "Availability",
            "Professional Rating",
        ]

    else:   # opportunity

        available = [
            "Industry",
            "Location",
            "Budget",
            "Priority",
            "Required Skills",
            "Deadline",
            "Client Name",
        ]

    # ---------------- Unavailable Fields ----------------

    unavailable = []

    objective = requirement.objective.lower()

    if "price" in objective or "budget" in objective:
        unavailable.append("Price")

    if "payment" in objective:
        unavailable.append("Payment Terms")

    if "gst" in objective:
        unavailable.append("GST Details")

    if "warranty" in objective:
        unavailable.append("Warranty")

    if "iso 22000" in objective:
        unavailable.append("ISO 22000")

    return DatasetCapability(
        available=available,
        unavailable=unavailable,
    )


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement

    request = """
Find food packaging opportunities in South India.
"""

    req = normalize_requirement(parse_requirement(request))

    result = check_dataset_capability(req)

    print(result.model_dump_json(indent=2))
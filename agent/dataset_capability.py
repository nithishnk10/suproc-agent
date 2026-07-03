from models.dataset_capability import DatasetCapability
from models.requirement import Requirement


AVAILABLE_FIELDS = [
    "Product Category",
    "State",
    "Monthly Capacity",
    "Delivery Days",
    "Supplier Rating",
    "Sustainability Score",
    "Startup Friendly",
    "Certifications"
]


def check_dataset_capability(requirement: Requirement):

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
        available=AVAILABLE_FIELDS,
        unavailable=unavailable
    )


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement

    request = """
Need suppliers under ₹50,000
with ISO 22000
and payment terms.
"""

    req = normalize_requirement(parse_requirement(request))

    result = check_dataset_capability(req)

    print(result.model_dump_json(indent=2))
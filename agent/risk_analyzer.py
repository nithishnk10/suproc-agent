from models.risk import SupplierRisk


def analyze_supplier_risk(supplier: dict):

    risks = []

    # Rating risk
    if supplier["rating"] < 4.6:
        risks.append(
            f"Supplier rating is {supplier['rating']}/5."
        )

    # Delivery risk
    if supplier["delivery_days"] > 25:
        risks.append(
            "Delivery timeline is close to the requested limit."
        )

    # Sustainability risk
    if supplier["sustainability_score"] < 80:
        risks.append(
            "Sustainability score is relatively low."
        )

    # Startup friendliness
    if supplier["startup_friendly"] == 0:
        risks.append(
            "Supplier is not marked as startup friendly."
        )

    if not risks:
        risks.append("No significant risks detected.")

    return SupplierRisk(
        supplier_id=supplier["supplier_id"],
        supplier_name=supplier["name"],
        risks=risks,
    )


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from agent.executor import execute_search

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    req = normalize_requirement(parse_requirement(request))

    suppliers = execute_search(req)

    for supplier in suppliers:
        risk = analyze_supplier_risk(supplier)
        print(risk.model_dump_json(indent=2))
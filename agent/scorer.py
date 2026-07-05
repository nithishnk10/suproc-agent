from models.match import Match
from models.requirement import Requirement


def calculate_supplier_score(
    supplier: dict,
    requirement: Requirement
    
) -> Match:
    evidence = []

    breakdown = {}

    score = 0

    # Product Match (30)

    supplier_product = supplier["product_category"].lower().replace("-", " ")
    required_product = requirement.hard_constraints.product_category.lower().replace("-", " ")

    if all(word in supplier_product for word in required_product.split()):
        score += 30
        breakdown["product"] = 30.0
        evidence.append("Product category matches the requirement.")
        
    else:
        breakdown["product"] = 0

    # Location (20)

    locations = requirement.hard_constraints.locations

    if not locations or supplier["state"] in locations:

        breakdown["location"] = 20
        score += 20

        if locations:
            evidence.append(f"Located in {supplier['state']}.")

    else:
        breakdown["location"] = 0

    # Capacity (25)

    capacity = requirement.hard_constraints.minimum_capacity

    if capacity is None or supplier["monthly_capacity"] >= capacity:

        breakdown["capacity"] = 25
        score += 25

        if capacity is not None:
            evidence.append(
                f"Monthly capacity {supplier['monthly_capacity']} meets the required capacity."
            )

    else:
        breakdown["capacity"] = 0

    # Delivery (15)

    delivery = requirement.hard_constraints.maximum_delivery_days

    if delivery is None or supplier["delivery_days"] <= delivery:

        breakdown["delivery"] = 15
        score += 15

        if delivery is not None:
            evidence.append(
                f"Delivery time of {supplier['delivery_days']} days satisfies the deadline."
            )

    else:
        breakdown["delivery"] = 0

    # Rating (10)

    # Rating (5)

    rating_score = round((supplier["rating"] / 5) * 5, 2)

    breakdown["rating"] = rating_score
    score += rating_score

    evidence.append(
        f"Supplier rating: {supplier['rating']}/5."
    )

    # Sustainability (2)

    sustainability = supplier["sustainability_score"]

    sustainability_score = round((sustainability / 100) * 2, 2)

    breakdown["sustainability"] = sustainability_score
    score += sustainability_score

    evidence.append(
        f"Sustainability score: {sustainability}/100."
    )

    # Startup Friendly (1)

    if supplier["startup_friendly"]:
        breakdown["startup"] = 1.0
        score += 1
        evidence.append("Startup friendly supplier.")
    else:
        breakdown["startup"] = 0.0

    # Previous Projects (2)

    projects = supplier["previous_projects"]

    project_score = min(projects / 20, 1) * 2

    project_score = round(project_score, 2)

    breakdown["projects"] = project_score
    score += project_score

    evidence.append(
        f"Completed {projects} previous projects."
    )

    return Match(
        entity_id=supplier["supplier_id"],
        entity_name=supplier["name"],
        entity_type="supplier",
        location=supplier["state"],
        score=round(score, 2),
        breakdown=breakdown,
        evidence=evidence,
    )

def calculate_professional_score(
    professional: dict,
    requirement: Requirement
) -> Match:

    evidence = []
    breakdown = {}
    score = 0

    # Role Match (30)

    role = requirement.hard_constraints.role

    if not role:
        score += 30
        breakdown["role"] = 30.0

    else:
        required_words = role.lower().split()
        professional_role = professional["role"].lower()

        if any(word in professional_role for word in required_words):
            score += 30
            breakdown["role"] = 30.0
            evidence.append(f"Role matches: {professional['role']}")
        else:
            breakdown["role"] = 0

    # Skills Match (25)

    required_skills = requirement.hard_constraints.skills

    if not required_skills:
        breakdown["skills"] = 25
        score += 25
    else:
        professional_skills = professional["skills"].lower()

        matched = all(
            skill.lower() in professional_skills
            for skill in required_skills
        )

        if matched:
            breakdown["skills"] = 25
            score += 25
            evidence.append("Required skills matched.")
        else:
            breakdown["skills"] = 0

    # Location (20)

    locations = requirement.hard_constraints.locations

    if not locations or professional["state"] in locations:
        breakdown["location"] = 20
        score += 20

        if locations:
            evidence.append(f"Located in {professional['state']}.")
    else:
        breakdown["location"] = 0

    # Experience (15)

    minimum_experience = requirement.hard_constraints.minimum_experience

    if (
        minimum_experience is None
        or professional["experience_years"] >= minimum_experience
    ):
        breakdown["experience"] = 15
        score += 15

        evidence.append(
            f"{professional['experience_years']} years experience."
        )
    else:
        breakdown["experience"] = 0

    # Rating (10)

    rating_score = round((professional["rating"] / 5) * 10, 2)

    breakdown["rating"] = rating_score
    score += rating_score

    evidence.append(
        f"Professional rating: {professional['rating']}/5."
    )

    return Match(
        entity_id=professional["professional_id"],
        entity_name=professional["name"],
        entity_type="professional",
        location=professional["state"],
        score=round(score, 2),
        breakdown=breakdown,
        evidence=evidence,
    )


def calculate_opportunity_score(
    opportunity: dict,
    requirement: Requirement,
) -> Match:

    evidence = []
    breakdown = {}
    score = 0

    # Industry (30)

    industry = requirement.hard_constraints.industry


    if not industry or industry.lower() in opportunity["industry"].lower():
        score += 30
        breakdown["industry"] = 30.0

        if industry:
            evidence.append(
                f"Industry matches {opportunity['industry']}."
            )
    else:
        breakdown["industry"] = 0

    # Location (20)

    locations = requirement.hard_constraints.locations

    if not locations or opportunity["location"] in locations:
        score += 20
        breakdown["location"] = 20.0

        if locations:
            evidence.append(
                f"Located in {opportunity['location']}."
            )
    else:
        breakdown["location"] = 0

    # Budget (25)

    budget = requirement.hard_constraints.minimum_budget

    if budget is None or opportunity["budget"] >= budget:
        score += 25
        breakdown["budget"] = 25.0

        if budget is not None:
            evidence.append(
                f"Budget ₹{opportunity['budget']:,} satisfies the requirement."
            )
    else:
        breakdown["budget"] = 0

    # Priority (15)

    # Priority (15)

    priority = opportunity["priority"].lower()

    if priority == "high":
        breakdown["priority"] = 15.0
        score += 15
        evidence.append("High priority opportunity.")

    elif priority == "medium":
        breakdown["priority"] = 10.0
        score += 10
        evidence.append("Medium priority opportunity.")

    else:
        breakdown["priority"] = 5.0
        score += 5
        evidence.append("Low priority opportunity.")


    # Status / Quality (10)

    status = opportunity["status"].lower()

    if status == "open":
        breakdown["quality"] = 10.0
        score += 10
        evidence.append("Opportunity is currently open.")

    elif status == "in review":
        breakdown["quality"] = 5.0
        score += 5
        evidence.append("Opportunity is under review.")

    else:
        breakdown["quality"] = 0.0

    return Match(
        entity_id=opportunity["opportunity_id"],
        entity_name=opportunity["title"],
        entity_type="opportunity",
        location=opportunity["location"],
        score=round(score, 2),
        breakdown=breakdown,
        evidence=evidence,
    )


def calculate_match_score(entity: dict, requirement: Requirement) -> Match:

    if requirement.entity_type == "supplier":
        return calculate_supplier_score(entity, requirement)

    elif requirement.entity_type == "professional":
        return calculate_professional_score(entity, requirement)

    elif requirement.entity_type == "opportunity":
        return calculate_opportunity_score(entity, requirement)

    else:
        raise ValueError(f"Unsupported entity type: {requirement.entity_type}")


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from agent.executor import execute_search

    request = """
Find food packaging opportunities in South India.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    entities = execute_search(req)


    for entity in entities:
        match = calculate_match_score(
            entity,
            req
        )

        print(match.model_dump_json(indent=2))


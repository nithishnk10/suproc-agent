from models.plan import ExecutionPlan
from models.requirement import Requirement

def create_execution_plan(requirement: Requirement) -> ExecutionPlan:

    if requirement.entity_type == "supplier":
        steps = [
            "Search suppliers by product category and location",
            "Inspect capabilities and certifications",
            "Filter records that fail hard constraints",
            "Rank remaining matches",
            "Validate recommendations",
            "Prepare outreach message",
        ]

    elif requirement.entity_type == "professional":
        steps = [
            "Search professionals by role and location",
            "Evaluate skills and experience",
            "Filter records that fail hard constraints",
            "Rank remaining matches",
            "Validate recommendations",
            "Prepare interview recommendations",
        ]

    else:   # opportunity
        steps = [
            "Search opportunities by industry and location",
            "Evaluate budget and priority",
            "Filter records that fail hard constraints",
            "Rank remaining matches",
            "Validate recommendations",
            "Prepare application recommendations",
        ]

    return ExecutionPlan(steps=steps)

if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    plan = create_execution_plan(req)

    print(plan.model_dump_json(indent=2))
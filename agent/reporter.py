from models.requirement import Requirement
from models.plan import ExecutionPlan
from models.match import Match
from models.validation import ValidationResult
from models.search_summary import SearchSummary


def generate_report(
    requirement,
    plan,
    matches,
    validation,
    summary: SearchSummary,
):

    print("=" * 65)
    print("        SUPROC AI PROCUREMENT AGENT")
    print("=" * 65)

    print("\n📋 BUSINESS REQUIREMENT")
    print("-" * 65)

    print("Objective:")
    print(requirement.objective)

    print("\nEntity Type:")
    print(requirement.entity_type)

    print("\nHard Constraints")

    print(f"Product : {requirement.hard_constraints.product_category}")
    print(f"Capacity: {requirement.hard_constraints.minimum_capacity}")
    print(f"Delivery: {requirement.hard_constraints.maximum_delivery_days} days")

    print("\nLocations")

    for location in requirement.hard_constraints.locations:
        print(f"• {location}")

    print("\n🧠 EXECUTION PLAN")
    print("-" * 65)

    print("\n📊 SEARCH SUMMARY")
    print("-" * 65)

    print(f"Total Suppliers        : {summary.total_suppliers}")
    print(f"Product Matches        : {summary.product_matches}")
    print(f"Passed Capacity Check  : {summary.capacity_matches}")
    print(f"Passed Delivery Check  : {summary.delivery_matches}")
    print(f"Final Recommendations  : {summary.final_matches}")

    for step in plan.steps:
        print(f"✓ {step}")

    print("\n🏆 RECOMMENDED SUPPLIERS")
    print("-" * 65)

    for i, match in enumerate(matches, start=1):

        print(f"\n{i}. {match.supplier_name}")
        print(f"Supplier ID : {match.supplier_id}")
        print(f"Score       : {match.score}")

        print("\nScore Breakdown")

        for key, value in match.breakdown.items():
            print(f"   {key:12} {value}")

        print("\nEvidence")

        for item in match.evidence:
            print(f"   ✓ {item}")

        print("-" * 65)

    print("\n✅ VALIDATION")
    print("-" * 65)

    if validation.passed:
        print("PASSED")
    else:
        print("FAILED")

        for error in validation.errors:
            print(error)

    print("\n⚠ NEXT ACTION")
    print("-" * 65)

    print("Recommended:")
    print("Send procurement enquiry.")

    print("\nSTATUS")
    print("Awaiting Human Approval")

    print("=" * 65)


if __name__ == "__main__":

    from agent.controller import run_agent

    request = """
We need three suppliers from South India
that provide food-grade biodegradable containers,
support 10000 units
and deliver within 30 days.
"""

    result = run_agent(request)

    generate_report(
        result["requirement"],
        result["plan"],
        result["matches"],
        result["validation"],
        result["summary"],
    )
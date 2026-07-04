from models.requirement import Requirement
from models.plan import ExecutionPlan
from models.match import Match
from models.validation import ValidationResult
from models.search_summary import SearchSummary
from agent.human_approval import request_human_approval
from agent.email_generator import generate_procurement_email


def generate_report(
    requirement,
    plan,
    matches,
    validation,
    summary: SearchSummary,
    risks,
    missing_information,
    capability,
    trace,
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
    capacity = requirement.hard_constraints.minimum_capacity
    delivery = requirement.hard_constraints.maximum_delivery_days

    print(f"Capacity: {capacity if capacity is not None else 'Not specified'}")

    print(
        f"Delivery: {str(delivery) + ' days' if delivery is not None else 'Not specified'}"
    )

    print("\nLocations")

    for location in requirement.hard_constraints.locations:
        print(f"• {location}")

    print("\n🧠 EXECUTION PLAN")
    print("-" * 65)

    for step in plan.steps:
        print(f"✓ {step}")

    print("\n📊 SEARCH SUMMARY")
    print("-" * 65)

    print(f"Total Suppliers        : {summary.total_suppliers}")
    print(f"Product Matches        : {summary.product_matches}")
    print(f"Passed Capacity Check  : {summary.capacity_matches}")
    print(f"Passed Delivery Check  : {summary.delivery_matches}")
    print(f"Final Recommendations  : {summary.final_matches}")

    print("\n📦 DATASET CAPABILITY CHECK")
    print("-" * 65)

    print("\nAvailable")

    for field in capability.available:
        print(f"✓ {field}")

    if capability.unavailable:
        print("\nUnavailable")

        for field in capability.unavailable:
            print(f"✗ {field}")

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

    print("\n⚠ RISK ANALYSIS")
    print("-" * 65)

    for risk in risks:
        print(f"\n{risk.supplier_name} ({risk.supplier_id})")

        for item in risk.risks:
            print(f"   • {item}")

    print("\n❓ MISSING INFORMATION")
    print("-" * 65)

    if missing_information.items:
        for item in missing_information.items:
            print(f"• {item}")
    else:
        print("No missing information detected.")

    print("\n✅ VALIDATION")
    print("-" * 65)

    if validation.passed:
        print("PASSED")
    else:
        print("FAILED")

        for error in validation.errors:
            print(error)

    print("\n📜 EXECUTION TRACE")
    print("-" * 65)

    for step in trace.steps:
        print(f"✓ {step}")

    if matches:
        print("\n⚠ NEXT ACTION")
        print("-" * 65)

        print("\nRecommended Workflow")

        actions = [
            "Review the top-ranked suppliers.",
            "Confirm missing certification requirements.",
            "Obtain procurement manager approval.",
            "Generate procurement enquiry email.",
            "Send enquiry to selected suppliers.",
            "Await supplier quotations."
        ]

        for i, action in enumerate(actions, start=1):
            print(f"{i}. {action}")

        print("\nCurrent Status")
        print("⏳ Awaiting Human Approval")


    print("=" * 65)


if __name__ == "__main__":

    from agent.controller import run_agent

    request = """
Find three suppliers from South India providing food-grade biodegradable containers with minimum capacity of 10000 units and delivery within 30 days.
"""

    result = run_agent(request)

    generate_report(
        result["requirement"],
        result["plan"],
        result["matches"],
        result["validation"],
        result["summary"],
        result["risks"],
        result["missing_information"],
        result["capability"],
        result["trace"],
    )


    if not result["matches"]:
        print("\nNo suppliers matched the requested criteria.")

        print("-" * 65)
        print("Try one or more of the following:")
        print("1. Use a broader product category.")
        print("2. Reduce capacity requirements.")
        print("3. Increase the delivery window.")
        print("4. Expand the search location.")
        print("5. Add more suppliers to the database.")

        print("\nSTATUS")
        print("Workflow Completed")

    else:
        approved = request_human_approval()

        if approved:
            print("\n✅ Recommendations Approved")
            print("\nGenerating procurement enquiry...\n")

            supplier = result["suppliers"][0]

            email = generate_procurement_email(
                result["requirement"],
                supplier
            )
            print(email)
        else:
            print("\n❌ Recommendations Rejected")
            print("\nWorkflow terminated.")

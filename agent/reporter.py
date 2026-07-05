from models.requirement import Requirement
from models.plan import ExecutionPlan
from models.match import Match
from models.validation import ValidationResult
from models.search_summary import SearchSummary
from agent.human_approval import request_human_approval
from agent.email_generator import generate_procurement_email

ENTITY_LABELS = {
    "supplier": "Suppliers",
    "professional": "Professionals",
    "opportunity": "Opportunities",
}


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

    titles = {
        "supplier": "SUPROC AI PROCUREMENT AGENT",
        "professional": "SUPROC PROFESSIONAL MATCHING AGENT",
        "opportunity": "SUPROC OPPORTUNITY DISCOVERY AGENT",
    }

    print("=" * 65)
    print(f"        {titles[requirement.entity_type]}")
    print("=" * 65)

    print("\n📋 BUSINESS REQUIREMENT")
    print("-" * 65)

    print("Objective:")
    print(requirement.objective)

    print("\nEntity Type:")
    print(requirement.entity_type)

    print("\nHard Constraints")

    if requirement.entity_type == "supplier":

        print(f"Product : {requirement.hard_constraints.product_category}")

        capacity = requirement.hard_constraints.minimum_capacity
        delivery = requirement.hard_constraints.maximum_delivery_days

        print(f"Capacity: {capacity if capacity is not None else 'Not specified'}")

        print(
            f"Delivery: {str(delivery) + ' days' if delivery is not None else 'Not specified'}"
        )

    elif requirement.entity_type == "professional":

        print(f"Role      : {requirement.hard_constraints.role}")
        print(f"Skills    : {requirement.hard_constraints.skills}")
        print(f"Experience: {requirement.hard_constraints.minimum_experience}")

    elif requirement.entity_type == "opportunity":

        industry = requirement.hard_constraints.industry

        if industry:
            industry = industry.title()

        print(f"Industry : {industry}")
        print(f"Budget   : {requirement.hard_constraints.minimum_budget}")
        priority = requirement.hard_constraints.priority

        print(
            f"Priority : {priority if priority else 'Not specified'}"
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

    label = ENTITY_LABELS[requirement.entity_type]

    print(f"Total {label:<22}: {summary.total_entities}")
    print(f"Location Matches       : {summary.location_matches}")

    if requirement.entity_type == "supplier":

        print(f"Product Matches        : {summary.match1}")

        if requirement.hard_constraints.minimum_capacity is None:
            print("Capacity Matches       : Not Applied")
        else:
            print(f"Capacity Matches       : {summary.match2}")

        if requirement.hard_constraints.maximum_delivery_days is None:
            print("Delivery Matches       : Not Applied")
        else:
            print(f"Delivery Matches       : {summary.match3}")

    elif requirement.entity_type == "professional":

        print(f"Role Matches           : {summary.match1}")

        if requirement.hard_constraints.skills:
            print(f"Skills Matches         : {summary.match2}")
        else:
            print("Skills Matches         : Not Applied")

        if requirement.hard_constraints.minimum_experience is not None:
            print(f"Experience Matches     : {summary.match3}")
        else:
            print("Experience Matches     : Not Applied")

    else:   # opportunity

        print(f"Industry Matches       : {summary.match1}")
        print(f"Budget Matches         : {summary.match2}")
        print(f"Priority Matches       : {summary.match3}")

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

    print(f"\n🏆 RECOMMENDED {ENTITY_LABELS[requirement.entity_type].upper()}")
    print("-" * 65)

    for i, match in enumerate(matches, start=1):

        print(f"\n{i}. {match.entity_name}")
        print(f"{requirement.entity_type.capitalize()} ID : {match.entity_id}")
        print(f"Score       : {match.score}")

        print("\nScore Breakdown")

        for key, value in match.breakdown.items():
            print(f"   {key:12} {value}")

        print("\nEvidence")

        for item in match.evidence:
            print(f"   ✓ {item}")

        print("-" * 65)

    if requirement.entity_type == "supplier":

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

        if requirement.entity_type == "supplier":

            actions = [
                "Review the top-ranked suppliers.",
                "Confirm missing certification requirements.",
                "Obtain procurement manager approval.",
                "Generate procurement enquiry email.",
                "Send enquiry to selected suppliers.",
                "Await supplier quotations."
            ]

        elif requirement.entity_type == "professional":

            actions = [
                "Review the recommended professionals.",
                "Schedule interviews.",
                "Verify experience.",
                "Contact shortlisted professionals."
            ]

        else:

            actions = [
                "Review matching opportunities.",
                "Check eligibility.",
                "Prepare proposal.",
                "Submit application."
            ]

        for i, action in enumerate(actions, start=1):
            print(f"{i}. {action}")

        print("\nCurrent Status")
        print("⏳ Awaiting Human Approval")


    print("=" * 65)


if __name__ == "__main__":

    from agent.controller import run_agent

    request = """
Find food packaging opportunities in South India.
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
        entity_label = ENTITY_LABELS[result["requirement"].entity_type].lower()

        print(f"\nNo {entity_label} matched the requested criteria.")

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

            if result["requirement"].entity_type == "supplier":

                print("\nGenerating procurement enquiry...\n")

                from tools.entity_details import get_entity_details

                match = result["matches"][0]

                supplier = get_entity_details(match.entity_id)

                email = generate_procurement_email(
                    result["requirement"],
                    supplier
                )

                print(email)

            elif result["requirement"].entity_type == "professional":

                print("\nRecommended next step:")
                print("Contact the shortlisted professionals and schedule interviews.")

            elif result["requirement"].entity_type == "opportunity":

                print("\nRecommended next step:")
                print("Review the opportunity details and prepare an application.")

        else:

            print("\n❌ Recommendations Rejected")
            print("\nWorkflow terminated.")

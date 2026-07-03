from models.requirement import Requirement


from models.requirement import Requirement


def generate_procurement_email(requirement: Requirement, supplier: dict):

    product = requirement.hard_constraints.product_category
    quantity = requirement.hard_constraints.minimum_capacity
    delivery = requirement.hard_constraints.maximum_delivery_days
    location = supplier["state"]

    email = f"""
=================================================================
                    PROCUREMENT ENQUIRY
=================================================================

Subject: Procurement Enquiry – {product.title()}

To: Sales Team, {supplier['name']}

Dear {supplier['name']} Team,

We are currently evaluating suppliers for an upcoming procurement
requirement and would like to request a quotation.

-------------------------------------------------------------
REQUIREMENT DETAILS
-------------------------------------------------------------
Product            : {product.title()}
Required Quantity  : {quantity:,} units
Delivery Window    : Within {delivery} days
Preferred Region   : {location}

-------------------------------------------------------------
REQUESTED INFORMATION
-------------------------------------------------------------
• Product catalogue / specification sheet
• Commercial quotation (pricing)
• Available certifications
• Monthly production capacity
• Estimated lead time
• Payment terms
• Stock availability

-------------------------------------------------------------
NEXT STEPS
-------------------------------------------------------------
If your products meet the above requirements, kindly share the
requested information at your earliest convenience.

We appreciate your time and look forward to your response.

Best Regards,

Procurement Team
AI Procurement Agent
=================================================================
"""

    return email



if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from agent.executor import execute_search

    request = """
Need food-grade biodegradable containers
10000 units
within 30 days.
"""

    requirement = normalize_requirement(parse_requirement(request))

    supplier = execute_search(requirement)[0]

    print(generate_procurement_email(requirement, supplier))
from models.requirement import Requirement
from agent.security import is_safe_supplier


def filter_by_constraints(suppliers: list[dict], requirement: Requirement):

    filtered = []

    for supplier in suppliers:

        # Minimum Capacity
        if (
            requirement.hard_constraints.minimum_capacity is not None
            and supplier["monthly_capacity"] < requirement.hard_constraints.minimum_capacity
        ):
            continue

        # Maximum Delivery
        if (
            requirement.hard_constraints.maximum_delivery_days is not None
            and supplier["delivery_days"] > requirement.hard_constraints.maximum_delivery_days
        ):
            continue

        # Certifications
        if requirement.hard_constraints.certifications:

            supplier_certs = supplier["certifications"].lower()

            missing = False

            for cert in requirement.hard_constraints.certifications:
                if cert.lower() not in supplier_certs:
                    missing = True
                    break

            if missing:
                continue
        
        if not is_safe_supplier(supplier):
          continue

        filtered.append(supplier)

    return filtered
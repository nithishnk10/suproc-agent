from models.requirement import Requirement


def filter_opportunities(results, requirement: Requirement):

    filtered = []

    locations = requirement.hard_constraints.locations
    industry = requirement.hard_constraints.industry
    minimum_budget = requirement.hard_constraints.minimum_budget
    priority = requirement.hard_constraints.priority

    for opportunity in results:


        if locations and opportunity["location"] not in locations:
            continue

        if industry:

          required = industry.lower().strip()
          available = opportunity["industry"].lower().strip()

          if required not in available:
              continue

        if minimum_budget is not None:
            if opportunity["budget"] < minimum_budget:
                continue

        if priority and priority.lower() != "default":

            if opportunity["priority"].lower().strip() != priority.lower().strip():
                continue
          
        # Only recommend active opportunities

        status = opportunity["status"].lower().strip()

        if status == "closed":
            continue

        

        filtered.append(opportunity)

    return filtered
from models.requirement import Requirement


def filter_professionals(results, requirement: Requirement):

    filtered = []

    role = requirement.hard_constraints.role
    skills = requirement.hard_constraints.skills
    locations = requirement.hard_constraints.locations
    minimum_experience = requirement.hard_constraints.minimum_experience

    for professional in results:

        if locations and professional["state"] not in locations:
            continue

        if role:

          requested_words = role.lower().split()
          professional_role = professional["role"].lower()

          if not any(word in professional_role for word in requested_words):
              continue

        if minimum_experience is not None:
            if professional["experience_years"] < minimum_experience:
                continue

        if skills:
            professional_skills = professional["skills"].lower()

            if not all(
                skill.lower() in professional_skills
                for skill in skills
            ):
                continue

        filtered.append(professional)

    return filtered
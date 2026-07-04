from models.requirement import Requirement


def filter_professionals(
    professionals: list[dict],
    requirement: Requirement,
):

    filtered = []

    for professional in professionals:

        # Location filter
        if (
            requirement.hard_constraints.locations
            and professional["state"] not in requirement.hard_constraints.locations
        ):
            continue

        filtered.append(professional)

    return filtered


if __name__ == "__main__":

    from agent.parser import parse_requirement
    from agent.normalizer import normalize_requirement
    from tools.search import search_entities

    request = """
Find procurement professionals in Karnataka.
"""

    req = parse_requirement(request)
    req = normalize_requirement(req)

    professionals = search_entities(
        entity_type="professional",
        state="Karnataka"
    )

    results = filter_professionals(
        professionals,
        req
    )

    print(f"\nFound {len(results)} professionals\n")

    for p in results:
        print(
            p["professional_id"],
            p["name"],
            p["state"]
        )
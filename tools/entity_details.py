from tools.search import search_entities


def get_entity_details(supplier_id: str):

    suppliers = search_entities()

    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            return supplier

    return None
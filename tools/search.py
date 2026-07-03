from database.database_manager import DatabaseManager


def search_entities(
    entity_type="supplier",
    state=None,
    product_category=None,
    certification=None
):
    """
    Search entities from the local database.
    Currently supports suppliers.
    """

    db = DatabaseManager()
    db.connect()

    query = "SELECT * FROM suppliers WHERE 1=1"
    params = []

    if state:
        query += " AND state = ?"
        params.append(state)

    if product_category:
        query += " AND LOWER(product_category) = LOWER(?)"
        params.append(product_category)

    if certification:
        query += " AND certifications LIKE ?"
        params.append(f"%{certification}%")

    rows = db.fetchall(query, tuple(params))
    db.close()

    return [dict(row) for row in rows]

if __name__ == "__main__":

    suppliers = search_entities(
        product_category="Food-grade biodegradable containers"
    )

    print(f"Found {len(suppliers)} suppliers\n")

    for supplier in suppliers:
        print(
            supplier["supplier_id"],
            supplier["state"],
            supplier["product_category"]
        )
from database.database_manager import DatabaseManager


TABLE_MAP = {
    "supplier": "suppliers",
    "professional": "professionals",
    "opportunity": "opportunities",
}


def search_entities(
    entity_type="supplier",
    state=None,
    product_category=None,
    certification=None,
    skills=None,
    category=None,
):
    """
    Generic search across suppliers, professionals and opportunities.
    """

    db = DatabaseManager()
    db.connect()

    table = TABLE_MAP.get(entity_type)

    if table is None:
        db.close()
        raise ValueError(f"Unsupported entity type: {entity_type}")

    query = f"SELECT * FROM {table} WHERE 1=1"
    params = []

    # ---------------- Suppliers ----------------

    if entity_type == "supplier":

        if state:
            query += " AND state = ?"
            params.append(state)

        if product_category:
            normalized_product = (
                product_category.lower()
                .replace("-", " ")
                .strip()
            )

            query += """
            AND LOWER(REPLACE(product_category, '-', ' ')) LIKE ?
            """

            params.append(f"%{normalized_product}%")

        if certification:
            query += " AND certifications LIKE ?"
            params.append(f"%{certification}%")

    # ---------------- Professionals ----------------

    elif entity_type == "professional":

        if state:
            query += " AND state = ?"
            params.append(state)

        if skills:
            query += " AND LOWER(skills) LIKE ?"
            params.append(f"%{skills.lower()}%")

    # ---------------- Opportunities ----------------

    elif entity_type == "opportunity":

        if category:
            query += " AND LOWER(category) LIKE ?"
            params.append(f"%{category.lower()}%")

        if state:
            query += " AND LOWER(location) LIKE ?"
            params.append(f"%{state.lower()}%")

    rows = db.fetchall(query, tuple(params))

    db.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":

    print("\nSuppliers")
    print(search_entities(
        entity_type="supplier",
        product_category="biodegradable"
    ))

    print("\nProfessionals")
    print(search_entities(
        entity_type="professional",
        skills="Supply"
    ))

    print("\nOpportunities")
    print(search_entities(
        entity_type="opportunity"
    ))
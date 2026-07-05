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
    role=None,
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

            words = (
                product_category.lower()
                .replace("-", " ")
                .split()
            )

            for word in words:
                query += """
                AND LOWER(REPLACE(product_category,'-',' ')) LIKE ?
                """
                params.append(f"%{word}%")

        if certification:
            query += " AND certifications LIKE ?"
            params.append(f"%{certification}%")

    # ---------------- Professionals ----------------

    elif entity_type == "professional":

        if state:
            query += " AND state = ?"
            params.append(state)

        if role:
            query += " AND LOWER(role) LIKE ?"
            params.append(f"%{role.lower()}%")

        if skills:
            query += " AND LOWER(skills) LIKE ?"
            params.append(f"%{skills.lower()}%")

    # ---------------- Opportunities ----------------

    # ---------------- Opportunities ----------------

    elif entity_type == "opportunity":

        if state:
            query += " AND location = ?"
            params.append(state)

        if product_category:
            query += " AND LOWER(industry) LIKE ?"
            params.append(f"%{product_category.lower()}%")

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
from database.database_manager import DatabaseManager
import random
from datetime import datetime


from utils.constants import (
    STATES,
    CITIES,
    PRODUCTS,
    CERTIFICATIONS,
    INDUSTRIES,
    SKILLS,
    AVAILABILITY
)

# Make data deterministic
random.seed(42)



COMPANY_PREFIXES = [
    "Green",
    "Eco",
    "Nature",
    "Bio",
    "Fresh",
    "Pure",
    "Earth",
    "Smart",
    "Prime",
    "Nova"
]

COMPANY_SUFFIXES = [
    "Pack",
    "Containers",
    "Solutions",
    "Industries",
    "Supplies",
    "Products"
]

def generate_supplier_name():
    return (
        random.choice(COMPANY_PREFIXES)
        + " "
        + random.choice(COMPANY_SUFFIXES)
    )

def random_city_state():
    state = random.choice(STATES)
    city = random.choice(CITIES[state])
    return city, state

def timestamp():
    return datetime.now().isoformat()

def generate_supplier(index: int):
    city, state = random_city_state()

    supplier = {
        "supplier_id": f"SUP-{index:03}",
        "name": generate_supplier_name(),
        "city": city,
        "state": state,
        "product_category": random.choice(PRODUCTS),
        "certifications": "|".join(random.sample(CERTIFICATIONS, 2)),
        "monthly_capacity": random.randint(10000, 50000),
        "delivery_days": random.randint(7, 30),
        "rating": round(random.uniform(4.0, 5.0), 1),
        "availability": random.choice(AVAILABILITY),
        "sustainability_score": random.randint(70, 100),
        "startup_friendly": random.choice([0, 1]),
        "previous_projects": random.randint(10, 250),
        "description": "Reliable supplier",
        "created_at": timestamp(),
        "updated_at": timestamp(),
    }

    return supplier

def seed_suppliers(db):
    """Generate and insert supplier records into the database."""

    db.clear_table("suppliers")

    # Clear existing supplier data
    db.execute("DELETE FROM suppliers")

    for i in range(1, 31):
        supplier = generate_supplier(i)

        db.execute("""
        INSERT INTO suppliers (
            supplier_id,
            name,
            city,
            state,
            product_category,
            certifications,
            monthly_capacity,
            delivery_days,
            rating,
            availability,
            sustainability_score,
            startup_friendly,
            previous_projects,
            description,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            supplier["supplier_id"],
            supplier["name"],
            supplier["city"],
            supplier["state"],
            supplier["product_category"],
            supplier["certifications"],
            supplier["monthly_capacity"],
            supplier["delivery_days"],
            supplier["rating"],
            supplier["availability"],
            supplier["sustainability_score"],
            supplier["startup_friendly"],
            supplier["previous_projects"],
            supplier["description"],
            supplier["created_at"],
            supplier["updated_at"]
        ))

    print("✅ Inserted 30 suppliers")


def main():
    db = DatabaseManager()

    db.connect()

    seed_suppliers(db)

    db.commit()

    db.close()

    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    main()

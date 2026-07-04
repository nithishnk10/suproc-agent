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
    AVAILABILITY,

    PROFESSIONAL_NAMES,
    PROFESSIONAL_ROLES,

    BUSINESS_NAMES,

    OPPORTUNITY_TITLES,
    OPPORTUNITY_CATEGORIES,

    REQUEST_STATUS,

    INTERACTION_OUTCOMES
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

# --------------------------------------------------
# PROFESSIONAL
# --------------------------------------------------

def generate_professional(index: int):
    city, state = random_city_state()

    return {
        "professional_id": f"PRO-{index:03}",
        "name": PROFESSIONAL_NAMES[(index - 1) % len(PROFESSIONAL_NAMES)],
        "role": random.choice(PROFESSIONAL_ROLES),
        "skills": "|".join(random.sample(SKILLS, 3)),
        "certifications": "|".join(random.sample(CERTIFICATIONS, 2)),
        "preferred_industry": random.choice(INDUSTRIES),
        "experience_years": random.randint(2, 15),
        "hourly_rate": random.randint(1500, 6000),
        "remote_available": random.choice([0, 1]),
        "city": city,
        "state": state,
        "availability": random.choice(AVAILABILITY),
        "rating": round(random.uniform(4.0, 5.0), 1),
        "created_at": timestamp(),
        "updated_at": timestamp(),
    }

# --------------------------------------------------
# BUSINESS
# --------------------------------------------------

def generate_business(index: int):
    city, state = random_city_state()

    return {
        "business_id": f"BUS-{index:03}",
        "company_name": random.choice(BUSINESS_NAMES),
        "industry": random.choice(INDUSTRIES),
        "city": city,
        "state": state,
        "employee_count": random.randint(20, 500),
        "requirements": random.choice(PRODUCTS),
        "created_at": timestamp(),
        "updated_at": timestamp(),
    }


# --------------------------------------------------
# OPPORTUNITY
# --------------------------------------------------

def generate_opportunity(index: int):

    return {
        "opportunity_id": f"OPP-{index:03}",
        "title": random.choice(OPPORTUNITY_TITLES),
        "industry": random.choice(INDUSTRIES),
        "product_category": random.choice(PRODUCTS),
        "location": random.choice(STATES),
        "required_skills": "|".join(random.sample(SKILLS, 3)),
        "budget": random.randint(100000, 1000000),
        "deadline_days": random.randint(7, 90),
        "client_name": random.choice(BUSINESS_NAMES),
        "priority": random.choice(["High", "Medium", "Low"]),
        "status": random.choice(["Open", "In Review", "Closed"]),
        "description": "Business procurement opportunity",
        "created_at": timestamp(),
        "updated_at": timestamp(),
    }


# --------------------------------------------------
# PROCUREMENT REQUEST
# --------------------------------------------------

def generate_procurement_request(index: int):

    return {
        "request_id": f"REQ-{index:03}",
        "business_id": f"BUS-{random.randint(1,30):03}",
        "product_category": random.choice(PRODUCTS),
        "quantity": random.randint(5000,50000),
        "budget": random.randint(50000,1000000),
        "deadline": f"{random.randint(15,60)} days",
        "status": random.choice(REQUEST_STATUS),
        "created_at": timestamp(),
    }


# --------------------------------------------------
# INTERACTION
# --------------------------------------------------

def generate_interaction(index: int):

    return {
        "interaction_id": f"INT-{index:03}",
        "supplier_id": f"SUP-{random.randint(1,30):03}",
        "interaction_date": timestamp(),
        "outcome": random.choice(INTERACTION_OUTCOMES),
        "satisfaction_score": random.randint(1,5),
        "notes": "Historical supplier interaction",
    }


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

def seed_professionals(db):
    """Generate and insert professional records."""

    db.clear_table("professionals")

    for i in range(1, 16):

        professional = generate_professional(i)

        db.execute("""
        INSERT INTO professionals (
            professional_id,
            name,
            role,
            skills,
            certifications,
            preferred_industry,
            experience_years,
            hourly_rate,
            remote_available,
            city,
            state,
            availability,
            rating,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            professional["professional_id"],
            professional["name"],
            professional["role"],
            professional["skills"],
            professional["certifications"],
            professional["preferred_industry"],
            professional["experience_years"],
            professional["hourly_rate"],
            professional["remote_available"],
            professional["city"],
            professional["state"],
            professional["availability"],
            professional["rating"],
            professional["created_at"],
            professional["updated_at"],
        ))

    print("✅ Inserted 15 professionals")


def seed_opportunities(db):
    """Generate and insert opportunity records."""

    db.clear_table("opportunities")

    for i in range(1, 11):

        opportunity = generate_opportunity(i)

        db.execute("""
       INSERT INTO opportunities (
            opportunity_id,
            title,
            industry,
            product_category,
            location,
            required_skills,
            budget,
            deadline_days,
            client_name,
            priority,
            status,
            description,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            (
                opportunity["opportunity_id"],
                opportunity["title"],
                opportunity["industry"],
                opportunity["product_category"],
                opportunity["location"],
                opportunity["required_skills"],
                opportunity["budget"],
                opportunity["deadline_days"],
                opportunity["client_name"],
                opportunity["priority"],
                opportunity["status"],
                opportunity["description"],
                opportunity["created_at"],
                opportunity["updated_at"],
            )
        ))

    print("✅ Inserted 10 opportunities")


def main():

    db = DatabaseManager()

    db.connect()

    seed_suppliers(db)

    seed_professionals(db)

    seed_opportunities(db)

    db.commit()

    db.close()

    print("\n✅ Database seeded successfully!")


if __name__ == "__main__":
    main()

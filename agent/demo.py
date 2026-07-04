from tools.search import search_entities


def supplier_demo():
    print("\nSearching Suppliers...\n")

    suppliers = search_entities(
        entity_type="supplier",
        product_category="biodegradable"
    )

    if not suppliers:
        print("No suppliers found.")
        return

    for supplier in suppliers:
        print(f"""
Supplier : {supplier['name']}
ID       : {supplier['supplier_id']}
State    : {supplier['state']}
Product  : {supplier['product_category']}
Rating   : {supplier['rating']}
------------------------------
""")


def professional_demo():
    print("\nSearching Professionals...\n")

    professionals = search_entities(
        entity_type="professional",
        skills="Supply"
    )

    if not professionals:
        print("No professionals found.")
        return

    for professional in professionals:
        print(f"""
Professional : {professional['name']}
ID           : {professional['professional_id']}
State        : {professional['state']}
Skills       : {professional['skills']}
Experience   : {professional['experience_years']} years
Rating       : {professional['rating']}
------------------------------
""")


def opportunity_demo():
    print("\nSearching Opportunities...\n")

    opportunities = search_entities(
        entity_type="opportunity"
    )

    if not opportunities:
        print("No opportunities found.")
        return

    for opportunity in opportunities:
        print(f"""
Opportunity : {opportunity['title']}
ID          : {opportunity['opportunity_id']}
Category    : {opportunity['category']}
Location    : {opportunity['location']}
Budget      : ₹{opportunity['budget']}
Deadline    : {opportunity['deadline']}
------------------------------
""")


def main():

    while True:

        print("""
====================================
     SUPROC AI BUSINESS AGENT
====================================

1. Supplier Search

2. Professional Search

3. Opportunity Search

4. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            supplier_demo()

        elif choice == "2":
            professional_demo()

        elif choice == "3":
            opportunity_demo()

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
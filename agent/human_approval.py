def request_human_approval():

  
    while True:

        choice = input("\nApprove recommendations? (y/n): ").strip().lower()

        if choice == "y":
            print("\n✅ Recommendations Approved")
            return True

        if choice == "n":
            print("\n❌ Recommendations Rejected")
            return False

        print("Please enter y or n.")
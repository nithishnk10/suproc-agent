def request_human_approval():

  
    while True:

        choice = input("\nApprove recommendations? (y/n): ").strip().lower()

        if choice == "y":
            return True

        if choice == "n":
            return False

        print("Please enter y or n.")
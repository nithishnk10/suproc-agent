from models.validation import ValidationResult

MAX_RETRIES = 3


def correction_loop(
    validation: ValidationResult,
    search_callback,
):
    """
    Retry the search when validation fails.
    """

    attempts = 0

    while not validation.passed and attempts < MAX_RETRIES:

        print(f"Correction Attempt {attempts + 1}")

        validation = search_callback()

        attempts += 1

    return validation

if __name__ == "__main__":

    from models.validation import ValidationResult

    def fake_retry():
        print("Searching again...")

        return ValidationResult(
            passed=True,
            errors=[]
        )

    validation = ValidationResult(
        passed=False,
        errors=["Delivery failed"]
    )

    result = correction_loop(
        validation,
        fake_retry
    )

    print(result.model_dump_json(indent=2))
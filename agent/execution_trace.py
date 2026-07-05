from models.execution_trace import ExecutionTrace


def build_execution_trace(entity_type):

    steps = [
        "Requirement parsed",
        "Requirement normalized",
        "Execution plan generated",
    ]

    if entity_type == "supplier":
        steps.extend([
            "Supplier search completed",
            "Suppliers scored",
        ])

    elif entity_type == "professional":
        steps.extend([
            "Professional search completed",
            "Professionals scored",
        ])

    else:
        steps.extend([
            "Opportunity search completed",
            "Opportunities scored",
        ])

    steps.extend([
        "Evidence generated",
        "Risk analysis completed",
        "Missing information analyzed",
        "Dataset capability checked",
        "Validation completed",
        "Report generated",
    ])

    return ExecutionTrace(steps=steps)


if __name__ == "__main__":
    trace = build_execution_trace()

    print(trace.model_dump_json(indent=2))
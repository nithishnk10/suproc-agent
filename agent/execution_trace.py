from models.execution_trace import ExecutionTrace


def build_execution_trace():

    return ExecutionTrace(
        steps=[
            "Requirement parsed",
            "Requirement normalized",
            "Execution plan generated",
            "Supplier search completed",
            "Suppliers scored",
            "Evidence generated",
            "Risk analysis completed",
            "Missing information analyzed",
            "Dataset capability checked",
            "Validation completed",
            "Report generated"
        ]
    )


if __name__ == "__main__":
    trace = build_execution_trace()

    print(trace.model_dump_json(indent=2))
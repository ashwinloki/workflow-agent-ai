from backend.planner.workflow_planner import create_workflow


def test_rule_based_workflow_creation():
    objective = "Summarize the document and identify risks"

    tasks = create_workflow(objective)

    assert "summarize" in tasks
    assert "identify_risks" in tasks
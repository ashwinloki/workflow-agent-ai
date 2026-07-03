import json

from backend.services.llm_service import generate_completion


ALLOWED_TASKS = {
    "summarize",
    "extract_action_items",
    "identify_risks",
    "draft_email",
    "generate_report",
}


def create_workflow(objective: str) -> list[str]:
    """Create a workflow using simple keyword matching."""

    objective = objective.lower()
    tasks = []

    if "summary" in objective or "summarize" in objective:
        tasks.append("summarize")

    if "action" in objective or "task" in objective:
        tasks.append("extract_action_items")

    if "risk" in objective:
        tasks.append("identify_risks")

    if "email" in objective or "mail" in objective:
        tasks.append("draft_email")

    if "report" in objective:
        tasks.append("generate_report")

    return tasks


async def create_ai_workflow(objective: str) -> list[str]:
    """Use an LLM to convert a user objective into workflow tasks."""

    system_prompt = """
You are a workflow planning assistant.

Analyze the user's objective and return only a JSON array containing
the required workflow tasks.

Allowed tasks:
- summarize
- extract_action_items
- identify_risks
- draft_email
- generate_report

Rules:
- Select only tasks explicitly or clearly requested by the user.
- Do not infer a task merely because its keyword appears as the name
  of an input document.
- Return only valid JSON.
- Do not include markdown.
- Do not include explanations.
"""

    response = await generate_completion(
        system_prompt=system_prompt,
        user_prompt=objective,
    )

    try:
        tasks = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError("LLM returned invalid JSON") from error

    if not isinstance(tasks, list):
        raise ValueError("LLM response must be a list of tasks")

    invalid_tasks = [
        task
        for task in tasks
        if task not in ALLOWED_TASKS
    ]

    if invalid_tasks:
        raise ValueError(
            f"LLM returned unsupported tasks: {invalid_tasks}"
        )

    return tasks
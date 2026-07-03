from backend.services.llm_service import generate_completion


# --------------------------------------------------
# 1. SUMMARY TASK
# --------------------------------------------------

async def execute_summary(content: str) -> str:
    """Generate a concise summary of the provided content."""

    system_prompt = """
You are a professional business analyst.

Summarize the provided content clearly and concisely.

Focus on:
- main objective
- important information
- key decisions
- important conclusions

Do not invent information that is not present in the content.
"""

    return await generate_completion(
        system_prompt=system_prompt,
        user_prompt=content,
    )


# --------------------------------------------------
# 2. ACTION ITEMS TASK
# --------------------------------------------------

async def execute_action_items(content: str) -> str:
    """Extract actionable tasks from the provided content."""

    system_prompt = """
You are a project management assistant.

Extract actionable tasks from the provided content.

For each action item, identify when available:
- task
- owner
- deadline
- priority

Do not invent missing information.
Clearly state when an owner or deadline is not specified.
"""

    return await generate_completion(
        system_prompt=system_prompt,
        user_prompt=content,
    )


# --------------------------------------------------
# 3. RISK ANALYSIS TASK
# --------------------------------------------------

async def execute_risk_analysis(content: str) -> str:
    """Identify risks and blockers from the provided content."""

    system_prompt = """
You are a business risk analyst.

Analyze the provided content and identify:
- risks
- blockers
- dependencies
- possible impact

Only identify risks supported by the provided content.
Do not invent unsupported risks.
"""

    return await generate_completion(
        system_prompt=system_prompt,
        user_prompt=content,
    )


# --------------------------------------------------
# 4. EMAIL DRAFT TASK
# --------------------------------------------------

async def execute_email_draft(content: str) -> str:
    """Draft a professional follow-up email."""

    system_prompt = """
You are a professional business communication assistant.

Using only the provided content, draft a concise professional
follow-up email.

Include:
- a clear subject
- important updates
- required actions
- professional closing

Do not invent names, deadlines, or commitments.
"""

    return await generate_completion(
        system_prompt=system_prompt,
        user_prompt=content,
    )


# --------------------------------------------------
# 5. REPORT GENERATION TASK
# --------------------------------------------------

async def execute_report(content: str) -> str:
    """Generate a structured business report."""

    system_prompt = """
You are a professional business analyst.

Convert the provided content into a structured report containing:
- Executive Summary
- Key Updates
- Action Items
- Risks and Blockers
- Recommended Next Steps

Do not invent information that is not present in the content.
"""

    return await generate_completion(
        system_prompt=system_prompt,
        user_prompt=content,
    )


# --------------------------------------------------
# TASK REGISTRY
# --------------------------------------------------

TASK_REGISTRY = {
    "summarize": execute_summary,
    "extract_action_items": execute_action_items,
    "identify_risks": execute_risk_analysis,
    "draft_email": execute_email_draft,
    "generate_report": execute_report,
}


# --------------------------------------------------
# WORKFLOW EXECUTOR
# --------------------------------------------------

async def execute_workflow(
    tasks: list[str],
    content: str,
) -> dict[str, str]:
    """Execute registered workflow tasks and collect their results."""

    results = {}

    for task in tasks:

        task_function = TASK_REGISTRY.get(task)

        if task_function is None:
            results[task] = "Unsupported task"
            continue

        results[task] = await task_function(content)

    return results
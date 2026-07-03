from backend.executor.task_executor import execute_workflow
from backend.models.workflow import (
    WorkflowRequest,
    WorkflowResponse,
    WorkflowExecutionRequest,
    WorkflowExecutionResponse,
    AgentRequest,
    AgentResponse,
)
from backend.services.llm_service import generate_completion
from backend.models.workflow import WorkflowRequest, WorkflowResponse
from backend.planner.workflow_planner import create_workflow
from fastapi import APIRouter, HTTPException
from backend.services.llm_service import LLMServiceError
from backend.planner.workflow_planner import (
    create_workflow,
    create_ai_workflow,
)

router = APIRouter()


@router.get("/")
def read_root() -> dict[str, str]:
    """Return a confirmation that the backend is running."""
    return {"message": "Workflow Agent AI Backend Running"}


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return the current health status of the API."""
    return {"status": "healthy"}

@router.post("/workflow", response_model=WorkflowResponse)
def generate_workflow(request: WorkflowRequest) -> WorkflowResponse:
    tasks = create_workflow(request.objective)

    return WorkflowResponse(
        objective=request.objective,
        tasks=tasks,
    )


@router.post("/workflow/ai", response_model=WorkflowResponse)
async def generate_ai_workflow(
    request: WorkflowRequest,
) -> WorkflowResponse:

    tasks = await create_ai_workflow(request.objective)

    return WorkflowResponse(
        objective=request.objective,
        tasks=tasks,
    )
@router.post(
    "/workflow/execute",
    response_model=WorkflowExecutionResponse,
)
async def run_workflow(
    request: WorkflowExecutionRequest,
) -> WorkflowExecutionResponse:

    results = await execute_workflow(
        tasks=request.tasks,
        content=request.content,
    )

    return WorkflowExecutionResponse(
        results=results,
    )

@router.post(
    "/agent/run",
    response_model=AgentResponse,
)
async def run_agent(
    request: AgentRequest,
) -> AgentResponse:
    """Plan and execute an AI workflow."""

    try:
        tasks = await create_ai_workflow(
            request.objective
        )

        results = await execute_workflow(
            tasks=tasks,
            content=request.content,
        )

        return AgentResponse(
            objective=request.objective,
            tasks=tasks,
            results=results,
        )

    except LLMServiceError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error
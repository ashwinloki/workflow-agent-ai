from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    objective: str


class WorkflowResponse(BaseModel):
    objective: str
    tasks: list[str]


class WorkflowExecutionRequest(BaseModel):
    tasks: list[str]
    content: str


class WorkflowExecutionResponse(BaseModel):
    results: dict[str, str]


class AgentRequest(BaseModel):
    objective: str = Field(
        min_length=5,
        max_length=500,
    )

    content: str = Field(
        min_length=20,
        max_length=20_000,
    )


class AgentResponse(BaseModel):
    objective: str
    tasks: list[str]
    results: dict[str, str]
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from backend.main import app
from backend.services.llm_service import LLMServiceError

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }

def test_agent_run():
    mock_tasks = [
        "summarize",
        "identify_risks",
    ]

    mock_results = {
        "summarize": "Test summary",
        "identify_risks": "Test risk analysis",
    }

    with patch(
        "backend.api.routes.create_ai_workflow",
        new=AsyncMock(return_value=mock_tasks),
    ), patch(
        "backend.api.routes.execute_workflow",
        new=AsyncMock(return_value=mock_results),
    ):
        response = client.post(
            "/agent/run",
            json={
                "objective": "Summarize the update and identify risks",
                "content": (
                    "The project authentication module is complete, "
                    "but payment integration remains blocked because "
                    "required API credentials are still unavailable."
                ),
            },
        )

    assert response.status_code == 200

    assert response.json() == {
        "objective": "Summarize the update and identify risks",
        "tasks": mock_tasks,
        "results": mock_results,
    }

def test_agent_run_llm_failure():
    with patch(
        "backend.api.routes.create_ai_workflow",
        new=AsyncMock(
            side_effect=LLMServiceError(
                "Unable to connect to the LLM service."
            )
        ),
    ):
        response = client.post(
            "/agent/run",
            json={
                "objective": "Summarize this project update",
                "content": (
                    "The authentication module is complete and "
                    "testing is scheduled to begin next Monday."
                ),
            },
        )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Unable to connect to the LLM service."
    }


def test_agent_run_invalid_planner_output():
    with patch(
        "backend.api.routes.create_ai_workflow",
        new=AsyncMock(
            side_effect=ValueError(
                "LLM returned invalid JSON"
            )
        ),
    ):
        response = client.post(
            "/agent/run",
            json={
                "objective": "Summarize this project update",
                "content": (
                    "The authentication module is complete and "
                    "testing is scheduled to begin next Monday."
                ),
            },
        )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "LLM returned invalid JSON"
    }
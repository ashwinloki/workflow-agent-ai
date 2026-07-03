import httpx

from backend.config.settings import OPENROUTER_API_KEY


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMServiceError(Exception):
    """Raised when communication with the LLM service fails."""


async def generate_completion(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Send prompts to the LLM and return the generated text."""

    if not OPENROUTER_API_KEY:
        raise LLMServiceError(
            "OpenRouter API key is not configured."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
            )

            response.raise_for_status()

    except httpx.TimeoutException as error:
        raise LLMServiceError(
            "The LLM request timed out."
        ) from error

    except httpx.HTTPStatusError as error:
        raise LLMServiceError(
            f"LLM API returned status code "
            f"{error.response.status_code}."
        ) from error

    except httpx.RequestError as error:
        raise LLMServiceError(
            "Unable to connect to the LLM service."
        ) from error

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError) as error:
        raise LLMServiceError(
            "LLM API returned an unexpected response format."
        ) from error
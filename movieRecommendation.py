from typing import Optional, Literal
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys


# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)


# Pydantic model
class RecommendationResponse(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    genre: Literal["action", "comedy", "drama", "sci-fi", "thriller", "horror", "romance"]
    year: int = Field(..., ge=1900, le=2025)
    rating: float = Field(..., ge=0.0, le=10.0)
    synopsis: str = Field(..., min_length=10, max_length=500)

    director: Optional[str] = None
    lead_actor: Optional[str] = None
    recommended_for: Optional[Literal["family", "adults", "teens"]] = None


def get_recommendation(user_query: str) -> Optional[RecommendationResponse]:
    try:
        response = client.responses.parse(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "You are a movie recommendation expert. Provide accurate movie recommendations with ratings and details."
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            text_format=RecommendationResponse
        )
        return response.output_parsed

    except Exception as e:
        print(f"API error: {e}")
        return None


def validate_and_print(response: RecommendationResponse) -> None:
    if response is None:
        return

    try:
        validated = RecommendationResponse(**response.model_dump())
        print(validated.model_dump_json(indent=2))
    except ValidationError as e:
        print("Validation error:")
        for error in e.errors():
            field = ".".join(map(str, error["loc"]))
            print(f"{field}: {error['msg']}")


if __name__ == "__main__":

    queries = [
        "Recommend a sci-fi movie for a relaxing weekend",
        "I want an action thriller with a strong female lead",
        "Suggest a comedy suitable for family viewing"
    ]

    for query in queries:
        print(f"\nRequest: {query}")
        result = get_recommendation(query)
        validate_and_print(result)
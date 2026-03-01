from typing import List, Literal, Optional
from pydantic import BaseModel, Field, model_validator
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


# =========================
# Pydantic Models
# =========================

class Movie(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Movie title"
    )
    year: int = Field(
        ...,
        ge=1900,
        le=2025,
        description="Release year"
    )
    genre: Literal[
        "Action", "Comedy", "Drama", "Horror",
        "Sci-Fi", "Romance", "Thriller"
    ]
    rating: float = Field(
        ...,
        ge=0,
        le=10,
        description="IMDB-style rating (0-10)"
    )
    summary: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Short movie summary"
    )


class RecommendationResponse(BaseModel):
    user_query: str = Field(
        ...,
        min_length=5,
        max_length=300
    )
    mood: Literal["happy", "sad", "excited", "thoughtful"]

    recommendations: List[Movie] = Field(
        ...,
        min_length=1,
        max_length=5
    )

    total_recommendations: int = Field(
        ...,
        ge=1,
        le=5
    )

    note: Optional[str] = Field(
        default=None,
        max_length=200
    )

    # Cross-field validation
    @model_validator(mode="after")
    def validate_total_count(self):
        if self.total_recommendations != len(self.recommendations):
            raise ValueError(
                "total_recommendations must match number of recommendations"
            )
        return self


# =========================
# LLM Prompt
# =========================

prompt = """
User wants movie recommendations.

Return structured data matching this schema:
- user_query
- mood
- recommendations (1-5 movies)
- total_recommendations (must match actual count)
- optional note

User query:
"I feel nostalgic and want something emotional but inspiring."
"""


# =========================
# OpenAI Call
# =========================

client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input=prompt,
    text_format=RecommendationResponse
)

validated_output = response.output_parsed

print("\n=== VALIDATED OUTPUT ===")
print(validated_output.model_dump_json(indent=2))
from pydantic import BaseModel, Field


class ContentGeneration(BaseModel):
    url: str  # Example field for students to follow

    # TODO: Add a field for the new target audience
    target_audience: str

    # TODO: Add a field for the new tone
    new_tone: str= Field(..., description="Desired tone of the content")

    # TODO: Add a field for the language
    language: str
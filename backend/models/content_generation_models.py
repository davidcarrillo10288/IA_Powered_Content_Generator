from pydantic import BaseModel, Field

"""
BaseModel: Clase base de Pydantic. Cada clase que hereda de aquí puede validar tipos de datos.

Field(...): Permite agregar descripciones, valores por defecto, validaciones, etc.

"""
class ContentGenerationScript(BaseModel):
    content: str = Field(..., description="Contenido textual del reel")


# TODO: Define the ToneGenerationScript class with a field for the refined content
class ToneGenerationScript(BaseModel):
    refined_content: str = Field(..., description="Contenido refinado con el tono deseado")


# TODO: Define the ContentGeneration class with fields for URL, target audience, tone, and language
class ContentGeneration(BaseModel):
    url: str = Field(..., description="URL del contenido de origen")
    target_audience: str = Field(..., description="Audiencia objetivo")
    new_tone: str = Field(..., description="Tono del contenido (ej. profesional, casual, inspirador)")
    language: str = Field(..., description="Idioma del contenido")
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from prompts.tone_generator import GENERATE_REFINED_INFO
from prompts.content_generation_prompts import GENERATE_INFO
from scr.llm import GroqModelHandler
from models.content_generation_models import (
    ContentGenerationScript,
    ToneGenerationScript,
)

load_dotenv()

class ContentGenerator:

    def __init__(self):
        """Inicializa el generador de texto con un modelo LLM de Groq."""
        # TODO: Inicializar el manejador del modelo LLM de Groq
        self.llm = GroqModelHandler().get_llm()


    def create_parser(self):
        """Crea un parser para el contenido del reel."""
        # TODO: Crear un JsonOutputParser para ContentGenerationScript
        return JsonOutputParser(pydantic_object=ContentGenerationScript)


    def create_tone_parser(self):
        """Crea un parser para el tono del reel."""
        # TODO: Crear un JsonOutputParser para ToneGenerationScript
        return JsonOutputParser(pydantic_object=ToneGenerationScript)


    def create_script_chain(self, template, parser, input_variables):
        """Crea la cadena de resumen con un PromptTemplate y el parser definido."""
        # TODO: Crear un PromptTemplate con el template, input_variables y format_instructions
        reduce_prompt = PromptTemplate(
            template=template,
            input_variables=input_variables,
            partial_variables={'format_instructions': parser.get_format_instructions()}
        )
        # TODO: Crear un LLMChain con el modelo, el prompt y el parser
        
        # return LLMChain(model=self.llm, prompt=reduce_prompt, output_parser = parser)
        chain = reduce_prompt | self.llm | parser
        return chain


    def generate_text(self, info):
        """Genera un texto basado en la información de entrada."""
        parser = self.create_parser()
        content_chain = self.create_script_chain(
            template=GENERATE_INFO,
            parser=parser,
            input_variables=[
                "title",
                "price",
                "description",
                "available_sizes",
                "additional_info",
                "image_description",
            ],
        )

        return content_chain.invoke(
            {
                "title": info["title"],
                "price": info["price"],
                "description": info["description"],
                "available_sizes": info["available_sizes"],
                "additional_info": info["additional_info"],
                "image_description": info["image_description"],
            }
        )

    def apply_tone(self, previous_script, new_target_audience, new_tone, language):
        # TODO: Crear el parser para el tono
        parser_tone = self.create_tone_parser()
        # TODO: Crear la cadena de generación de tono
        generation_chain = self.create_script_chain(
            template = GENERATE_REFINED_INFO,
            parser = parser_tone,
            input_variables= [
                "previous_script",
                "new_target_audience",
                "new_tone",
                "language"
            ]
        )

        # TODO: Invocar la cadena con el script, audiencia, tono y lenguaje
        return generation_chain.invoke(
            {
                "previous_script": previous_script,
                "new_target_audience": new_target_audience,
                "new_tone": new_tone,
                "language": language
            }
        )

    def generate_content(self, metadata, new_target_audience, new_tone, language):
        # TODO: Generar el texto inicial
        generate_text = self.generate_text(metadata)
        # TODO: Aplicar el tono al texto generado
        return self.apply_tone(
            previous_script = generate_text['content'],
            new_target_audience = new_target_audience,
            new_tone = new_tone,
            language = language
        )
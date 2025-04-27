import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq


# Cargar variables del archivo .env
load_dotenv()

class GroqModelHandler:
    def __init__(self):
        # TODO: Load the Groq API key and model name from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME")

        # TODO: Validate if the API key is provided
        if not self.api_key:
            raise ValueError(
                "La API Key de Groq no está configurada en el archivo .env"
            )
        
        # Validar si el modelo está configurado
        if not self.model_name:
            print("No se encontró GROQ_MODEL_NAME en .env, usando modelo predeterminado 'llama3-8b-8192'")
            self.model_name = "llama-3.2-11b-vision-preview"

        # TODO: Initialize the Groq client and ChatGroq LLM
        self.client = Groq(api_key=self.api_key)
        self.llm = ChatGroq(groq_api_key = self.api_key, model = self.model_name)

    def get_client(self):
        # TODO: Return the Groq client instance
        return self.client

    def get_llm(self):
        # Example method for students to follow
        return self.llm
import requests
from models.content_generation_models import ContentGeneration
import streamlit as st

def compute_content(payload: ContentGeneration, server_url: str):
    try:
        # Send a POST request to the server with the payload
        r = requests.post(
            url=f"{server_url}/content_generator",
            json=payload.dict(),  # Convertir el modelo Pydantic a diccionario
            headers={"Content-Type": "application/json"}
        )
        
        # Raise an exception if the request fails
        r.raise_for_status()
        
        # Extract and return the generated content from the response
        response_data = r.json()
        print("🔵 Respuesta del servidor:", response_data)
        # generated_content = response_data.get("generated_content", {}).get("content")
        # Verificar si 'content' está presente en la respuesta
        if "generated_content" in response_data:
            generated_content = response_data["generated_content"]
        else:
            st.error("No se encontró la clave 'generated_content' en la respuesta del servidor.")
            generated_content = None

        return generated_content
    
    except requests.exceptions.RequestException as e:
        # Handle request exceptions and return an error message
        error_message = f"Error al comunicarse con el servidor: {str(e)}"
        st.error(error_message)
        return None
import os
import json
from dotenv import load_dotenv
import streamlit as st
from models.content_generation_models import ContentGeneration
from generate_content import compute_content

# Load environment variables from .env file
load_dotenv()

# Set the title of the Streamlit app
st.title("AI-Powered Reel Content Generator")

# Add a description for the app
st.write(
    """
Ingresa una url de un producto para crear el guion
"""
)

# Create input fields for URL, target audience, tone, and language
input_url = st.text_input("URL del producto", placeholder="https://www.falabella.com.pe/falabella-pe/product/...")
new_target_audience = st.selectbox(
    "Audiencia objetivo",
    ["Adultos", "Jóvenes", "Profesionales", "Familias", "Deportistas"]
)
new_tone = st.selectbox(
    "Tono del contenido",
    ["Informativo, dando bastantes detalles", "Casual y amigable", "Entusiasta", "Profesional", "Persuasivo"]
)
language = st.selectbox("Idioma", ["español", "english"])

# Add a button to trigger content generation
if st.button("Generar Guion"):
    if input_url and new_target_audience and new_tone and language:
        # Show a spinner while processing
        with st.spinner("Generando contenido..."):
            backend_url = os.getenv("BACKEND_URL", "http://backend:8004/content_generator")
            
            # Create a payload using the ContentGeneration model
            payload = ContentGeneration(
                url=input_url,
                target_audience=new_target_audience,  # Asumiendo que tu modelo usa target_audience
                new_tone=new_tone,  # Asumiendo que tu modelo usa tone
                language=language,
            )
            
            # Call the compute_content function to generate the script
            refined_script = compute_content(payload, backend_url)
            
            if refined_script:
                # Display the generated script
                st.header("Guion Finalizado")
                st.write(refined_script)
                
                # Prepare data for download
                script_data = {"content": refined_script}
                script_json = json.dumps(script_data, ensure_ascii=False, indent=2)
                
                # Add download button
                st.download_button(
                    label="Descargar Guion en JSON",
                    data=script_json,
                    file_name="guion_generado.json",
                    mime="application/json",
                )
            else:
                st.error("No se pudo generar el contenido. Por favor, intenta de nuevo.")
    else:
        # Show a warning if any input field is missing
        st.warning("Por favor, completa todos los campos.")
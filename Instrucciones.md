# Instrucciones para completar el proyecto

Este proyecto está diseñado para que los estudiantes completen ciertas partes del código con el fin de construir un generador de contenido automatizado utilizando modelos de lenguaje avanzados (LLMs). A continuación, se detallan las instrucciones para completar cada archivo.

## Estructura del Proyecto

El proyecto está dividido en dos partes principales: `backend` y `frontend`. Cada una de estas partes contiene varios archivos que deben ser completados por los estudiantes.

### Backend

#### Dockerfile
- **Descripción**: Este archivo define la configuración del contenedor Docker para el backend.
- **Tareas**:
  - Asegúrate de que el Dockerfile esté correctamente configurado para instalar las dependencias y ejecutar la aplicación FastAPI.

#### models/content_generation_models.py
- **Descripción**: Este archivo define los modelos Pydantic para la generación de contenido.
- **Tareas**:
  - Completa la clase `ToneGenerationScript` con un campo para el contenido refinado.
  - Completa la clase `ContentGeneration` con campos para la URL, audiencia objetivo, tono y idioma.

#### prompts/content_generation_prompts.py
- **Descripción**: Este archivo contiene las plantillas de prompts para la generación de contenido.
- **Tareas**:
  - Define la plantilla `GENERATE_INFO` para generar un guion atractivo y dinámico para reels de Instagram o TikTok.

#### prompts/tone_generator.py
- **Descripción**: Este archivo contiene las plantillas de prompts para refinar y mejorar un guion.
- **Tareas**:
  - Define la plantilla `GENERATE_REFINED_INFO` para refinar y mejorar un guion existente.

#### src/content_generator.py
- **Descripción**: Este archivo contiene la lógica para generar contenido utilizando un modelo LLM.
- **Tareas**:
  - Inicializa el manejador del modelo LLM de Groq.
  - Crea un `JsonOutputParser` para `ContentGenerationScript` y `ToneGenerationScript`.
  - Crea un `PromptTemplate` y un `LLMChain` para generar el contenido.
  - Implementa los métodos `generate_text`, `apply_tone`, y `generate_content`.

#### src/image_describer.py
- **Descripción**: Este archivo contiene la lógica para describir imágenes utilizando un modelo de visión.
- **Tareas**:
  - Inicializa el cliente `GroqModelHandler` y carga el nombre del modelo de visión desde las variables de entorno.
  - Implementa el método `encode_image` para codificar una imagen en una cadena base64.
  - Implementa el método `concatenate_images_square` para concatenar múltiples imágenes en una cuadrícula cuadrada.

#### src/llm.py
- **Descripción**: Este archivo contiene la lógica para manejar el modelo LLM de Groq.
- **Tareas**:
  - Carga la clave API de Groq y el nombre del modelo desde las variables de entorno.
  - Inicializa el cliente de Groq y el LLM `ChatGroq`.

#### src/scraping.py
- **Descripción**: Este archivo contiene la lógica para extraer datos de productos de una página web.
- **Tareas**:
  - Implementa los métodos para extraer el nombre, precio, enlaces de imágenes, especificaciones, información adicional y tallas disponibles del producto.
  - Implementa el método `scrape` para extraer todos los datos relevantes del producto y devolverlos como un diccionario.

#### src/server.py
- **Descripción**: Este archivo contiene la lógica del servidor FastAPI.
- **Tareas**:
  - Implementa el endpoint `/content_generator` para generar contenido basado en los metadatos extraídos de una URL.

### Frontend

#### Dockerfile
- **Descripción**: Este archivo define la configuración del contenedor Docker para el frontend.
- **Tareas**:
  - Asegúrate de que el Dockerfile esté correctamente configurado para instalar las dependencias y ejecutar la aplicación Streamlit.

#### models/content_generation_models.py
- **Descripción**: Este archivo define los modelos Pydantic para la generación de contenido en el frontend.
- **Tareas**:
  - Completa la clase `ContentGeneration` con campos para la audiencia objetivo, tono y idioma.

#### src/generate_content.py
- **Descripción**: Este archivo contiene la lógica para enviar solicitudes al backend y generar contenido.
- **Tareas**:
  - Implementa el método `compute_content` para enviar una solicitud POST al backend y obtener el contenido generado.

#### src/ui.py
- **Descripción**: Este archivo contiene la interfaz de usuario de la aplicación Streamlit.
- **Tareas**:
  - Crea campos de entrada para la URL, audiencia objetivo, tono y idioma.
  - Implementa un botón para generar el contenido y mostrar el guion generado.
  - Añade un botón de descarga para guardar el guion en formato JSON.

## Ejecución del Proyecto

1. **Configuración del Entorno**: Asegúrate de tener Docker y Docker Compose instalados en tu máquina.
2. **Variables de Entorno**: Crea un archivo `.env` en la raíz del proyecto y añade las variables de entorno necesarias, como la clave API de Groq.
3. **Construcción y Ejecución**: Ejecuta `docker-compose up` para construir y ejecutar los contenedores de backend y frontend.
4. **Acceso a la Aplicación**: Accede a la aplicación Streamlit en `http://localhost:8501` y a la API FastAPI en `http://localhost:8004`.

## Evaluación

- **Completitud**: Asegúrate de que todas las partes del código estén completas y funcionen correctamente.
- **Calidad del Código**: Escribe código limpio, bien documentado y siguiendo las mejores prácticas. PEP8 y Clean code
- **Funcionalidad**: Verifica que la aplicación funcione como se espera, generando contenido basado en los datos de entrada.

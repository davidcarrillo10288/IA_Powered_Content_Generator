from groq import Groq
from io import BytesIO
from PIL import Image
import requests
import base64
import math
import os
from dotenv import load_dotenv
from scr.llm import GroqModelHandler

# Cargar variables del archivo .env
load_dotenv()

class ImageGridDescriber:
    def __init__(self):
        # TODO: Initialize the GroqModelHandler client and load the vision model name from environment variables
        groq_handler = GroqModelHandler()
        self.client = groq_handler.get_client()
        self.vision_model = os.getenv("VISION_MODEL_NAME")
        self.prompt = "Describe detalladamente el producto que aparece en la imagen collage, destacando sus características clave, el tipo de producto, el color, el diseño y cualquier detalle visual que sea relevante. Asegúrate de incluir cualquier texto visible en la imagen que pueda ayudar a identificar el producto o proporcionar más información sobre sus características."

    @staticmethod
    def encode_image(image: Image.Image) -> str:
        # TODO: Encode an image to a base64 string
        buffered = BytesIO()
        image.save(buffered, format="JPEG")  # Puedes usar "PNG" si prefieres
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_base64

    def concatenate_images_square(self, image_links, img_size=200):
        # TODO: Concatenate multiple images into a square grid
        grid_size = math.ceil(math.sqrt(len(image_links)))

        # Crear una imagen en blanco del tamaño adecuado
        collage = Image.new('RGB', (img_size * grid_size, img_size * grid_size), color='white')

        # Descargar, redimensionar y pegar imágenes
        for idx, url in enumerate(image_links):
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content)).convert("RGB").resize((img_size, img_size))
                row = idx // grid_size
                col = idx % grid_size
                collage.paste(img, (col * img_size, row * img_size))
            except Exception as e:
                print(f"Error cargando imagen {idx}: {e}")

        return collage

    def get_image_description(self, concatenated_image):
        # Example method for students to follow
        base64_image = self.encode_image(concatenated_image)

        completion = self.client.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
        )

        return completion.choices[0].message.content
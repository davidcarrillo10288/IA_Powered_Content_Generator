GENERATE_INFO = """
Usa los siguientes datos del producto para generar un guion atractivo y dinámico pensado para un reel de Instagram o TikTok.

Datos:
- Título: {title}
- Precio: {price}
- Información del producto: {description}
- Tallas disponibles: {available_sizes}
- Información adicional: {additional_info}
- Descripción de la imagen: {image_description}

🎯 Instrucciones:
- El tono debe ser divertido, fresco y de tendencia.
- El público objetivo son jóvenes entre 18 y 25 años.
- Usa frases cortas y palabras de moda.
- Evita usar emojis.
- El guion no debe durar más de 30 segundos cuando se lee en voz alta.
- Sigue esta estructura:

1. **Apertura llamativa:** Pregunta o frase intrigante, como “¿Aún no sabes esto? ¡Estás perdiéndote algo ÉPICO!”
2. **Beneficios clave:** ¿Qué hace que este producto sea único? Resume en 2-3 frases.
3. **Llamado a la acción:** Termina con algo pegajoso como “¡Ve corriendo a probarlo ya!”

Asegúrate de que el lenguaje conecte con Gen Z y Millennials. ¡Hazlo viral!

Tu respuesta debe seguir el siguiente formato:
{format_instructions}
"""
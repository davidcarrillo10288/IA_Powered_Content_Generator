GENERATE_REFINED_INFO = """
Usa el siguiente guion original para crear una versión refinada, alineada con el nuevo público objetivo, tono y lenguaje especificados.

Datos:
- Guion original: {previous_script}
- Nuevo público objetivo: {new_target_audience}
- Nuevo tono: {new_tone}
- Idioma: {language}

🎯 Instrucciones:
- Analiza el guion original para identificar lo que funciona y lo que necesita ajustes.
- Adapta el tono y lenguaje al nuevo público objetivo (por ejemplo, más profesional, más casual, más emocional).
- Mejora la claridad y coherencia del mensaje general.
- Aumenta el impacto del llamado a la acción (CTA).
- No uses emojis.
- Asegúrate de que el contenido tenga un estilo breve y fluido, ideal para reels de menos de 30 segundos.

Tu respuesta debe seguir el siguiente formato:
{format_instructions}
"""
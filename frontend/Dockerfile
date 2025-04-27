FROM python:3.9-slim

# Crear y establecer el directorio de trabajo
WORKDIR /frontend

# Copiar y actualizar pip antes de instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY . .

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando de ejecución
ENTRYPOINT ["python", "-m", "streamlit", "run", "scr/ui.py"]
FROM tiangolo/uvicorn-gunicorn:python3.9

# Instalar dependencias necesarias para Selenium y Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    libx11-xcb1 \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libappindicator3-1 \
    libasound2 \
    libgconf-2-4 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    xvfb \  
    # Install Xvfb for display management in headless mode, although --headless=new might not need it
    # However, having it and setting DISPLAY can sometimes help with unexpected issues
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Setear las variables de entorno para Chrome y Chromedriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Crear y establecer el directorio de trabajo
WORKDIR /backend

# Copiar los archivos de dependencias
COPY requirements.txt ./

# Instalar dependencias y actualizar pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir webdriver-manager selenium && \
    pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

# Forzar la actualización de webdriver-manager y limpiar la caché
RUN pip install --no-cache-dir --upgrade webdriver-manager && rm -rf /root/.wdm

# Copiar el código fuente
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8004

# Definir el punto de entrada
ENTRYPOINT ["uvicorn", "scr.server:app", "--host", "0.0.0.0", "--port", "8004"]
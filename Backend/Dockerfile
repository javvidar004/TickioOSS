FROM python:3.12-slim

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY --chown=appuser:appuser ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Cambiar al usuario no-root
USER appuser

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"] 
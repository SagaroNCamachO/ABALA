"""
Punto de entrada para Vercel Serverless Functions.
Usando el formato correcto para Vercel Python runtime.
"""

import sys
import os

# Configurar paths
if os.path.exists('/var/task'):
    base_path = '/var/task'
else:
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if base_path not in sys.path:
    sys.path.insert(0, base_path)

# Importar la aplicación Flask
try:
    from api.app import app
except ImportError:
    try:
        from app import app
    except ImportError:
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def error(path):
            return jsonify({
                "error": "No se pudo importar la aplicación Flask"
            }), 500

# Para Vercel Python runtime, necesitamos usar serverless_wsgi
# que convierte la app Flask a un formato que Vercel entiende
try:
    from serverless_wsgi import handle_request
    
    def handler(event, context):
        """Handler que usa serverless_wsgi para convertir Flask a formato Vercel."""
        return handle_request(app, event, context)
    
    application = handler
    
except ImportError:
    # Si serverless_wsgi no está disponible, usar método alternativo
    # Vercel puede manejar Flask directamente si lo exportamos correctamente
    # Pero necesitamos asegurarnos de que sea reconocido como una aplicación WSGI
    
    # Crear un wrapper que Vercel pueda reconocer
    class FlaskHandler:
        """Wrapper para Flask que Vercel puede reconocer."""
        def __init__(self, flask_app):
            self.app = flask_app
        
        def __call__(self, environ, start_response):
            """WSGI callable."""
            return self.app(environ, start_response)
    
    # Exportar como handler y application
    handler = FlaskHandler(app)
    application = handler
